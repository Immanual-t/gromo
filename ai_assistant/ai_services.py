import os
import json
import logging
import openai
from django.conf import settings
from django.utils import timezone
from .models import AIResponse
from dashboard.models import AIInsight, CustomerLead

# Configure OpenAI API
openai.api_key = settings.OPENAI_API_KEY

# Set up logging
logger = logging.getLogger(__name__)


class AIService:
    """Base class for all AI services"""

    @staticmethod
    def generate_response(messages, max_tokens=500):
        """
        Generate a response using OpenAI API

        Args:
            messages (list): List of message dictionaries with role and content
            max_tokens (int): Maximum tokens for response

        Returns:
            str: Generated response text
        """
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=max_tokens,
                temperature=0.7,
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            logger.error(f"Error generating OpenAI response: {str(e)}")
            return "I'm sorry, I'm having trouble connecting to my AI services. Please try again later."

    @staticmethod
    def log_interaction(user, request_type, prompt, response):
        """Log AI interaction to database"""
        try:
            AIResponse.objects.create(
                user=user,
                request_type=request_type,
                prompt=json.dumps(prompt) if isinstance(prompt, list) else prompt,
                response=response
            )
        except Exception as e:
            logger.error(f"Error logging AI interaction: {str(e)}")


class SalesCopilotService(AIService):
    """Service for sales co-pilot functionality"""

    @classmethod
    def generate_sales_suggestion(cls, user, messages):
        """Generate sales suggestion based on conversation"""
        try:
            # Extract conversation context
            prompt = messages

            # Generate response
            response = cls.generate_response(prompt, max_tokens=600)

            # Log interaction
            cls.log_interaction(user, 'copilot', prompt, response)

            return {'status': 'success', 'response': response}

        except Exception as e:
            logger.error(f"Error in sales suggestion: {str(e)}")
            return {'status': 'error', 'message': str(e)}

    @classmethod
    def handle_objection(cls, user, objection, product_type):
        """Generate response to customer objection"""
        try:
            # Create prompt
            prompt = [
                {"role": "system",
                 "content": f"You are an AI sales assistant helping a financial agent sell {product_type} products in India. You provide concise, effective responses to customer objections."},
                {"role": "user",
                 "content": f"The customer has raised this objection: '{objection}'. How should I respond to overcome this objection and continue the sale? Give me a short, practical response I can use with the customer."}
            ]

            # Generate response
            response = cls.generate_response(prompt, max_tokens=400)

            # Log interaction
            cls.log_interaction(user, 'copilot', prompt, response)

            return {'status': 'success', 'response': response}

        except Exception as e:
            logger.error(f"Error handling objection: {str(e)}")
            return {'status': 'error', 'message': str(e)}


class LearningService(AIService):
    """Service for personalized learning content"""

    @classmethod
    def generate_learning_content(cls, user, product_type, skill_level):
        """Generate personalized learning content"""
        try:
            # Create prompt
            prompt = [
                {"role": "system",
                 "content": f"You are an AI educator specializing in teaching financial agents how to sell {product_type} products in India. Create personalized learning content for a {skill_level} level agent."},
                {"role": "user",
                 "content": f"Create a concise, practical learning module about selling {product_type} products. Include key features, benefits, common objections, and effective sales techniques. The content should be appropriate for a {skill_level} level agent working in India. Format with headings and bullet points for readability."}
            ]

            # Generate response
            response = cls.generate_response(prompt, max_tokens=1000)

            # Log interaction
            cls.log_interaction(user, 'learning', prompt, response)

            return {'status': 'success', 'response': response}

        except Exception as e:
            logger.error(f"Error generating learning content: {str(e)}")
            return {'status': 'error', 'message': str(e)}

    @classmethod
    def generate_quiz_questions(cls, user, product_type, skill_level):
        """Generate quiz questions for skill assessment"""
        try:
            # Create prompt
            prompt = [
                {"role": "system",
                 "content": f"You are an AI educator creating assessment questions for financial agents selling {product_type} products in India."},
                {"role": "user",
                 "content": f"Create 5 multiple-choice questions to assess knowledge about {product_type} products for a {skill_level} level agent. Each question should have 4 options with 1 correct answer. Format the response as a JSON array of question objects."}
            ]

            # Generate response
            response = cls.generate_response(prompt, max_tokens=800)

            # Try to parse JSON
            try:
                questions = json.loads(response)
            except json.JSONDecodeError:
                # If response is not valid JSON, extract JSON part
                import re
                json_match = re.search(r'(\[{.*}])', response.replace('\n', ''))
                if json_match:
                    try:
                        questions = json.loads(json_match.group(1))
                    except json.JSONDecodeError:
                        questions = []
                else:
                    questions = []

            # Log interaction
            cls.log_interaction(user, 'learning', prompt, response)

            return {'status': 'success', 'questions': questions}

        except Exception as e:
            logger.error(f"Error generating quiz questions: {str(e)}")
            return {'status': 'error', 'message': str(e)}


