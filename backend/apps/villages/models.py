from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.regions.models import Region
from apps.users.models import User


class Village(models.Model):
    """
    乡村模型
    """
    STATUS_CHOICES = (
        ('pending', '待审核'),
        ('approved', '已通过'),
        ('rejected', '已拒绝'),
    )
    
    name = models.CharField(_('乡村名称'), max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='villages',
                              verbose_name=_('所属区域'))
    intro = models.TextField(_('简介'))
    description = models.TextField(_('详细描述'))
    cover_image = models.URLField(_('封面图URL'), max_length=255)
    location = models.CharField(_('地理位置'), max_length=100, help_text=_('格式：纬度,经度'))
    features = models.TextField(_('特色标签'), blank=True, help_text=_('JSON格式'))
    views = models.IntegerField(_('浏览量'), default=0)
    rating = models.DecimalField(_('平均评分'), max_digits=2, decimal_places=1, default=0)
    status = models.CharField(_('状态'), max_length=10, choices=STATUS_CHOICES, default='pending')
    is_recommended = models.BooleanField(_('是否推荐'), default=False)
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)
    
    class Meta:
        verbose_name = _('乡村')
        verbose_name_plural = _('乡村')
        ordering = ['-is_recommended', '-created_at']
    
    def __str__(self):
        return self.name


class VillageGallery(models.Model):
    """
    乡村图库
    """
    village = models.ForeignKey(Village, on_delete=models.CASCADE, related_name='gallery',
                               verbose_name=_('乡村'))
    image_url = models.URLField(_('图片URL'), max_length=255)
    caption = models.CharField(_('图片说明'), max_length=255, blank=True)
    order = models.IntegerField(_('排序'), default=0)
    
    class Meta:
        verbose_name = _('乡村图库')
        verbose_name_plural = _('乡村图库')
        ordering = ['order']
    
    def __str__(self):
        return f"{self.village.name}的图片-{self.id}"


class Attraction(models.Model):
    """
    景点模型
    """
    STATUS_CHOICES = (
        ('active', '启用'),
        ('inactive', '禁用'),
    )
    
    name = models.CharField(_('景点名称'), max_length=100)
    village = models.ForeignKey(Village, on_delete=models.CASCADE, related_name='attractions',
                               verbose_name=_('所属乡村'))
    intro = models.TextField(_('简介'))
    description = models.TextField(_('详细描述'))
    cover_image = models.URLField(_('封面图URL'), max_length=255)
    location = models.CharField(_('地理位置'), max_length=100, help_text=_('格式：纬度,经度'))
    opening_hours = models.CharField(_('开放时间'), max_length=255)
    ticket_price = models.DecimalField(_('票价'), max_digits=10, decimal_places=2, default=0)
    status = models.CharField(_('状态'), max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)
    
    class Meta:
        verbose_name = _('景点')
        verbose_name_plural = _('景点')
        ordering = ['village', '-created_at']
    
    def __str__(self):
        return self.name


class AttractionGallery(models.Model):
    """
    景点图库
    """
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE, related_name='gallery',
                                  verbose_name=_('景点'))
    image_url = models.URLField(_('图片URL'), max_length=255)
    caption = models.CharField(_('图片说明'), max_length=255, blank=True)
    order = models.IntegerField(_('排序'), default=0)
    
    class Meta:
        verbose_name = _('景点图库')
        verbose_name_plural = _('景点图库')
        ordering = ['order']
    
    def __str__(self):
        return f"{self.attraction.name}的图片-{self.id}" 