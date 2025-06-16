import logging
import json
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from apps.utils.response import ApiResponse

logger = logging.getLogger(__name__)

class ErrorHandlingMiddleware(MiddlewareMixin):
    """统一错误处理中间件"""
    
    def process_exception(self, request, exception):
        """处理未捕获的异常"""
        try:
            # 记录详细错误信息
            error_info = {
                'path': request.path,
                'method': request.method,
                'user': str(request.user) if hasattr(request, 'user') else 'Anonymous',
                'ip': request.META.get('REMOTE_ADDR', 'Unknown'),
                'user_agent': request.META.get('HTTP_USER_AGENT', 'Unknown'),
                'exception_type': type(exception).__name__,
                'exception_message': str(exception)
            }
            
            logger.error(f"未处理的异常: {json.dumps(error_info, ensure_ascii=False)}")
            
            # 根据异常类型返回不同的错误信息
            if isinstance(exception, ValueError):
                return JsonResponse(
                    ApiResponse.error("输入数据格式错误，请检查请求参数").data,
                    status=400
                )
            elif isinstance(exception, PermissionError):
                return JsonResponse(
                    ApiResponse.error("权限不足，无法执行此操作").data,
                    status=403
                )
            elif isinstance(exception, FileNotFoundError):
                return JsonResponse(
                    ApiResponse.error("请求的资源不存在").data,
                    status=404
                )
            else:
                return JsonResponse(
                    ApiResponse.error("系统内部错误，请稍后重试").data,
                    status=500
                )
                
        except Exception as e:
            logger.critical(f"错误处理中间件异常: {str(e)}")
            return JsonResponse({
                'success': False,
                'message': '系统发生严重错误，请联系管理员',
                'code': 500
            }, status=500)