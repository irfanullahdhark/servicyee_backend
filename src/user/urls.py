from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import register_user, login_user

router = DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    path("register/", register_user, name="register_user"),
    path("login/", login_user, name="login_user"),
]
