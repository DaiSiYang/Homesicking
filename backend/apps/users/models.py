from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    用户模型
    """
    USER_TYPE_CHOICES = (
        ('tourist', '游客'),
        ('merchant', '商户'),
        ('admin', '管理员'),
    )
    
    phone = models.CharField(_('手机号码'), max_length=20, blank=True)
    avatar = models.URLField(_('头像URL'), max_length=255, blank=True)
    bio = models.TextField(_('个人简介'), blank=True)
    user_type = models.CharField(_('用户类型'), max_length=10, choices=USER_TYPE_CHOICES, default='tourist')
    is_verified = models.BooleanField(_('是否通过验证'), default=False)
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)
    
    class Meta:
        verbose_name = _('用户')
        verbose_name_plural = _('用户')
        ordering = ['-id']
    
    def __str__(self):
        return self.username


class UserProfile(models.Model):
    """
    用户资料
    """
    GENDER_CHOICES = (
        ('male', '男'),
        ('female', '女'),
        ('other', '其他'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name=_('用户'))
    real_name = models.CharField(_('真实姓名'), max_length=50, blank=True)
    id_card = models.CharField(_('身份证号'), max_length=50, blank=True)
    gender = models.CharField(_('性别'), max_length=10, choices=GENDER_CHOICES, default='other')
    birthday = models.DateField(_('生日'), null=True, blank=True)
    address = models.CharField(_('地址'), max_length=255, blank=True)
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)
    
    class Meta:
        verbose_name = _('用户资料')
        verbose_name_plural = _('用户资料')
    
    def __str__(self):
        return f"{self.user.username}的资料"


class MerchantProfile(models.Model):
    """
    商户资料
    """
    STATUS_CHOICES = (
        ('pending', '待审核'),
        ('approved', '已通过'),
        ('rejected', '已拒绝'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='merchant_profile', verbose_name=_('用户'))
    business_name = models.CharField(_('商户名称'), max_length=100)
    business_license = models.URLField(_('营业执照图片URL'), max_length=255)
    contact_person = models.CharField(_('联系人'), max_length=50)
    contact_phone = models.CharField(_('联系电话'), max_length=20)
    address = models.CharField(_('商户地址'), max_length=255)
    description = models.TextField(_('商户描述'), blank=True)
    status = models.CharField(_('状态'), max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)
    
    class Meta:
        verbose_name = _('商户资料')
        verbose_name_plural = _('商户资料')
    
    def __str__(self):
        return self.business_name


class Favorite(models.Model):
    """
    收藏
    """
    TARGET_TYPE_CHOICES = (
        ('village', '乡村'),
        ('homestay', '民宿'),
        ('product', '农产品'),
        ('food', '美食'),
        ('travel_note', '游记'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites', verbose_name=_('用户'))
    target_type = models.CharField(_('目标类型'), max_length=20, choices=TARGET_TYPE_CHOICES)
    target_id = models.IntegerField(_('目标ID'))
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('收藏')
        verbose_name_plural = _('收藏')
        unique_together = ('user', 'target_type', 'target_id')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username}收藏的{self.get_target_type_display()}" 