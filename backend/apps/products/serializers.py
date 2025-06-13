import json
from rest_framework import serializers
from .models import ProductCategory, Product, ProductGallery, Food, FoodGallery
from apps.villages.models import Village


class ProductCategorySerializer(serializers.ModelSerializer):
    """产品类别序列化器"""
    class Meta:
        model = ProductCategory
        fields = ['id', 'name', 'type', 'icon']


class ProductGallerySerializer(serializers.ModelSerializer):
    """特产图库序列化器"""
    class Meta:
        model = ProductGallery
        fields = ['id', 'image_url', 'caption', 'order']


class FoodGallerySerializer(serializers.ModelSerializer):
    """美食图库序列化器"""
    class Meta:
        model = FoodGallery
        fields = ['id', 'image_url', 'caption', 'order']


class ProductListSerializer(serializers.ModelSerializer):
    """特产列表序列化器"""
    village_name = serializers.SerializerMethodField()
    merchant_name = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    current_price = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'merchant_id', 'merchant_name', 'village_id', 'village_name',
                 'category_id', 'category_name', 'cover_image', 'intro', 'price', 
                 'discount_price', 'current_price', 'stock', 'sales', 'rating', 'is_featured']
    
    def get_village_name(self, obj):
        return obj.village.name if obj.village else None
    
    def get_merchant_name(self, obj):
        return obj.merchant.username if obj.merchant else None
    
    def get_category_name(self, obj):
        return obj.category.name if obj.category else None
    
    def get_current_price(self, obj):
        return obj.discount_price if obj.discount_price else obj.price


class ProductDetailSerializer(serializers.ModelSerializer):
    """特产详情序列化器"""
    village_name = serializers.SerializerMethodField()
    merchant_name = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    current_price = serializers.SerializerMethodField()
    gallery = ProductGallerySerializer(many=True, read_only=True)
    specs_data = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'merchant_id', 'merchant_name', 'village_id', 'village_name',
                 'category_id', 'category_name', 'cover_image', 'intro', 'description', 
                 'price', 'discount_price', 'current_price', 'stock', 'sales', 'rating', 
                 'is_featured', 'specs_data', 'views', 'gallery', 'created_at']
    
    def get_village_name(self, obj):
        return obj.village.name if obj.village else None
    
    def get_merchant_name(self, obj):
        return obj.merchant.username if obj.merchant else None
    
    def get_category_name(self, obj):
        return obj.category.name if obj.category else None
    
    def get_current_price(self, obj):
        return obj.discount_price if obj.discount_price else obj.price
    
    def get_specs_data(self, obj):
        if not obj.specs:
            return {}
        try:
            return json.loads(obj.specs)
        except:
            return {}


class FoodListSerializer(serializers.ModelSerializer):
    """美食列表序列化器"""
    village_name = serializers.SerializerMethodField()
    merchant_name = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    current_price = serializers.SerializerMethodField()
    
    class Meta:
        model = Food
        fields = ['id', 'name', 'merchant_id', 'merchant_name', 'village_id', 'village_name',
                 'category_id', 'category_name', 'cover_image', 'intro', 'price', 
                 'discount_price', 'current_price', 'rating', 'is_featured']
    
    def get_village_name(self, obj):
        return obj.village.name if obj.village else None
    
    def get_merchant_name(self, obj):
        return obj.merchant.username if obj.merchant else None
    
    def get_category_name(self, obj):
        return obj.category.name if obj.category else None
    
    def get_current_price(self, obj):
        return obj.discount_price if obj.discount_price else obj.price


class FoodDetailSerializer(serializers.ModelSerializer):
    """美食详情序列化器"""
    village_name = serializers.SerializerMethodField()
    merchant_name = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    current_price = serializers.SerializerMethodField()
    gallery = FoodGallerySerializer(many=True, read_only=True)
    
    class Meta:
        model = Food
        fields = ['id', 'name', 'merchant_id', 'merchant_name', 'village_id', 'village_name',
                 'category_id', 'category_name', 'cover_image', 'intro', 'description', 
                 'price', 'discount_price', 'current_price', 'rating', 'is_featured', 
                 'ingredients', 'views', 'gallery', 'created_at']
    
    def get_village_name(self, obj):
        return obj.village.name if obj.village else None
    
    def get_merchant_name(self, obj):
        return obj.merchant.username if obj.merchant else None
    
    def get_category_name(self, obj):
        return obj.category.name if obj.category else None
    
    def get_current_price(self, obj):
        return obj.discount_price if obj.discount_price else obj.price 