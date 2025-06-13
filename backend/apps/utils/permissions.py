from rest_framework import permissions
import logging
from datetime import datetime
from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from apps.utils.response import ApiResponse

# 获取logger实例
logger = logging.getLogger(__name__)

# 错误代码常量
class ErrorCodes:
    # 认证相关错误
    AUTH_TOKEN_MISSING = 'AUTH_001'
    AUTH_TOKEN_INVALID = 'AUTH_002'
    AUTH_TOKEN_EXPIRED = 'AUTH_003'
    AUTH_USER_NOT_FOUND = 'AUTH_004'
    AUTH_USER_TYPE_MISMATCH = 'AUTH_005'
    AUTH_PERMISSION_DENIED = 'AUTH_006'
    AUTH_SYSTEM_ERROR = 'AUTH_007'
    
    # 权限相关错误
    PERM_ADMIN_REQUIRED = 'PERM_001'
    PERM_MERCHANT_REQUIRED = 'PERM_002'
    PERM_OWNER_REQUIRED = 'PERM_003'
    PERM_OBJECT_ACCESS_DENIED = 'PERM_004'

class IsAdminUser(permissions.BasePermission):
    """
    管理员权限
    """
    def has_permission(self, request, view):
        if not request.user:
            logger.warning(f"管理员权限检查失败 - 用户未认证, Path: {request.path}, IP: {request.META.get('REMOTE_ADDR', 'Unknown')}, Time: {datetime.now()}")
            return False
            
        if not request.user.is_authenticated:
            logger.warning(f"管理员权限检查失败 - 用户未通过认证, User: {getattr(request.user, 'username', 'Anonymous')}, Path: {request.path}, IP: {request.META.get('REMOTE_ADDR', 'Unknown')}, Time: {datetime.now()}")
            return False
            
        if request.user.user_type != 'admin':
            logger.warning(f"管理员权限检查失败 - 用户类型不匹配, User: {getattr(request.user, 'username', 'Anonymous')}, UserType: {getattr(request.user, 'user_type', 'None')}, Expected: admin, Path: {request.path}, IP: {request.META.get('REMOTE_ADDR', 'Unknown')}, Time: {datetime.now()}")
            return False
            
        logger.info(f"管理员权限检查通过 - User: {request.user.username}, Path: {request.path}, Time: {datetime.now()}")
        return True

