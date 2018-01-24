from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view
from restAPI.views import PostViewSet, TagViewSet, UserViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'tags', TagViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]
