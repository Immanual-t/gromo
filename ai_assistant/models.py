from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Conversation(models.Model):
    """Model to store sales conversations"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations')
    customer_type = models.CharField(
        max_length=20,
        choices=[
            ('new', 'New Customer'),
            ('existing', 'Existing Customer'),
            ('referred', 'Referred Customer')
        ]
    )
    product_type = models.CharField(
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
    title = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_product_type_display()} - {self.created_at.strftime('%Y-%m-%d')}"


class Message(models.Model):
    """Model to store conversation messages"""
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(
        max_length=10,
        choices=[
            ('user', 'User'),
            ('assistant', 'Assistant'),
            ('system', 'System')
        ]
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.conversation.id} - {self.role} - {self.created_at.strftime('%H:%M:%S')}"

    class Meta:
        ordering = ['created_at']


class AIResponse(models.Model):
    """Model to track all AI responses"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ai_responses')
    request_type = models.CharField(
        max_length=20,
        choices=[
            ('copilot', 'Sales Co-Pilot'),
            ('learning', 'Learning Content'),
            ('lead', 'Lead Suggestion'),
            ('message', 'Customer Message')
        ]
    )
    prompt = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.request_type} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"


class LearningContent(models.Model):
    """Model to store AI-generated learning content"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='learning_content')
    product_type = models.CharField(
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
    topic = models.CharField(max_length=100)
    content = models.TextField()
    summary = models.TextField()
    difficulty_level = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced')
        ],
        default='beginner'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.product_type} - {self.topic}"


class SalesTemplate(models.Model):
    """Model to store AI-generated sales templates"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sales_templates')
    product_type = models.CharField(
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
    title = models.CharField(max_length=100)
    content = models.TextField()
    template_type = models.CharField(
        max_length=20,
        choices=[
            ('pitch', 'Sales Pitch'),
            ('objection', 'Objection Handling'),
            ('followup', 'Follow-up Message'),
            ('closing', 'Closing Script')
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product_type} - {self.template_type}"