class IsMerchantUser(permissions.BasePermission):
    """
    商户权限
    """
    def has_permission(self, request, view):
        if not request.user:
            logger.warning(f"商户权限检查失败 - 用户未认证, Path: {request.path}, IP: {request.META.get('REMOTE_ADDR', 'Unknown')}, Time: {datetime.now()}")
            return False
            
        if not request.user.is_authenticated:
            logger.warning(f"商户权限检查失败 - 用户未通过认证, User: {getattr(request.user, 'username', 'Anonymous')}, Path: {request.path}, IP: {request.META.get('REMOTE_ADDR', 'Unknown')}, Time: {datetime.now()}")
            return False
            
        if request.user.user_type != 'merchant':
            logger.warning(f"商户权限检查失败 - 用户类型不匹配, User: {getattr(request.user, 'username', 'Anonymous')}, UserType: {getattr(request.user, 'user_type', 'None')}, Expected: merchant, Path: {request.path}, IP: {request.META.get('REMOTE_ADDR', 'Unknown')}, Time: {datetime.now()}")
            return False
            
        logger.info(f"商户权限检查通过 - User: {request.user.username}, Path: {request.path}, Time: {datetime.now()}")
        return True

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    对象所有者权限：只有所有者可以修改，其他用户只读
    """
    def has_object_permission(self, request, view, obj):
        # 安全方法总是允许
        if request.method in permissions.SAFE_METHODS:
            logger.info(f"对象访问权限检查通过 - 安全方法, User: {getattr(request.user, 'username', 'Anonymous')}, Method: {request.method}, Path: {request.path}, Time: {datetime.now()}")
            return True
        
        # 检查用户是否认证
        if not request.user or not request.user.is_authenticated:
            logger.warning(f"对象所有者权限检查失败 - 用户未认证, Method: {request.method}, Path: {request.path}, IP: {request.META.get('REMOTE_ADDR', 'Unknown')}, Time: {datetime.now()}")
            return False
        
        # 获取对象的user属性
        if hasattr(obj, 'user'):
            if obj.user == request.user:
                logger.info(f"对象所有者权限检查通过 - User属性匹配, User: {request.user.username}, Method: {request.method}, Path: {request.path}, Time: {datetime.now()}")
                return True
            else:
                logger.warning(f"对象所有者权限检查失败 - User属性不匹配, User: {request.user.username}, ObjectOwner: {getattr(obj.user, 'username', 'None')}, Method: {request.method}, Path: {request.path}, Time: {datetime.now()}")
                return False
        
        # 获取对象的owner属性
        if hasattr(obj, 'owner'):
            if obj.owner == request.user:
                logger.info(f"对象所有者权限检查通过 - Owner属性匹配, User: {request.user.username}, Method: {request.method}, Path: {request.path}, Time: {datetime.now()}")
                return True
            else:
                logger.warning(f"对象所有者权限检查失败 - Owner属性不匹配, User: {request.user.username}, ObjectOwner: {getattr(obj.owner, 'username', 'None')}, Method: {request.method}, Path: {request.path}, Time: {datetime.now()}")
                return False
        
        # 默认不允许
        logger.warning(f"对象所有者权限检查失败 - 对象没有user或owner属性, User: {request.user.username}, ObjectType: {type(obj).__name__}, Method: {request.method}, Path: {request.path}, Time: {datetime.now()}")
        return False

# === 增强的错误响应函数 ===

def create_auth_error_response(error_code, message, details=None, suggestions=None):
    """
    创建认证错误响应
    """
    error_data = {
        'error_code': error_code,
        'message': message,
        'timestamp': datetime.now().isoformat(),
        'type': 'authentication_error'
    }
    
    if details:
        error_data['details'] = details
        
    if suggestions:
        error_data['suggestions'] = suggestions
    
    return ApiResponse.error(
        message=message,
        code=401,
        data=error_data
    )

def get_user_friendly_suggestions(error_type, user_type=None):
    """
    获取用户友好的建议信息
    """
    suggestions = {
        'token_missing': [
            '请确保在请求头中包含 Authorization 字段',
            '格式应为: Authorization: Bearer <your_token>',
            '如果没有token，请先登录获取'
        ],
        'token_invalid': [
            '请检查token格式是否正确',
            '确认token没有被截断或修改',
            '如果问题持续，请重新登录获取新token'
        ],
        'token_expired': [
            'Token已过期，请重新登录',
            '建议启用自动刷新token功能',
            '检查系统时间是否正确'
        ],
        'user_type_mismatch': [
            f'当前用户类型为 {user_type}，无法访问此功能',
            '请使用正确类型的账户登录',
            '如需权限升级，请联系管理员'
        ],
        'permission_denied': [
            '您没有访问此资源的权限',
            '请确认您的账户状态正常',
            '如需帮助，请联系客服或管理员'
        ]
    }
    return suggestions.get(error_type, ['请联系技术支持获取帮助'])

# === 多端API权限装饰器 ===

def user_api_permission(view_func):
    """用户端API权限装饰器"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # JWT认证
        jwt_auth = JWTAuthentication()
        try:
            auth_result = jwt_auth.authenticate(request)
            if auth_result is None:
                logger.warning(f"用户端API认证失败 - 无有效token, Path: {request.path}, IP: {request.META.get('REMOTE_ADDR', 'Unknown')}, UserAgent: {request.META.get('HTTP_USER_AGENT', 'Unknown')}, Time: {datetime.now()}")
                return create_auth_error_response(
                    ErrorCodes.AUTH_TOKEN_MISSING,
                    '用户认证失败：请求头中缺少有效的Authorization token',
                    details='未在请求头中找到有效的JWT token',
                    suggestions=get_user_friendly_suggestions('token_missing')
                )
            
            user, token = auth_result
            if not user:
                logger.warning(f"用户端API认证失败 - token有效但用户不存在, Path: {request.path}, IP: {request.META.get('REMOTE_ADDR', 'Unknown')}, Time: {datetime.now()}")
                return create_auth_error_response(
                    ErrorCodes.AUTH_USER_NOT_FOUND,
                    '用户认证失败：Token有效但对应用户不存在',
                    details='JWT token解析成功但数据库中找不到对应用户',
                    suggestions=['请重新登录', '如果问题持续，请联系客服']
                )
            
            if user.user_type != 'tourist':
                logger.warning(f"用户端API权限不足 - User: {user.username}, UserType: {user.user_type}, Expected: tourist, Path: {request.path}, IP: {request.META.get('REMOTE_ADDR', 'Unknown')}, Time: {datetime.now()}")
                return create_auth_error_response(
                    ErrorCodes.AUTH_USER_TYPE_MISMATCH,
                    f'用户认证失败：用户类型不匹配，当前类型: {user.user_type}，需要类型: tourist',
                    details=f'用户 {user.username} 的类型为 {user.user_type}，但此接口仅允许 tourist 类型用户访问',
                    suggestions=get_user_friendly_suggestions('user_type_mismatch', user.user_type)
                )
            
            # 检查用户状态
            if not user.is_active:
                logger.warning(f"用户端API认证失败 - 用户已被禁用, User: {user.username}, Path: {request.path}, Time: {datetime.now()}")
                return create_auth_error_response(
                    ErrorCodes.AUTH_PERMISSION_DENIED,
                    '用户认证失败：账户已被禁用',
                    details=f'用户 {user.username} 的账户状态为非活跃状态',
                    suggestions=['请联系管理员恢复账户', '检查是否违反了使用条款']
                )
            
            logger.info(f"用户端API认证成功 - User: {user.username}, UserType: {user.user_type}, Path: {request.path}, Time: {datetime.now()}")
            request.user = user
            return view_func(request, *args, **kwargs)
            
        except InvalidToken as e:
            logger.warning(f"用户端API JWT token无效 - Error: {str(e)}, Path: {request.path}, IP: {request.META.get('REMOTE_ADDR', 'Unknown')}, Time: {datetime.now()}")
            return create_auth_error_response(
                ErrorCodes.AUTH_TOKEN_INVALID,
                f'用户认证失败：JWT token无效: {str(e)}',
                details=f'Token验证失败: {str(e)}',
                suggestions=get_user_friendly_suggestions('token_invalid')
            )
        except TokenError as e:
            logger.warning(f"用户端API JWT token错误 - Error: {str(e)}, Path: {request.path}, IP: {request.META.get('REMOTE_ADDR', 'Unknown')}, Time: {datetime.now()}")
            if 'expired' in str(e).lower():
                return create_auth_error_response(
                    ErrorCodes.AUTH_TOKEN_EXPIRED,
                    f'用户认证失败：JWT token已过期: {str(e)}',
                    details=f'Token过期: {str(e)}',
                    suggestions=get_user_friendly_suggestions('token_expired')
                )
            else:
                return create_auth_error_response(
                    ErrorCodes.AUTH_TOKEN_INVALID,
                    f'用户认证失败：JWT token错误: {str(e)}',
                    details=f'Token处理错误: {str(e)}',
                    suggestions=get_user_friendly_suggestions('token_invalid')
                )
        except Exception as e:
            logger.error(f"用户端API认证异常 - Error: {str(e)}, Path: {request.path}, IP: {request.META.get('REMOTE_ADDR', 'Unknown')}, Time: {datetime.now()}", exc_info=True)
            return create_auth_error_response(
                ErrorCodes.AUTH_SYSTEM_ERROR,
                f'用户认证失败：认证过程中发生系统错误',
                details=f'系统异常: {str(e)}',
                suggestions=['请稍后重试', '如果问题持续，请联系技术支持']
            )
    return wrapper

