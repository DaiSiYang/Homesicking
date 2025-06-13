<template>
  <div class="page-container py-8">
    <div class="mb-6 flex items-center">
      <el-button link class="mr-2" @click="$router.push('/orders')">
        <el-icon><ArrowLeft /></el-icon>
      </el-button>
      <h1 class="text-2xl font-bold text-gray-800">订单详情</h1>
    </div>

    <el-skeleton :loading="orderStore.loading" animated>
      <template #default>
        <div v-if="!order" class="card p-10 text-center">
          <el-empty description="订单不存在或已被删除">
            <el-button type="primary" @click="$router.push('/orders')">返回订单列表</el-button>
          </el-empty>
        </div>
        
        <template v-else>
          <!-- 订单状态卡片 -->
          <div class="card mb-6 p-6">
            <div class="flex justify-between items-center">
              <div class="flex-1">
                <h2 class="text-lg font-bold mb-2">订单状态：
                  <span :class="getOrderStatusClass(order.status)">
                    {{ orderStore.orderStatusMap[order.status] }}
                  </span>
                </h2>
                <p class="text-gray-500">
                  订单编号：{{ order.order_no }}
                  <span class="mx-4">|</span>
                  下单时间：{{ formatDateTime(order.created_at) }}
                </p>
              </div>
              <div class="flex items-center space-x-3">
                <!-- 根据订单状态显示不同按钮 -->
                <template v-if="order.status === 'pending_payment'">
                  <el-button type="primary" @click="goToPayment(order.id)">去支付</el-button>
                  <el-button type="danger" @click="cancelOrder(order.id)">取消订单</el-button>
                </template>
                
                <template v-else-if="order.status === 'paid' || order.status === 'confirmed'">
                  <el-button type="warning" @click="applyRefund(order.id)">申请退款</el-button>
                </template>
                
                <template v-else-if="order.status === 'completed'">
                  <el-button type="success">评价</el-button>
                </template>
              </div>
            </div>
          </div>
          
          <!-- 订单进度 -->
          <div class="card mb-6 p-6">
            <el-steps :active="getOrderStepActive(order.status)" finish-status="success" align-center>
              <el-step title="提交订单" :description="formatDate(order.created_at)" />
              <el-step title="支付订单" :description="order.payment_time ? formatDate(order.payment_time) : '待支付'" />
              <el-step title="确认订单" :description="order.confirm_time ? formatDate(order.confirm_time) : '待确认'" />
              <el-step title="订单完成" :description="order.complete_time ? formatDate(order.complete_time) : '进行中'" />
            </el-steps>
          </div>
          
          <!-- 收货人信息 -->
          <div class="card mb-6 p-6">
            <h2 class="text-lg font-bold mb-4">联系人信息</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <p class="text-gray-600 mb-2">联系人：<span class="text-gray-800">{{ order.contact_name }}</span></p>
                <p class="text-gray-600 mb-2">联系电话：<span class="text-gray-800">{{ order.contact_phone }}</span></p>
              </div>
              <div>
                <p class="text-gray-600 mb-2">联系邮箱：<span class="text-gray-800">{{ order.contact_email || '无' }}</span></p>
                <p class="text-gray-600 mb-2">备注：<span class="text-gray-800">{{ order.remark || '无' }}</span></p>
              </div>
            </div>
          </div>
          
          <!-- 订单商品 -->
          <div class="card mb-6">
            <div class="flex bg-gray-50 py-3 px-6 rounded-t-lg font-medium text-gray-600">
              <div class="flex-1">商品信息</div>
              <div class="w-32 text-center">单价</div>
              <div class="w-32 text-center">数量</div>
              <div class="w-32 text-center">小计</div>
            </div>
            
            <!-- 商品列表 -->
            <div v-for="item in order.items" :key="item.id" class="border-b last:border-0 py-4 px-6">
              <div class="flex items-center">
                <div class="flex-1">
                  <!-- 商品信息 -->
                  <div class="flex">
                    <img :src="item.image" alt="商品图片" class="w-20 h-20 object-cover rounded mr-4">
                    <div>
                      <h3 class="text-base font-medium text-gray-800 mb-2">{{ item.name }}</h3>
                      <p class="text-sm text-gray-500">
                        {{ getItemTypeText(item.item_type) }}
                        <span v-if="item.item_type === 'room' && item.check_in_date && item.check_out_date">
                          · {{ formatDate(item.check_in_date) }} 至 {{ formatDate(item.check_out_date) }}
                        </span>
                      </p>
                    </div>
                  </div>
                </div>
                <div class="w-32 text-center">
                  <span class="text-red-600 font-medium">¥{{ item.price.toFixed(2) }}</span>
                </div>
                <div class="w-32 text-center">
                  <span>× {{ item.quantity }}</span>
                </div>
                <div class="w-32 text-center">
                  <span class="text-red-600 font-medium">¥{{ item.amount.toFixed(2) }}</span>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 订单汇总 -->
          <div class="card mb-6 p-6">
            <div class="flex justify-end">
              <div class="w-72">
                <div class="flex justify-between py-2">
                  <span class="text-gray-600">商品总额：</span>
                  <span class="text-gray-800">¥{{ order.total_amount.toFixed(2) }}</span>
                </div>
                <div class="flex justify-between py-2">
                  <span class="text-gray-600">配送费：</span>
                  <span class="text-gray-800">¥0.00</span>
                </div>
                <div class="flex justify-between py-2">
                  <span class="text-gray-600">优惠金额：</span>
                  <span class="text-gray-800">-¥{{ order.discount_amount ? order.discount_amount.toFixed(2) : '0.00' }}</span>
                </div>
                <div class="flex justify-between py-2 border-t border-gray-200 mt-2 pt-2">
                  <span class="text-gray-800 font-medium">实付金额：</span>
                  <span class="text-red-600 font-medium text-xl">¥{{ order.payment_amount.toFixed(2) }}</span>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 支付信息 -->
          <div v-if="order.payment" class="card mb-6 p-6">
            <h2 class="text-lg font-bold mb-4">支付信息</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <p class="text-gray-600 mb-2">支付方式：
                  <span class="text-gray-800">
                    {{ getPaymentMethodText(order.payment.payment_method) }}
                  </span>
                </p>
                <p class="text-gray-600 mb-2">支付时间：
                  <span class="text-gray-800">
                    {{ formatDateTime(order.payment.payment_time) }}
                  </span>
                </p>
              </div>
              <div>
                <p class="text-gray-600 mb-2">交易号：
                  <span class="text-gray-800">{{ order.payment.transaction_id || '无' }}</span>
                </p>
                <p class="text-gray-600 mb-2">支付状态：
                  <span :class="order.payment.status === 'success' ? 'text-green-600' : 'text-red-600'">
                    {{ order.payment.status === 'success' ? '支付成功' : '支付失败' }}
                  </span>
                </p>
              </div>
            </div>
          </div>
        </template>
      </template>
    </el-skeleton>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ArrowLeft } from '@element-plus/icons-vue'
