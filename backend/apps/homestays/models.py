from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.villages.models import Village
from apps.users.models import User


class Homestay(models.Model):
    """
    民宿模型
    """
    STATUS_CHOICES = (
        ('pending', '待审核'),
        ('approved', '已通过'),
        ('rejected', '已拒绝'),
    )
    
    PROPERTY_TYPE_CHOICES = (
        ('house', '独栋房屋'),
        ('apartment', '公寓'),
        ('farm', '农场'),
        ('guesthouse', '客栈'),
    )
    
    name = models.CharField(_('民宿名称'), max_length=100)
    merchant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='homestays',
                                verbose_name=_('所属商户'))
    village = models.ForeignKey(Village, on_delete=models.CASCADE, related_name='homestays',
                               verbose_name=_('所属乡村'))
    property_type = models.CharField(_('物业类型'), max_length=20, choices=PROPERTY_TYPE_CHOICES)
    address = models.CharField(_('详细地址'), max_length=255)
    location = models.CharField(_('地理位置'), max_length=100, help_text=_('格式：纬度,经度'))
    intro = models.TextField(_('简介'))
    description = models.TextField(_('详细描述'))
    cover_image = models.URLField(_('封面图URL'), max_length=255)
    views = models.IntegerField(_('浏览量'), default=0)
    rating = models.DecimalField(_('平均评分'), max_digits=2, decimal_places=1, default=0)
    orders_count = models.IntegerField(_('订单数'), default=0)
    lowest_price = models.DecimalField(_('最低价格'), max_digits=10, decimal_places=2, default=0)
    features = models.TextField(_('设施特色'), blank=True, help_text=_('JSON格式'))
    check_in_time = models.CharField(_('入住时间'), max_length=50, default='14:00')
    check_out_time = models.CharField(_('退房时间'), max_length=50, default='12:00')
    status = models.CharField(_('状态'), max_length=10, choices=STATUS_CHOICES, default='pending')
    is_featured = models.BooleanField(_('是否特色'), default=False)
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)
    
    class Meta:
        verbose_name = _('民宿')
        verbose_name_plural = _('民宿')
        ordering = ['-is_featured', '-created_at']
    
    def __str__(self):
        return self.name


class HomestayGallery(models.Model):
    """
    民宿图库
    """
    homestay = models.ForeignKey(Homestay, on_delete=models.CASCADE, related_name='gallery',
                                verbose_name=_('民宿'))
    image_url = models.URLField(_('图片URL'), max_length=255)
    caption = models.CharField(_('图片说明'), max_length=255, blank=True)
    order = models.IntegerField(_('排序'), default=0)
    
    class Meta:
        verbose_name = _('民宿图库')
        verbose_name_plural = _('民宿图库')
        ordering = ['order']
    
    def __str__(self):
        return f"{self.homestay.name}的图片-{self.id}"


class RoomType(models.Model):
    """
    房间类型模型
    """
    STATUS_CHOICES = (
        ('active', '上架'),
        ('inactive', '下架'),
    )
    
    BED_TYPE_CHOICES = (
        ('single', '单人床'),
        ('double', '双人床'),
        ('queen', '大床'),
        ('king', '特大床'),
        ('bunk', '上下铺'),
        ('sofa', '沙发床'),
    )
    
    homestay = models.ForeignKey(Homestay, on_delete=models.CASCADE, related_name='room_types',
                                verbose_name=_('所属民宿'))
    name = models.CharField(_('房型名称'), max_length=100)
    cover_image = models.URLField(_('封面图URL'), max_length=255)
    area = models.IntegerField(_('面积(㎡)'))
    price = models.DecimalField(_('价格'), max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(_('优惠价'), max_digits=10, decimal_places=2, null=True, blank=True)
    bed_type = models.CharField(_('床型'), max_length=20, choices=BED_TYPE_CHOICES)
    max_guests = models.IntegerField(_('最大入住人数'))
    room_count = models.IntegerField(_('房间数量'))
    description = models.TextField(_('房型描述'))
    facilities = models.TextField(_('设施'), blank=True, help_text=_('JSON格式'))
    breakfast = models.BooleanField(_('含早餐'), default=False)
    cancellation = models.CharField(_('取消政策'), max_length=255, blank=True)
    status = models.CharField(_('状态'), max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)
    
    class Meta:
        verbose_name = _('房间类型')
        verbose_name_plural = _('房间类型')
        ordering = ['price']
    
    def __str__(self):
        return f"{self.homestay.name}-{self.name}"


class RoomGallery(models.Model):
    """
    房间图库
    """
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name='gallery',
                                 verbose_name=_('房型'))
    image_url = models.URLField(_('图片URL'), max_length=255)
    caption = models.CharField(_('图片说明'), max_length=255, blank=True)
    order = models.IntegerField(_('排序'), default=0)
    
    class Meta:
        verbose_name = _('房间图库')
        verbose_name_plural = _('房间图库')
        ordering = ['order']
    
    def __str__(self):
        return f"{self.room_type.name}的图片-{self.id}"


class RoomInventory(models.Model):
    """
    房间库存模型
    """
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name='inventory',
                                 verbose_name=_('房型'))
    date = models.DateField(_('日期'))
    available = models.IntegerField(_('可用数量'))
    original_price = models.DecimalField(_('原价'), max_digits=10, decimal_places=2)
    current_price = models.DecimalField(_('当前价格'), max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)
    
    class Meta:
        verbose_name = _('房间库存')
        verbose_name_plural = _('房间库存')
        ordering = ['date']
        unique_together = ['room_type', 'date']
    
    def __str__(self):
        return f"{self.room_type.name}-{self.date}" 