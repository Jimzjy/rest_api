from rest_framework import serializers
from restAPI.models import Post, Tag
from django.contrib.auth.models import User


class PostSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    tag = serializers.HyperlinkedRelatedField(many=True, view_name='tag-detail', queryset=Tag.objects.all())

    class Meta:
        model = Post
        fields = ('url', 'id', 'title', 'pub_time', 'author', 'body', 'tag')


class TagSerializer(serializers.HyperlinkedModelSerializer):
    posts = serializers.HyperlinkedRelatedField(many=True, view_name='post-detail', read_only=True)

    class Meta:
        model = Tag
        fields = ('url', 'id', 'name', 'posts')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    posts = serializers.HyperlinkedRelatedField(many=True, view_name='post-detail', read_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'posts')
