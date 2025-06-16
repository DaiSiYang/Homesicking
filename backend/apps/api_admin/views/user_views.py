from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from apps.utils.response import ApiResponse
from apps.utils.permissions import IsAdminUser
from apps.users.models import User
from apps.orders.models import Order
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.hashers import make_password
import logging
import traceback

logger = logging.getLogger(__name__)

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def user_list(request):
    """获取用户列表"""
    try:
        logger.info(f"用户列表请求 - 用户: {request.user.username}, 参数: {dict(request.GET)}")
        
        # 参数验证
        page = request.GET.get('page', 1)
        page_size = request.GET.get('page_size', 10)
        search = request.GET.get('search', '').strip()
        user_type = request.GET.get('user_type', '').strip()
        
        logger.debug(f"请求参数 - page: {page}, page_size: {page_size}, search: '{search}', user_type: '{user_type}'")
        
        # 参数类型验证
        try:
            page = int(page)
            page_size = int(page_size)
        except ValueError as e:
            error_msg = f"参数类型错误 - page: {request.GET.get('page')}, page_size: {request.GET.get('page_size')}, 错误: {str(e)}"
            logger.warning(error_msg)
            return ApiResponse.error(message="页码和每页数量必须为数字", code=400)
            
        # 参数范围验证
        if page < 1:
            logger.warning(f"页码参数错误 - page: {page}")
            return ApiResponse.error(message="页码不能小于1", code=400)
        if page_size < 1 or page_size > 100:
            logger.warning(f"页面大小参数错误 - page_size: {page_size}")
            return ApiResponse.error(message="每页数量必须在1-100之间", code=400)
            
        # 用户类型验证
        valid_user_types = ['tourist', 'merchant', 'admin', 'super_admin']
        if user_type and user_type not in valid_user_types:
            logger.warning(f"无效用户类型 - user_type: '{user_type}'")
            return ApiResponse.error(message=f"无效的用户类型，支持的类型: {', '.join(valid_user_types)}", code=400)
        
        # 搜索关键词长度验证
        if search and len(search) > 50:
            logger.warning(f"搜索关键词过长 - search: '{search}', length: {len(search)}")
            return ApiResponse.error(message="搜索关键词长度不能超过50个字符", code=400)
            
        # 查询用户数据
        try:
            from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
            from apps.users.models import User as CustomUser
            
            logger.debug("开始查询用户数据")
            queryset = CustomUser.objects.all()
            initial_count = queryset.count()
            logger.debug(f"数据库中总用户数: {initial_count}")
            
            # 应用过滤条件
            if search:
                logger.debug(f"应用搜索过滤 - 关键词: '{search}'")
                queryset = queryset.filter(
                    Q(username__icontains=search) | 
                    Q(email__icontains=search) |
                    Q(phone__icontains=search)
                )
                search_count = queryset.count()
                logger.debug(f"搜索过滤后用户数: {search_count}")
                
            # 只有当明确指定用户类型时才进行过滤，否则显示所有用户
            if user_type:
                logger.debug(f"应用用户类型过滤 - 类型: '{user_type}'")
                queryset = queryset.filter(user_type=user_type)
                type_count = queryset.count()
                logger.debug(f"类型过滤后用户数: {type_count}")
            else:
                logger.debug("未指定用户类型，显示所有用户")
            
            # 按创建时间倒序排列，确保最新用户在前面
            queryset = queryset.order_by('-date_joined')
            final_count = queryset.count()
            logger.debug(f"最终查询结果用户数: {final_count}")
            
            # 分页处理
            logger.debug(f"开始分页处理 - page: {page}, page_size: {page_size}")
            paginator = Paginator(queryset, page_size)
            logger.debug(f"分页信息 - 总页数: {paginator.num_pages}, 总记录数: {paginator.count}")
            
            try:
                users = paginator.page(page)
                logger.debug(f"成功获取第{page}页数据，包含{len(users)}条记录")
            except PageNotAnInteger as e:
                error_msg = f"页码格式错误 - page: {page}, 错误: {str(e)}"
                logger.warning(error_msg)
                return ApiResponse.error(message="页码必须为整数", code=400)
            except EmptyPage as e:
                error_msg = f"页码超出范围 - page: {page}, 总页数: {paginator.num_pages}, 错误: {str(e)}"
                logger.warning(error_msg)
                return ApiResponse.error(message=f"页码超出范围，总共{paginator.num_pages}页", code=400)
                
        except Exception as e:
            error_msg = f"数据库查询异常: {str(e)}, 堆栈: {traceback.format_exc()}"
            logger.error(error_msg)
            return ApiResponse.error(message=f"数据库查询失败: {str(e)}", code=500)
            
        # 序列化数据
        try:
            logger.debug("开始序列化用户数据")
            user_data = []
            failed_users = []
            
            for user in users:
                try:
                    user_info = {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'phone': user.phone or '',
                        'user_type': user.user_type,
                        'is_active': user.is_active,
                        'date_joined': user.date_joined.strftime('%Y-%m-%d %H:%M:%S'),
                        'last_login': user.last_login.strftime('%Y-%m-%d %H:%M:%S') if user.last_login else '从未登录'
                    }
                    user_data.append(user_info)
                except Exception as e:
                    error_msg = f"序列化用户数据失败 - UserID: {user.id}, Username: {getattr(user, 'username', 'Unknown')}, Error: {str(e)}"
                    logger.warning(error_msg)
                    failed_users.append({'id': user.id, 'error': str(e)})
                    continue
                    
            logger.info(f"序列化完成 - 成功: {len(user_data)}条, 失败: {len(failed_users)}条")
            if failed_users:
                logger.warning(f"序列化失败的用户: {failed_users}")
                
        except Exception as e:
            error_msg = f"序列化过程异常: {str(e)}, 堆栈: {traceback.format_exc()}"
            logger.error(error_msg)
            return ApiResponse.error(message=f"数据序列化失败: {str(e)}", code=500)
                
        result = {
            'users': user_data,
            'pagination': {
                'current_page': page,
                'total_pages': paginator.num_pages,
                'total_count': paginator.count,
                'page_size': page_size,
                'has_next': users.has_next(),
                'has_previous': users.has_previous()
            },
            'debug_info': {
                'query_params': {
                    'page': page,
                    'page_size': page_size,
                    'search': search,
                    'user_type': user_type
                },
                'filter_applied': {
                    'search_filter': bool(search),
                    'type_filter': bool(user_type)
                },
                'serialization_stats': {
                    'success_count': len(user_data),
                    'failed_count': len(failed_users) if 'failed_users' in locals() else 0
                }
            }
        }
        
        logger.info(f"用户列表请求成功 - 返回{len(user_data)}条记录")
        return ApiResponse.success(result, message=f"成功获取用户列表，共{paginator.count}条记录")
        
    except PermissionError as e:
        error_msg = f"权限错误 - 用户: {request.user.username}, 错误: {str(e)}"
        logger.error(error_msg)
        return ApiResponse.error(message="权限不足，无法访问用户列表", code=403)
    except Exception as e:
        error_msg = f"用户列表请求异常 - 用户: {getattr(request, 'user', 'Unknown')}, 错误: {str(e)}, 堆栈: {traceback.format_exc()}"
        logger.error(error_msg)
        return ApiResponse.error(message=f"获取用户列表失败: {str(e)}", code=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def user_detail(request, user_id):
    """获取用户详情"""
    try:
        user = User.objects.get(id=user_id, user_type='user')
        
        data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'phone': getattr(user, 'phone', ''),
            'nickname': getattr(user.profile, 'nickname', '') if hasattr(user, 'profile') else '',
            'avatar': getattr(user.profile, 'avatar', '') if hasattr(user, 'profile') else '',
            'created_at': user.date_joined.isoformat(),
            'last_login_time': user.last_login.isoformat() if user.last_login else None,
            'status': 'active' if user.is_active else 'disabled'
        }
        
        return ApiResponse.success(data=data)
    except User.DoesNotExist:
        return ApiResponse.error(message="用户不存在")
    except Exception as e:
        return ApiResponse.error(message=f"获取用户详情失败: {str(e)}")

