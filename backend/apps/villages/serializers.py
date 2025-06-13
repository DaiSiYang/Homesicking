import json
from rest_framework import serializers
from .models import Village, VillageGallery, Attraction, AttractionGallery
from apps.regions.models import Region


class VillageGallerySerializer(serializers.ModelSerializer):
    """乡村图库序列化器"""
    class Meta:
        model = VillageGallery
        fields = ['id', 'image_url', 'caption', 'order']


class AttractionGallerySerializer(serializers.ModelSerializer):
    """景点图库序列化器"""
    class Meta:
        model = AttractionGallery
        fields = ['id', 'image_url', 'caption', 'order']


class VillageListSerializer(serializers.ModelSerializer):
    """乡村列表序列化器"""
    region_name = serializers.SerializerMethodField()
    features = serializers.SerializerMethodField()
    
    class Meta:
        model = Village
        fields = ['id', 'name', 'region_id', 'region_name', 'cover_image', 'intro', 
                 'features', 'rating', 'is_recommended']
    
    def get_region_name(self, obj):
        return obj.region.name if obj.region else None
    
    def get_features(self, obj):
        if not obj.features:
            return []
        try:
            return json.loads(obj.features)
        except:
            return []


class VillageDetailSerializer(serializers.ModelSerializer):
    """乡村详情序列化器"""
    region_name = serializers.SerializerMethodField()
    region_full_name = serializers.SerializerMethodField()
    features = serializers.SerializerMethodField()
    gallery = VillageGallerySerializer(many=True, read_only=True)
    location_obj = serializers.SerializerMethodField()
    
    class Meta:
        model = Village
        fields = ['id', 'name', 'region_id', 'region_name', 'region_full_name', 'intro', 
                 'description', 'cover_image', 'location', 'location_obj', 'features', 
                 'views', 'rating', 'is_recommended', 'gallery', 'created_at']
    
    def get_region_name(self, obj):
        return obj.region.name if obj.region else None
    
    def get_region_full_name(self, obj):
        if not obj.region:
            return None
        return obj.region.full_name
    
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


class AttractionListSerializer(serializers.ModelSerializer):
    """景点列表序列化器"""
    village_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Attraction
        fields = ['id', 'name', 'village_id', 'village_name', 'cover_image', 
                 'intro', 'ticket_price', 'opening_hours']
    
    def get_village_name(self, obj):
        return obj.village.name if obj.village else None


class AttractionDetailSerializer(serializers.ModelSerializer):
    """景点详情序列化器"""
    village_name = serializers.SerializerMethodField()
    gallery = AttractionGallerySerializer(many=True, read_only=True)
    location_obj = serializers.SerializerMethodField()
    
    class Meta:
        model = Attraction
        fields = ['id', 'name', 'village_id', 'village_name', 'intro', 'description', 
                 'cover_image', 'location', 'location_obj', 'opening_hours', 
                 'ticket_price', 'gallery', 'created_at']
    
    def get_village_name(self, obj):
        return obj.village.name if obj.village else None
    
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