def merchant_api_permission(view_func):
    """商户端API权限装饰器"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # JWT认证
        jwt_auth = JWTAuthentication()
        try:
            auth_result = jwt_auth.authenticate(request)
            if auth_result is None:
                logger.warning(f"商户端API认证失败 - 无有效token, Path: {request.path}, IP: {request.META.get('REMOTE_ADDR', 'Unknown')}, UserAgent: {request.META.get('HTTP_USER_AGENT', 'Unknown')}, Time: {datetime.now()}")
                return create_auth_error_response(
                    ErrorCodes.AUTH_TOKEN_MISSING,
                    '商户认证失败：请求头中缺少有效的Authorization token',
                    details='未在请求头中找到有效的JWT token',
                    suggestions=get_user_friendly_suggestions('token_missing')
                )
            
            user, token = auth_result
            if not user:
                logger.warning(f"商户端API认证失败 - token有效但用户不存在, Path: {request.path}, IP: {request.META.get('REMOTE_ADDR', 'Unknown')}, Time: {datetime.now()}")
                return create_auth_error_response(
                    ErrorCodes.AUTH_USER_NOT_FOUND,
                    '商户认证失败：Token有效但对应用户不存在',
                    details='JWT token解析成功但数据库中找不到对应用户',
                    suggestions=['请重新登录', '如果问题持续，请联系客服']
                )
            
            if user.user_type != 'merchant':
                logger.warning(f"商户端API权限不足 - User: {user.username}, UserType: {user.user_type}, Expected: merchant, Path: {request.path}, IP: {request.META.get('REMOTE_ADDR', 'Unknown')}, Time: {datetime.now()}")
                return create_auth_error_response(
                    ErrorCodes.AUTH_USER_TYPE_MISMATCH,
                    f'商户认证失败：用户类型不匹配，当前类型: {user.user_type}，需要类型: merchant',
                    details=f'用户 {user.username} 的类型为 {user.user_type}，但此接口仅允许 merchant 类型用户访问',
                    suggestions=get_user_friendly_suggestions('user_type_mismatch', user.user_type)
                )
            
            # 检查用户状态
            if not user.is_active:
                logger.warning(f"商户端API认证失败 - 用户已被禁用, User: {user.username}, Path: {request.path}, Time: {datetime.now()}")
                return create_auth_error_response(
                    ErrorCodes.AUTH_PERMISSION_DENIED,
                    '商户认证失败：账户已被禁用',
                    details=f'用户 {user.username} 的账户状态为非活跃状态',
                    suggestions=['请联系管理员恢复账户', '检查是否违反了使用条款']
                )
            
            logger.info(f"商户端API认证成功 - User: {user.username}, UserType: {user.user_type}, Path: {request.path}, Time: {datetime.now()}")
            request.user = user
            return view_func(request, *args, **kwargs)
            
        except InvalidToken as e:
            logger.warning(f"商户端API JWT token无效 - Error: {str(e)}, Path: {request.path}, IP: {request.META.get('REMOTE_ADDR', 'Unknown')}, Time: {datetime.now()}")
            return create_auth_error_response(
                ErrorCodes.AUTH_TOKEN_INVALID,
                f'商户认证失败：JWT token无效: {str(e)}',
                details=f'Token验证失败: {str(e)}',
                suggestions=get_user_friendly_suggestions('token_invalid')
            )
        except TokenError as e:
            logger.warning(f"商户端API JWT token错误 - Error: {str(e)}, Path: {request.path}, IP: {request.META.get('REMOTE_ADDR', 'Unknown')}, Time: {datetime.now()}")
            if 'expired' in str(e).lower():
                return create_auth_error_response(
                    ErrorCodes.AUTH_TOKEN_EXPIRED,
                    f'商户认证失败：JWT token已过期: {str(e)}',
                    details=f'Token过期: {str(e)}',
                    suggestions=get_user_friendly_suggestions('token_expired')
                )
            else:
                return create_auth_error_response(
                    ErrorCodes.AUTH_TOKEN_INVALID,
                    f'商户认证失败：JWT token错误: {str(e)}',
                    details=f'Token处理错误: {str(e)}',
                    suggestions=get_user_friendly_suggestions('token_invalid')
                )
        except Exception as e:
            logger.error(f"商户端API认证异常 - Error: {str(e)}, Path: {request.path}, IP: {request.META.get('REMOTE_ADDR', 'Unknown')}, Time: {datetime.now()}", exc_info=True)
            return create_auth_error_response(
                ErrorCodes.AUTH_SYSTEM_ERROR,
                f'商户认证失败：认证过程中发生系统错误',
                details=f'系统异常: {str(e)}',
                suggestions=['请稍后重试', '如果问题持续，请联系技术支持']
            )
    return wrapper

def admin_api_permission(view_func):
    """管理员端API权限装饰器"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # JWT认证
        jwt_auth = JWTAuthentication()
        try:
            auth_result = jwt_auth.authenticate(request)
            if auth_result is None:
                logger.warning(f"管理员端API认证失败 - 无有效token, Path: {request.path}, IP: {request.META.get('REMOTE_ADDR', 'Unknown')}, UserAgent: {request.META.get('HTTP_USER_AGENT', 'Unknown')}, Time: {datetime.now()}")
                return create_auth_error_response(
                    ErrorCodes.AUTH_TOKEN_MISSING,
                    '管理员认证失败：请求头中缺少有效的Authorization token',
                    details='未在请求头中找到有效的JWT token',
                    suggestions=get_user_friendly_suggestions('token_missing')
                )
            
            user, token = auth_result
            if not user:
                logger.warning(f"管理员端API认证失败 - token有效但用户不存在, Path: {request.path}, IP: {request.META.get('REMOTE_ADDR', 'Unknown')}, Time: {datetime.now()}")
                return create_auth_error_response(
                    ErrorCodes.AUTH_USER_NOT_FOUND,
                    '管理员认证失败：Token有效但对应用户不存在',
                    details='JWT token解析成功但数据库中找不到对应用户',
                    suggestions=['请重新登录', '如果问题持续，请联系技术支持']
                )
            
            if user.user_type != 'admin':
                logger.warning(f"管理员端API权限不足 - User: {user.username}, UserType: {user.user_type}, Expected: admin, Path: {request.path}, IP: {request.META.get('REMOTE_ADDR', 'Unknown')}, Time: {datetime.now()}")
                return create_auth_error_response(
                    ErrorCodes.AUTH_USER_TYPE_MISMATCH,
                    f'管理员认证失败：用户类型不匹配，当前类型: {user.user_type}，需要类型: admin',
                    details=f'用户 {user.username} 的类型为 {user.user_type}，但此接口仅允许 admin 类型用户访问',
                    suggestions=get_user_friendly_suggestions('user_type_mismatch', user.user_type)
                )
            
            # 检查用户状态
            if not user.is_active:
                logger.warning(f"管理员端API认证失败 - 用户已被禁用, User: {user.username}, Path: {request.path}, Time: {datetime.now()}")
                return create_auth_error_response(
                    ErrorCodes.AUTH_PERMISSION_DENIED,
                    '管理员认证失败：账户已被禁用',
                    details=f'用户 {user.username} 的账户状态为非活跃状态',
                    suggestions=['请联系系统管理员', '检查账户状态']
                )
            
            logger.info(f"管理员端API认证成功 - User: {user.username}, UserType: {user.user_type}, Path: {request.path}, Time: {datetime.now()}")
            request.user = user
            return view_func(request, *args, **kwargs)
            
        except InvalidToken as e:
            logger.warning(f"管理员端API JWT token无效 - Error: {str(e)}, Path: {request.path}, IP: {request.META.get('REMOTE_ADDR', 'Unknown')}, Time: {datetime.now()}")
            return create_auth_error_response(
                ErrorCodes.AUTH_TOKEN_INVALID,
                f'管理员认证失败：JWT token无效: {str(e)}',
                details=f'Token验证失败: {str(e)}',
                suggestions=get_user_friendly_suggestions('token_invalid')
            )
        except TokenError as e:
            logger.warning(f"管理员端API JWT token错误 - Error: {str(e)}, Path: {request.path}, IP: {request.META.get('REMOTE_ADDR', 'Unknown')}, Time: {datetime.now()}")
            if 'expired' in str(e).lower():
                return create_auth_error_response(
                    ErrorCodes.AUTH_TOKEN_EXPIRED,
                    f'管理员认证失败：JWT token已过期: {str(e)}',
                    details=f'Token过期: {str(e)}',
                    suggestions=get_user_friendly_suggestions('token_expired')
                )
            else:
                return create_auth_error_response(
                    ErrorCodes.AUTH_TOKEN_INVALID,
                    f'管理员认证失败：JWT token错误: {str(e)}',
                    details=f'Token处理错误: {str(e)}',
                    suggestions=get_user_friendly_suggestions('token_invalid')
                )
        except Exception as e:
            logger.error(f"管理员端API认证异常 - Error: {str(e)}, Path: {request.path}, IP: {request.META.get('REMOTE_ADDR', 'Unknown')}, Time: {datetime.now()}", exc_info=True)
            return create_auth_error_response(
                ErrorCodes.AUTH_SYSTEM_ERROR,
                f'管理员认证失败：认证过程中发生系统错误',
                details=f'系统异常: {str(e)}',
                suggestions=['请稍后重试', '如果问题持续，请联系技术支持']
            )
    return wrapper
