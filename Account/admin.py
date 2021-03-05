from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.contrib.auth.models import Group

class AdminUserCreateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ["username", "email", "password"]
        widgets = {"password": forms.PasswordInput()}

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class AdminUserPage(UserAdmin):

    fieldsets = [
        (None, {"fields": ("username", 'email', "password")}),
        ("Profile", {"fields": ("profile_photo", )}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")})
    ]

    add_form = AdminUserCreateForm
    add_fieldsets = [
        ("Create New User", {"fields": ("username", "email", "password")})
    ]

    list_display = ("username", "email")
    list_filter = ()
    ordering = ("username", )
    filter_horizontal = ()

admin.site.register(User, AdminUserPage)
admin.site.unregister(Group)

