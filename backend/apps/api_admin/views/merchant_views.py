from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from rest_framework.decorators import api_view
from apps.users.models import User
from apps.utils.response import ApiResponse
import json

@api_view(['GET'])
def merchant_list(request):
    """获取商户列表"""
    try:
        # 获取查询参数
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        search = request.GET.get('search', '')
        status = request.GET.get('status', '')
        
        # 查询商户用户（user_type='merchant'）
        merchants = User.objects.filter(user_type='merchant')
        
        # 搜索过滤
        if search:
            merchants = merchants.filter(
                username__icontains=search
            )
        
        # 状态过滤（如果有相关字段）
        if status:
            # 根据实际的状态字段进行过滤
            pass
        
        # 分页
        paginator = Paginator(merchants, page_size)
        page_obj = paginator.get_page(page)
        
        # 构造响应数据
        results = []
        for merchant in page_obj:
            results.append({
                'id': merchant.id,
                'name': merchant.username,  # 或其他名称字段
                'contact_person': merchant.username,
                'contact_phone': merchant.phone or '',
                'email': merchant.email,
                'address': '',  # 根据实际字段调整
                'status': 'approved',  # 根据实际状态字段调整
                'created_at': merchant.date_joined.strftime('%Y-%m-%d %H:%M:%S'),
                'logo': ''  # 根据实际字段调整
            })
        
        return ApiResponse.success({
            'results': results,
            'count': paginator.count,
            'page': page,
            'page_size': page_size
        })
        
    except Exception as e:
        return ApiResponse.error(f"获取商户列表失败: {str(e)}")

@api_view(['GET'])
def merchant_detail(request, merchant_id):
    """获取商户详情"""
    try:
        merchant = User.objects.get(id=merchant_id, user_type='merchant')
        data = {
            'id': merchant.id,
            'name': merchant.username,
            'contact_person': merchant.username,
            'contact_phone': merchant.phone or '',
            'email': merchant.email,
            'address': '',
            'status': 'approved',
            'created_at': merchant.date_joined.strftime('%Y-%m-%d %H:%M:%S'),
            'logo': ''
        }
        return ApiResponse.success(data)
    except User.DoesNotExist:
        return ApiResponse.error("商户不存在", code=404)
    except Exception as e:
        return ApiResponse.error(f"获取商户详情失败: {str(e)}")

@api_view(['POST'])
def review_merchant(request, merchant_id):
    """审核商户"""
    try:
        data = json.loads(request.body)
        action = data.get('action')
        
        merchant = User.objects.get(id=merchant_id, user_type='merchant')
        # 根据实际需求更新商户状态
        # merchant.status = action
        # merchant.save()
        
        return ApiResponse.success("审核成功")
    except User.DoesNotExist:
        return ApiResponse.error("商户不存在", code=404)
    except Exception as e:
        return ApiResponse.error(f"审核失败: {str(e)}")

@api_view(['PATCH'])
def update_merchant_status(request, merchant_id):
    """更新商户状态"""
    try:
        data = json.loads(request.body)
        status = data.get('status')
        
        merchant = User.objects.get(id=merchant_id, user_type='merchant')
        # 根据实际需求更新商户状态
        # merchant.status = status
        # merchant.save()
        
        return ApiResponse.success("状态更新成功")
    except User.DoesNotExist:
        return ApiResponse.error("商户不存在", code=404)
    except Exception as e:
        return ApiResponse.error(f"状态更新失败: {str(e)}")

@api_view(['GET'])
def merchant_products(request, merchant_id):
    """获取商户产品列表"""
    try:
        # 根据实际的产品模型实现
        return ApiResponse.success({
            'results': [],
            'count': 0
        })
    except Exception as e:
        return ApiResponse.error(f"获取商户产品失败: {str(e)}")