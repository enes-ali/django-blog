from django.shortcuts import render, get_object_or_404
from .serializers import *
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import FormParser, MultiPartParser
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


@api_view(["GET"])
def AllPosts(request):
    posts = Post.objects.all()
    posts_serializer = PostSerializer(posts, many=True)
    return JsonResponse(data=posts_serializer.data, safe=False)


@api_view(["GET"])
def PostDetail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post_serializer = PostSerializer(post)
    return JsonResponse(post_serializer.data, safe=False)

@api_view(["GET"])
def PostComments(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = Comment.objects.filter(post=post)
    comments_serializer = CommentSerializer(comments, many=True)
    return JsonResponse(comments_serializer.data, safe=False)


@api_view(["GET"])
def UserDetail(request, id):
    user = get_object_or_404(User, id=id)
    user_serializer = UserSerializer(user)
    return JsonResponse(user_serializer.data, safe=False)


class UploadPost(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [FormParser, MultiPartParser]

    def post(self, request):
        post_serializer = PostSerializer(data=request.data)
        if post_serializer.is_valid():
            post = post_serializer.save(owner=request.user)

            return JsonResponse(PostSerializer(post).data, safe=False)

        else:
            return JsonResponse({"error": post_serializer.errors}, status=400)


class MakeComment(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        post = get_object_or_404(Post, slug=request.data["slug"])
        request.data["post"] = post.id
        comment_serializer = CommentSerializer(data=request.data)
        if comment_serializer.is_valid():
            if request.user.is_authenticated:
                comment = comment_serializer.save(owner=request.user)
            else:
                comment = comment_serializer.save()

            return JsonResponse(CommentSerializer(comment).data, safe=False)
        
        else:
            return JsonResponse({"errors": comment_serializer.errors}, status=400)


class Register(APIView):

    parser_classes = [FormParser, MultiPartParser]

    def post(self, request):
        user_serializer = UserRegisterSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save()

            return JsonResponse(UserRegisterSerializer(user).data, safe=False)
        
        else:
            return JsonResponse({"errors": user_serializer.errors}, status=400)