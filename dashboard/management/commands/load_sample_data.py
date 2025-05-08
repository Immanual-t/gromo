# Create a file at: finarva_ai/dashboard/management/commands/load_sample_data.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import UserProfile, Skill, LearningProgress
from dashboard.models import SalesPerformance, AIInsight, CustomerLead
from ai_assistant.models import LearningContent
from django.utils import timezone
import datetime


class Command(BaseCommand):
    help = 'Loads sample data for FinArva AI project'

    def handle(self, *args, **kwargs):
        self.stdout.write('Loading sample data...')

        # Sample user data
        # Sample data to populate User and UserProfile models
        users_data = [
            {
                'username': 'rahul_sharma',
                'email': 'rahul.sharma@example.com',
                'first_name': 'Rahul',
                'last_name': 'Sharma',
                'password': 'securepassword123',
                'profile': {
                    'phone_number': '9876543210',
                    'city': 'Mumbai',
                    'state': 'Maharashtra',
                    'partner_id': 'GP001',
                    'experience_level': 'intermediate'
                }
            },
            {
                'username': 'priya_patel',
                'email': 'priya.patel@example.com',
                'first_name': 'Priya',
                'last_name': 'Patel',
                'password': 'securepassword456',
                'profile': {
                    'phone_number': '9876543211',
                    'city': 'Delhi',
                    'state': 'Delhi',
                    'partner_id': 'GP002',
                    'experience_level': 'beginner'
                }
            },
            {
                'username': 'amit_kumar',
                'email': 'amit.kumar@example.com',
                'first_name': 'Amit',
                'last_name': 'Kumar',
                'password': 'securepassword789',
                'profile': {
                    'phone_number': '9876543212',
                    'city': 'Bangalore',
                    'state': 'Karnataka',
                    'partner_id': 'GP003',
                    'experience_level': 'expert'
                }
            }
        ]

        # Sample data for Skills
        skills_data = [
            {
                'username': 'rahul_sharma',
                'product_type': 'insurance',
                'proficiency_level': 7
            },
            {
                'username': 'rahul_sharma',
                'product_type': 'credit_card',
                'proficiency_level': 5
            },
            {
                'username': 'rahul_sharma',
                'product_type': 'loan',
                'proficiency_level': 6
            },
            {
                'username': 'priya_patel',
                'product_type': 'insurance',
                'proficiency_level': 3
            },
            {
                'username': 'priya_patel',
                'product_type': 'investment',
                'proficiency_level': 4
            },
            {
                'username': 'amit_kumar',
                'product_type': 'insurance',
                'proficiency_level': 9
            },
            {
                'username': 'amit_kumar',
                'product_type': 'credit_card',
                'proficiency_level': 8
            },
            {
                'username': 'amit_kumar',
                'product_type': 'loan',
                'proficiency_level': 8
            },
            {
                'username': 'amit_kumar',
                'product_type': 'investment',
                'proficiency_level': 9
            }
        ]

        # Sample data for SalesPerformance
        import datetime
        from django.utils import timezone

        today = timezone.now().date()
        yesterday = today - datetime.timedelta(days=1)
        week_ago = today - datetime.timedelta(days=7)

        sales_data = [
            {
                'username': 'rahul_sharma',
                'date': today,
                'product': 'Term Life Insurance',
                'customer_name': 'Vikram Mehta',
                'customer_type': 'new',
                'amount': 25000,
                'product_category': 'insurance',
                'lead_source': 'direct'
            },
            {
                'username': 'rahul_sharma',
                'date': yesterday,
                'product': 'Health Insurance',
                'customer_name': 'Sneha Reddy',
                'customer_type': 'referred',
                'amount': 15000,
                'product_category': 'insurance',
                'lead_source': 'referral'
            },
            {
                'username': 'rahul_sharma',
                'date': week_ago,
                'product': 'HDFC Credit Card',
                'customer_name': 'Rajesh Khanna',
                'customer_type': 'existing',
                'amount': 1000,
                'product_category': 'credit_card',
                'lead_source': 'ai_suggested'
            },
            {
                'username': 'priya_patel',
                'date': today,
                'product': 'SBI Mutual Fund',
                'customer_name': 'Ananya Singh',
                'customer_type': 'new',
                'amount': 50000,
                'product_category': 'investment',
                'lead_source': 'direct'
            },
            {
                'username': 'priya_patel',
                'date': week_ago,
                'product': 'Personal Loan',
                'customer_name': 'Karan Malhotra',
                'customer_type': 'referred',
                'amount': 200000,
                'product_category': 'loan',
                'lead_source': 'referral'
            },
            {
                'username': 'amit_kumar',
                'date': today,
                'product': 'ICICI Credit Card',
                'customer_name': 'Neha Sharma',
                'customer_type': 'new',
                'amount': 2000,
                'product_category': 'credit_card',
                'lead_source': 'ai_suggested'
            },
            {
                'username': 'amit_kumar',
                'date': yesterday,
                'product': 'Car Insurance',
                'customer_name': 'Suresh Kumar',
                'customer_type': 'existing',
                'amount': 12000,
                'product_category': 'insurance',
                'lead_source': 'direct'
            },
            {
                'username': 'amit_kumar',
                'date': week_ago,
                'product': 'Home Loan',
                'customer_name': 'Divya Patel',
                'customer_type': 'referred',
                'amount': 1500000,
                'product_category': 'loan',
                'lead_source': 'campaign'
            }
        ]

        # Sample leads data
        # Sample data for CustomerLead
        leads_data = [
            {
                'username': 'rahul_sharma',
                'name': 'Ajay Verma',
                'phone': '9988776655',
                'email': 'ajay.verma@example.com',
                'interest': 'insurance',
                'status': 'new',
                'lead_source': 'manual',
                'priority_score': 0.85
            },
            {
                'username': 'rahul_sharma',
                'name': 'Meena Gupta',
                'phone': '9988776656',
                'email': 'meena.gupta@example.com',
                'interest': 'credit_card',
                'status': 'contacted',
                'lead_source': 'ai_suggested',
                'priority_score': 0.75
            },
            {
                'username': 'rahul_sharma',
                'name': 'Rahul Verma',
                'phone': '9988776657',
                'email': 'rahul.verma@example.com',
                'interest': 'loan',
                'status': 'interested',
                'lead_source': 'referral',
                'priority_score': 0.90
            },
            {
                'username': 'priya_patel',
                'name': 'Kavita Singh',
                'phone': '9988776658',
                'email': 'kavita.singh@example.com',
                'interest': 'investment',
                'status': 'new',
                'lead_source': 'manual',
                'priority_score': 0.80
            },
            {
                'username': 'priya_patel',
                'name': 'Sameer Joshi',
                'phone': '9988776659',
                'email': 'sameer.joshi@example.com',
                'interest': 'insurance',
                'status': 'contacted',
                'lead_source': 'campaign',
                'priority_score': 0.70
            },
            {
                'username': 'amit_kumar',
                'name': 'Preeti Sharma',
                'phone': '9988776660',
                'email': 'preeti.sharma@example.com',
                'interest': 'credit_card',
                'status': 'interested',
                'lead_source': 'ai_suggested',
                'priority_score': 0.95
            },
            {
                'username': 'amit_kumar',
                'name': 'Vishal Mehta',
                'phone': '9988776661',
                'email': 'vishal.mehta@example.com',
                'interest': 'loan',
                'status': 'contacted',
                'lead_source': 'referral',
                'priority_score': 0.85
            },
            {
                'username': 'amit_kumar',
                'name': 'Sanjay Patel',
                'phone': '9988776662',
                'email': 'sanjay.patel@example.com',
                'interest': 'investment',
                'status': 'converted',
                'lead_source': 'manual',
                'priority_score': 0.60
            }
        ]

        # Sample learning content data
        # Sample data for LearningContent
        learning_content_data = [
            {
                'username': 'rahul_sharma',
                'product_type': 'insurance',
                'topic': 'Understanding Term Life Insurance',
                'summary': 'A comprehensive guide to term life insurance products and their key benefits.',
                'content': """
        # Understanding Term Life Insurance

        Term Life Insurance is a pure protection plan that provides financial security to your family in case of your untimely demise. It's the most straightforward form of life insurance.

        ## Key Features

        - **Pure Protection**: Focuses solely on providing a death benefit
        - **Affordable Premiums**: Lower cost compared to other life insurance products
        - **Fixed Term**: Coverage for a specific period (10, 20, 30 years)
        - **No Maturity Benefit**: No returns if you survive the policy term
        - **Tax Benefits**: Premium payments qualify for tax deductions under Section 80C

        ## Benefits for Customers

        - **High Coverage at Low Cost**: Get significant coverage amount at affordable premium rates
        - **Financial Security**: Ensures your family's financial needs are met in your absence
        - **Loan Coverage**: Can be used to cover outstanding loans
        - **Simplicity**: Easy to understand with no complex investment components
        - **Riders**: Additional benefits like critical illness coverage can be added

        ## Common Objections & Responses

        ### "I already have life insurance through my employer"
        Response: Employer coverage is typically limited and ends when you leave the job. A personal term plan ensures consistent coverage regardless of employment status.

        ### "Term insurance has no returns"
        Response: True, but this is why it's so affordable. The low premium means you can invest the difference in other high-return instruments, potentially earning more overall.

        ### "I'm young and healthy, I don't need insurance yet"
        Response: Youth is actually the best time to buy term insurance! Premiums are lowest when you're young and healthy, and you can lock in these rates for decades.

        ## Selling Tips

        1. Focus on the **protection amount** rather than the premium cost
        2. Calculate the **human life value** to help customers understand how much coverage they need
        3. Highlight the **tax benefits** under Section 80C
        4. Explain how term insurance fits into a **complete financial plan**
        5. Use **real-life examples** of how families benefited from term insurance in difficult times

        Remember, term insurance isn't just a product—it's peace of mind for your customer's family.
                """,
                'difficulty_level': 'intermediate',
                'is_read': True
            },
            {
                'username': 'priya_patel',
                'product_type': 'investment',
                'topic': 'Mutual Funds Basics',
                'summary': 'Introduction to mutual funds and techniques for explaining them to customers.',
                'content': """
        # Mutual Funds Basics

        Mutual funds are investment vehicles that pool money from multiple investors to purchase securities like stocks, bonds, and other assets.

        ## Key Features

        - **Professional Management**: Managed by investment professionals
        - **Diversification**: Money spread across multiple securities
        - **Affordability**: Start with as little as ₹500 per month
        - **Liquidity**: Generally easy to buy and sell
        - **Regulated**: Overseen by SEBI for investor protection

        ## Types of Mutual Funds

        1. **Equity Funds**: Invest primarily in stocks
           - Large Cap: Lower risk, stable companies
           - Mid Cap: Medium risk, growth potential
           - Small Cap: Higher risk, higher growth potential
           - Sector Funds: Focus on specific industries

        2. **Debt Funds**: Invest in fixed income securities
           - Liquid Funds: Very low risk, short-term
           - Corporate Bond Funds: Medium risk
           - Government Securities Funds: Low risk

        3. **Hybrid Funds**: Mix of equity and debt
           - Balanced Funds: Equal mix of stocks and bonds
           - Monthly Income Plans: Focus on regular income

        ## Benefits for Customers

        - **Professional Management**: Expert handling of investments
        - **Diversification**: Reduced risk through variety
        - **Affordability**: Start small and increase over time
        - **Convenience**: Easy to monitor and manage
        - **Tax Efficiency**: Equity funds have tax advantages for long-term holding

        ## Common Objections & Responses

        ### "Mutual funds are too risky"
        Response: Different types of mutual funds have different risk levels. We can choose one that matches your risk tolerance, including very conservative options like liquid funds.

        ### "I don't understand the market"
        Response: That's exactly why mutual funds are beneficial! Professional fund managers make the investment decisions based on research and expertise.

        ### "I've heard people lose money in mutual funds"
        Response: While all investments carry some risk, mutual funds reduce risk through diversification. Additionally, historical data shows that equity mutual funds have outperformed traditional savings over long periods.

        ## Selling Tips

        1. Always start with understanding the **customer's financial goals**
        2. Explain mutual funds using **simple analogies** rather than technical terms
        3. Show the power of **compounding** with practical examples
        4. Highlight the **SIP approach** for disciplined investing
        5. Use **visual aids** to explain concepts like diversification and fund types

        Remember, selling mutual funds is about matching the right product to the right customer needs and risk profile.
                """,
                'difficulty_level': 'beginner',
                'is_read': False
            },
            {
                'username': 'amit_kumar',
                'product_type': 'credit_card',
                'topic': 'Advanced Credit Card Sales Techniques',
                'summary': 'Advanced strategies for selling credit cards to different customer segments.',
                'content': """
        # Advanced Credit Card Sales Techniques

        This module covers sophisticated approaches to selling credit cards to different customer segments, with a focus on needs-based selling and overcoming complex objections.

        ## Segmentation Strategies

        ### Premium Customers
        - Focus on exclusive benefits, concierge services, and status
        - Emphasize travel benefits, lounge access, and premium metal cards
        - Highlight higher credit limits and premium insurance covers

        ### Middle-Income Segment
        - Focus on rewards programs, cashback, and EMI conversion facilities
        - Emphasize fuel surcharge waivers and dining discounts
        - Highlight special offers and festival discounts

        ### First-Time Users
        - Focus on credit building benefits and financial discipline
        - Emphasize zero annual fee options and simple reward structures
        - Highlight security features and low minimum income requirements

        ## Advanced Needs Analysis

        1. **Spending Pattern Analysis**
           - Analyze monthly expenditure across categories
           - Identify high-spend areas (dining, travel, shopping)
           - Match card benefits to spending patterns

        2. **Lifestyle Mapping**
           - Assess travel frequency and destinations
           - Evaluate entertainment and dining preferences
           - Understand shopping habits (online vs. offline)

        3. **Financial Behavior Assessment**
           - Credit utilization patterns
           - Payment behaviors (full payment vs. EMI)
           - Revolving credit needs

        ## Handling Sophisticated Objections

        ### "I've calculated the value of rewards, and they don't offset the annual fee"
        Response: Let's analyze your specific spending pattern and demonstrate the actual value including hidden benefits like complimentary insurance, lounge access, and concierge services that aren't easily quantifiable.

        ### "I'm concerned about hidden charges and interest complications"
        Response: That's a valid concern. Let me walk you through our transparent fee structure, interest calculation method, and interest-free periods. We can also set up automatic reminders to help you avoid any unexpected charges.

        ### "I already have multiple cards and don't see the value in another one"
        Response: Having multiple cards can actually be strategic. Different cards optimize different spending categories. Based on your spending pattern, this card could complement your existing cards by providing superior benefits for [specific category] where you spend significantly.

        ## Conversion Acceleration Techniques

        1. **Limited-Time Welcome Benefits**
           - Highlight special introductory offers with clear deadlines
           - Create urgency with time-bound application bonuses

        2. **Immediate Gratification Hooks**
           - Instant approval processes
           - Digital card issuance for immediate use
           - Same-day physical card delivery options

        3. **Competitive Displacement Strategies**
           - Direct comparison with competitor cards
           - Balance transfer opportunities with preferential terms
           - Reward point transfer/matching programs

        4. **Social Proof Leveraging**
           - Share anonymized success stories from similar customers
           - Reference industry awards and recognition
           - Highlight user satisfaction statistics

        Remember that advanced credit card sales require you to position yourself as a financial advisor rather than just a salesperson. Your goal is to help customers optimize their financial instruments for maximum benefit.
                """,
                'difficulty_level': 'advanced',
                'is_read': False
            }
        ]

        # Sample data for AIInsight
        ai_insight_data = [
            {
                'username': 'rahul_sharma',
                'insight_text': 'Your insurance sales have increased by 15% this month. Consider cross-selling credit cards to your recent insurance customers for greater commission potential.',
                'category': 'performance',
                'is_read': False
            },
            {
                'username': 'rahul_sharma',
                'insight_text': 'Your customer Meena Gupta has shown interest in credit cards. Based on her profile, the Premium Travel Card would be a good match for her spending habits.',
                'category': 'lead',
                'is_read': True
            },
            {
                'username': 'priya_patel',
                'insight_text': 'Consider completing the Mutual Funds Basics course to improve your investment product knowledge. This could help increase your conversion rate for investment leads.',
                'category': 'learning',
                'is_read': False
            },
            {
                'username': 'priya_patel',
                'insight_text': 'Your average sale value is 20% higher than the platform average. Great job focusing on higher-value products!',
                'category': 'performance',
                'is_read': True
            },
            {
                'username': 'amit_kumar',
                'insight_text': 'Your lead Preeti Sharma has been in "interested" status for 7 days. This is a good time to follow up with a personalized offer to convert the lead.',
                'category': 'lead',
                'is_read': False
            },
            {
                'username': 'amit_kumar',
                'insight_text': 'Try scheduling your customer calls in the evening. Your data shows a 25% higher conversion rate for calls made between 6-8 PM compared to morning calls.',
                'category': 'sales',
                'is_read': True
            }
        ]

        # Create users and profiles
        for user_data in users_data:
            # Check if user exists
            if not User.objects.filter(username=user_data['username']).exists():
                user = User.objects.create_user(
                    username=user_data['username'],
                    email=user_data['email'],
                    password=user_data['password']
                )
                user.first_name = user_data['first_name']
                user.last_name = user_data['last_name']
                user.save()

                # Create or update profile
                profile = user.profile
                profile.phone_number = user_data['profile']['phone_number']
                profile.city = user_data['profile']['city']
                profile.state = user_data['profile']['state']
                profile.partner_id = user_data['profile']['partner_id']
                profile.experience_level = user_data['profile']['experience_level']
                profile.save()

                self.stdout.write(self.style.SUCCESS(f'Created user: {user.username}'))
            else:
                self.stdout.write(f'User {user_data["username"]} already exists, skipping...')

        # Create skills
        for skill_data in skills_data:
            user = User.objects.get(username=skill_data['username'])
            skill, created = Skill.objects.get_or_create(
                user=user,
                product_type=skill_data['product_type'],
                defaults={'proficiency_level': skill_data['proficiency_level']}
            )
            if not created:
                skill.proficiency_level = skill_data['proficiency_level']
                skill.save()

            if created:
                self.stdout.write(self.style.SUCCESS(f'Created skill: {user.username} - {skill.product_type}'))

        # Create sales
        for sale_data in sales_data:
            user = User.objects.get(username=sale_data['username'])
            sale, created = SalesPerformance.objects.get_or_create(
                user=user,
                date=sale_data['date'],
                product=sale_data['product'],
                customer_name=sale_data['customer_name'],
                defaults={
                    'customer_type': sale_data['customer_type'],
                    'amount': sale_data['amount'],
                    'commission': sale_data['amount'] * 0.1,  # Simple commission calculation
                    'product_category': sale_data['product_category'],
                    'lead_source': sale_data['lead_source']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created sale: {user.username} - {sale.product}'))

        # Create leads
        for lead_data in leads_data:
            user = User.objects.get(username=lead_data['username'])
            lead, created = CustomerLead.objects.get_or_create(
                user=user,
                name=lead_data['name'],
                phone=lead_data['phone'],
                defaults={
                    'email': lead_data['email'],
                    'interest': lead_data['interest'],
                    'status': lead_data['status'],
                    'lead_source': lead_data['lead_source'],
                    'priority_score': lead_data['priority_score']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created lead: {user.username} - {lead.name}'))

        # Create learning content
        for content_data in learning_content_data:
            user = User.objects.get(username=content_data['username'])
            content, created = LearningContent.objects.get_or_create(
                user=user,
                topic=content_data['topic'],
                defaults={
                    'product_type': content_data['product_type'],
                    'summary': content_data['summary'],
                    'content': content_data['content'],
                    'difficulty_level': content_data['difficulty_level'],
                    'is_read': content_data['is_read']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created learning content: {user.username} - {content.topic}'))

        # Create AI insights
        for insight_data in ai_insight_data:
            user = User.objects.get(username=insight_data['username'])
            insight, created = AIInsight.objects.get_or_create(
                user=user,
                insight_text=insight_data['insight_text'],
                defaults={
                    'category': insight_data['category'],
                    'is_read': insight_data['is_read']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created AI insight: {user.username} - {insight.category}'))

        self.stdout.write(self.style.SUCCESS('Successfully loaded all sample data!'))