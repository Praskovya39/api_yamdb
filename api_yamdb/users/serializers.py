import re

from rest_framework import serializers
from users.models import User



class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    class Meta:
        fields = ("username", "confirmation_code")


class SignUpSerializers(serializers.Serializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)

    def validate(self, data):

        if not User.objects.filter(
                username=data.get("username"), email=data.get("email")
        ).exists():
            if User.objects.filter(username=data.get("username")):
                raise serializers.ValidationError(
                    "Пользователь с таким username уже существует"
                )

            if User.objects.filter(email=data.get("email")):
                raise serializers.ValidationError(
                    "Пользователь с таким Email уже существует"
                )

        return data

    def validate_email(self,value):
        if len(value) > 254:
            raise serializers.ValidationError('Количество символов поля email не должно превышать 254')
        return value

    def validate_username(self,value):
        if re.fullmatch(r"^[\w.@+-]+\Z", value) is None:
            raise serializers.ValidationError('Полое username не соответсвует паттерну')
        if len(value) > 150:
            raise serializers.ValidationError('Количество символов поля username не должно превышать 150')
        if value == 'me':
            raise serializers.ValidationError('Значение поля username не может быть me')
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