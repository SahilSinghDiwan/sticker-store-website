from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.payment import create_payment_intent, handle_payment_success
from utils import handle_error
import stripe
import os

payment_routes = Blueprint('payment_routes', __name__)

@payment_routes.route('/create-payment-intent', methods=['POST'])
@jwt_required()
async def create_intent():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        result = await create_payment_intent(
            user_id=user_id,
            shipping_address=data.get('shipping_address')
        )
        
        return jsonify(result), 200
    except Exception as e:
        return handle_error(e)

@payment_routes.route('/webhook', methods=['POST'])
async def webhook():
    payload = request.get_data()
    sig_header = request.headers.get('Stripe-Signature')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, os.getenv('STRIPE_WEBHOOK_SECRET')
        )
        
        if event['type'] == 'payment_intent.succeeded':
            payment_intent = event['data']['object']
            await handle_payment_success(payment_intent['id'])
            
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        return handle_error(e) 