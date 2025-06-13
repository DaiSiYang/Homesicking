from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from .models import User, UserProfile, MerchantProfile, Favorite


class UserProfileSerializer(serializers.ModelSerializer):
    """用户资料序列化器"""
    class Meta:
        model = UserProfile
        fields = ['real_name', 'gender', 'birthday', 'address']
        extra_kwargs = {
            'real_name': {'required': False},
            'gender': {'required': False},
            'birthday': {'required': False},
            'address': {'required': False}
        }


class UserSerializer(serializers.ModelSerializer):
    """用户序列化器"""
    profile = UserProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'avatar', 'bio', 'user_type', 'created_at', 'profile']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': False},
            'phone': {'required': False},
            'avatar': {'required': False},
            'bio': {'required': False}
        }
    
    def update(self, instance, validated_data):
        """更新用户信息和关联的用户资料"""
        profile_data = validated_data.pop('profile', None)
        
        # 更新用户信息
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # 更新用户资料
        if profile_data:
            for attr, value in profile_data.items():
                setattr(instance.profile, attr, value)
            instance.profile.save()
        
        return instance


class RegisterSerializer(serializers.ModelSerializer):
    """用户注册序列化器"""
    confirm_password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password', 'email', 'phone', 'user_type']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'phone': {'required': True}
        }
    
    def validate(self, data):
        """验证密码是否匹配"""
        if data['password'] != data.pop('confirm_password'):
            raise serializers.ValidationError({"confirm_password": _("两次密码不一致")})
        return data
    
    def validate_username(self, value):
        """验证用户名是否已存在"""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(_("用户名已存在"))
        return value
    
    def validate_email(self, value):
        """验证邮箱是否已存在"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(_("邮箱已存在"))
        return value
    
    def validate_phone(self, value):
        """验证手机号是否已存在"""
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError(_("手机号已存在"))
        return value
    
    def create(self, validated_data):
        """创建用户"""
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            phone=validated_data['phone'],
            user_type=validated_data.get('user_type', 'tourist')
        )
        return user


class LoginSerializer(serializers.Serializer):
    """用户登录序列化器"""
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    
    def validate(self, data):
        """验证用户凭证"""
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError(_("用户名或密码错误"))
        if not user.is_active:
            raise serializers.ValidationError(_("用户已被禁用"))
        
        data['user'] = user
        return data


class ChangePasswordSerializer(serializers.Serializer):
    """修改密码序列化器"""
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)
    
    def validate(self, data):
        """验证新密码是否匹配"""
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": _("两次密码不一致")})
        return data
    
    def validate_old_password(self, value):
        """验证旧密码是否正确"""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(_("旧密码不正确"))
        return value


class MerchantProfileSerializer(serializers.ModelSerializer):
    """商户资料序列化器"""
    class Meta:
        model = MerchantProfile
        fields = ['id', 'business_name', 'business_license', 'contact_person', 
                 'contact_phone', 'address', 'description', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'status', 'created_at', 'updated_at']


class FavoriteSerializer(serializers.ModelSerializer):
    """收藏序列化器"""
    class Meta:
        model = Favorite
        fields = ['id', 'target_type', 'target_id', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate(self, data):
        """验证收藏对象是否存在"""
        # 这里只是一个示例，实际实现时需要根据target_type判断对应模型
        # 并验证target_id是否存在
        target_type = data['target_type']
        target_id = data['target_id']
        
        # 验证用户是否已收藏过该对象
        user = self.context['request'].user
        if Favorite.objects.filter(user=user, target_type=target_type, target_id=target_id).exists():
            raise serializers.ValidationError(_("已收藏过该对象"))
        
        return data 