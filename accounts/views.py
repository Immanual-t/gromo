from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .forms import (
    CustomUserCreationForm,
    CustomAuthenticationForm,
    UserProfileForm,
    SkillAssessmentForm,
    NotificationPreferenceForm
)
from .models import UserProfile, Skill, LearningProgress
from dashboard.models import SalesPerformance


def register_view(request):
    """View for user registration"""
    if request.user.is_authenticated:
        return redirect('dashboard:index')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Your account has been created successfully!')
            return redirect('dashboard:index')
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """View for user login"""
    if request.user.is_authenticated:
        # If admin cookie is set, don't redirect from user login
        if not request.COOKIES.get('admin_logged_in') == 'true':
            return redirect('dashboard:index')

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name}!')

                # Redirect to the page the user was trying to access, or dashboard
                next_page = request.GET.get('next', 'dashboard:index')
                return redirect(next_page)
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = CustomAuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})



@login_required
def logout_view(request):
    """View for user logout"""
    # Only log out if not an admin session
    if not request.COOKIES.get('admin_logged_in') == 'true':
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
    return redirect('accounts:login')



@login_required
def profile_view(request):
    """View for displaying and updating user profile"""
    user_profile = request.user.profile

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=user_profile)

    # Get user's skills
    skills = Skill.objects.filter(user=request.user).order_by('product_type')

    # Get user's learning progress
    learning_progress = LearningProgress.objects.filter(user=request.user).order_by('-last_activity')

    # Get user's sales performance
    sales_data = SalesPerformance.objects.filter(user=request.user).order_by('-date')[:5]

    context = {
        'form': form,
        'profile': user_profile,
        'skills': skills,
        'learning_progress': learning_progress,
        'sales_data': sales_data,
        'profile_completion': user_profile.calculate_completion()
    }

    return render(request, 'accounts/profile.html', context)


@login_required
def skill_assessment_view(request, product_type):
    """View for skill assessment"""
    skill, created = Skill.objects.get_or_create(
        user=request.user,
        product_type=product_type,
        defaults={'proficiency_level': 1}
    )

    if request.method == 'POST':
        form = SkillAssessmentForm(request.POST, product_type=product_type)
        if form.is_valid():
            # Process assessment and update skill level
            # In a real app, this would involve more complex logic
            answers = form.cleaned_data.get('questions', {})
            correct_answers = 0
            total_questions = len(answers)

            if total_questions > 0:
                # Simple scoring mechanism - in real app would be more sophisticated
                correct_answers = sum(1 for answer in answers.values() if answer.get('correct', False))
                score = (correct_answers / total_questions) * 10

                # Update skill level
                skill.proficiency_level = int(score)
                skill.save()

                messages.success(request,
                                 f'Your {product_type} skill assessment has been completed. Your score: {score:.1f}/10')
            else:
                messages.error(request, 'No assessment questions were submitted.')

            return redirect('accounts:profile')
    else:
        form = SkillAssessmentForm(product_type=product_type)

    # In a real app, we would fetch questions from a database
    # Here we're using sample questions
    sample_questions = {
        'insurance': [
            {'id': 1, 'text': 'What is term insurance?',
             'options': ['A type of life insurance that provides coverage for a specific term',
                         'A type of health insurance', 'A type of car insurance', 'A type of home insurance']},
            {'id': 2, 'text': 'What is the waiting period in health insurance?',
             'options': ['Time before policy becomes effective', 'Time to renew policy', 'Time to claim insurance',
                         'Time to pay premium']},
            {'id': 3, 'text': 'What is a premium?',
             'options': ['Regular payment for insurance coverage', 'One-time payment', 'Claim amount', 'Bonus payment']}
        ],
        'credit_card': [
            {'id': 1, 'text': 'What is a credit limit?',
             'options': ['Maximum amount you can borrow', 'Minimum payment due', 'Interest rate', 'Annual fee']},
            {'id': 2, 'text': 'What is an EMI?',
             'options': ['Equated Monthly Installment', 'Extra Money Interest', 'Easy Money Insurance',
                         'Electronic Money Instruction']},
            {'id': 3, 'text': 'What is a balance transfer?',
             'options': ['Moving debt from one card to another', 'Paying off debt', 'Increasing credit limit',
                         'Reducing interest rate']}
        ],
        'loan': [
            {'id': 1, 'text': 'What is a personal loan?',
             'options': ['Unsecured loan for personal use', 'Loan for business', 'Loan for house', 'Loan for car']},
            {'id': 2, 'text': 'What is a floating interest rate?',
             'options': ['Interest rate that changes over time', 'Fixed interest rate', 'Zero interest rate',
                         'Negative interest rate']},
            {'id': 3, 'text': 'What is a co-applicant?',
             'options': ['Person who applies for loan with primary applicant', 'Primary applicant', 'Guarantor',
                         'Beneficiary']}
        ],
        'investment': [
            {'id': 1, 'text': 'What is a mutual fund?',
             'options': ['Investment vehicle that pools money from investors', 'Fixed deposit', 'Government bond',
                         'Stock']},
            {'id': 2, 'text': 'What is SIP?',
             'options': ['Systematic Investment Plan', 'Special Interest Payment', 'Systematic Income Plan',
                         'Single Investment Policy']},
            {'id': 3, 'text': 'What is asset allocation?',
             'options': ['Distribution of investments across different asset classes',
                         'Investing all money in one asset', 'Withdrawing money from investment',
                         'Taking a loan against investment']}
        ]
    }

    context = {
        'form': form,
        'skill': skill,
        'product_type': product_type,
        'questions': sample_questions.get(product_type, [])
    }

    return render(request, 'accounts/skill_assessment.html', context)


@login_required
def notification_preferences_view(request):
    """View for setting notification preferences"""
    user_profile = request.user.profile

    if request.method == 'POST':
        form = NotificationPreferenceForm(request.POST)
        if form.is_valid():
            # Update notification preferences
            preferences = {
                'email_notifications': form.cleaned_data['email_notifications'],
                'app_notifications': form.cleaned_data['app_notifications'],
                'learning_reminders': form.cleaned_data['learning_reminders'],
                'sales_tips': form.cleaned_data['sales_tips'],
                'performance_updates': form.cleaned_data['performance_updates']
            }

            user_profile.notification_preferences = preferences
            user_profile.save()

            messages.success(request, 'Your notification preferences have been updated.')
            return redirect('accounts:profile')
    else:
        # Initialize form with current preferences
        initial_data = user_profile.notification_preferences
        form = NotificationPreferenceForm(initial=initial_data)

    context = {
        'form': form
    }

    return render(request, 'accounts/notification_preferences.html', context)