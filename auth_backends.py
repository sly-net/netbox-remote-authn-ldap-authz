import logging

from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import Group, Permission
from django_auth_ldap.backend import LDAPBackend, _LDAPUser


class ViewExemptModelBackend(ModelBackend):
    """
    Custom implementation of Django's stock ModelBackend which allows for the exemption of arbitrary models from view
    permission enforcement.
    """
    def has_perm(self, user_obj, perm, obj=None):

        # If this is a view permission, check whether the model has been exempted from enforcement
        try:
            app, codename = perm.split('.')
            action, model = codename.split('_')
            if action == 'view':
                if (
                    # All models are exempt from view permission enforcement
                    '*' in settings.EXEMPT_VIEW_PERMISSIONS
                ) or (
                    # This specific model is exempt from view permission enforcement
                    '{}.{}'.format(app, model) in settings.EXEMPT_VIEW_PERMISSIONS
                ):
                    return True
        except ValueError:
            pass

        return super().has_perm(user_obj, perm, obj)


class RemoteLDAPBackend(LDAPBackend):
    """
    Custom implementation of Django's LDAPBackend which provides configuration hooks for basic customization and allows remote authentication.
    """

    def authenticate(self, request, remote_user):
        username = self.clean_username(remote_user)
        ldap_user = _RemoteLDAPUser(self, username=username.strip(), request=request)
        user = self.authenticate_ldap_user(ldap_user, '')

        return user

    def clean_username(self, username):
        # Do whatever you need here. For example remove any @ and following characters.
        return username


class _RemoteLDAPUser(_LDAPUser):
    def _authenticate_user_dn(self, password):
        if self.dn is None:
            raise self.AuthenticationFailed("failed to map the username to a DN.")        
