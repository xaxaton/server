from django.urls import path

from users.views import (
    RegistrationAPIView, LoginAPIView,
    ConfirmRegistration, CancelRegistration
)


app_name = "users"

urlpatterns = [
    path("register/", RegistrationAPIView.as_view(), name="register"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path(
        "activate/<uidb64>/<token>/", ConfirmRegistration.as_view(),
        name="activate"
    ),
    path(
        "cancel-registration/<uidb64>/<token>/",
        CancelRegistration.as_view(), name='cancel_registration'),
]
