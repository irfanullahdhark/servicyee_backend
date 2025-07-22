from dj_rest_auth.views import PasswordResetConfirmView, PasswordResetView
from django.urls import include, path

from users.views import RegisterView

urlpatterns = [
    path("", include("dj_rest_auth.urls")),
    path("register/", RegisterView.as_view(), name="register"),
    path("password/reset/", PasswordResetView.as_view(), name="password_reset"),
    path(
        "password/reset/confirm/<str:uidb64>/<str:token>/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
]
