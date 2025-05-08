from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Sum, Count, Avg
from datetime import datetime, timedelta
import json
import random

from .models import SalesPerformance, PerformanceGoal, AIInsight, CustomerLead
from accounts.models import Skill, LearningProgress, UserProfile


@login_required
def index_view(request):
    """Main dashboard view"""
    user = request.user
    today = timezone.now().date()


    # Get current month's data
    current_month = today.month
    current_year = today.year

    # Calculate sales metrics
    month_sales = SalesPerformance.objects.filter(
        user=user,
        date__month=current_month,
        date__year=current_year
    )

    month_total = month_sales.aggregate(total=Sum('amount'))['total'] or 0
    month_commission = month_sales.aggregate(total=Sum('commission'))['total'] or 0
    month_count = month_sales.count()

    # Get monthly goal
    try:
        monthly_goal = PerformanceGoal.objects.get(user=user, month=current_month, year=current_year)
        goal_percentage = monthly_goal.get_achieved_percentage()
    except PerformanceGoal.DoesNotExist:
        monthly_goal = None
        goal_percentage = 0

    # Get recent sales
    recent_sales = SalesPerformance.objects.filter(user=user).order_by('-date')[:5]

    # Get recent insights
    recent_insights = AIInsight.objects.filter(user=user).order_by('-created_at')[:3]

    # Get high priority leads
    high_priority_leads = CustomerLead.objects.filter(
        user=user,
        status__in=['new', 'contacted', 'interested']
    ).order_by('-priority_score')[:5]

    # Get learning progress
    learning_modules = LearningProgress.objects.filter(user=user).order_by('-last_activity')[:3]

    # Calculate product distribution
    product_distribution = month_sales.values('product_category').annotate(
        count=Count('id'),
        total=Sum('amount')
    ).order_by('-total')

    # Prepare chart data
    chart_labels = [item['product_category'] for item in product_distribution]
    chart_values = [float(item['total']) for item in product_distribution]

    # Prepare recent performance data (last 7 days)
    last_week_data = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        day_sales = SalesPerformance.objects.filter(user=user, date=day)
        day_total = day_sales.aggregate(total=Sum('amount'))['total'] or 0
        last_week_data.append({
            'date': day.strftime('%d %b'),
            'amount': float(day_total)
        })

    week_labels = [day['date'] for day in last_week_data]
    week_values = [day['amount'] for day in last_week_data]

    context = {
        'month_total': month_total,
        'month_commission': month_commission,
        'month_count': month_count,
        'monthly_goal': monthly_goal,
        'goal_percentage': goal_percentage,
        'recent_sales': recent_sales,
        'recent_insights': recent_insights,
        'high_priority_leads': high_priority_leads,
        'learning_modules': learning_modules,
        'product_distribution': product_distribution,
        'chart_labels': json.dumps(chart_labels),
        'chart_values': json.dumps(chart_values),
        'week_labels': json.dumps([day['date'] for day in last_week_data]),
        'week_values': json.dumps([day['amount'] for day in last_week_data])
    }

    return render(request, 'dashboard/index.html', context)


@login_required
def analytics_view(request):
    """Performance analytics view"""
    user = request.user

    # Get date range from request or default to current month
    today = timezone.now().date()
    current_month = today.month
    current_year = today.year

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    else:
        start_date = datetime(current_year, current_month, 1).date()

    if end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    else:
        if current_month == 12:
            next_month = 1
            next_year = current_year + 1
        else:
            next_month = current_month + 1
            next_year = current_year

        end_date = datetime(next_year, next_month, 1).date() - timedelta(days=1)

    # Get sales data for selected period
    sales_data = SalesPerformance.objects.filter(
        user=user,
        date__gte=start_date,
        date__lte=end_date
    )

    # Calculate summary metrics
    period_total = sales_data.aggregate(total=Sum('amount'))['total'] or 0
    period_commission = sales_data.aggregate(total=Sum('commission'))['total'] or 0
    period_count = sales_data.count()
    avg_sale_value = period_total / period_count if period_count > 0 else 0

    # Calculate product category distribution
    product_categories = sales_data.values('product_category').annotate(
        count=Count('id'),
        total=Sum('amount'),
        avg_amount=Avg('amount')
    ).order_by('-total')

    # Calculate customer type distribution
    customer_types = sales_data.values('customer_type').annotate(
        count=Count('id'),
        total=Sum('amount')
    ).order_by('-count')

    # Calculate day-by-day performance
    daily_performance = []
    current_date = start_date
    while current_date <= end_date:
        day_sales = sales_data.filter(date=current_date)
        day_total = day_sales.aggregate(total=Sum('amount'))['total'] or 0
        day_count = day_sales.count()

        daily_performance.append({
            'date': current_date.strftime('%d %b'),
            'total': float(day_total),
            'count': day_count
        })

        current_date += timedelta(days=1)

    # Prepare chart data
    period_labels = [day['date'] for day in daily_performance]
    period_values = [day['total'] for day in daily_performance]

    # Product distribution chart
    product_labels = [item['product_category'] for item in product_categories]
    product_values = [float(item['total']) for item in product_categories]

    # Customer type chart
    customer_labels = [item['customer_type'] for item in customer_types]
    customer_values = [item['count'] for item in customer_types]

    context = {
        'start_date': start_date,
        'end_date': end_date,
        'period_total': period_total,
        'period_commission': period_commission,
        'period_count': period_count,
        'avg_sale_value': avg_sale_value,
        'product_categories': product_categories,
        'customer_types': customer_types,
        'daily_performance': daily_performance,
        'period_labels': json.dumps(period_labels),
        'period_values': json.dumps(period_values),
        'product_labels': json.dumps(product_labels),
        'product_values': json.dumps(product_values),
        'customer_labels': json.dumps(customer_labels),
        'customer_values': json.dumps(customer_values)
    }

    return render(request, 'dashboard/analytics.html', context)


