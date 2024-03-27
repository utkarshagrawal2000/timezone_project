from drf_yasg import openapi

# Define Swagger schema for UserRegistrationView
user_registration_view_swagger = {
    "post": {
        "tags": ["User Registration"],
        "operation_summary": "User Registration",
        "description": "Register a new user.",
        "request_body": {
            "required": True,
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "email": {"type": "string"},
                            "username": {"type": "string"},
                            "tc": {"type": "string"},
                            "mobile": {"type": "string"},
                            "password": {"type": "string", "format": "password"},
                            "password2": {"type": "string", "format": "password"},
                            "is_admin": {"type": "string", "enum": ["admin", "user"]}
                        },
                        "required": ["email", "username", "tc", "mobile", "password", "password2", "is_admin"]
                    }
                }
            }
        },
        "responses": {
            201: {
                "description": "Registration Successful",
                "content": {"application/json": {"example": {"msg": "Registration Successful"}}}
            }
        }
    }
}
