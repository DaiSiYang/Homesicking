from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.utils.translation import gettext_lazy as _

from apps.utils.response import ApiResponse
from apps.utils.permissions import IsMerchantUser
from ..models import MerchantProfile, User
from ..serializers import MerchantProfileSerializer


class MerchantApplyView(APIView):
    """
    商户入驻申请
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        # 验证用户是否已经是商户
        if request.user.user_type == 'merchant':
            return ApiResponse(
                code=400,
                message=_("您已经是商户"),
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 验证用户是否已经提交过申请
        if hasattr(request.user, 'merchant_profile'):
            return ApiResponse(
                code=400,
                message=_("您已提交过申请，请勿重复提交"),
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 创建商户资料
        serializer = MerchantProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, status='pending')
        
        return ApiResponse(
            code=200,
            message=_("申请提交成功，等待审核"),
            data=serializer.data
        )


class MerchantProfileView(RetrieveUpdateAPIView):
    """
    商户资料获取和更新
    """
    serializer_class = MerchantProfileSerializer
    permission_classes = [IsAuthenticated, IsMerchantUser]
    
    def get_object(self):
        return self.request.user.merchant_profile
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return ApiResponse(data=serializer.data)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        
        # 商户资料审核状态为已拒绝或已通过时才允许修改
        if instance.status not in ['rejected', 'approved']:
            return ApiResponse(
                code=400,
                message=_("当前状态不允许修改"),
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        # 如果状态是已拒绝，修改后重新设为待审核
        if instance.status == 'rejected':
            instance.status = 'pending'
        
        self.perform_update(serializer)
        
        return ApiResponse(
            message=_("更新成功"),
            data=serializer.data
        ) 