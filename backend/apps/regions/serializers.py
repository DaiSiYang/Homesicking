from rest_framework import serializers
from .models import Region


class RegionSerializer(serializers.ModelSerializer):
    """区域序列化器"""
    class Meta:
        model = Region
        fields = ['id', 'name', 'code', 'level', 'parent_id', 'is_hot']


class RegionDetailSerializer(serializers.ModelSerializer):
    """区域详情序列化器"""
    parent_name = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()
    
    class Meta:
        model = Region
        fields = ['id', 'name', 'code', 'level', 'parent_id', 'parent_name', 'is_hot', 'children']
    
    def get_parent_name(self, obj):
        """获取父级区域名称"""
        return obj.parent.name if obj.parent else None
    
    def get_children(self, obj):
        """获取子区域列表"""
        children = obj.children.filter(status='active')
        return RegionSerializer(children, many=True).data 