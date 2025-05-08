from django.urls import path
from . import views

app_name = 'ai_assistant'

urlpatterns = [
    # Sales Co-Pilot
    path('copilot/', views.copilot_view, name='copilot'),
    path('generate-suggestion/', views.generate_suggestion_view, name='generate_suggestion'),
    path('save-conversation/', views.save_conversation_view, name='save_conversation'),
    path('conversation/<int:conversation_id>/', views.conversation_detail_view, name='conversation_detail'),

    # Learning
    path('learning/', views.learning_view, name='learning'),
    path('generate-learning-content/', views.generate_learning_content_view, name='generate_learning_content'),
    path('learning-content/<int:content_id>/', views.learning_content_detail_view, name='learning_content_detail'),
    path('mark-content-complete/<int:content_id>/', views.mark_content_complete_view, name='mark_content_complete'),
    # Add these URLs
    path('get-quiz-questions/<int:content_id>/', views.get_quiz_questions_view, name='get_quiz_questions'),
    path('submit-quiz-results/<int:content_id>/', views.submit_quiz_results_view, name='submit_quiz_results'),

    # Leads
    path('leads/', views.leads_view, name='leads'),
    path('add-lead/', views.add_lead_view, name='add_lead'),
    path('update-lead-status/<int:lead_id>/', views.update_lead_status_view, name='update_lead_status'),
    path('generate-lead-message/<int:lead_id>/', views.generate_lead_message_view, name='generate_lead_message'),
    path('analyze-leads/', views.analyze_leads_view, name='analyze_leads'),

    # Insights
    path('check-insights/', views.check_insights_view, name='check_insights'),
    path('insights/', views.insights_view, name='insights'),
]