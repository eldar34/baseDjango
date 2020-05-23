from rest_framework import serializers

from .models import Post

class PostListSerializer(serializers.ModelSerializer):
    """ Get Post List """

    class Meta:
        model = Post
        fields = ('id', 'title', 'author')

class PostDetailSerializer(serializers.ModelSerializer):
    """ Full information about actor"""

    class Meta:
        model = Post
        fields = "__all__"