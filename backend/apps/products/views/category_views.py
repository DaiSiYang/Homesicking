from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from apps.utils.response import ApiResponse
from ..models import ProductCategory
from ..serializers import ProductCategorySerializer


class CategoryListView(ListAPIView):
    """
    产品类别列表视图
    """
    serializer_class = ProductCategorySerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = ProductCategory.objects.filter(is_active=True)
        
        # 根据类型筛选
        type_param = self.request.query_params.get('type')
        if type_param:
            queryset = queryset.filter(type=type_param)
        
        return queryset.order_by('order')
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return ApiResponse(data=serializer.data) 