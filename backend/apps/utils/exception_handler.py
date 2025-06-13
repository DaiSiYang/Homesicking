from rest_framework.views import exception_handler
from rest_framework import status
from django.http import Http404
from django.core.exceptions import PermissionDenied
from rest_framework.exceptions import (
    AuthenticationFailed, NotAuthenticated, PermissionDenied as RestPermissionDenied,
    ValidationError, NotFound, MethodNotAllowed
)
from .response import ApiResponse
import logging

# 获取logger实例
logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    """
    自定义异常处理
    """
    # 获取请求信息
    request = context.get('request')
    view = context.get('view')
    
    # 记录详细的错误信息
    if request:
        user_info = f"User: {getattr(request.user, 'username', 'Anonymous')} (ID: {getattr(request.user, 'id', 'None')})"
        request_info = f"Method: {request.method}, Path: {request.path}, IP: {request.META.get('REMOTE_ADDR', 'Unknown')}"
        logger.error(f"Exception occurred - {user_info}, {request_info}, Exception: {type(exc).__name__}: {str(exc)}")
    
    # 先调用REST framework默认的异常处理方法获取标准错误响应
    response = exception_handler(exc, context)
    
    # 如果是REST framework的异常，自定义响应格式
    if response is not None:
        code = 400
        message = "请求错误"
        errors = None
        
        if isinstance(exc, (NotAuthenticated, AuthenticationFailed)):
            code = 401
            if isinstance(exc, NotAuthenticated):
                message = f"未认证访问: {str(exc)} - 请检查Authorization头是否包含有效的JWT token"
                logger.warning(f"未认证访问尝试 - Path: {request.path if request else 'Unknown'}, Error: {str(exc)}")
            else:
                message = f"认证失败: {str(exc)} - JWT token可能已过期或无效"
                logger.warning(f"认证失败 - Path: {request.path if request else 'Unknown'}, Error: {str(exc)}")
        elif isinstance(exc, (PermissionDenied, RestPermissionDenied)):
            code = 403
            message = f"权限不足: {str(exc)} - 当前用户无权访问此资源"
            logger.warning(f"权限不足 - User: {getattr(request.user, 'username', 'Anonymous')}, Path: {request.path if request else 'Unknown'}, Error: {str(exc)}")
        elif isinstance(exc, (Http404, NotFound)):
            code = 404
            message = f"资源不存在: {str(exc)}"
        elif isinstance(exc, MethodNotAllowed):
            code = 405
            message = f"方法不允许: {str(exc)} - 请检查HTTP方法是否正确"
        elif isinstance(exc, ValidationError):
            code = 422
            message = f"数据验证失败: {str(exc)}"
            errors = exc.detail
            logger.warning(f"数据验证失败 - Path: {request.path if request else 'Unknown'}, Errors: {errors}")
        
        # 使用自定义响应格式
        response = ApiResponse(
            code=code,
            message=message,
            errors=errors,
            status=response.status_code
        )
    
    # 未处理的异常
    else:
        # 处理服务器错误
        logger.error(f"未处理的服务器错误 - Exception: {type(exc).__name__}: {str(exc)}, Path: {request.path if request else 'Unknown'}")
        response = ApiResponse(
            code=500,
            message=f"服务器内部错误: {str(exc)}",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    return response