from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, action
from django.contrib.auth.tokens import default_token_generator
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import viewsets, pagination, permissions, filters

from users.models import User
from users.serializers import TokenSerializer, SignUpSerializers, UserSerializer
from users.permissions import IsAdmin


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin, ]
    pagination_class = pagination.LimitOffsetPagination
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username', )

    @action(
        detail=False,
        methods=['GET', 'PATCH'],
        url_path='me',
        permission_classes=[permissions.IsAuthenticated]
    )
    def get_self(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(
                serializer.data,
                status=200
            )
        serializer = UserSerializer(instance=request.user,
                                    data=request.data,
                                    partial=True)
        serializer.save(partial=True)
        return Response(serializer.data, status=200)


@api_view(['POST'])
def token(request):
    serializer = TokenSerializer(data=request.data)
    if serializer.is_valid():
        user = get_object_or_404(
            User, username=serializer.validated_data['username'])
        confirmation_code = serializer.validated_data['confirmation_code']
        if default_token_generator.check_token(user, confirmation_code):
            token = AccessToken.for_user(user)
            data = {
                'username': serializer.validated_data['username'],
                'token': str(token)
            }
            return Response(data, status=200)
    return Response(serializer.errors, status=400)


@api_view(['POST'])
def signup(request):
    serializer = SignUpSerializers(data=request.data)
    serializer.is_valid(raise_exception=True)
    user, _ = User.objects.get_or_create(
        username=serializer.validated_data['username'],
        email=serializer.validated_data['email']
    )
    confirmation_code = default_token_generator.make_token(user)
    user.email_user(
        subject='Ваш код',
        message=f'Код подтверждения - {confirmation_code}',
        from_email='egor@yamdb.com'
    )
    return Response(serializer.data, status=200)
