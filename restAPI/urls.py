from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view
from restAPI.views import PostViewSet, TagViewSet, UserViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'tags', TagViewSet)
router.register(r'users', UserViewSet)

schema_view = get_schema_view(title='Pastebin API')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('schema/', schema_view)
]
