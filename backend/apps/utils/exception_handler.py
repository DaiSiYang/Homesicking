from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging
from .response import ApiResponse

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    # 调用 REST framework 默认的异常处理器
    response = exception_handler(exc, context)
    
    # 记录异常信息
    request = context.get('request')
    user = getattr(request, 'user', None)
    logger.error(
        f"Exception occurred - User: {user} (ID: {getattr(user, 'id', None)}), "
        f"Method: {request.method}, Path: {request.path}, "
        f"IP: {request.META.get('REMOTE_ADDR', 'Unknown')}, "
        f"Exception: {exc.__class__.__name__}: {str(exc)}"
    )
    
    if response is not None:
        # 如果 DRF 已经处理了异常，使用 ApiResponse 格式化响应
        custom_response_data = {
            'success': False,
            'message': '请求处理失败',
            'data': None,
            'errors': response.data
        }
        
        # 根据状态码返回相应的 ApiResponse
        if response.status_code >= 500:
            return ApiResponse.server_error(
                message='服务器内部错误',
                errors=response.data
            )
        else:
            return ApiResponse.error(
                message='请求处理失败',
                errors=response.data,
                status_code=response.status_code
            )
    else:
        # 如果 DRF 没有处理异常，返回通用服务器错误
        return ApiResponse.server_error(
            message='服务器内部错误，请稍后重试',
            errors={'detail': str(exc)}
        )