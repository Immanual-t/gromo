from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """Extended user profile for GroMo Partners"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_pic = models.ImageField(upload_to='profile_pics', default='profile_pics/default.png')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)

    # Partner details
    partner_id = models.CharField(max_length=10, blank=True, null=True)
    partner_since = models.DateField(blank=True, null=True)

    # Performance metrics
    monthly_target = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    experience_level = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
            ('expert', 'Expert')
        ],
        default='beginner'
    )

    # Preferences
    preferred_products = models.JSONField(default=list, blank=True)
    notification_preferences = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def get_full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def get_experience_level_display(self):
        return dict(self._meta.get_field('experience_level').choices)[self.experience_level]

    def calculate_completion(self):
        """Calculate profile completion percentage"""
        fields = ['profile_pic', 'phone_number', 'city', 'state']
        completed = sum(1 for field in fields if getattr(self, field))
        user_fields = ['first_name', 'last_name', 'email']
        completed += sum(1 for field in user_fields if getattr(self.user, field))
        return (completed / (len(fields) + len(user_fields))) * 100


class Skill(models.Model):
    """Skills for GroMo Partners"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skills')
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
    proficiency_level = models.IntegerField(default=1)  # Scale of 1-10
    last_assessed = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'product_type']

    def __str__(self):
        return f"{self.user.username} - {self.product_type} ({self.proficiency_level}/10)"


class LearningProgress(models.Model):
    """Track learning progress for partners"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='learning_progress')
    module_name = models.CharField(max_length=100)
    completion_percentage = models.IntegerField(default=0)
    last_activity = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ['user', 'module_name']

    def __str__(self):
        return f"{self.user.username} - {self.module_name} ({self.completion_percentage}%)"


# Signal to create user profile when a new user is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()