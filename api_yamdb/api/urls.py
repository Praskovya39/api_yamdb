from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import (TitleViewSet, CategoryViewSet, GenreViewSet,
                       CommentViewSet, ReviewViewSet)

router = DefaultRouter()
router.register('titles', TitleViewSet)
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')

urlpatterns = [
    path('v1/', include(router.urls)),
]
