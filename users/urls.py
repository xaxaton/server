from django.urls import path

from users.views import (
    RegistrationAPIView,
    LoginAPIView,
    ConfirmRegistration,
    CancelRegistration,
    RegistrationOrganizationAPIView,
    FreeUsersAPIView,
    EmployeesAPIView,
    SendInviteView,
    CurrentUserView
)


app_name = "users"

urlpatterns = [
    path("register/", RegistrationAPIView.as_view(), name="register"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path(
        "activate/<uidb64>/<token>/",
        ConfirmRegistration.as_view(),
        name="activate",
    ),
    path(
        "cancel-registration/<uidb64>/<token>/",
        CancelRegistration.as_view(),
        name="cancel_registration",
    ),
    path(
        "organizations/register/",
        RegistrationOrganizationAPIView.as_view(),
        name="org-register",
    ),
    path(
        "users/",
        FreeUsersAPIView.as_view(),
        name="free",
    ),
    path(
        "organizations/employees/",
        EmployeesAPIView.as_view(),
        name="employees",
    ),
    path(
        "organizations/invite/",
        SendInviteView.as_view(),
        name="org-invite",
    ),
    path(
        "confirm/<orgidb64>/<token>/",
        ConfirmRegistration.as_view(),
        name="confirm-invite",
    ),
    path("auth/", CurrentUserView.as_view(), name="auth")
]
