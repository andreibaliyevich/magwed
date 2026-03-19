from django.apps import apps
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.utils.translation import ugettext_lazy as _
from .choices import UserType


class MWUserManager(BaseUserManager):
    """ User Model Manager """

    def create_user(
            self,
            username,
            email,
            password,
            user_type,
            **extra_fields):
        """
        Create and save a user with the given username, email,
        password and user_type.
        """
        if not username:
            raise ValueError(_('The Username must be set.'))

        if not email:
            raise ValueError(_('The Email must be set.'))

        if not user_type or user_type not in UserType.values:
            raise ValueError(_('Invalid user type.'))

        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        username = GlobalUserModel.normalize_username(username)
        email = self.normalize_email(email)

        user = self.model(
            username=username,
            email=email,
            user_type=user_type,
            **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
            self,
            username,
            email,
            password,
            user_type=None,
            **extra_fields):
        """
        Create and save a superuser with the given username, email, password.
        """
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        user_type =  user_type if user_type else UserType.ADMIN

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_active') is not True:
            raise ValueError('Superuser must have is_active=True.')
        if user_type is not UserType.ADMIN:
            raise ValueError('Superuser must have user_type=ADMIN.')

        return self.create_user(
            username, email, password, user_type, **extra_fields)
