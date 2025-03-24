from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from ..db import db

shop = Blueprint('shop', __name__)

@shop.route('/products', methods=['GET'])
def get_products():
    try:
        products = list(db.products.find({'active': True}))
        for product in products:
            product['_id'] = str(product['_id'])
        return jsonify({'products': products})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@shop.route('/cart', methods=['GET'])
@jwt_required()
def get_cart():
    try:
        user_id = get_jwt_identity()
        cart = db.carts.find_one({'user_id': user_id})
        if cart:
            cart['_id'] = str(cart['_id'])
        return jsonify({'cart': cart})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@shop.route('/cart/add', methods=['POST'])
@jwt_required()
def add_to_cart():
    try:
        user_id = get_jwt_identity()
        data = request.json
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)

        product = db.products.find_one({'_id': ObjectId(product_id)})
        if not product:
            return jsonify({'error': 'Product not found'}), 404

        db.carts.update_one(
            {'user_id': user_id},
            {
                '$push': {
                    'items': {
                        'product_id': product_id,
                        'quantity': quantity,
                        'price': product['price']
                    }
                }
            },
            upsert=True
        )
        return jsonify({'message': 'Product added to cart'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500 