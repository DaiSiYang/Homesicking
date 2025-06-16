
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.models import User as CustomUser
import logging

# 获取logger实例
logger = logging.getLogger(__name__)

class AuthService:
    @staticmethod
    def user_login(username, password, request=None):
        """用户登录"""
        try:
            # 记录登录尝试
            ip_address = request.META.get('REMOTE_ADDR', 'Unknown') if request else 'Unknown'
            logger.info(f"用户登录尝试 - Username: {username}, IP: {ip_address}")
            
            # 首先检查用户是否存在
            try:
                user_obj = CustomUser.objects.get(username=username)
                logger.info(f"找到用户 - Username: {username}, UserType: {user_obj.user_type}, IsActive: {user_obj.is_active}")
            except CustomUser.DoesNotExist:
                logger.warning(f"用户登录失败 - 用户不存在, Username: {username}, IP: {ip_address}")
                return None, "用户名或密码错误"
            
            # 检查用户类型
            if user_obj.user_type != 'tourist':
                logger.warning(f"用户登录失败 - 用户类型不匹配, Username: {username}, UserType: {user_obj.user_type}, Expected: tourist, IP: {ip_address}")
                return None, f"用户类型错误，当前类型: {user_obj.user_type}，需要类型: tourist"
            
            # 检查用户是否激活
            if not user_obj.is_active:
                logger.warning(f"用户登录失败 - 用户未激活, Username: {username}, IP: {ip_address}")
                return None, "用户账户已被禁用"
            
            # 进行认证
            user = authenticate(username=username, password=password)
            if user and user.user_type == 'tourist':
                # 生成token
                refresh = RefreshToken.for_user(user)
                logger.info(f"用户登录成功 - Username: {username}, UserID: {user.id}, IP: {ip_address}")
                return {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'token': str(refresh.access_token),  # 前端期望的token字段
                    'user_id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'user_type': user.user_type
                }, None
            else:
                logger.warning(f"用户登录失败 - 密码错误或认证失败, Username: {username}, IP: {ip_address}")
                return None, "用户名或密码错误"
                
        except Exception as e:
            logger.error(f"用户登录异常 - Username: {username}, Error: {str(e)}, IP: {ip_address if 'ip_address' in locals() else 'Unknown'}")
            return None, f"登录过程中发生错误: {str(e)}"
    
    @staticmethod
    def merchant_login(username, password, request=None):
        """商户登录"""
        try:
            ip_address = request.META.get('REMOTE_ADDR', 'Unknown') if request else 'Unknown'
            logger.info(f"商户登录尝试 - Username: {username}, IP: {ip_address}")
            
            try:
                user_obj = CustomUser.objects.get(username=username)
                logger.info(f"找到商户 - Username: {username}, UserType: {user_obj.user_type}, IsActive: {user_obj.is_active}")
            except CustomUser.DoesNotExist:
                logger.warning(f"商户登录失败 - 用户不存在, Username: {username}, IP: {ip_address}")
                return None, "用户名或密码错误"
            
            if user_obj.user_type != 'merchant':
                logger.warning(f"商户登录失败 - 用户类型不匹配, Username: {username}, UserType: {user_obj.user_type}, Expected: merchant, IP: {ip_address}")
                return None, f"用户类型错误，当前类型: {user_obj.user_type}，需要类型: merchant"
            
            if not user_obj.is_active:
                logger.warning(f"商户登录失败 - 用户未激活, Username: {username}, IP: {ip_address}")
                return None, "商户账户已被禁用"
            
            user = authenticate(username=username, password=password)
            if user and user.user_type == 'merchant':
                refresh = RefreshToken.for_user(user)
                logger.info(f"商户登录成功 - Username: {username}, UserID: {user.id}, IP: {ip_address}")
                return {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'token': str(refresh.access_token),  # 前端期望的token字段
                    'user_id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'user_type': user.user_type
                }, None
            else:
                logger.warning(f"商户登录失败 - 密码错误或认证失败, Username: {username}, IP: {ip_address}")
                return None, "用户名或密码错误"
                
        except Exception as e:
            logger.error(f"商户登录异常 - Username: {username}, Error: {str(e)}, IP: {ip_address if 'ip_address' in locals() else 'Unknown'}")
            return None, f"登录过程中发生错误: {str(e)}"
    
    @staticmethod
    def admin_login(username, password, request=None):
        """管理员登录"""
        try:
            # 参数验证
            if not username or not username.strip():
                return None, "用户名不能为空"
            if not password or not password.strip():
                return None, "密码不能为空"
            if len(username) < 3:
                return None, "用户名长度不能少于3个字符"
            if len(password) < 6:
                return None, "密码长度不能少于6个字符"
                
            ip_address = request.META.get('REMOTE_ADDR', 'Unknown') if request else 'Unknown'
            logger.info(f"管理员登录尝试 - Username: {username}, IP: {ip_address}")
            
            try:
                user_obj = CustomUser.objects.get(username=username)
                logger.info(f"找到管理员 - Username: {username}, UserType: {user_obj.user_type}, IsActive: {user_obj.is_active}")
            except CustomUser.DoesNotExist:
                logger.warning(f"管理员登录失败 - 用户不存在, Username: {username}, IP: {ip_address}")
                return None, "用户名或密码错误，请检查输入信息"
            
            # 详细的用户类型检查
            if user_obj.user_type not in ['admin', 'super_admin']:
                logger.warning(f"管理员登录失败 - 用户类型不匹配, Username: {username}, UserType: {user_obj.user_type}, Expected: admin/super_admin, IP: {ip_address}")
                if user_obj.user_type == 'tourist':
                    return None, "此账户为普通用户账户，请使用用户端登录"
                elif user_obj.user_type == 'merchant':
                    return None, "此账户为商户账户，请使用商户端登录"
                else:
                    return None, f"账户类型错误，当前类型: {user_obj.user_type}，需要管理员权限"
            
            # 账户状态检查
            if not user_obj.is_active:
                logger.warning(f"管理员登录失败 - 用户未激活, Username: {username}, IP: {ip_address}")
                return None, "管理员账户已被禁用，请联系系统管理员"
            
            # 密码验证
            user = authenticate(username=username, password=password)
            if user and user.user_type in ['admin', 'super_admin']:
                refresh = RefreshToken.for_user(user)
                logger.info(f"管理员登录成功 - Username: {username}, UserID: {user.id}, IP: {ip_address}")
                return {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'token': str(refresh.access_token),
                    'user_id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'user_type': user.user_type,
                    'permissions': ['admin'] if user.user_type == 'admin' else ['admin', 'super_admin']
                }, None
            else:
                logger.warning(f"管理员登录失败 - 密码错误或认证失败, Username: {username}, IP: {ip_address}")
                return None, "用户名或密码错误，请检查输入信息"
                
        except Exception as e:
            logger.error(f"管理员登录异常 - Username: {username}, Error: {str(e)}, IP: {ip_address if 'ip_address' in locals() else 'Unknown'}")
            return None, f"登录服务暂时不可用，请稍后重试。错误详情: {str(e)}"

    @staticmethod
    def admin_register(username, password, email, request=None):
        """管理员注册"""
        try:
            ip_address = request.META.get('REMOTE_ADDR', 'Unknown') if request else 'Unknown'
            logger.info(f"管理员注册尝试 - Username: {username}, Email: {email}, IP: {ip_address}")
            
            # 检查用户名是否已存在
            if CustomUser.objects.filter(username=username).exists():
                logger.warning(f"管理员注册失败 - 用户名已存在, Username: {username}, IP: {ip_address}")
                return None, "用户名已存在"
            
            # 检查邮箱是否已存在
            if CustomUser.objects.filter(email=email).exists():
                logger.warning(f"管理员注册失败 - 邮箱已存在, Email: {email}, IP: {ip_address}")
                return None, "邮箱已存在"
            
            # 创建管理员用户
            user = CustomUser.objects.create_user(
                username=username,
                password=password,
                email=email,
                user_type='admin',  # 设置为管理员类型
                is_active=True  # 管理员账户默认激活
            )
            
            # 生成token
            refresh = RefreshToken.for_user(user)
            logger.info(f"管理员注册成功 - Username: {username}, UserID: {user.id}, IP: {ip_address}")
            
            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'token': str(refresh.access_token),
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'user_type': user.user_type,
                'permissions': ['admin']
            }, None
            
        except Exception as e:
            logger.error(f"管理员注册异常 - Username: {username}, Error: {str(e)}, IP: {ip_address if 'ip_address' in locals() else 'Unknown'}")
            return None, f"注册服务暂时不可用，请稍后重试。错误详情: {str(e)}"

    @staticmethod
    def user_register(username, password, email, phone=None, request=None):
        """用户注册"""
        try:
            ip_address = request.META.get('REMOTE_ADDR', 'Unknown') if request else 'Unknown'
            logger.info(f"用户注册尝试 - Username: {username}, Email: {email}, IP: {ip_address}")
            
            # 检查用户名是否已存在
            if CustomUser.objects.filter(username=username).exists():
                logger.warning(f"用户注册失败 - 用户名已存在, Username: {username}, IP: {ip_address}")
                return None, "用户名已存在"
            
            # 检查邮箱是否已存在
            if CustomUser.objects.filter(email=email).exists():
                logger.warning(f"用户注册失败 - 邮箱已存在, Email: {email}, IP: {ip_address}")
                return None, "邮箱已存在"
            
            # 创建用户
            user = CustomUser.objects.create_user(
                username=username,
                password=password,
                email=email,
                phone=phone,
                user_type='tourist'  # 修正为 'tourist'
            )
            
            # 生成token
            refresh = RefreshToken.for_user(user)
            logger.info(f"用户注册成功 - Username: {username}, UserID: {user.id}, IP: {ip_address}")
            
            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'token': str(refresh.access_token),  # 前端期望的token字段
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'user_type': user.user_type,
                    'phone': user.phone,
                    'date_joined': user.date_joined.isoformat() if user.date_joined else None
                }
            }, None
            
        except Exception as e:
            logger.error(f"用户注册异常 - Username: {username}, Error: {str(e)}, IP: {ip_address if 'ip_address' in locals() else 'Unknown'}")
            return None, f"注册过程中发生错误: {str(e)}"
    
    @staticmethod
    def merchant_register(data):
        """商户注册"""
        try:
            username = data.get('username')
            password = data.get('password')
            email = data.get('email')
            phone = data.get('phone')
            company_name = data.get('company_name')  # 商户特有字段
            
            logger.info(f"商户注册尝试 - Username: {username}, Email: {email}")
            
            # 检查用户名是否已存在
            if CustomUser.objects.filter(username=username).exists():
                logger.warning(f"商户注册失败 - 用户名已存在, Username: {username}")
                raise Exception("用户名已存在")
            
            # 检查邮箱是否已存在
            if CustomUser.objects.filter(email=email).exists():
                logger.warning(f"商户注册失败 - 邮箱已存在, Email: {email}")
                raise Exception("邮箱已存在")
            
            # 创建商户用户
            user = CustomUser.objects.create_user(
                username=username,
                password=password,
                email=email,
                phone=phone,
                user_type='merchant'  # 设置为商户类型
            )
            
            # 如果有商户特有信息，可以在这里处理
            # 例如创建商户档案等
            
            # 生成token
            refresh = RefreshToken.for_user(user)
            logger.info(f"商户注册成功 - Username: {username}, UserID: {user.id}")
            
            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'token': str(refresh.access_token),  # 前端期望的token字段
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'user_type': user.user_type
            }
            
        except Exception as e:
            logger.error(f"商户注册异常 - Error: {str(e)}")
            raise Exception(f"注册过程中发生错误: {str(e)}")

    @staticmethod
    def user_logout(request):
        """用户登出"""
        try:
            ip_address = request.META.get('REMOTE_ADDR', 'Unknown')
            user = request.user
            logger.info(f"用户登出 - Username: {user.username}, UserID: {user.id}, IP: {ip_address}")
            
            # 对于JWT token，通常不需要服务端处理，客户端删除token即可
            # 如果需要黑名单功能，可以在这里添加token到黑名单
            
            return {
                'message': '登出成功'
            }
            
        except Exception as e:
            logger.error(f"用户登出异常 - Error: {str(e)}, IP: {ip_address if 'ip_address' in locals() else 'Unknown'}")
            raise Exception(f"登出过程中发生错误: {str(e)}")
