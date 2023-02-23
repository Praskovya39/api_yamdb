from rest_framework import viewsets, mixins, filters
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.pagination import LimitOffsetPagination

from .models import User
from .serializer import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)

