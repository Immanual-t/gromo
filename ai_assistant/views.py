from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import json
import random

from .models import Conversation, Message, AIResponse, LearningContent, SalesTemplate
from .ai_services import SalesCopilotService, LearningService, LeadService, PerformanceInsightService
from dashboard.models import SalesPerformance, AIInsight, CustomerLead
from accounts.models import Skill, LearningProgress


@login_required
def copilot_view(request):
    """View for sales co-pilot interface"""
    # Get user's skill levels
    skills = Skill.objects.filter(user=request.user)

    # Define customer types and product types
    customer_types = [
        ('new', 'New Customer'),
        ('existing', 'Existing Customer'),
        ('referred', 'Referred Customer')
    ]

    product_types = [
        ('insurance', 'Insurance'),
        ('credit_card', 'Credit Card'),
        ('loan', 'Loan'),
        ('savings', 'Savings Account'),
        ('demat', 'Demat Account'),
        ('investment', 'Investment')
    ]

    # Get recent conversations
    recent_conversations = Conversation.objects.filter(
        user=request.user
    ).order_by('-last_updated')[:5]

    context = {
        'skills': skills,
        'customer_types': customer_types,
        'product_types': product_types,
        'recent_conversations': recent_conversations
    }

    return render(request, 'ai_assistant/copilot.html', context)


@login_required
@csrf_exempt
def generate_suggestion_view(request):
    """API view for generating sales suggestions"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            messages = data.get('messages', [])

            # Generate suggestion
            result = SalesCopilotService.generate_sales_suggestion(request.user, messages)

            if result['status'] == 'success':
                return JsonResponse({'response': result['response']})
            else:
                return JsonResponse({'error': result.get('message', 'An error occurred')}, status=500)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


@login_required
def save_conversation_view(request):
    """View for saving a conversation"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            customer_type = data.get('customer_type')
            product_type = data.get('product_type')
            messages = data.get('messages', [])
            title = data.get('title', f"{product_type.title()} conversation - {timezone.now().strftime('%Y-%m-%d')}")

            # Create conversation
            conversation = Conversation.objects.create(
                user=request.user,
                customer_type=customer_type,
                product_type=product_type,
                title=title
            )

            # Add messages
            for msg in messages:
                if msg['role'] != 'system':  # Skip system messages
                    Message.objects.create(
                        conversation=conversation,
                        role=msg['role'],
                        content=msg['content']
                    )

            return JsonResponse({'success': True, 'conversation_id': conversation.id})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


@login_required
def conversation_detail_view(request, conversation_id):
    """View for viewing a conversation"""
    conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
    messages = conversation.messages.all()

    context = {
        'conversation': conversation,
        'messages': messages
    }

    return render(request, 'ai_assistant/conversation_detail.html', context)


@login_required
def learning_view(request):
    """View for personalized learning"""
    # Get user's skills
    skills = Skill.objects.filter(user=request.user)

    # Get user's learning progress
    learning_progress = LearningProgress.objects.filter(user=request.user).order_by('-last_activity')

    # Get learning content
    learning_content = LearningContent.objects.filter(user=request.user).order_by('-created_at')[:10]

    context = {
        'skills': skills,
        'learning_progress': learning_progress,
        'learning_content': learning_content,
        'product_types': [
            ('insurance', 'Insurance'),
            ('credit_card', 'Credit Card'),
            ('loan', 'Loan'),
            ('savings', 'Savings Account'),
            ('demat', 'Demat Account'),
            ('investment', 'Investment')
        ]
    }

    return render(request, 'ai_assistant/learning.html', context)


@login_required
def generate_learning_content_view(request):
    """View for generating personalized learning content"""
    if request.method == 'POST':
        product_type = request.POST.get('product_type')

        # Get user's skill level
        try:
            skill = Skill.objects.get(user=request.user, product_type=product_type)
            skill_level = 'beginner'
            if skill.proficiency_level > 3:
                skill_level = 'intermediate'
            if skill.proficiency_level > 7:
                skill_level = 'advanced'
        except Skill.DoesNotExist:
            skill_level = 'beginner'

        # Generate content
        result = LearningService.generate_learning_content(request.user, product_type, skill_level)

        if result['status'] == 'success':
            # Save content
            content = result['response']
            summary = content.split('\n\n')[0] if '\n\n' in content else content[:100] + '...'

            learning_content = LearningContent.objects.create(
                user=request.user,
                product_type=product_type,
                topic=f"Selling {product_type.replace('_', ' ').title()} Products",
                content=content,
                summary=summary,
                difficulty_level=skill_level
            )

            # Update learning progress
            learning_progress, created = LearningProgress.objects.get_or_create(
                user=request.user,
                module_name=f"{product_type.replace('_', ' ').title()} Basics",
                defaults={
                    'completion_percentage': 0,
                    'completed': False
                }
            )

            return redirect('ai_assistant:learning_content_detail', content_id=learning_content.id)
        else:
            messages.error(request, 'Failed to generate learning content. Please try again.')
            return redirect('ai_assistant:learning')

    return redirect('ai_assistant:learning')


