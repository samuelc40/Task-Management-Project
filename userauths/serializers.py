# from rest_framework import serializers
# from django.contrib.auth import get_user_model
# from rest_framework_simplejwt.tokens import RefreshToken

# User = get_user_model()

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email']  # Add any other fields you want to include

# class TokenSerializer(serializers.Serializer):
#     access = serializers.CharField()
#     refresh = serializers.CharField()
