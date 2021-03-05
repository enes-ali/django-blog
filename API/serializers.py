from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["username", "email", "profile_photo"]

class PostSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    class Meta:
        model = Post
        fields = ["title", "content", "cover_photo", 'category', "owner", "upload_date", "slug"]
        read_only_fields = ["owner"]


class CommentSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    class Meta:
        model = Comment
        exclude = ["replyed_comment"]
        read_only_fields = ["owner"]


class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["username", "email", "password", "profile_photo"]

    def create(self, validated_data):
        username = validated_data["username"]
        email = validated_data["email"]
        password = validated_data["password"]
        profile_photo = validated_data["profile_photo"]
        user = User(username=username, email=email, profile_photo=profile_photo)
        user.set_password(password)
        user.save()
        return user

    