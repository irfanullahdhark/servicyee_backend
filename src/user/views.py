import os

import environ
from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer

env = environ.Env()
environ.Env.read_env(
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    keycloak_roles = {
        "GET": ["admin"],
        "POST": ["admin"],
        "PUT": ["admin"],
        "PATCH": ["admin"],
        "DELETE": ["admin"],
    }

    def list(self, request):
        print(env("KEYCLOAK_SERVER_URL"))
        return Response({"message": "Hello, World!"}, status=status.HTTP_200_OK)
