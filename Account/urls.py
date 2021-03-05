from django.urls import path
from .views import *


urlpatterns = [
    path("login/", LoginPage.as_view(), name="login"),
    path("register/", RegisterPage.as_view(), name="register"),
    path("logout/", Logout, name="logout"),
]