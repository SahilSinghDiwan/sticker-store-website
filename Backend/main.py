"""Minimal Flask API for local Docker development."""

import os
import re
import time
from datetime import datetime, timedelta
from pathlib import PurePosixPath
from urllib.parse import quote

import boto3
from bson import ObjectId
from bson.errors import InvalidId
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
)
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from werkzeug.security import check_password_hash, generate_password_hash

load_dotenv()

app = Flask(__name__)

def require_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"{name} is not set; refusing to start. Set it in .env (see .env.example).")
    return value


app.config["SECRET_KEY"] = require_env("SECRET_KEY")
app.config["JWT_SECRET_KEY"] = require_env("JWT_SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)

cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost")
CORS(app, origins=[origin.strip() for origin in cors_origins.split(",") if origin.strip()], supports_credentials=True)

jwt = JWTManager(app)

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017/auth_db")
DB_NAME = os.getenv("MONGODB_DB_NAME", "auth_db")

client = None
db = None
users = None
products = None
carts = None

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
MIN_PASSWORD_LENGTH = 8

R2_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".avif", ".svg"}


def connect_db(retries: int = 30, delay: float = 2.0) -> None:
    global client, db, users, products, carts

    last_error = None
    for _ in range(retries):
        try:
            client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
            client.admin.command("ping")
            db = client[DB_NAME]
            users = db.users
            products = db.products
            carts = db.carts
            users.create_index("email", unique=True)
            return
        except ServerSelectionTimeoutError as exc:
            last_error = exc
            time.sleep(delay)

    raise RuntimeError(f"Could not connect to MongoDB at {MONGO_URI}") from last_error


def is_valid_email(value) -> bool:
    return isinstance(value, str) and len(value) <= 254 and bool(EMAIL_RE.match(value))


def to_object_id(value):
    """Return an ObjectId for value, or None if it is not a valid id."""
    try:
        return ObjectId(value)
    except (InvalidId, TypeError):
        return None


def serialize_user(doc: dict) -> dict:
    return {
        "_id": str(doc["_id"]),
        "email": doc["email"],
        "firstName": doc.get("firstName", ""),
        "lastName": doc.get("lastName", ""),
        "phoneNumber": doc.get("phoneNumber", ""),
        "role": doc.get("role", "user"),
    }


def serialize_product(doc: dict) -> dict:
    return {
        "_id": str(doc["_id"]),
        "name": doc["name"],
        "description": doc.get("description", ""),
        "price": doc.get("price", 0),
        "imageUrl": doc.get("imageUrl", ""),
        "stock": doc.get("stock", 0),
        "category": doc.get("category", "general"),
        "createdAt": doc.get("createdAt", datetime.utcnow()).isoformat(),
        "updatedAt": doc.get("updatedAt", datetime.utcnow()).isoformat(),
    }


def build_r2_client():
    access_key = os.getenv("R2_ACCESS_KEY_ID")
    secret_key = os.getenv("R2_SECRET_ACCESS_KEY")
    account_id = os.getenv("R2_ACCOUNT_ID")
    bucket = os.getenv("R2_BUCKET_NAME")

    if not all([access_key, secret_key, account_id, bucket]):
        return None, None

    endpoint = f"https://{account_id}.r2.cloudflarestorage.com"
    client = boto3.client(
        "s3",
        endpoint_url=endpoint,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name="auto",
    )
    return client, bucket


def format_product_name_from_key(key: str) -> str:
    filename = PurePosixPath(key).name
    name_without_ext = os.path.splitext(filename)[0]
    name_with_spaces = name_without_ext.replace("_", " ").replace("-", " ")
    return " ".join(word.capitalize() for word in name_with_spaces.split())


def derive_category_from_key(key: str) -> str:
    path_parts = PurePosixPath(key).parts
    if len(path_parts) > 1:
        return path_parts[0].strip().lower().replace(" ", "-")
    return "general"


def build_r2_public_url(base_url: str, key: str) -> str:
    encoded_segments = [quote(segment, safe="") for segment in PurePosixPath(key).parts]
    return f"{base_url.rstrip('/')}/{'/'.join(encoded_segments)}"


def list_r2_image_products(limit: int = 60) -> list[dict]:
    r2_public_base_url = os.getenv("R2_PUBLIC_BASE_URL", "").strip()
    if not r2_public_base_url:
        return []

    client, bucket = build_r2_client()
    if not client or not bucket:
        return []

    image_keys: list[str] = []
    paginator = client.get_paginator("list_objects_v2")

    try:
        for page in paginator.paginate(Bucket=bucket):
            for item in page.get("Contents", []):
                key = item.get("Key", "")
                if os.path.splitext(key)[1].lower() in R2_IMAGE_EXTENSIONS:
                    image_keys.append(key)
                    if len(image_keys) >= limit:
                        break
            if len(image_keys) >= limit:
                break
    except Exception:
        return []

    products_list = []
    now = datetime.utcnow()
    for key in image_keys:
        products_list.append(
            {
                "name": format_product_name_from_key(key),
                "description": f"Sticker from {derive_category_from_key(key)} collection.",
                "price": 4.99,
                "imageUrl": build_r2_public_url(r2_public_base_url, key),
                "stock": 100,
                "category": derive_category_from_key(key),
                "createdAt": now,
                "updatedAt": now,
            }
        )

    return products_list


