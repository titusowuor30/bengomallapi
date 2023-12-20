from .models import Blog, Post
from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model

User = get_user_model()

class FrontStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = FrontStore
        fields = '__all__'
        depth = 1


# serializers.py
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'pic')

class CommentsSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Comments
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    comments = CommentsSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = '__all__'


class BlogSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True, read_only=True)
    author=UserSerializer(read_only=True)

    class Meta:
        model = Blog
        fields = '__all__'
        depth=1
