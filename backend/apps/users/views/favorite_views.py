from rest_framework.generics import ListCreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.utils.translation import gettext_lazy as _

from apps.utils.response import ApiResponse
from apps.utils.pagination import StandardResultsSetPagination
from ..models import Favorite
from ..serializers import FavoriteSerializer


class FavoriteListCreateView(ListCreateAPIView):
    """
    收藏列表和创建
    """
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        queryset = Favorite.objects.filter(user=self.request.user)
        
        # 筛选收藏类型
        target_type = self.request.query_params.get('type')
        if target_type:
            queryset = queryset.filter(target_type=target_type)
            
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return ApiResponse(data=serializer.data)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return ApiResponse(
            message=_("收藏成功"),
            data=serializer.data
        )
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FavoriteDeleteView(DestroyAPIView):
    """
    取消收藏
    """
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'
    
    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        
        return ApiResponse(
            message=_("取消收藏成功")
        ) 