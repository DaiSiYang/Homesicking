
from apps.users.models import User, UserProfile
from apps.api_user.serializers.user_serializers import UserSerializer, UserProfileSerializer

class UserService:
    """用户服务"""
    
    @staticmethod
    def get_user_profile(user):
        """获取用户资料"""
        serializer = UserSerializer(user)
        return serializer.data
    
    @staticmethod
    def update_user_profile(user, data):
        """更新用户资料"""
        profile, created = UserProfile.objects.get_or_create(user=user)
        serializer = UserProfileSerializer(profile, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return UserSerializer(user).data
        raise Exception('数据验证失败')
