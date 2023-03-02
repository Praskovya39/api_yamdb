import re
from rest_framework import serializers
from users.models import User


LEN_EMAIL = 254  # максимальная допустима длина email
LEN_USERNAME = 150  # максимальная допустима длина username
USERNAME_PATTERN = r'^[\w.@+-]+\Z'  # паттерн поля username


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    class Meta:
        fields = ('username', 'confirmation_code')


class SignUpSerializers(serializers.Serializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)

    def validate(self, data):
        username = data.get('username', None)
        email = data.get('email', None)

        if User.objects.filter(email=email, username=username).exists():
            return data

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'Данный email занят.'
            )
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                'Данный username занят.'
            )
        return data

    def validate_email(self, value):
        if len(value) > LEN_EMAIL:
            raise serializers.ValidationError(
                f'Количество символов поля email не должно превышать {LEN_EMAIL}')
        return value

    def validate_username(self, value):
        if re.fullmatch(USERNAME_PATTERN, value) is None:
            raise serializers.ValidationError(
                'Поле username не соответсвует паттерну')
        if len(value) > LEN_USERNAME:
            raise serializers.ValidationError(
                f'Количество символов поля username не должно превышать {LEN_USERNAME}')
        if value == 'me':
            raise serializers.ValidationError(
                'Значение поля username не может быть me')
        return value

    class Meta:
        fields = ('email', 'username')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'bio',
            'role'
        )


class UserNotAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role')
        read_only_fields = ('role',)
