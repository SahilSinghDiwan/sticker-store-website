import stripe
from typing import Dict, Any
import os
from datetime import datetime
from .orders import update_order_status, get_order
from .email import send_order_confirmation
from ..models.order import OrderStatus

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET')

async def create_payment_intent(
    amount: float,
    currency: str = 'usd',
    metadata: Dict[str, str] = None
) -> Dict[str, Any]:
    """Create a Stripe PaymentIntent"""
    try:
        # Convert amount to cents
        amount_cents = int(amount * 100)
        
        intent = stripe.PaymentIntent.create(
            amount=amount_cents,
            currency=currency,
            metadata=metadata or {},
            automatic_payment_methods={"enabled": True}
        )
        
        return {
            "client_secret": intent.client_secret,
            "payment_intent_id": intent.id
        }
    except stripe.error.StripeError as e:
        print(f"Stripe error: {str(e)}")
        raise ValueError("Failed to create payment intent")

async def handle_webhook_event(payload: Dict[str, Any], sig_header: str) -> None:
    """Handle Stripe webhook events"""
    try:
        # Verify webhook signature
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
        
        # Handle payment intent events
        if event['type'] == 'payment_intent.succeeded':
            payment_intent = event['data']['object']
            order_id = payment_intent['metadata'].get('order_id')
            
            if order_id:
                # Update order status
                order = await get_order(order_id)
                if order:
                    await update_order_status(order_id, 'paid')
                    # Send order confirmation email
                    await send_order_confirmation(order)
                
        elif event['type'] == 'payment_intent.payment_failed':
            payment_intent = event['data']['object']
            order_id = payment_intent['metadata'].get('order_id')
            
            if order_id:
                # Update order status to failed
                await update_order_status(order_id, 'payment_failed')
                
    except stripe.error.SignatureVerificationError:
        print("Invalid webhook signature")
        raise ValueError("Invalid webhook signature")
    except Exception as e:
        print(f"Error handling webhook: {str(e)}")
        raise ValueError("Failed to process webhook") 