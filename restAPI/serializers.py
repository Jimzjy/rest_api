from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from restAPI.models import Post, Tag, Comment


class UserSerializerLite(serializers.HyperlinkedModelSerializer):
    """
    只包含 'url' 'username' 的User序列化器
    """
    class Meta:
        model = User
        fields = ('url', 'username')


class TagSerializerLite(serializers.HyperlinkedModelSerializer):
    """
    只包含 'url' 'name' 的Tag序列化器
    """
    class Meta:
        model = Tag
        fields = ('url', 'name')


class ReplyCommentSerializer(serializers.HyperlinkedModelSerializer):
    """
    Comment序列化器, 用于序列化 被回复者 的信息
    """
    user = UserSerializerLite(read_only=True)

    class Meta:
        model = Comment
        fields = ('url', 'id', 'user')


class CommentSerializerLite(serializers.HyperlinkedModelSerializer):
    """
    只包含 'url', 'id', 'pub_time', 'body', 'reply_comment' 的Comment序列化器
    """
    reply_comment = ReplyCommentSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('url', 'id', 'pub_time', 'body', 'reply_comment')


class PostSerializer(serializers.HyperlinkedModelSerializer):
    """
    Post序列化器
    """
    author = UserSerializerLite(read_only=True)
    tags = TagSerializerLite(many=True)
    comments = CommentSerializerLite(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('url', 'id', 'title', 'pub_time', 'author', 'body', 'tags', 'comments')

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
        tags = validated_data.pop('tags')
        post = Post.objects.create(**validated_data)
        if tags is not None:
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
        instance.tags.clear()
        tags = validated_data.get('tags')
        if tags is not None:
            self.addtag(tags, instance)
        return instance


class PostSerializerLite(serializers.HyperlinkedModelSerializer):
    """
    只包含 'url' 'title' 'author' 'body' 的Post序列化器
    excerpt: Post 的 excerpt() 方法, 将 'body' 中 长度大于 50 的截断 + "..."
    """
    author = UserSerializerLite(read_only=True)

    # def to_representation(self, instance):
    #     """
    #     重写 to_representation 改变生成的序列, 将 'body' 中大于 50 长度的截断
    #     """
    #     ret = super(PostSerializerLite, self).to_representation(instance)
    #     excerpt = ret['body']
    #     if str(excerpt).__len__() > 50:
    #         excerpt = excerpt[:50] + '...'
    #     ret['body'] = excerpt
    #     return ret

    class Meta:
        model = Post
        fields = ('url', 'title', 'author', 'excerpt')


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


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    """
    Comment序列化器
    """
    reply_comment = ReplyCommentSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('url', 'id', 'pub_time', 'body', 'reply_comment', 'in_post', 'replies')
