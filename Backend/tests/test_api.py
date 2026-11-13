import os
import sys

os.environ["SECRET_KEY"] = "test-secret"
os.environ["JWT_SECRET_KEY"] = "test-jwt-secret-that-is-long-enough-for-hs256"
os.environ["SKIP_DB_INIT"] = "1"
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from unittest.mock import MagicMock  # noqa: E402

import pytest  # noqa: E402
from bson import ObjectId  # noqa: E402
from flask_jwt_extended import create_access_token  # noqa: E402

import main  # noqa: E402

GOOD = {
    "email": "a@example.com",
    "password": "longenough1",
    "firstName": "A",
    "lastName": "B",
    "phoneNumber": "123",
}


@pytest.fixture()
def client(monkeypatch):
    users, products, carts = MagicMock(), MagicMock(), MagicMock()
    users.find_one.return_value = None
    users.insert_one.return_value = MagicMock(inserted_id=ObjectId())
    carts.find_one.return_value = None
    monkeypatch.setattr(main, "users", users)
    monkeypatch.setattr(main, "products", products)
    monkeypatch.setattr(main, "carts", carts)
    c = main.app.test_client()
    c.mocks = {"users": users, "products": products, "carts": carts}
    return c


def auth(identity):
    with main.app.app_context():
        return {"Authorization": f"Bearer {create_access_token(identity=identity)}"}


def test_register_ok(client):
    assert client.post("/api/auth/register", json=GOOD).status_code == 201


@pytest.mark.parametrize("email", ["nope", "a@b", "a b@c.com", "", None, 5])
def test_register_bad_email(client, email):
    assert client.post("/api/auth/register", json={**GOOD, "email": email}).status_code == 400


def test_register_short_password(client):
    assert client.post("/api/auth/register", json={**GOOD, "password": "short"}).status_code == 400


def test_login_bad_email_format(client):
    assert client.post("/api/auth/login", json={"email": "nope", "password": "whatever1"}).status_code == 400


def test_login_non_string_password(client):
    assert client.post("/api/auth/login", json={"email": "a@example.com", "password": 12345678}).status_code == 400


def test_me_bad_identity_is_401_not_500(client):
    assert client.get("/api/auth/me", headers=auth("not-an-objectid")).status_code == 401


@pytest.mark.parametrize("qty", ["abc", "1.5", None, [1], {"a": 1}, True])
def test_cart_non_numeric_quantity_400(client, qty):
    r = client.post("/api/cart/items", json={"productId": str(ObjectId()), "quantity": qty}, headers=auth("u1"))
    assert r.status_code == 400


def test_cart_zero_quantity_400(client):
    r = client.post("/api/cart/items", json={"productId": str(ObjectId()), "quantity": 0}, headers=auth("u1"))
    assert r.status_code == 400


def test_cart_malformed_product_id_400(client):
    r = client.post("/api/cart/items", json={"productId": "xyz", "quantity": 1}, headers=auth("u1"))
    assert r.status_code == 400


def test_cart_unknown_product_404(client):
    client.mocks["products"].find_one.return_value = None
    r = client.post("/api/cart/items", json={"productId": str(ObjectId()), "quantity": 1}, headers=auth("u1"))
    assert r.status_code == 404


def test_cart_ok(client):
    client.mocks["products"].find_one.return_value = {"_id": ObjectId()}
    r = client.post("/api/cart/items", json={"productId": str(ObjectId()), "quantity": "2"}, headers=auth("u1"))
    assert r.status_code == 200
    assert r.get_json()["items"][0]["quantity"] == 2


def test_refuses_to_start_without_secrets(monkeypatch):
    monkeypatch.delenv("JWT_SECRET_KEY")
    with pytest.raises(RuntimeError):
        main.require_env("JWT_SECRET_KEY")
