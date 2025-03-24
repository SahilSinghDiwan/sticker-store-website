from flask_openapi3 import OpenAPI, Info
from typing import Dict, List

info = Info(
    title="Sticker Shop API",
    version="1.0.0",
    description="API documentation for the Sticker Shop application"
)

def setup_openapi(app) -> None:
    """Configure OpenAPI documentation"""
    api = OpenAPI(app, info=info)
    
    # Security Schemes
    api.security_schemes = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    # Common Response Schemas
    api.components.schema("Error", {
        "type": "object",
        "properties": {
            "error": {"type": "string"},
            "details": {"type": "string"}
        }
    })

    api.components.schema("User", {
        "type": "object",
        "properties": {
            "id": {"type": "string"},
            "email": {"type": "string"},
            "name": {"type": "string"},
            "role": {"type": "string", "enum": ["admin", "customer"]}
        }
    })

    # Example endpoint documentation
    @api.get("/api/products", tags=["Products"])
    def get_products():
        """
        Get all products
        ---
        parameters:
          - name: category_id
            in: query
            schema:
              type: string
          - name: search
            in: query
            schema:
              type: string
        responses:
          200:
            description: List of products
            content:
              application/json:
                schema:
                  type: array
                  items:
                    $ref: '#/components/schemas/Product'
          401:
            $ref: '#/components/responses/UnauthorizedError'
        """
        pass  # Actual implementation in routes

    @api.post("/api/auth/login", tags=["Authentication"])
    def login():
        """
        User login
        ---
        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: object
                properties:
                  email:
                    type: string
                  password:
                    type: string
                required:
                  - email
                  - password
        responses:
          200:
            description: Login successful
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    token:
                      type: string
                    user:
                      $ref: '#/components/schemas/User'
          401:
            $ref: '#/components/responses/UnauthorizedError'
        """
        pass  # Actual implementation in routes

    # Common Response References
    api.components.response("UnauthorizedError", {
        "description": "Authentication required",
        "content": {
            "application/json": {
                "schema": {
                    "$ref": "#/components/schemas/Error"
                }
            }
        }
    }) 