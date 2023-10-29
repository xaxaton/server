"""
User activation token
"""
import six

from django.contrib.auth.tokens import PasswordResetTokenGenerator


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.id)
            + six.text_type(timestamp)
            + six.text_type(user.is_active)
        )


class OrganizationQRTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, organization, timestamp):
        return six.text_type(organization.id) + six.text_type(timestamp)


account_activation_token = TokenGenerator()
invite_confirm_token = TokenGenerator()
qr_invite_token = OrganizationQRTokenGenerator()
