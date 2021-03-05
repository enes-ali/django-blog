from django.urls import path
from .views import *


urlpatterns = [ 
    path("posts/", AllPosts),
    path("posts/<slug:slug>/", PostDetail),
    path("comments/<slug:slug>/", PostComments),
    path("user/<int:id>", UserDetail),
    path("post-upload/", UploadPost.as_view()),
    path("register/", Register.as_view()),
    path("make-comment/", MakeComment.as_view()),
]