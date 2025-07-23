import os

import environ
import requests

env = environ.Env()
environ.Env.read_env(
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
)


# get admin access token
def get_admin_access_token():
    url = f"{env('KEYCLOAK_SERVER_URL')}/realms/master/protocol/openid-connect/token"
    data = {
        "client_id": env("KEYCLOAK_ADMIN_CLIENT_ID"),
        "grant_type": "password",
        "username": env("KEYCLOAK_ADMIN_USERNAME"),
        "password": env("KEYCLOAK_ADMIN_PASSWORD"),
        "client_secret": env("KEYCLOAK_ADMIN_CLIENT_SECRET"),
        "scope": "openid",
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        return response.json().get("access_token")
    return None


def create_user(data, user_url, headers):
    first_name, *last = data.get("full_name").split(" ")
    last_name = " ".join(last) if last else ""

    user_data = {
        "username": data.get("email"),
        "email": data.get("email"),
        "firstName": first_name,
        "lastName": last_name,
        "enabled": True,
        "emailVerified": False,
        "credentials": [
            {
                "type": "password",
                "value": data.get("password"),
                "temporary": False,
            }
        ],
    }
    create_resp = requests.post(user_url, headers=headers, json=user_data)
    return create_resp
