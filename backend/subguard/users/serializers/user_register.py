from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from users.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(
        queryset=User.objects.all(),
        message='Email is already taken',
        lookup='iexact',
    )])
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirmation = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'password', 'password_confirmation', 'date_joined')
        read_only_fields = ('id', 'first_name', 'last_name', 'date_joined')

    def validate(self, attrs: dict) -> dict:
        if attrs.get('password') != attrs.get('password_confirmation'):
            raise serializers.ValidationError(detail={'password': 'Passwords does not match'}, code="invalid_passwords")
        return super().validate(attrs)

    @transaction.atomic
    def create(self, validated_data: dict) -> User:
        validated_data.pop("password_confirmation")
        return super().create(validated_data)

        