@login_required
def set_goals_view(request):
    """View for setting performance goals"""
    user = request.user
    today = timezone.now().date()
    current_month = today.month
    current_year = today.year

    if request.method == 'POST':
        target_amount = request.POST.get('target_amount')
        target_customers = request.POST.get('target_customers')
        insurance_target = request.POST.get('insurance_target', 0)
        credit_card_target = request.POST.get('credit_card_target', 0)
        loan_target = request.POST.get('loan_target', 0)
        investment_target = request.POST.get('investment_target', 0)

        # Create or update goal
        goal, created = PerformanceGoal.objects.update_or_create(
            user=user,
            month=current_month,
            year=current_year,
            defaults={
                'target_amount': target_amount,
                'target_customers': target_customers,
                'insurance_target': insurance_target,
                'credit_card_target': credit_card_target,
                'loan_target': loan_target,
                'investment_target': investment_target
            }
        )

        return redirect('dashboard:index')

    # Get current goal if exists
    try:
        current_goal = PerformanceGoal.objects.get(
            user=user,
            month=current_month,
            year=current_year
        )
    except PerformanceGoal.DoesNotExist:
        current_goal = None

    context = {
        'current_goal': current_goal,
        'current_month': today.strftime('%B'),
        'current_year': current_year
    }

    return render(request, 'dashboard/set_goals.html', context)


@login_required
def refresh_card_view(request, card_id):
    """AJAX view for refreshing dashboard cards"""
    user = request.user
    today = timezone.now().date()

    if card_id == 'recent_sales':
        # Refresh recent sales card
        recent_sales = SalesPerformance.objects.filter(user=user).order_by('-date')[:5]
        html = render(request, 'dashboard/partials/recent_sales.html', {'recent_sales': recent_sales}).content.decode()
        return JsonResponse({'html': html})

    elif card_id == 'insights':
        # Refresh insights card
        recent_insights = AIInsight.objects.filter(user=user).order_by('-created_at')[:3]
        html = render(request, 'dashboard/partials/insights.html',
                      {'recent_insights': recent_insights}).content.decode()
        return JsonResponse({'html': html})

    elif card_id == 'leads':
        # Refresh leads card
        high_priority_leads = CustomerLead.objects.filter(
            user=user,
            status__in=['new', 'contacted', 'interested']
        ).order_by('-priority_score')[:5]
        html = render(request, 'dashboard/partials/leads.html',
                      {'high_priority_leads': high_priority_leads}).content.decode()
        return JsonResponse({'html': html})

    return JsonResponse({'error': 'Invalid card ID'}, status=400)


@login_required
def add_sale_view(request):
    """View for adding a new sale"""
    user = request.user
    today = timezone.now().date()

    # Get current month's data for insight generation
    current_month = today.month
    current_year = today.year

    # Calculate current month sales count for insights
    month_sales = SalesPerformance.objects.filter(
        user=user,
        date__month=current_month,
        date__year=current_year
    )
    month_count = month_sales.count()

    if request.method == 'POST':
        # Process form data
        product = request.POST.get('product')
        customer_name = request.POST.get('customer_name')
        customer_type = request.POST.get('customer_type')
        amount = request.POST.get('amount')
        product_category = request.POST.get('product_category')
        lead_source = request.POST.get('lead_source', 'direct')
        notes = request.POST.get('notes', '')

        # Calculate commission (in a real app, this would be more complex)
        commission_rates = {
            'insurance': 0.15,
            'credit_card': 0.10,
            'loan': 0.08,
            'savings': 0.05,
            'demat': 0.07,
            'investment': 0.12
        }

        commission_rate = commission_rates.get(product_category, 0.10)
        commission = float(amount) * commission_rate

        # Create sale record
        sale = SalesPerformance.objects.create(
            user=request.user,
            product=product,
            customer_name=customer_name,
            customer_type=customer_type,
            amount=amount,
            commission=commission,
            product_category=product_category,
            lead_source=lead_source,
            notes=notes
        )

        # If sale was from a lead, update lead status
        if lead_source == 'ai_suggested':
            leads = CustomerLead.objects.filter(
                user=request.user,
                name=customer_name,
                status__in=['new', 'contacted', 'interested']
            )

            if leads.exists():
                lead = leads.first()
                lead.status = 'converted'
                lead.notes = (lead.notes or '') + f"\nConverted to sale on {timezone.now().date()}"
                lead.save()

        # Generate AI insight about the sale
        insight_text = f"Congratulations on your {product} sale! You earned ₹{commission:.2f} in commission. This is your {month_count + 1} sale this month."

        AIInsight.objects.create(
            user=request.user,
            insight_text=insight_text,
            category='performance'
        )

        return redirect('dashboard:index')

    # If not POST, show the form
    context = {
        'product_categories': [
            ('insurance', 'Insurance'),
            ('credit_card', 'Credit Card'),
            ('loan', 'Loan'),
            ('savings', 'Savings Account'),
            ('demat', 'Demat Account'),
            ('investment', 'Investment')
        ],
        'customer_types': [
            ('new', 'New Customer'),
            ('existing', 'Existing Customer'),
            ('referred', 'Referred Customer')
        ],
        'lead_sources': [
            ('direct', 'Direct Contact'),
            ('referral', 'Referral'),
            ('ai_suggested', 'AI Suggested'),
            ('campaign', 'Campaign'),
            ('other', 'Other')
        ]
    }

    return render(request, 'dashboard/add_sale.html', context)