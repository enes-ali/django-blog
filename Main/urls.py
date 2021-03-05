from django.urls import path
from .views import *

app_label = "Main"

urlpatterns = [
    path("", HomePage, name="home"),
    path("post/<slug:slug>/", PostDetailPage.as_view(), name="post_detail"),
    path("upload/", PostUploadPage.as_view(), name="upload"),
    path("search", SearchPost, name="search"),
]