from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate


class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'first_name',
            'second_name',
            'mobile',
            'email',
            'password',
            'confirm_password'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }


    def validate_mobile(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("Mobile number is invalid")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data

  
    def create(self, validated_data):
        validated_data.pop('confirm_password')

        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            second_name=validated_data['second_name'],
            mobile=validated_data['mobile']
        )
        return user



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            email=data['email'],
            password=data['password']
        )

        if not user:
            raise serializers.ValidationError("Invalid email or password")

        data['user'] = user
        return data