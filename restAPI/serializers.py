from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from restAPI.models import Post, Tag


class UserSerializerLite(serializers.HyperlinkedModelSerializer):
    """
    用于在Post的序列化器中的, 只包含 'url' 'username' 的User序列化器
    """
    class Meta:
        model = User
        fields = ('url', 'username')


class TagSerializerLite(serializers.HyperlinkedModelSerializer):
    """
    用于在Post的序列化器中, 只包含 'url' 'name' 的Tag序列化器
    """
    class Meta:
        model = Tag
        fields = ('url', 'name')


class PostSerializer(serializers.HyperlinkedModelSerializer):
    """
    Post序列化器
    """
    author = UserSerializerLite(read_only=True)
    tag = TagSerializerLite(many=True)

    class Meta:
        model = Post
        fields = ('url', 'id', 'title', 'pub_time', 'author', 'body', 'tag')

    @staticmethod
    def addtag(tags, post):
        """
        为传入的 post 添加 tag ,如果 tag 已经存在,添加的关系是库中已经存在的 tag,
        如果 tag 不存在,则将 tag 添加到 Tag,添加的关系是新入库的 tag
        :param tags: validated_data 中的 tag
        :param post: Post类实例
        """
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
        """
        重写 create ,从 validated_data 中取出 tag ,
        添加 Post 后调用 addtag() 添加 tag 关系
        """
        tags = validated_data.pop('tag')
        post = Post.objects.create(**validated_data)
        self.addtag(tags, post)
        return post

    def update(self, instance, validated_data):
        """
        重写 update ,实例中的 'title' 'body' 更新后删除所有 tag 关系
        再调用 addtag() 添加 tag 关系
        """
        instance.title = validated_data.get('title', instance.title)
        instance.body = validated_data.get('body', instance.body)
        instance.save()
        instance.tag.clear()
        tags = validated_data.get('tag')
        self.addtag(tags, instance)
        return instance


class PostSerializerLite(serializers.HyperlinkedModelSerializer):
    """
    用于 Tag, User 序列化器中, 只包含 'url' 'title' 'author' 'body' 的序列化器
    """
    author = UserSerializerLite(read_only=True)

    def to_representation(self, instance):
        """
        重写 to_representation 改变生成的序列, 将 'body' 中大于 50 长度的截断
        """
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
    """
    Tag 序列化器
    """
    posts = PostSerializerLite(many=True, read_only=True)

    class Meta:
        model = Tag
        fields = ('url', 'id', 'name', 'posts')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    User 序列化器
    """
    posts = PostSerializerLite(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'posts')
