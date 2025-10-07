from rest_framework import serializers
from .models import Account 
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Account
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'phone_num']

    def create(self, validated_data):
        user = Account.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone_num=validated_data.get('phone_num', ''),
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    # def validate(self, attrs):
    #     email = attrs.get('email')
    #     password = attrs.get('password')
    #     user = authenticate(email=email, password=password)
    #     if user is None:
    #         raise serializers.ValidationError('Invalid credentials')
    #     return attrs