from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password_confirm', 'first_name', 'last_name')

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm', None)

        first_name = attrs.get('first_name')
        last_name = attrs.get('last_name')

        if not first_name or not last_name:
            raise serializers.ValidationError("First and last names shouldn`t be empty")

        if password != password_confirm:
            raise serializers.ValidationError("Passwords do not match")

        try:
            validate_password(password=password)
        except ValidationError as e:
            raise serializers.ValidationError(str(e))

        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

