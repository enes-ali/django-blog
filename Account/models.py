from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, username, email, password):
        user = self.model(username=username, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.model(username=username, email=email, password=password)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

def profilePhotoUploadPath(instance, file_name):
    return f"profile photos/{instance.username}/{file_name}"

class User(AbstractBaseUser, PermissionsMixin):
    # Fields required for django's admin site
    is_active = models.BooleanField("Is user active", default=True)
    is_staff = models.BooleanField("Is user staff", default=False, help_text="Does user have access to admin site")
    is_superuser = models.BooleanField("Is user superuser", default=False, help_text="Is user and admin")

    # Required fields
    username = models.CharField("Username", max_length=155)
    email = models.EmailField("Email", max_length=155, unique=True)

    # Optional Fields
    profile_photo = models.ImageField("Profile Photo", upload_to=profilePhotoUploadPath, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", ]

    # Manager
    objects = UserManager()