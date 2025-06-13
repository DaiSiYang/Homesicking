import json
from rest_framework import serializers
from django.db.models import Min
from .models import Homestay, HomestayGallery, RoomType, RoomGallery, RoomInventory
from apps.villages.models import Village
from apps.users.models import User


class HomestayGallerySerializer(serializers.ModelSerializer):
    """民宿图库序列化器"""
    class Meta:
        model = HomestayGallery
        fields = ['id', 'image_url', 'caption', 'order']


class RoomGallerySerializer(serializers.ModelSerializer):
    """房间图库序列化器"""
    class Meta:
        model = RoomGallery
        fields = ['id', 'image_url', 'caption', 'order']


class RoomTypeListSerializer(serializers.ModelSerializer):
    """房间类型列表序列化器"""
    current_price = serializers.SerializerMethodField()
    
    class Meta:
        model = RoomType
        fields = ['id', 'name', 'cover_image', 'area', 'price', 'discount_price', 
                 'current_price', 'bed_type', 'max_guests', 'breakfast']
    
    def get_current_price(self, obj):
        """获取当前可预订日期的最低价格"""
        # 假设当前日期为查询日期
        today = self.context.get('today')
        if not today:
            return obj.discount_price or obj.price
        
        # 查询当日库存的价格
        inventory = obj.inventory.filter(date=today).first()
        if inventory:
            return inventory.current_price
        
        return obj.discount_price or obj.price


class RoomTypeDetailSerializer(serializers.ModelSerializer):
    """房间类型详情序列化器"""
    gallery = RoomGallerySerializer(many=True, read_only=True)
    facilities = serializers.SerializerMethodField()
    inventory = serializers.SerializerMethodField()
    
    class Meta:
        model = RoomType
        fields = ['id', 'name', 'cover_image', 'area', 'price', 'discount_price', 
                 'bed_type', 'max_guests', 'room_count', 'description', 'facilities',
                 'breakfast', 'cancellation', 'gallery', 'inventory']
    
    def get_facilities(self, obj):
        if not obj.facilities:
            return []
        try:
            return json.loads(obj.facilities)
        except:
            return []
    
    def get_inventory(self, obj):
        """获取指定日期范围内的库存"""
        check_in = self.context.get('check_in')
        check_out = self.context.get('check_out')
        
        if not check_in or not check_out:
            return []
        
        inventories = obj.inventory.filter(date__gte=check_in, date__lt=check_out)
        return [
            {
                'date': inventory.date,
                'available': inventory.available,
                'price': inventory.current_price
            }
            for inventory in inventories
        ]


class HomestayListSerializer(serializers.ModelSerializer):
    """民宿列表序列化器"""
    village_name = serializers.SerializerMethodField()
    merchant_name = serializers.SerializerMethodField()
    features = serializers.SerializerMethodField()
    
    class Meta:
        model = Homestay
        fields = ['id', 'name', 'merchant_id', 'merchant_name', 'village_id', 'village_name',
                 'property_type', 'cover_image', 'intro', 'features', 'rating', 
                 'lowest_price', 'is_featured']
    
    def get_village_name(self, obj):
        return obj.village.name if obj.village else None
    
    def get_merchant_name(self, obj):
        return obj.merchant.username if obj.merchant else None
    
    def get_features(self, obj):
        if not obj.features:
            return []
        try:
            return json.loads(obj.features)
        except:
            return []


class HomestayDetailSerializer(serializers.ModelSerializer):
    """民宿详情序列化器"""
    village_name = serializers.SerializerMethodField()
    merchant_name = serializers.SerializerMethodField()
    features = serializers.SerializerMethodField()
    gallery = HomestayGallerySerializer(many=True, read_only=True)
    room_types = serializers.SerializerMethodField()
    location_obj = serializers.SerializerMethodField()
    
    class Meta:
        model = Homestay
        fields = ['id', 'name', 'merchant_id', 'merchant_name', 'village_id', 'village_name',
                 'property_type', 'address', 'location', 'location_obj', 'intro', 'description',
                 'cover_image', 'features', 'check_in_time', 'check_out_time', 'views', 
                 'rating', 'orders_count', 'lowest_price', 'is_featured', 'gallery', 
                 'room_types', 'created_at']
    
    def get_village_name(self, obj):
        return obj.village.name if obj.village else None
    
    def get_merchant_name(self, obj):
        return obj.merchant.username if obj.merchant else None
    
    def get_features(self, obj):
        if not obj.features:
            return []
        try:
            return json.loads(obj.features)
        except:
            return []
    
    def get_location_obj(self, obj):
        if not obj.location:
            return {"latitude": 0, "longitude": 0}
        try:
            lat, lng = obj.location.split(',')
            return {
                "latitude": float(lat),
                "longitude": float(lng)
            }
        except:
            return {"latitude": 0, "longitude": 0}
    
    def get_room_types(self, obj):
        """获取民宿的房型列表"""
        room_types = obj.room_types.filter(status='active')
        serializer = RoomTypeListSerializer(room_types, many=True, context=self.context)
        return serializer.data 