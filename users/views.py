from django.forms.models import model_to_dict
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.shortcuts import render

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

from core.permissions import IsRecruiter
from users.models import User, Organization
from users.serializers import (
    RegistrationSerializer,
    LoginSerializer,
    OrganizationSerializer,
    UserSerializer
)
from users.renderers import UserJSONRenderer
from users.token import account_activation_token


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer
    renderer_classes = (UserJSONRenderer,)

    def post(self, request):
        user = request.data.get("user", {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        new_user = User.objects.get(email=serializer.data["email"])
        current_site = get_current_site(request)
        mail_subject = "Активация аккаунта ПрофТестиум"
        message = render_to_string("user_activation.html", {
            "user": new_user,
            "domain": current_site.domain,
            "uid": urlsafe_base64_encode(force_bytes(new_user.id)),
            "token": account_activation_token.make_token(new_user),
        })
        email = EmailMessage(
                    mail_subject, message, to=[new_user.email]
        )
        email.send()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get("user", {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ConfirmRegistration(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        user_model = get_user_model()
        try:
            uid = force_text(urlsafe_base64_decode(self.kwargs["uidb64"]))
            user = user_model.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, user_model.DoesNotExist):
            user = None
        if (
            user is not None and
                account_activation_token.check_token(
                    user, self.kwargs["token"])):
            user.is_active = True
            user.save()
            status = "Аккаунт подтвержден!"
        else:
            status = "Вы воспользовались невалидной ссылкой"
        return render(request, "confirm_user.html", {"message": status})


class CancelRegistration(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        user_model = get_user_model()
        try:
            uid = force_text(urlsafe_base64_decode(self.kwargs["uidb64"]))
            user = user_model.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, user_model.DoesNotExist):
            user = None
        if (
            user is not None and
                account_activation_token.check_token(
                    user, self.kwargs["token"])):
            user.delete()
            status = "Регистрация отменена!"
        else:
            status = "Вы воспользовались невалидной ссылкой"
        return render(request, "confirm_user.html", {"message": status})


class RegistrationOrganizationAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        organization = request.data.get("organization", {})
        serializer_org = OrganizationSerializer(data=organization)
        serializer_org.is_valid(raise_exception=True)
        serializer_org.save()

        user = request.data.get("user", {})
        serializer_user = RegistrationSerializer(data=user)
        serializer_user.is_valid(raise_exception=True)
        serializer_user.save()
        new_user = User.objects.get(email=serializer_user.data["email"])
        new_user.role = 2
        new_user.organization = Organization.objects.get(
            id=serializer_org.data["id"]
        )
        new_user.save()
        current_site = get_current_site(request)
        mail_subject = "Активация аккаунта ПрофТестиум"
        message = render_to_string("user_activation.html", {
            "user": new_user,
            "domain": current_site.domain,
            "uid": urlsafe_base64_encode(force_bytes(new_user.id)),
            "token": account_activation_token.make_token(new_user),
        })
        email = EmailMessage(
                    mail_subject, message, to=[new_user.email]
        )
        email.send()
        return Response(
            {
                "user": {
                    "email": serializer_user.data["email"],
                    "name": serializer_user.data["name"],
                    "surname": serializer_user.data["surname"],
                    "middle_name": serializer_user.data["middle_name"],
                    "organization": model_to_dict(new_user.organization),
                    "role": 2,
                    "department": None,
                    "position": None,
                },
            },
            status=status.HTTP_201_CREATED
        )


class FreeUsersAPIView(ListAPIView):
    permission_classes = (IsAuthenticated, IsRecruiter, )
    serializer_class = UserSerializer
    queryset = User.objects.filter(organization=None)


class EmployeesAPIView(ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = UserSerializer

    def get_queryset(self):
        if self.request.user.organization:
            return User.objects.filter(
                organization__id=self.request.user.organization.id
            )
        return []
