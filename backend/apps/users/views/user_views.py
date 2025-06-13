from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from django.utils.translation import gettext_lazy as _

from apps.utils.response import ApiResponse
from ..serializers import UserSerializer, ChangePasswordSerializer


class UserProfileView(RetrieveUpdateAPIView):
    """
    获取和更新当前用户信息
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return ApiResponse(data=serializer.data)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return ApiResponse(
            message=_("更新成功"),
            data=serializer.data
        )


class ChangePasswordView(APIView):
    """
    修改密码
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        # 更新密码
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        return ApiResponse(
            message=_("密码修改成功")
        ) 