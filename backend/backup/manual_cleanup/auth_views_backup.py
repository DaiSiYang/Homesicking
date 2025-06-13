from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.utils.translation import gettext_lazy as _
import logging
import json

from apps.utils.response import ApiResponse
from ..serializers import RegisterSerializer, LoginSerializer

logger = logging.getLogger(__name__)

class RegisterView(GenericAPIView):
    """
    用户注册视图
    """
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        # 记录接收到的请求数据
        logger.info(f"注册请求数据: {json.dumps(request.data, ensure_ascii=False)}")
        
        try:
            serializer = self.get_serializer(data=request.data)
            
            # 详细验证并记录错误
            if not serializer.is_valid():
                logger.error(f"注册数据验证失败: {serializer.errors}")
                return Response({
                    'code': 400,
                    'message': '注册数据验证失败',
                    'errors': serializer.errors,
                    'received_data': request.data
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 保存用户
            user = serializer.save()
            logger.info(f"用户注册成功: {user.username}")
            
            # 生成JWT token
            refresh = RefreshToken.for_user(user)
            
            return ApiResponse(
                code=201,
                message=_("注册成功"),
                data={
                    "user_id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "token": str(refresh.access_token),
                    "refresh_token": str(refresh)
                },
                status=status.HTTP_201_CREATED
            )
            
        except Exception as e:
            logger.error(f"注册过程中发生错误: {str(e)}")
            return Response({
                'code': 500,
                'message': '注册失败，请稍后重试',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoginView(GenericAPIView):
    """
    用户登录视图
    """
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        # 记录登录请求数据
        logger.info(f"登录请求数据: {json.dumps(request.data, ensure_ascii=False)}")
        
        try:
            serializer = self.get_serializer(data=request.data)
            
            # 详细验证并记录错误
            if not serializer.is_valid():
                logger.error(f"登录数据验证失败: {serializer.errors}")
                return Response({
                    'code': 400,
                    'message': '登录数据验证失败',
                    'errors': serializer.errors,
                    'received_data': request.data
                }, status=status.HTTP_400_BAD_REQUEST)
            
            user = serializer.validated_data['user']
            logger.info(f"用户登录成功: {user.username}")
            
            # 生成JWT token
            refresh = RefreshToken.for_user(user)
            
            return ApiResponse(
                code=200,
                message=_("登录成功"),
                data={
                    "user_id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "token": str(refresh.access_token),
                    "refresh_token": str(refresh)
                }
            )
            
        except Exception as e:
            logger.error(f"登录过程中发生错误: {str(e)}")
            return Response({
                'code': 500,
                'message': '登录失败，请稍后重试',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LogoutView(APIView):
    """
    用户登出视图
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        try:
            # 获取token
            refresh_token = request.data.get('refresh_token')
            if refresh_token:
                # 尝试使token失效
                token = RefreshToken(refresh_token)
                token.blacklist()
        except TokenError:
            pass
        
        return ApiResponse(
            code=200,
            message=_("登出成功")
        )

class RefreshTokenView(APIView):
    """
    刷新Token视图
    """
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            return ApiResponse(
                code=400,
                message=_("刷新Token不能为空"),
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            refresh = RefreshToken(refresh_token)
            
            return ApiResponse(
                code=200,
                message=_("刷新成功"),
                data={
                    "token": str(refresh.access_token),
                    "refresh_token": str(refresh)
                }
            )
        except TokenError:
            return ApiResponse(
                code=401,
                message=_("Token无效或已过期"),
                status=status.HTTP_401_UNAUTHORIZED
            )
        except Exception as e:
            logger.error(f"刷新Token时发生错误: {str(e)}")
            return ApiResponse(
                code=500,
                message=_("刷新失败，请重新登录"),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )