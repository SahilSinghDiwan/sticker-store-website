from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from google.oauth2 import id_token
import requests

from auth import register_user, login_user, logout_user
from db import users_collection
from utils import setup_logger, handle_error
from services.cart import get_user_cart, add_to_cart, update_cart_item, remove_from_cart, clear_cart
from services.orders import get_user_orders, create_order
from services.products import get_products_from_s3
from services.users import get_user_by_provider_id, create_user

logger = setup_logger()

routes = Blueprint('routes', __name__)

@routes.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    required_fields = ['firstName', 'lastName', 'email', 'password', 'phoneNumber']
    
    # Validate required fields
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
        
    try:
        response = register_user(
            firstName=data['firstName'],
            lastName=data['lastName'],
            email=data['email'],
            password=data['password'],
            phoneNumber=data['phoneNumber']
        )
        logger.info(f"New user registered: {data['email']}")
        return response
    except Exception as e:
        logger.error(f"Error during signup: {e}")
        return handle_error(e)

@routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    try:
        response = login_user(data['email'], data['password'])
        logger.info(f"User logged in: {data['email']}")
        return response
    except Exception as e:
        logger.error(f"Error during login: {e}")
        return handle_error(e)

@routes.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    return {"message": "You have accessed a protected route!"}, 200

@routes.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    try:
        response = logout_user()
        logger.info(f"User logged out")
        return response
    except Exception as e:
        logger.error(f"Error during logout: {e}")
        return handle_error(e)

@routes.route('/products', methods=['GET'])
def get_products():
    try:
        products = get_products_from_s3()
        return jsonify({"products": products}), 200
    except Exception as e:
        logger.error(f"Error fetching products: {e}")
        return handle_error(e)

@routes.route('/cart', methods=['GET', 'POST', 'PUT', 'DELETE'])
@jwt_required()
def manage_cart():
    current_user_id = get_jwt_identity()
    
    try:
        if request.method == 'GET':
            cart = get_user_cart(current_user_id)
            return jsonify({"cart": cart}), 200
            
        elif request.method == 'POST':
            data = request.get_json()
            if not all(k in data for k in ['product_id', 'quantity']):
                return jsonify({"error": "Missing product_id or quantity"}), 400
                
            cart = add_to_cart(current_user_id, data['product_id'], data['quantity'])
            return jsonify({"cart": cart}), 201
            
        elif request.method == 'PUT':
            data = request.get_json()
            if not all(k in data for k in ['product_id', 'quantity']):
                return jsonify({"error": "Missing product_id or quantity"}), 400
                
            cart = update_cart_item(current_user_id, data['product_id'], data['quantity'])
            return jsonify({"cart": cart}), 200
            
        elif request.method == 'DELETE':
            data = request.get_json()
            if 'product_id' not in data:
                return jsonify({"error": "Missing product_id"}), 400
                
            cart = remove_from_cart(current_user_id, data['product_id'])
            return jsonify({"cart": cart}), 200
            
    except Exception as e:
        logger.error(f"Error managing cart for user {current_user_id}: {e}")
        return handle_error(e)

@routes.route('/orders', methods=['GET', 'POST'])
@jwt_required()
def manage_orders():
    current_user_id = get_jwt_identity()

    if request.method == 'GET':
        # Get user's order history
        try:
            orders = get_user_orders(current_user_id)
            return jsonify(orders), 200
        except Exception as e:
            logger.error(f"Error fetching orders for user {current_user_id}: {e}")
            return handle_error(e)

    elif request.method == 'POST':
        # Create new order from cart
        try:
            # Get cart contents
            cart = get_user_cart(current_user_id)
            
            if not cart or not cart['items']:
                return jsonify({'error': 'Cart is empty'}), 400

            # Create order from cart
            order = create_order(current_user_id, cart)
            
            # Clear the cart after successful order
            clear_cart(current_user_id)
            
            logger.info(f"Created new order for user {current_user_id}")
            return jsonify(order), 201

        except Exception as e:
            logger.error(f"Error creating order for user {current_user_id}: {e}")
            return handle_error(e)

@routes.route('/auth/google', methods=['POST'])
def google_auth():
    # Get the token from the request
    data = request.get_json()
    token = data.get('credential')
    
    if not token:
        return jsonify({'error': 'No credential provided'}), 400
        
    try:
        # Verify the token with Google
        idinfo = id_token.verify_oauth2_token(
            token, 
            requests.Request(),
            "190673516026-su10s74fljsnvamh06g7ivgbv1hls22l.apps.googleusercontent.com"
        )

        # Get user info from token
        user_id = idinfo['sub']
        email = idinfo['email']
        first_name = idinfo.get('given_name', '')
        last_name = idinfo.get('family_name', '')

        # Check if user exists
        user = get_user_by_provider_id('google', user_id)
        
        if not user:
            # Create new user
            user = create_user({
                'email': email,
                'details': {
                    'firstName': first_name,
                    'lastName': last_name,
                    'phoneNumber': ''  # Phone number will be empty for Google sign-ins
                },
                'provider': 'google',
                'providerId': user_id
            })

        # Generate JWT token
        access_token = create_access_token(identity=str(user['id']))
        
        return jsonify({
            'token': access_token,
            'userId': str(user['id'])
        }), 200
        
    except ValueError:
        # Invalid token
        return jsonify({'error': 'Invalid token'}), 401
    except Exception as e:
        logger.error(f"Error in Google authentication: {e}")
        return handle_error(e)