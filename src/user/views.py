import json
import os

import environ
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .utils import create_user, get_admin_access_token, get_user_access_token

env = environ.Env()
environ.Env.read_env(
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
)


@csrf_exempt
def register_user(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    try:
        data = json.loads(request.body)
        email = data.get("email")
        password = data.get("password")
        confirm_password = data.get("confirm_password")
        full_name = data.get("full_name")

        if not all([email, password, confirm_password, full_name]):
            return JsonResponse({"error": "Missing required fields"}, status=400)

        if password != confirm_password:
            return JsonResponse({"error": "Passwords do not match"}, status=400)

        # Step 1: Get admin token
        access_token = get_admin_access_token()
        user_url = (
            f"{env('KEYCLOAK_SERVER_URL')}/admin/realms/{env('KEYCLOAK_REALM')}/users"
        )
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        data = {
            "full_name": full_name,
            "email": email,
            "password": password,
        }

        create_resp = create_user(data=data, user_url=user_url, headers=headers)
        if create_resp.status_code not in [201, 204]:
            return JsonResponse(
                {"error": "Failed to create user", "details": create_resp.text},
                status=400,
            )

        # Get created user ID
        get_users_resp = requests.get(
            user_url, headers=headers, params={"email": email}
        )
        user_id = get_users_resp.json()[0]["id"]

        # Trigger email verification
        verify_email_url = f"{env('KEYCLOAK_SERVER_URL')}/admin/realms/{env('KEYCLOAK_REALM')}/users/{user_id}/send-verify-email"
        requests.put(verify_email_url, headers=headers)

        return JsonResponse({"message": "User registered successfully"})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



@csrf_exempt
def login_user(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)
    try:
        data = json.loads(request.body)
        email = data.get("email")
        password = data.get("password")

        if not all([email, password]):
            return JsonResponse({"error": "Missing credentials"}, status=400)
        access_token = get_user_access_token(email, password)
        if access_token is None:
            return JsonResponse({
                "error": "Login failed",
                "details": access_token
            }, status=400)

        return JsonResponse({"access_token": access_token})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
