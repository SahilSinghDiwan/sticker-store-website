import stripe
import os
from datetime import datetime
from db import orders_collection
from .cart import get_user_cart
from .orders import create_order
from .email import send_order_confirmation

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

async def create_payment_intent(user_id, shipping_address):
    """Create a Stripe PaymentIntent"""
    try:
        # Get cart total
        cart = get_user_cart(user_id)
        if not cart or not cart["items"]:
            raise ValueError("Cart is empty")
        
        # Create payment intent
        intent = stripe.PaymentIntent.create(
            amount=int(cart["total"] * 100),  # Convert to cents
            currency='usd',
            metadata={
                'user_id': user_id,
                'shipping_address': str(shipping_address)
            }
        )
        
        return {
            'client_secret': intent.client_secret,
            'total': cart["total"]
        }
    except stripe.error.StripeError as e:
        raise ValueError(f"Stripe error: {str(e)}")

async def handle_payment_success(payment_intent_id):
    """Handle successful payment"""
    try:
        # Retrieve payment intent
        intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        
        # Create order
        order = create_order(
            user_id=intent.metadata['user_id'],
            shipping_address=eval(intent.metadata['shipping_address']),
            payment_info={
                'payment_id': payment_intent_id,
                'amount': intent.amount / 100,
                'status': 'completed',
                'payment_method': intent.payment_method
            }
        )
        
        # Send confirmation email
        send_order_confirmation(order)
        
        return order
    except stripe.error.StripeError as e:
        raise ValueError(f"Stripe error: {str(e)}") 