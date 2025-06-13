from django.db import models
from django.utils.translation import gettext_lazy as _


class Region(models.Model):
    """
    区域模型：省市县三级
    """
    LEVEL_CHOICES = (
        ('province', '省'),
        ('city', '市'),
        ('county', '县/区'),
    )
    STATUS_CHOICES = (
        ('active', '启用'),
        ('inactive', '禁用'),
    )
    
    name = models.CharField(_('区域名称'), max_length=100)
    code = models.CharField(_('区域编码'), max_length=20, unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', 
                              null=True, blank=True, verbose_name=_('上级区域'))
    level = models.CharField(_('级别'), max_length=10, choices=LEVEL_CHOICES)
    is_hot = models.BooleanField(_('是否热门'), default=False)
    status = models.CharField(_('状态'), max_length=10, choices=STATUS_CHOICES, default='active')
    
    class Meta:
        verbose_name = _('区域')
        verbose_name_plural = _('区域')
        ordering = ['code']
    
    def __str__(self):
        return self.name
    
    @property
    def full_name(self):
        """获取完整地区名称，如"浙江省杭州市西湖区" """
        if not self.parent:
            return self.name
        
        if self.level == 'province':
            return self.name
        elif self.level == 'city':
            return f"{self.parent.name}{self.name}"
        elif self.level == 'county':
            return f"{self.parent.parent.name}{self.parent.name}{self.name}"
        return self.name 