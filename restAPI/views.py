from rest_framework import viewsets, permissions, mixins
from rest_framework.response import Response
from django.contrib.auth.models import User
from restAPI.models import Post, Tag, Comment
from restAPI.serializers import PostSerializer, TagSerializer, UserSerializer, PostSerializerLite, CommentSerializer, UserChangedSerializer
from restAPI.permissions import IsAuthorOrReadOnly, IsUserOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    """
    处理 /api/posts/ GET POST , 处理 /api/post/<pk>/ GET PUT PATCH DELETE
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)

    def perform_create(self, serializer):
        """
        重写 perform_create
        user 信息不在 request.data 中, 在保存时加入 user 信息
        """
        serializer.save(author=self.request.user)

    def list(self, request, *args, **kwargs):
        """
        重写 list
        GET /api/posts/ 时调用的序列化器默认是 PostSerializer, 改成 PostSerializerLite 去除多余信息
        """
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = PostSerializerLite(page, many=True, context={'request': self.request})
            return self.get_paginated_response(serializer.data)

        serializer = PostSerializerLite(queryset, many=True, context={'request': self.request})
        return Response(serializer.data)


class TagViewSet(mixins.CreateModelMixin,
                 mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    """
    处理 /api/tags/ GET POST, 处理 /api/tags/<pk>/ GET
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class UserViewSet(viewsets.ReadOnlyModelViewSet,
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin):
    """
    处理 /api/users/ GET POST, 处理 /api/users/<pk>/ GET POST
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsUserOrReadOnly,)

    def create(self, request, *args, **kwargs):
        serializer = UserChangedSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = UserChangedSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class CommentViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    """
    处理 /api/comments POST, 处理 /api/comments/<pk> GET
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        """
        重写 perform_create
        user 信息不在 request.data 中, 在保存时加入 user 信息
        """
        serializer.save(user=self.request.user)
