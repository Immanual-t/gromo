from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class SalesPerformance(models.Model):
    """Model to track sales performance of partners"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sales')
    date = models.DateField(default=timezone.now)
    product = models.CharField(max_length=100)
    customer_name = models.CharField(max_length=100)
    customer_type = models.CharField(
        max_length=20,
        choices=[
            ('new', 'New Customer'),
            ('existing', 'Existing Customer'),
            ('referred', 'Referred Customer')
        ],
        default='new'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    commission = models.DecimalField(max_digits=10, decimal_places=2)
    product_category = models.CharField(
        max_length=20,
        choices=[
            ('insurance', 'Insurance'),
            ('credit_card', 'Credit Card'),
            ('loan', 'Loan'),
            ('savings', 'Savings Account'),
            ('demat', 'Demat Account'),
            ('investment', 'Investment')
        ]
    )

    # Additional metadata
    notes = models.TextField(blank=True, null=True)
    lead_source = models.CharField(
        max_length=20,
        choices=[
            ('direct', 'Direct Contact'),
            ('referral', 'Referral'),
            ('ai_suggested', 'AI Suggested'),
            ('campaign', 'Campaign'),
            ('other', 'Other')
        ],
        default='direct'
    )

    def __str__(self):
        return f"{self.user.username} - {self.product} - {self.date}"

    class Meta:
        ordering = ['-date']


class PerformanceGoal(models.Model):
    """Model to track performance goals"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goals')
    month = models.IntegerField()
    year = models.IntegerField()
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    target_customers = models.IntegerField(default=0)

    # Product-specific targets
    insurance_target = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    credit_card_target = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    loan_target = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    investment_target = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.month}/{self.year} - ₹{self.target_amount}"

    class Meta:
        unique_together = ['user', 'month', 'year']
        ordering = ['-year', '-month']

    def get_achieved_percentage(self):
        """Calculate percentage of goal achieved"""
        month_sales = SalesPerformance.objects.filter(
            user=self.user,
            date__month=self.month,
            date__year=self.year
        )

        total_sales = sum(sale.amount for sale in month_sales)
        if self.target_amount > 0:
            return (total_sales / self.target_amount) * 100
        return 0


class AIInsight(models.Model):
    """Model to store AI-generated insights"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ai_insights')
    insight_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(
        max_length=20,
        choices=[
            ('performance', 'Performance Insight'),
            ('learning', 'Learning Recommendation'),
            ('lead', 'Lead Suggestion'),
            ('sales', 'Sales Tip')
        ],
        default='performance'
    )
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.category} - {self.created_at.strftime('%Y-%m-%d')}"

    class Meta:
        ordering = ['-created_at']


class CustomerLead(models.Model):
    """Model to track customer leads"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leads')
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)

    # Lead details
    lead_source = models.CharField(
        max_length=20,
        choices=[
            ('manual', 'Manually Added'),
            ('ai_suggested', 'AI Suggested'),
            ('referral', 'Referral'),
            ('campaign', 'Campaign')
        ],
        default='manual'
    )
    interest = models.CharField(
        max_length=20,
        choices=[
            ('insurance', 'Insurance'),
            ('credit_card', 'Credit Card'),
            ('loan', 'Loan'),
            ('savings', 'Savings Account'),
            ('demat', 'Demat Account'),
            ('investment', 'Investment'),
            ('multiple', 'Multiple Products'),
            ('undecided', 'Undecided')
        ],
        default='undecided'
    )

    # Lead status
    status = models.CharField(
        max_length=20,
        choices=[
            ('new', 'New Lead'),
            ('contacted', 'Contacted'),
            ('interested', 'Interested'),
            ('converted', 'Converted'),
            ('lost', 'Lost')
        ],
        default='new'
    )

    priority_score = models.FloatField(default=0)  # AI-calculated score
    notes = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.interest} - {self.status}"

    class Meta:
        ordering = ['-priority_score', '-created_at']