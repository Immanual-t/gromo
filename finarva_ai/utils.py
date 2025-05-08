import json
import logging
from functools import wraps
from django.http import JsonResponse
from django.conf import settings

logger = logging.getLogger(__name__)


def api_error_handler(f):
    """
    Decorator to handle API errors gracefully
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            logger.error(f"API Error: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)

    return decorated


def format_currency(amount):
    """
    Format amount as Indian Rupees
    """
    try:
        return f"₹{float(amount):,.2f}"
    except (ValueError, TypeError):
        return "₹0.00"


def get_performance_insights(sales_data):
    """
    Generate simple performance insights from sales data
    """
    if not sales_data:
        return []

    insights = []

    # Total sales amount
    total_amount = sum(item.get('amount', 0) for item in sales_data)

    # Average sale value
    avg_sale = total_amount / len(sales_data) if sales_data else 0

    # Product distribution
    product_counts = {}
    for item in sales_data:
        product = item.get('product', 'Unknown')
        product_counts[product] = product_counts.get(product, 0) + 1

    # Most sold product
    if product_counts:
        most_sold = max(product_counts.items(), key=lambda x: x[1])
        insights.append(f"Your top selling product is {most_sold[0]} with {most_sold[1]} sales")

    # Average insight
    insights.append(f"Your average sale value is {format_currency(avg_sale)}")

    # Recent performance
    if len(sales_data) >= 5:
        recent_sales = sales_data[-5:]
        recent_total = sum(item.get('amount', 0) for item in recent_sales)
        recent_avg = recent_total / len(recent_sales)

        if recent_avg > avg_sale:
            insights.append("Your recent performance is above your overall average!")
        else:
            insights.append("Your recent sales are below your usual average")

    return insights