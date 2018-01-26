from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from restAPI.models import Post, Tag


class UserSerializerLite(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username')


class TagSerializerLite(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ('url', 'name')


class PostSerializer(serializers.HyperlinkedModelSerializer):
    author = UserSerializerLite(read_only=True)
    tag = TagSerializerLite(many=True)

    class Meta:
        model = Post
        fields = ('url', 'id', 'title', 'pub_time', 'author', 'body', 'tag')

    @staticmethod
    def addtag(tags, post):
        for tag in tags:
            try:
                t = Tag.objects.get(name=tag['name'])
                post.tag.add(t)
                flag = True
            except ObjectDoesNotExist:
                flag = False
            if not flag:
                t = Tag.objects.create(name=tag['name'])
                post.tag.add(t)

    def create(self, validated_data):
        tags = validated_data.pop('tag')
        post = Post.objects.create(**validated_data)
        self.addtag(tags, post)
        return post

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.body = validated_data.get('body', instance.body)
        instance.save()
        instance.tag.clear()
        tags = validated_data.get('tag')
        self.addtag(tags, instance)
        return instance


class PostSerializerLite(serializers.HyperlinkedModelSerializer):
    author = UserSerializerLite(read_only=True)

    def to_representation(self, instance):
        ret = super(PostSerializerLite, self).to_representation(instance)
        excerpt = ret['body']
        if str(excerpt).__len__() > 50:
            excerpt = excerpt[:50] + '...'
        ret['body'] = excerpt
        return ret

    class Meta:
        model = Post
        fields = ('url', 'title', 'author', 'body')


class TagSerializer(serializers.HyperlinkedModelSerializer):
    posts = PostSerializerLite(many=True, read_only=True)

    class Meta:
        model = Tag
        fields = ('url', 'id', 'name', 'posts')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    posts = PostSerializerLite(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'posts')
