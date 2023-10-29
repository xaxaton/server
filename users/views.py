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
from users.models import User, Organization, Tariff
from users.serializers import (
    RegistrationSerializer,
    LoginSerializer,
    OrganizationSerializer,
    UserSerializer,
    TariffSerializer
)
from users.renderers import UserJSONRenderer
from users.token import (
    account_activation_token,
    invite_confirm_token,
    qr_invite_token,
)


class TariffView(ListAPIView):
    serializer_class = TariffSerializer
    queryset = Tariff.objects.filter()


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
        message = render_to_string(
            "user_activation.html",
            {
                "user": new_user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(new_user.id)),
                "token": account_activation_token.make_token(new_user),
            },
        )
        email = EmailMessage(mail_subject, message, to=[new_user.email])
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
        if user is not None and account_activation_token.check_token(
            user, self.kwargs["token"]
        ):
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
        if user is not None and account_activation_token.check_token(
            user, self.kwargs["token"]
        ):
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
        message = render_to_string(
            "user_activation.html",
            {
                "user": new_user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(new_user.id)),
                "token": account_activation_token.make_token(new_user),
            },
        )
        email = EmailMessage(mail_subject, message, to=[new_user.email])
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
            status=status.HTTP_201_CREATED,
        )


class FreeUsersAPIView(ListAPIView):
    permission_classes = (
        IsAuthenticated,
        IsRecruiter,
    )
    serializer_class = UserSerializer
    queryset = User.objects.filter(organization=None)


class EmployeesAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_queryset(self):
        if self.request.user.organization:
            return User.objects.filter(
                organization__id=self.request.user.organization.id
            )
        return []


class SendInviteView(APIView):
    permission_classes = (
        IsAuthenticated,
        IsRecruiter,
    )

    def post(self, request):
        user_model = get_user_model()
        try:
            to_user = user_model.objects.get(id=request.data.get("id", None))
        except user_model.DoesNotExist:
            to_user = None
        if to_user:
            if to_user.organization:
                answer_message = "Данный пользователь уже в организации"
            else:
                current_site = get_current_site(request)
                mail_subject = "ПрофТестиум || Приглашение в организацию"
                organization = Organization.objects.get(
                    name=request.user.organization.name
                )
                message = render_to_string(
                    "invite.html",
                    {
                        "user": to_user,
                        "organization": organization,
                        "domain": current_site.domain,
                        "orgid": urlsafe_base64_encode(
                            force_bytes(organization.id)
                        ),
                        "uid": urlsafe_base64_encode(force_bytes(to_user.id)),
                        "token": invite_confirm_token.make_token(to_user),
                    },
                )
                email = EmailMessage(mail_subject, message, to=[to_user.email])
                email.send()
                answer_message = "Письмо успешно отправлено"
        else:
            answer_message = "Выбранного пользователя не существует"
        return Response(
            {"message": answer_message}, status=status.HTTP_201_CREATED
        )


class CurrentUserView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = User.objects.select_related("organization").get(
            id=request.user.id
        )
        organization = None
        if user.organization:
            organization = model_to_dict(user.organization)
        return Response(
            {
                "user": {
                    "email": user.email,
                    "name": user.name,
                    "surname": user.surname,
                    "middle_name": user.middle_name,
                    "organization": organization,
                    "role": user.role,
                    "department": user.department,
                    "position": user.position,
                },
            },
            status=status.HTTP_201_CREATED,
        )


class ConfirmTeamJoin(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(self.kwargs["uidb64"]))
            orgid = force_text(urlsafe_base64_decode(self.kwargs["orgidb64"]))
            organization = Organization.objects.get(id=orgid)
            user = User.objects.get(id=uid)
        except (
            TypeError,
            ValueError,
            OverflowError,
            organization.DoesNotExist,
            user.DoesNotExist,
        ):
            organization = None
            user = None
        if (
            user is not None
            and organization is not None
            and invite_confirm_token.check_token(user, self.kwargs["token"])
        ):
            user.organization = organization
            user.save()
            status = f"Вы вступили в организацию {organization.name}"
        else:
            status = "Вы воспользовались невалидной ссылкой"
        return render(request, "confirm_user.html", {"message": status})


class GetQRInviteView(APIView):
    permission_classes = (
        IsAuthenticated,
        IsRecruiter,
    )

    def get(self, request):
        organization = Organization.objects.get(
            name=request.user.organization.name
        )
        current_site = get_current_site(request)
        domain = current_site.domain
        orgid = urlsafe_base64_encode(force_bytes(organization.id))
        token = qr_invite_token.make_token(organization)

        url = f"https://{domain}/api/qr/{orgid}/{token}/"
        return Response({"url": url})


class ConfirmQRTeamJoin(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        try:
            user = request.user
            orgid = force_text(urlsafe_base64_decode(self.kwargs["orgid"]))
            organization = Organization.objects.get(id=orgid)
        except (
            TypeError,
            ValueError,
            OverflowError,
            user.DoesNotExist,
            organization.DoesNotExist,
        ):
            organization = None
            user = None
        if (
            not user.organization
            and user is not None
            and organization is not None
            and qr_invite_token.check_token(organization, self.kwargs["token"])
        ):
            user.organization = organization
            user.save()
            status = f"Вы вступили в организацию {organization.name}"
        else:
            status = (
                "Вы воспользовались невалидным "
                "QR-кодом или уже состоите в организации"
            )
        return Response({"message": status})
