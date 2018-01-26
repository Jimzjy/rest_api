from rest_framework import viewsets, permissions, mixins
from rest_framework.response import Response
from django.contrib.auth.models import User
from restAPI.models import Post, Tag
from restAPI.serializers import PostSerializer, TagSerializer, UserSerializer, PostSerializerLite
from restAPI.permissions import IsAuthorOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def list(self, request, *args, **kwargs):
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
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

