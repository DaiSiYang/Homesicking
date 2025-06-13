from django.utils import timezone
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.utils.response import ApiResponse
from apps.utils.pagination import StandardResultsSetPagination
from ..models import RoomType, RoomInventory
from ..serializers import RoomTypeListSerializer, RoomTypeDetailSerializer


class RoomTypeListView(ListAPIView):
    """
    房间类型列表视图
    """
    serializer_class = RoomTypeListSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        queryset = RoomType.objects.filter(status='active')
        
        # 根据民宿筛选
        homestay_id = self.request.query_params.get('homestay_id')
        if homestay_id:
            queryset = queryset.filter(homestay_id=homestay_id)
        else:
            # 如果未指定民宿，默认不返回结果
            return RoomType.objects.none()
        
        # 根据床型筛选
        bed_type = self.request.query_params.get('bed_type')
        if bed_type:
            queryset = queryset.filter(bed_type=bed_type)
        
        # 根据价格范围筛选
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=float(min_price))
        if max_price:
            queryset = queryset.filter(price__lte=float(max_price))
        
        # 根据人数筛选
        guests = self.request.query_params.get('guests')
        if guests:
            queryset = queryset.filter(max_guests__gte=int(guests))
        
        # 是否含早餐
        breakfast = self.request.query_params.get('breakfast')
        if breakfast:
            breakfast_value = breakfast.lower() == 'true'
            queryset = queryset.filter(breakfast=breakfast_value)
        
        # 排序
        sort_by = self.request.query_params.get('sort_by', 'price')
        sort_order = self.request.query_params.get('sort_order', 'asc')
        
        order_field = sort_by if sort_order == 'asc' else f'-{sort_by}'
        return queryset.order_by(order_field)
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        # 添加查询日期到上下文
        context = {'today': request.query_params.get('date', timezone.now().date())}
        
        if page is not None:
            serializer = self.get_serializer(page, many=True, context=context)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True, context=context)
        return ApiResponse(data=serializer.data)


class RoomTypeDetailView(RetrieveAPIView):
    """
    房间类型详情视图
    """
    queryset = RoomType.objects.filter(status='active')
    serializer_class = RoomTypeDetailSerializer
    permission_classes = [AllowAny]
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # 添加查询日期范围到上下文
        context = {
            'check_in': request.query_params.get('check_in'),
            'check_out': request.query_params.get('check_out')
        }
        
        serializer = self.get_serializer(instance, context=context)
        return ApiResponse(data=serializer.data)


class RoomAvailabilityView(APIView):
    """
    房间可用性查询视图
    """
    permission_classes = [AllowAny]
    
    def get(self, request, *args, **kwargs):
        room_id = request.query_params.get('room_id')
        check_in = request.query_params.get('check_in')
        check_out = request.query_params.get('check_out')
        
        if not room_id or not check_in or not check_out:
            return ApiResponse(code=400, message="缺少必要参数", data=None)
        
        try:
            room_type = RoomType.objects.get(id=room_id, status='active')
        except RoomType.DoesNotExist:
            return ApiResponse(code=404, message="房型不存在", data=None)
        
        # 查询日期范围内的库存
        inventories = RoomInventory.objects.filter(
            room_type_id=room_id,
            date__gte=check_in,
            date__lt=check_out
        ).order_by('date')
        
        # 检查是否所有日期都有库存记录
        if not inventories:
            return ApiResponse(data={
                "available": False,
                "message": "该日期范围内无可用房间",
                "inventory": []
            })
        
        # 检查是否所有日期都有足够库存
        available = all(inv.available > 0 for inv in inventories)
        
        # 计算总价
        total_price = sum(inv.current_price for inv in inventories)
        
        return ApiResponse(data={
            "available": available,
            "message": "可预订" if available else "部分日期无房",
            "total_price": total_price,
            "inventory": [
                {
                    "date": inv.date,
                    "available": inv.available,
                    "price": inv.current_price
                } for inv in inventories
            ]
        }) 