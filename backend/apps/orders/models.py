from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.users.models import User
from apps.products.models import Product, Food
from apps.homestays.models import RoomType


class CartItem(models.Model):
    """
    购物车项模型
    """
    TYPE_CHOICES = (
        ('product', '特产'),
        ('food', '美食'),
        ('room', '房间'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items',
                            verbose_name=_('用户'))
    item_type = models.CharField(_('商品类型'), max_length=10, choices=TYPE_CHOICES)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True,
                               related_name='cart_items', verbose_name=_('特产'))
    food = models.ForeignKey(Food, on_delete=models.CASCADE, null=True, blank=True,
                            related_name='cart_items', verbose_name=_('美食'))
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, null=True, blank=True,
                                 related_name='cart_items', verbose_name=_('房型'))
    quantity = models.IntegerField(_('数量'), default=1)
    check_in_date = models.DateField(_('入住日期'), null=True, blank=True)
    check_out_date = models.DateField(_('退房日期'), null=True, blank=True)
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)
    
    class Meta:
        verbose_name = _('购物车项')
        verbose_name_plural = _('购物车项')
        ordering = ['-created_at']
        unique_together = [
            ('user', 'item_type', 'product'),
            ('user', 'item_type', 'food'),
            ('user', 'item_type', 'room_type', 'check_in_date', 'check_out_date'),
        ]
    
    def __str__(self):
        if self.item_type == 'product' and self.product:
            return f"{self.user.username}的购物车-{self.product.name}"
        elif self.item_type == 'food' and self.food:
            return f"{self.user.username}的购物车-{self.food.name}"
        elif self.item_type == 'room' and self.room_type:
            return f"{self.user.username}的购物车-{self.room_type.name}"
        return f"{self.user.username}的购物车项-{self.id}"


class Order(models.Model):
    """
    订单模型
    """
    STATUS_CHOICES = (
        ('pending_payment', '待支付'),
        ('paid', '已支付'),
        ('confirmed', '已确认'),
        ('canceled', '已取消'),
        ('refunding', '退款中'),
        ('refunded', '已退款'),
        ('completed', '已完成'),
    )
    
    TYPE_CHOICES = (
        ('product', '特产'),
        ('food', '美食'),
        ('room', '住宿'),
    )
    
    order_no = models.CharField(_('订单号'), max_length=50, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders',
                            verbose_name=_('用户'))
    merchant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='merchant_orders',
                                verbose_name=_('商户'))
    order_type = models.CharField(_('订单类型'), max_length=10, choices=TYPE_CHOICES)
    total_amount = models.DecimalField(_('总金额'), max_digits=10, decimal_places=2)
    payment_amount = models.DecimalField(_('支付金额'), max_digits=10, decimal_places=2)
    status = models.CharField(_('状态'), max_length=20, choices=STATUS_CHOICES, default='pending_payment')
    contact_name = models.CharField(_('联系人'), max_length=50)
    contact_phone = models.CharField(_('联系电话'), max_length=20)
    contact_email = models.EmailField(_('联系邮箱'), blank=True)
    remark = models.TextField(_('备注'), blank=True)
    paid_at = models.DateTimeField(_('支付时间'), null=True, blank=True)
    canceled_at = models.DateTimeField(_('取消时间'), null=True, blank=True)
    refunded_at = models.DateTimeField(_('退款时间'), null=True, blank=True)
    completed_at = models.DateTimeField(_('完成时间'), null=True, blank=True)
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)
    
    class Meta:
        verbose_name = _('订单')
        verbose_name_plural = _('订单')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username}的订单-{self.order_no}"


class OrderItem(models.Model):
    """
    订单项模型
    """
    TYPE_CHOICES = (
        ('product', '特产'),
        ('food', '美食'),
        ('room', '房间'),
    )
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items',
                             verbose_name=_('订单'))
    item_type = models.CharField(_('商品类型'), max_length=10, choices=TYPE_CHOICES)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name='order_items', verbose_name=_('特产'))
    food = models.ForeignKey(Food, on_delete=models.SET_NULL, null=True, blank=True,
                            related_name='order_items', verbose_name=_('美食'))
    room_type = models.ForeignKey(RoomType, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='order_items', verbose_name=_('房型'))
    name = models.CharField(_('商品名称'), max_length=100)
    image = models.URLField(_('商品图片'), max_length=255)
    price = models.DecimalField(_('价格'), max_digits=10, decimal_places=2)
    quantity = models.IntegerField(_('数量'), default=1)
    amount = models.DecimalField(_('金额'), max_digits=10, decimal_places=2)
    check_in_date = models.DateField(_('入住日期'), null=True, blank=True)
    check_out_date = models.DateField(_('退房日期'), null=True, blank=True)
    days = models.IntegerField(_('天数'), default=1)
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('订单项')
        verbose_name_plural = _('订单项')
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.order.order_no}-{self.name}"


class Payment(models.Model):
    """
    支付记录模型
    """
    PAYMENT_METHOD_CHOICES = (
        ('alipay', '支付宝'),
        ('wechat', '微信支付'),
        ('bank', '银行转账'),
    )
    
    STATUS_CHOICES = (
        ('pending', '待处理'),
        ('success', '成功'),
        ('failed', '失败'),
    )
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments',
                             verbose_name=_('订单'))
    payment_no = models.CharField(_('支付流水号'), max_length=100, unique=True)
    payment_method = models.CharField(_('支付方式'), max_length=20, choices=PAYMENT_METHOD_CHOICES)
    amount = models.DecimalField(_('支付金额'), max_digits=10, decimal_places=2)
    status = models.CharField(_('状态'), max_length=10, choices=STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(_('交易号'), max_length=100, blank=True)
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)
    
    class Meta:
        verbose_name = _('支付记录')
        verbose_name_plural = _('支付记录')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.order.order_no}的支付-{self.payment_no}"


class Refund(models.Model):
    """
    退款记录模型
    """
    REFUND_REASON_CHOICES = (
        ('customer_request', '客户申请'),
        ('out_of_stock', '缺货'),
        ('quality_issue', '质量问题'),
        ('other', '其他'),
    )
    
    STATUS_CHOICES = (
        ('pending', '待处理'),
        ('approved', '已批准'),
        ('rejected', '已拒绝'),
        ('processing', '处理中'),
        ('completed', '已完成'),
    )
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='refunds',
                             verbose_name=_('订单'))
    refund_no = models.CharField(_('退款流水号'), max_length=100, unique=True)
    amount = models.DecimalField(_('退款金额'), max_digits=10, decimal_places=2)
    reason = models.CharField(_('退款原因'), max_length=20, choices=REFUND_REASON_CHOICES)
    reason_detail = models.TextField(_('详细原因'), blank=True)
    status = models.CharField(_('状态'), max_length=10, choices=STATUS_CHOICES, default='pending')
    merchant_remark = models.TextField(_('商户备注'), blank=True)
    refund_time = models.DateTimeField(_('退款时间'), null=True, blank=True)
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)
    
    class Meta:
        verbose_name = _('退款记录')
        verbose_name_plural = _('退款记录')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.order.order_no}的退款-{self.refund_no}"