import { useUserStore } from '@/store/user'
import { useOrderStore } from '@/store/order'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const orderStore = useOrderStore()

// 当前订单
const order = computed(() => orderStore.currentOrder)

// 获取商品类型文本
const getItemTypeText = (type) => {
  const typeMap = {
    'product': '特产',
    'food': '美食',
    'room': '住宿'
  }
  return typeMap[type] || '商品'
}

// 获取支付方式文本
const getPaymentMethodText = (method) => {
  const methodMap = {
    'alipay': '支付宝',
    'wechat': '微信支付',
    'bank': '银行卡'
  }
  return methodMap[method] || '其他方式'
}

// 获取订单状态样式
const getOrderStatusClass = (status) => {
  const statusClassMap = {
    'pending_payment': 'text-orange-500',
    'paid': 'text-blue-500',
    'confirmed': 'text-blue-500',
    'canceled': 'text-gray-500',
    'refunding': 'text-yellow-500',
    'refunded': 'text-gray-500',
    'completed': 'text-green-500'
  }
  return statusClassMap[status] || 'text-gray-500'
}

// 获取订单步骤的活跃状态
const getOrderStepActive = (status) => {
  const statusStepMap = {
    'pending_payment': 0,
    'paid': 1,
    'confirmed': 2,
    'completed': 3,
    'canceled': 0,
    'refunding': 1,
    'refunded': 1
  }
  return statusStepMap[status] || 0
}

// 格式化日期
const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
}

// 格式化日期时间
const formatDateTime = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return `${formatDate(dateStr)} ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`
}

// 去支付
const goToPayment = (orderId) => {
  router.push(`/payment/${orderId}`)
}

// 取消订单
const cancelOrder = (orderId) => {
  ElMessageBox.confirm('确定要取消该订单吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await orderStore.cancelUserOrder(orderId)
      ElMessage.success('订单已取消')
    } catch (error) {
      console.error('取消订单失败:', error)
    }
  }).catch(() => {})
}

// 申请退款
const applyRefund = (orderId) => {
  router.push({
    path: '/payment/refund/create',
    query: { order_id: orderId }
  })
}

// 初始化
onMounted(async () => {
  if (!userStore.isLoggedIn) {
    router.push('/login?redirect=' + route.fullPath)
    return
  }

  const orderId = route.params.id
  if (!orderId) {
    router.push('/orders')
    return
  }

  try {
    await orderStore.fetchOrderDetail(orderId)
  } catch (error) {
    console.error('获取订单详情失败:', error)
    ElMessage.error('获取订单详情失败')
  }
})
</script> 