@api_view(['PATCH'])
@permission_classes([IsAuthenticated, IsAdminUser])
def update_user_status(request, user_id):
    """更新用户状态"""
    try:
        user = User.objects.get(id=user_id, user_type='user')
        status = request.data.get('status')
        
        if status == 'active':
            user.is_active = True
        elif status == 'disabled':
            user.is_active = False
        else:
            return ApiResponse.error(message="无效的状态值")
        
        user.save()
        return ApiResponse.success(message="状态更新成功")
    except User.DoesNotExist:
        return ApiResponse.error(message="用户不存在")
    except Exception as e:
        return ApiResponse.error(message=f"更新状态失败: {str(e)}")

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def reset_user_password(request, user_id):
    """重置用户密码"""
    try:
        user = User.objects.get(id=user_id, user_type='user')
        password = request.data.get('password')
        
        if not password:
            return ApiResponse.error(message="密码不能为空")
        
        user.password = make_password(password)
        user.save()
        
        return ApiResponse.success(message="密码重置成功")
    except User.DoesNotExist:
        return ApiResponse.error(message="用户不存在")
    except Exception as e:
        return ApiResponse.error(message=f"重置密码失败: {str(e)}")

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def user_orders(request, user_id):
    """获取用户订单"""
    try:
        user = User.objects.get(id=user_id, user_type='user')
        orders = Order.objects.filter(user=user).order_by('-created_at')[:10]
        
        orders_data = []
        for order in orders:
            orders_data.append({
                'id': order.order_number,
                'type': 'product',  # 可以根据订单类型调整
                'title': f'订单 {order.order_number}',
                'amount': float(order.total_amount),
                'status': order.status,
                'created_at': order.created_at.isoformat()
            })
        
        return ApiResponse.success(data={
            'results': orders_data,
            'count': len(orders_data)
        })
    except User.DoesNotExist:
        return ApiResponse.error(message="用户不存在")
    except Exception as e:
        return ApiResponse.error(message=f"获取用户订单失败: {str(e)}")