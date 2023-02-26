from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet, token, signup

router = DefaultRouter()
router.register('users', UserViewSet)

authurls = [
    path('token/', token, name='token_obtain'),
    path('signup/', signup, name='signup'),
]


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/', include(authurls))
]