class LeadService(AIService):
    """Service for lead management and suggestions"""

    @classmethod
    def analyze_leads(cls, user, leads_data):
        """Analyze leads and provide insights"""
        try:
            # Create prompt
            leads_json = json.dumps(leads_data)
            prompt = [
                {"role": "system",
                 "content": "You are an AI sales assistant helping a financial agent analyze customer leads to identify the most promising ones."},
                {"role": "user",
                 "content": f"Analyze these leads and identify the 3 most promising ones with specific reasons for each. Also provide 1 general tip for improving lead conversion: {leads_json}"}
            ]

            # Generate response
            response = cls.generate_response(prompt, max_tokens=700)

            # Log interaction
            cls.log_interaction(user, 'lead', prompt, response)

            return {'status': 'success', 'response': response}

        except Exception as e:
            logger.error(f"Error analyzing leads: {str(e)}")
            return {'status': 'error', 'message': str(e)}

    @classmethod
    def generate_outreach_message(cls, user, lead_data, product_type):
        """Generate a personalized outreach message for a lead"""
        try:
            # Create prompt
            prompt = [
                {"role": "system",
                 "content": f"You are an AI assistant helping a financial agent create personalized outreach messages for potential {product_type} customers in India."},
                {"role": "user",
                 "content": f"Create a short, personalized WhatsApp or SMS message for this lead interested in {product_type}. The message should be friendly, concise, and include a clear next step: {json.dumps(lead_data)}"}
            ]

            # Generate response
            response = cls.generate_response(prompt, max_tokens=300)

            # Log interaction
            cls.log_interaction(user, 'lead', prompt, response)

            return {'status': 'success', 'response': response}

        except Exception as e:
            logger.error(f"Error generating outreach message: {str(e)}")
            return {'status': 'error', 'message': str(e)}


class PerformanceInsightService(AIService):
    """Service for generating performance insights"""

    @classmethod
    def generate_insight(cls, user, sales_data):
        """Generate performance insight from sales data"""
        try:
            # Create prompt
            sales_json = json.dumps(sales_data)
            prompt = [
                {"role": "system",
                 "content": "You are an AI assistant that analyzes sales performance data and provides helpful insights and suggestions for financial agents in India."},
                {"role": "user",
                 "content": f"Analyze this sales performance data and provide ONE concise, actionable insight that can help improve results: {sales_json}"}
            ]

            # Generate response
            response = cls.generate_response(prompt, max_tokens=300)

            # Create insight object
            insight = AIInsight.objects.create(
                user=user,
                insight_text=response,
                category='performance'
            )

            # Log interaction
            cls.log_interaction(user, 'performance', prompt, response)

            return {'status': 'success', 'insight': response, 'insight_id': insight.id}

        except Exception as e:
            logger.error(f"Error generating performance insight: {str(e)}")
            return {'status': 'error', 'message': str(e)}

    @classmethod
    def suggest_next_action(cls, user, recent_activity):
        """Suggest next best action for the agent"""
        try:
            # Create prompt
            activity_json = json.dumps(recent_activity)
            prompt = [
                {"role": "system",
                 "content": "You are an AI assistant that suggests the next best action for financial agents to maximize their sales and earnings."},
                {"role": "user",
                 "content": f"Based on this agent's recent activity, suggest ONE specific, high-value action they should take next to improve their results: {activity_json}"}
            ]

            # Generate response
            response = cls.generate_response(prompt, max_tokens=300)

            # Create insight object
            insight = AIInsight.objects.create(
                user=user,
                insight_text=response,
                category='sales'
            )

            # Log interaction
            cls.log_interaction(user, 'performance', prompt, response)

            return {'status': 'success', 'suggestion': response, 'insight_id': insight.id}

        except Exception as e:
            logger.error(f"Error suggesting next action: {str(e)}")
            return {'status': 'error', 'message': str(e)}