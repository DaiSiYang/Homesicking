from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.villages.models import Village
from apps.users.models import User


class ProductCategory(models.Model):
    """
    产品类别模型
    """
    TYPE_CHOICES = (
        ('product', '特产'),
        ('food', '美食'),
    )
    
    name = models.CharField(_('类别名称'), max_length=50)
    type = models.CharField(_('类型'), max_length=10, choices=TYPE_CHOICES)
    icon = models.URLField(_('图标URL'), max_length=255, blank=True)
    order = models.IntegerField(_('排序'), default=0)
    is_active = models.BooleanField(_('是否启用'), default=True)
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('产品类别')
        verbose_name_plural = _('产品类别')
        ordering = ['order']
    
    def __str__(self):
        return self.name


class Product(models.Model):
    """
    特产模型
    """
    STATUS_CHOICES = (
        ('pending', '待审核'),
        ('approved', '已通过'),
        ('rejected', '已拒绝'),
    )
    
    name = models.CharField(_('特产名称'), max_length=100)
    merchant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products',
                                verbose_name=_('所属商户'))
    village = models.ForeignKey(Village, on_delete=models.CASCADE, related_name='products',
                               verbose_name=_('所属乡村'))
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, related_name='products',
                                null=True, blank=True, verbose_name=_('所属类别'))
    cover_image = models.URLField(_('封面图URL'), max_length=255)
    intro = models.TextField(_('简介'))
    description = models.TextField(_('详细描述'))
    price = models.DecimalField(_('价格'), max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(_('优惠价'), max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.IntegerField(_('库存'), default=0)
    sales = models.IntegerField(_('销量'), default=0)
    rating = models.DecimalField(_('平均评分'), max_digits=2, decimal_places=1, default=0)
    is_featured = models.BooleanField(_('是否推荐'), default=False)
    specs = models.TextField(_('规格参数'), blank=True, help_text=_('JSON格式'))
    status = models.CharField(_('状态'), max_length=10, choices=STATUS_CHOICES, default='pending')
    views = models.IntegerField(_('浏览量'), default=0)
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)
    
    class Meta:
        verbose_name = _('特产')
        verbose_name_plural = _('特产')
        ordering = ['-is_featured', '-created_at']
    
    def __str__(self):
        return self.name


class ProductGallery(models.Model):
    """
    特产图库
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='gallery',
                               verbose_name=_('特产'))
    image_url = models.URLField(_('图片URL'), max_length=255)
    caption = models.CharField(_('图片说明'), max_length=255, blank=True)
    order = models.IntegerField(_('排序'), default=0)
    
    class Meta:
        verbose_name = _('特产图库')
        verbose_name_plural = _('特产图库')
        ordering = ['order']
    
    def __str__(self):
        return f"{self.product.name}的图片-{self.id}"


class Food(models.Model):
    """
    美食模型
    """
    STATUS_CHOICES = (
        ('pending', '待审核'),
        ('approved', '已通过'),
        ('rejected', '已拒绝'),
    )
    
    name = models.CharField(_('美食名称'), max_length=100)
    merchant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='foods',
                                verbose_name=_('所属商户'))
    village = models.ForeignKey(Village, on_delete=models.CASCADE, related_name='foods',
                               verbose_name=_('所属乡村'))
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, related_name='foods',
                                null=True, blank=True, verbose_name=_('所属类别'))
    cover_image = models.URLField(_('封面图URL'), max_length=255)
    intro = models.TextField(_('简介'))
    description = models.TextField(_('详细描述'))
    price = models.DecimalField(_('价格'), max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(_('优惠价'), max_digits=10, decimal_places=2, null=True, blank=True)
    rating = models.DecimalField(_('平均评分'), max_digits=2, decimal_places=1, default=0)
    is_featured = models.BooleanField(_('是否推荐'), default=False)
    ingredients = models.TextField(_('食材配料'), blank=True)
    status = models.CharField(_('状态'), max_length=10, choices=STATUS_CHOICES, default='pending')
    views = models.IntegerField(_('浏览量'), default=0)
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)
    
    class Meta:
        verbose_name = _('美食')
        verbose_name_plural = _('美食')
        ordering = ['-is_featured', '-created_at']
    
    def __str__(self):
        return self.name


class FoodGallery(models.Model):
    """
    美食图库
    """
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='gallery',
                            verbose_name=_('美食'))
    image_url = models.URLField(_('图片URL'), max_length=255)
    caption = models.CharField(_('图片说明'), max_length=255, blank=True)
    order = models.IntegerField(_('排序'), default=0)
    
    class Meta:
        verbose_name = _('美食图库')
        verbose_name_plural = _('美食图库')
        ordering = ['order']
    
    def __str__(self):
        return f"{self.food.name}的图片-{self.id}" 