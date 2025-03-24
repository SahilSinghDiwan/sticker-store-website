from flask import Blueprint, request, jsonify
from data.admin_config import require_admin
from services.products import add_product, update_product, delete_product, get_products
from werkzeug.utils import secure_filename
import os

admin_routes = Blueprint('admin_routes', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@admin_routes.route('/admin/products', methods=['GET', 'POST'])
@require_admin
def manage_products():
    if request.method == 'GET':
        try:
            products = get_products()
            return jsonify({"products": products}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    elif request.method == 'POST':
        try:
            if 'image' not in request.files:
                return jsonify({"error": "No image file provided"}), 400

            file = request.files['image']
            if file.filename == '':
                return jsonify({"error": "No selected file"}), 400

            if not allowed_file(file.filename):
                return jsonify({"error": "File type not allowed"}), 400

            # Get other product data
            name = request.form.get('name')
            price = request.form.get('price')
            description = request.form.get('description')

            if not all([name, price, description]):
                return jsonify({"error": "Missing required fields"}), 400

            product = add_product(name, float(price), description, file)
            return jsonify({"message": "Product added successfully", "product": product}), 201

        except Exception as e:
            return jsonify({"error": str(e)}), 500

@admin_routes.route('/admin/products/<product_id>', methods=['PUT', 'DELETE'])
@require_admin
def manage_product(product_id):
    if request.method == 'PUT':
        try:
            updates = {}
            if 'name' in request.form:
                updates['name'] = request.form['name']
            if 'price' in request.form:
                updates['price'] = float(request.form['price'])
            if 'description' in request.form:
                updates['description'] = request.form['description']

            if 'image' in request.files:
                file = request.files['image']
                if file.filename != '' and allowed_file(file.filename):
                    updates['image'] = file

            product = update_product(product_id, updates)
            return jsonify({"message": "Product updated successfully", "product": product}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    elif request.method == 'DELETE':
        try:
            success = delete_product(product_id)
            if success:
                return jsonify({"message": "Product deleted successfully"}), 200
            return jsonify({"error": "Product not found"}), 404

        except Exception as e:
            return jsonify({"error": str(e)}), 500 