from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                       PermissionsMixin
from rest_framework.pagination import PageNumberPagination


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Create and save User"""
        if not email:
            raise ValueError("Email must be provided")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password):
        """Create and save superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Search(models.Model):
    search = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now=True)
    website = models.CharField(max_length=20, null=True)

    def __str__(self):
        return f'{self.search}'


class SearchResponse(models.Model):
    title = models.CharField(max_length=100)
    page_url = models.URLField(max_length=255, null=False)
    price = models.CharField(max_length=255, blank=True)
    img = models.URLField(max_length=255, blank=True)


class Bookmark(models.Model):
    title = models.CharField(max_length=255, null=False)
    urls = models.URLField(max_length=255, null=False)
    price = models.CharField(max_length=255, blank=True)
    img = models.URLField(max_length=255, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}'