def seed_products() -> None:
    if products.count_documents({}) > 0:
        return

    max_seed = int(os.getenv("R2_MAX_PRODUCTS", "60"))
    r2_products = list_r2_image_products(limit=max_seed)
    if r2_products:
        products.insert_many(r2_products)
        return

    now = datetime.utcnow()
    products.insert_many(
        [
            {
                "name": "Classic Logo Sticker",
                "description": "A durable vinyl sticker for laptops and bottles.",
                "price": 4.99,
                "imageUrl": "https://placehold.co/400x400/png?text=Sticker+1",
                "stock": 100,
                "category": "logos",
                "createdAt": now,
                "updatedAt": now,
            },
            {
                "name": "Neon Pack",
                "description": "Set of 5 neon-themed stickers.",
                "price": 9.99,
                "imageUrl": "https://placehold.co/400x400/png?text=Sticker+2",
                "stock": 50,
                "category": "packs",
                "createdAt": now,
                "updatedAt": now,
            },
            {
                "name": "Custom Name Sticker",
                "description": "Personalized name sticker, weather resistant.",
                "price": 6.49,
                "imageUrl": "https://placehold.co/400x400/png?text=Sticker+3",
                "stock": 75,
                "category": "custom",
                "createdAt": now,
                "updatedAt": now,
            },
        ]
    )


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "sticker-shop-backend"})


@app.route("/api/auth/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    required = ["email", "password", "firstName", "lastName", "phoneNumber"]
    if not all(data.get(field) for field in required):
        return jsonify({"message": "Missing required fields"}), 400

    if not is_valid_email(data["email"]):
        return jsonify({"message": "Invalid email address"}), 400

    if not isinstance(data["password"], str) or len(data["password"]) < MIN_PASSWORD_LENGTH:
        return jsonify({"message": f"Password must be at least {MIN_PASSWORD_LENGTH} characters"}), 400

    if users.find_one({"email": data["email"]}):
        return jsonify({"message": "User already exists"}), 400

    user_doc = {
        "email": data["email"],
        "password": generate_password_hash(data["password"]),
        "firstName": data["firstName"],
        "lastName": data["lastName"],
        "phoneNumber": data["phoneNumber"],
        "role": "user",
        "createdAt": datetime.utcnow(),
    }
    result = users.insert_one(user_doc)
    user_doc["_id"] = result.inserted_id
    user = serialize_user(user_doc)
    token = create_access_token(identity=str(result.inserted_id))
    refresh_token = create_refresh_token(identity=str(result.inserted_id))
    return jsonify({"user": user, "token": token, "refreshToken": refresh_token}), 201


@app.route("/api/auth/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    if not is_valid_email(email) or not isinstance(password, str):
        return jsonify({"message": "Invalid email or password format"}), 400

    user_doc = users.find_one({"email": email})
    if not user_doc or not check_password_hash(user_doc["password"], password):
        return jsonify({"message": "Invalid credentials"}), 401

    user = serialize_user(user_doc)
    token = create_access_token(identity=str(user_doc["_id"]))
    refresh_token = create_refresh_token(identity=str(user_doc["_id"]))
    return jsonify({"user": user, "token": token, "refreshToken": refresh_token})


@app.route("/api/auth/me", methods=["GET"])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    object_id = to_object_id(user_id)
    if object_id is None:
        return jsonify({"message": "Invalid user identity in token"}), 401
    user_doc = users.find_one({"_id": object_id})
    if not user_doc:
        return jsonify({"message": "User not found"}), 404
    return jsonify({"user": serialize_user(user_doc)})


@app.route("/api/auth/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    token = create_access_token(identity=user_id)
    return jsonify({"token": token})


@app.route("/api/products", methods=["GET"])
def list_products():
    docs = list(products.find().sort("createdAt", -1))
    serialized = [serialize_product(doc) for doc in docs]
    return jsonify({"products": serialized, "total": len(serialized)})


@app.route("/api/cart/items", methods=["POST"])
@jwt_required()
def add_cart_item():
    data = request.get_json() or {}
    product_id = data.get("productId")
    try:
        quantity = int(str(data.get("quantity", 1)))
    except ValueError:
        return jsonify({"message": "quantity must be an integer"}), 400

    if not product_id or quantity < 1:
        return jsonify({"message": "productId and quantity are required"}), 400

    product_oid = to_object_id(product_id) if isinstance(product_id, str) else None
    if product_oid is None:
        return jsonify({"message": "productId is not a valid product id"}), 400
    if products.find_one({"_id": product_oid}, {"_id": 1}) is None:
        return jsonify({"message": "Product not found"}), 404

    user_id = get_jwt_identity()
    cart = carts.find_one({"userId": user_id}) or {"userId": user_id, "items": []}
    items = cart.get("items", [])

    found = False
    for item in items:
        if item["productId"] == product_id:
            item["quantity"] += quantity
            found = True
            break

    if not found:
        items.append({"productId": product_id, "quantity": quantity})

    carts.update_one({"userId": user_id}, {"$set": {"items": items, "updatedAt": datetime.utcnow()}}, upsert=True)
    return jsonify({"message": "Item added to cart", "items": items})


if os.getenv("SKIP_DB_INIT") != "1":  # tests set this and supply fake collections
    with app.app_context():
        connect_db()
        seed_products()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=True)