@login_required
def learning_content_detail_view(request, content_id):
    """View for displaying learning content"""
    content = get_object_or_404(LearningContent, id=content_id, user=request.user)

    # Mark as read
    if not content.is_read:
        content.is_read = True
        content.save()

    # Get related content
    related_content = LearningContent.objects.filter(
        user=request.user,
        product_type=content.product_type
    ).exclude(id=content_id).order_by('-created_at')[:3]

    context = {
        'content': content,
        'related_content': related_content
    }

    return render(request, 'ai_assistant/learning_content_detail.html', context)


@login_required
def leads_view(request):
    """View for smart lead management"""
    # Get leads
    leads = CustomerLead.objects.filter(user=request.user).order_by('-priority_score')

    # Group leads by status
    new_leads = leads.filter(status='new')
    contacted_leads = leads.filter(status='contacted')
    interested_leads = leads.filter(status='interested')
    converted_leads = leads.filter(status='converted')
    lost_leads = leads.filter(status='lost')

    context = {
        'new_leads': new_leads,
        'contacted_leads': contacted_leads,
        'interested_leads': interested_leads,
        'converted_leads': converted_leads,
        'lost_leads': lost_leads,
        'product_types': [
            ('insurance', 'Insurance'),
            ('credit_card', 'Credit Card'),
            ('loan', 'Loan'),
            ('savings', 'Savings Account'),
            ('demat', 'Demat Account'),
            ('investment', 'Investment')
        ]
    }

    return render(request, 'ai_assistant/leads.html', context)


@login_required
def add_lead_view(request):
    """View for adding a new lead"""
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email', '')
        interest = request.POST.get('interest')
        lead_source = request.POST.get('lead_source', 'manual')
        notes = request.POST.get('notes', '')

        # Create lead
        lead = CustomerLead.objects.create(
            user=request.user,
            name=name,
            phone=phone,
            email=email,
            interest=interest,
            lead_source=lead_source,
            notes=notes,
            status='new',
            priority_score=random.uniform(0.5, 0.8)  # In a real app, use AI to determine score
        )

        messages.success(request, f'Lead "{name}" has been added successfully.')
        return redirect('ai_assistant:leads')

    context = {
        'product_types': [
            ('insurance', 'Insurance'),
            ('credit_card', 'Credit Card'),
            ('loan', 'Loan'),
            ('savings', 'Savings Account'),
            ('demat', 'Demat Account'),
            ('investment', 'Investment'),
            ('multiple', 'Multiple Products'),
            ('undecided', 'Undecided')
        ],
        'lead_sources': [
            ('manual', 'Manually Added'),
            ('referral', 'Referral'),
            ('campaign', 'Campaign'),
            ('other', 'Other')
        ]
    }

    return render(request, 'ai_assistant/add_lead.html', context)


@login_required
def update_lead_status_view(request, lead_id):
    """View for updating lead status"""
    if request.method == 'POST':
        lead = get_object_or_404(CustomerLead, id=lead_id, user=request.user)
        status = request.POST.get('status')
        notes = request.POST.get('notes', '')

        # Update lead
        lead.status = status
        if notes:
            lead.notes = (lead.notes or '') + f"\n\n{timezone.now().strftime('%Y-%m-%d %H:%M')}: {notes}"
        lead.save()

        messages.success(request, f'Lead "{lead.name}" has been updated.')
        return redirect('ai_assistant:leads')

    return redirect('ai_assistant:leads')


@login_required
def generate_lead_message_view(request, lead_id):
    """View for generating a message for a lead"""
    lead = get_object_or_404(CustomerLead, id=lead_id, user=request.user)

    # Prepare lead data
    lead_data = {
        'name': lead.name,
        'interest': lead.interest,
        'status': lead.status,
        'notes': lead.notes
    }

    # Generate message
    result = LeadService.generate_outreach_message(request.user, lead_data, lead.interest)

    if result['status'] == 'success':
        return JsonResponse({'message': result['response']})
    else:
        return JsonResponse({'error': result.get('message', 'An error occurred')}, status=500)


@login_required
def analyze_leads_view(request):
    """View for analyzing leads"""
    # Get leads
    leads = CustomerLead.objects.filter(
        user=request.user,
        status__in=['new', 'contacted', 'interested']
    )

    if leads.count() < 3:
        messages.warning(request, 'You need at least 3 active leads for analysis.')
        return redirect('ai_assistant:leads')

    # Prepare lead data
    lead_data = []
    for lead in leads:
        lead_data.append({
            'id': lead.id,
            'name': lead.name,
            'interest': lead.interest,
            'status': lead.status,
            'lead_source': lead.lead_source,
            'notes': lead.notes,
            'created_at': lead.created_at.strftime('%Y-%m-%d')
        })

    # Analyze leads
    result = LeadService.analyze_leads(request.user, lead_data)

    if result['status'] == 'success':
        # Create insight
        AIInsight.objects.create(
            user=request.user,
            insight_text=result['response'],
            category='lead'
        )

        context = {
            'analysis': result['response'],
            'leads': leads
        }

        return render(request, 'ai_assistant/lead_analysis.html', context)
    else:
        messages.error(request, 'Failed to analyze leads. Please try again.')
        return redirect('ai_assistant:leads')


