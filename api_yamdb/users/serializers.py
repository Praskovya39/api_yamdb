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

    def validate_email(self,value):
        if len(value) > 254:
            raise serializers.ValidationError('Количество символов поля email не должно превышать 254')
        return value

    def validate_username(self,value):
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
