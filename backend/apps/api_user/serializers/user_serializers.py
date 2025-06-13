
from rest_framework import serializers
from apps.users.models import User, UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    """用户端用户资料序列化器"""
    class Meta:
        model = UserProfile
        fields = ['nickname', 'avatar', 'phone', 'email', 'gender', 'birthday']
        
class UserSerializer(serializers.ModelSerializer):
    """用户端用户序列化器"""
    profile = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'profile', 'date_joined']
        read_only_fields = ['id', 'date_joined']