@login_required
def check_insights_view(request):
    """API view for checking new insights"""
    # Get unread insights
    unread_insights = AIInsight.objects.filter(user=request.user, is_read=False)

    if unread_insights.exists():
        insight = unread_insights.first()
        insight.is_read = True
        insight.save()

        return JsonResponse({
            'has_new_insights': True,
            'insight': insight.insight_text,
            'category': insight.category
        })
    else:
        return JsonResponse({'has_new_insights': False})


@login_required
def insights_view(request):
    """View for displaying all insights"""
    insights = AIInsight.objects.filter(user=request.user).order_by('-created_at')

    # Mark all as read
    insights.update(is_read=True)

    context = {
        'insights': insights,
        'categories': {
            'performance': 'Performance Insight',
            'learning': 'Learning Recommendation',
            'lead': 'Lead Suggestion',
            'sales': 'Sales Tip'
        }
    }

    return render(request, 'ai_assistant/insights.html', context)


@login_required
def mark_content_complete_view(request, content_id):
    """View for marking learning content as complete"""
    content = get_object_or_404(LearningContent, id=content_id, user=request.user)

    # Mark content as complete
    content.is_read = True
    content.save()

    # Update learning progress
    learning_progress, created = LearningProgress.objects.get_or_create(
        user=request.user,
        module_name=f"{content.product_type.replace('_', ' ').title()} Basics",
        defaults={
            'completion_percentage': 0,
            'completed': False
        }
    )

    # Update completion percentage
    # In a real app, this would be more sophisticated
    learning_progress.completion_percentage += 20
    if learning_progress.completion_percentage >= 100:
        learning_progress.completion_percentage = 100
        learning_progress.completed = True
    learning_progress.save()

    # Create an AI insight about the learning
    AIInsight.objects.create(
        user=request.user,
        insight_text=f"Great job completing the {content.topic} module! Keep learning to improve your sales skills.",
        category='learning'
    )

    messages.success(request, 'Content marked as complete. Your learning progress has been updated!')
    return redirect('ai_assistant:learning_content_detail', content_id=content_id)


@login_required
def get_quiz_questions_view(request, content_id):
    """API view for fetching quiz questions"""
    content = get_object_or_404(LearningContent, id=content_id, user=request.user)

    # Get user's skill level
    try:
        skill = Skill.objects.get(user=request.user, product_type=content.product_type)
        skill_level = 'beginner'
        if skill.proficiency_level > 3:
            skill_level = 'intermediate'
        if skill.proficiency_level > 7:
            skill_level = 'advanced'
    except Skill.DoesNotExist:
        skill_level = 'beginner'

    # Generate questions
    result = LearningService.generate_quiz_questions(request.user, content.product_type, skill_level)

    if result['status'] == 'success':
        return JsonResponse({'status': 'success', 'questions': result['questions']})
    else:
        return JsonResponse({'status': 'error', 'message': 'Failed to generate questions'})


@login_required
@csrf_exempt
def submit_quiz_results_view(request, content_id):
    """API view for submitting quiz results"""
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

    content = get_object_or_404(LearningContent, id=content_id, user=request.user)

    try:
        data = json.loads(request.body)
        score = data.get('score', 0)
        total = data.get('total', 0)
        percentage = data.get('percentage', 0)

        # Mark content as read
        content.is_read = True
        content.save()

        # Update learning progress
        learning_progress, created = LearningProgress.objects.get_or_create(
            user=request.user,
            module_name=f"{content.product_type.replace('_', ' ').title()} Basics",
            defaults={
                'completion_percentage': 0,
                'completed': False
            }
        )

        # Update completion percentage based on quiz score
        progress_increase = min(30, int(percentage / 3))  # Max 30% increase per quiz
        learning_progress.completion_percentage += progress_increase
        if learning_progress.completion_percentage >= 100:
            learning_progress.completion_percentage = 100
            learning_progress.completed = True
        learning_progress.save()

        # Update skill level if score is good
        if percentage >= 70:
            try:
                skill = Skill.objects.get(user=request.user, product_type=content.product_type)
                if percentage >= 90:
                    skill.proficiency_level = min(skill.proficiency_level + 2, 10)
                else:
                    skill.proficiency_level = min(skill.proficiency_level + 1, 10)
                skill.save()
            except Skill.DoesNotExist:
                pass

        # Create an AI insight about the quiz
        if percentage >= 80:
            message = f"Great job on the {content.topic} quiz! Your score of {percentage:.0f}% shows you have a strong understanding of this topic."
        elif percentage >= 60:
            message = f"Good effort on the {content.topic} quiz. Your score of {percentage:.0f}% shows you're making progress!"
        else:
            message = f"You completed the {content.topic} quiz with a score of {percentage:.0f}%. Consider reviewing this material again."

        AIInsight.objects.create(
            user=request.user,
            insight_text=message,
            category='learning'
        )

        return JsonResponse({'status': 'success'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)