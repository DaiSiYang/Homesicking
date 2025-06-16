
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from apps.utils.response import ApiResponse
from apps.utils.permissions import IsAdminUser  # 修改这里
from apps.services.auth_service import AuthService
import logging
logger = logging.getLogger(__name__)

@api_view(['POST'])
def admin_login(request):
    """管理员登录"""
    try:
        # 请求数据验证
        if not request.data:
            return ApiResponse.error(message="请求数据不能为空")
            
        username = request.data.get('username')
        password = request.data.get('password')
        
        # 详细的参数验证
        if not username:
            return ApiResponse.error(message="请输入用户名")
        if not password:
            return ApiResponse.error(message="请输入密码")
            
        username = username.strip()
        if len(username) < 3:
            return ApiResponse.error(message="用户名长度不能少于3个字符")
        if len(password) < 6:
            return ApiResponse.error(message="密码长度不能少于6个字符")
        
        # 检查是否包含特殊字符
        import re
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return ApiResponse.error(message="用户名只能包含字母、数字和下划线")
        
        result, error_message = AuthService.admin_login(username, password, request)
        
        if result:
            return ApiResponse.success(
                data=result, 
                message="登录成功，欢迎回来！"
            )
        else:
            return ApiResponse.error(
                message=error_message or "登录失败，请检查用户名和密码",
                code=401
            )
    except ValueError as e:
        return ApiResponse.error(message=f"输入数据格式错误: {str(e)}")
    except ConnectionError as e:
        return ApiResponse.error(message="网络连接异常，请检查网络设置")
    except Exception as e:
        logger.error(f"管理员登录API异常: {str(e)}")
        return ApiResponse.error(
            message="系统繁忙，请稍后重试",
            code=500
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])  # 修改这里
def admin_logout(request):
    """管理员登出"""
    try:
        # 这里可以添加登出逻辑，如记录日志等
        return ApiResponse.success(message="登出成功")
    except Exception as e:
        return ApiResponse.error(message=f"登出失败: {str(e)}")

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])  # 修改这里
def admin_profile(request):
    """获取管理员资料"""
    try:
        user = request.user
        data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'avatar': getattr(user.profile, 'avatar', '') if hasattr(user, 'profile') else '',
            'role': 'admin'
        }
        return ApiResponse.success(data=data)
    except Exception as e:
        return ApiResponse.error(message=f"获取用户资料失败: {str(e)}")

@api_view(['POST'])
def admin_register(request):
    """管理员注册"""
    try:
        # 请求数据验证
        if not request.data:
            return ApiResponse.error(message="请求数据不能为空")
            
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        confirm_password = request.data.get('confirm_password')
        
        # 详细的参数验证
        if not username:
            return ApiResponse.error(message="请输入用户名")
        if not password:
            return ApiResponse.error(message="请输入密码")
        if not email:
            return ApiResponse.error(message="请输入邮箱")
        if not confirm_password:
            return ApiResponse.error(message="请确认密码")
            
        username = username.strip()
        email = email.strip()
        
        if len(username) < 3:
            return ApiResponse.error(message="用户名长度不能少于3个字符")
        if len(password) < 6:
            return ApiResponse.error(message="密码长度不能少于6个字符")
        if password != confirm_password:
            return ApiResponse.error(message="两次输入的密码不一致")
        
        # 检查是否包含特殊字符
        import re
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return ApiResponse.error(message="用户名只能包含字母、数字和下划线")
        
        # 邮箱格式验证
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return ApiResponse.error(message="请输入有效的邮箱地址")
        
        result, error_message = AuthService.admin_register(username, password, email, request)
        
        if result:
            return ApiResponse.success(
                data=result, 
                message="注册成功，欢迎加入管理团队！"
            )
        else:
            return ApiResponse.error(
                message=error_message or "注册失败，请检查输入信息",
                code=400
            )
    except ValueError as e:
        return ApiResponse.error(message=f"输入数据格式错误: {str(e)}")
    except Exception as e:
        logger.error(f"管理员注册API异常: {str(e)}")
        return ApiResponse.error(
            message="系统繁忙，请稍后重试",
            code=500
        )
