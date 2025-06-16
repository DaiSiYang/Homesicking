<template>
  <div class="page-container py-8">
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-gray-800">订单支付</h1>
    </div>

    <el-skeleton :loading="loading" animated>
      <template #default>
        <div v-if="!orderInfo" class="card p-10 text-center">
          <el-empty description="订单不存在或已取消">
            <el-button type="primary" @click="$router.push('/orders')">查看我的订单</el-button>
          </el-empty>
        </div>
        
        <template v-else>
          <!-- 订单信息 -->
          <div class="card mb-6 p-6">
            <h2 class="text-lg font-bold mb-4">订单信息</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <p class="text-gray-600 mb-2">订单编号：<span class="text-gray-800">{{ orderInfo.order_no }}</span></p>
                <p class="text-gray-600 mb-2">下单时间：<span class="text-gray-800">{{ formatDateTime(orderInfo.created_at) }}</span></p>
              </div>
              <div>
                <p class="text-gray-600 mb-2">订单状态：<span class="text-gray-800">{{ getOrderStatusText(orderInfo.status) }}</span></p>
                <p class="text-gray-600 mb-2">支付金额：<span class="text-red-600 font-medium">¥{{ orderInfo.payment_amount.toFixed(2) }}</span></p>
              </div>
            </div>
          </div>

          <!-- 支付方式选择 -->
          <div class="card mb-6 p-6">
            <h2 class="text-lg font-bold mb-4">支付方式</h2>
            <el-radio-group v-model="paymentMethod" class="mb-4">
              <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <el-radio-button label="alipay">
                  <div class="flex items-center px-4 py-2">
                    <el-icon class="text-blue-500 mr-2" :size="20"><Money /></el-icon>
                    <span>支付宝</span>
                  </div>
                </el-radio-button>
                <el-radio-button label="wechat">
                  <div class="flex items-center px-4 py-2">
                    <el-icon class="text-green-500 mr-2" :size="20"><ChatDotRound /></el-icon>
                    <span>微信支付</span>
                  </div>
                </el-radio-button>
                <el-radio-button label="bank">
                  <div class="flex items-center px-4 py-2">
                    <el-icon class="text-orange-500 mr-2" :size="20"><CreditCard /></el-icon>
                    <span>银行卡</span>
                  </div>
                </el-radio-button>
              </div>
            </el-radio-group>

            <!-- 支付按钮 -->
            <div class="flex justify-center mt-8">
              <el-button type="primary" size="large" :loading="submitting" @click="handlePay">
                立即支付 ¥{{ parseFloat(orderInfo.payment_amount || 0).toFixed(2) }}
              </el-button>
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
            <div v-for="item in orderInfo.items" :key="item.id" class="border-b last:border-0 py-4 px-6">
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
                  <span class="text-red-600 font-medium">¥{{ safeToFixed(item.price) }}</span>
                </div>
                <div class="w-32 text-center">
                  <span class="text-red-600 font-medium">¥{{ safeToFixed(item.total_price || item.amount) }}</span>
                </div>
                <div class="w-32 text-center">
                  <span>× {{ item.quantity }}</span>
                </div>
                <div class="w-32 text-center">
                  <span class="text-red-600 font-medium">¥{{ parseFloat(item.total_price || item.amount || 0).toFixed(2) }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- 订单操作 -->
          <div class="flex justify-between mt-6">
            <el-button type="default" @click="$router.push('/orders')">返回订单列表</el-button>
            <el-button type="danger" :disabled="submitting" @click="handleCancel">取消订单</el-button>
          </div>
        </template>
      </template>
    </el-skeleton>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Money, ChatDotRound, CreditCard } from '@element-plus/icons-vue'
import { useUserStore } from '@/store/user'
import { useOrderStore } from '@/store/order'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const orderStore = useOrderStore()

const loading = ref(true)
const submitting = ref(false)
const orderInfo = ref(null)
const paymentMethod = ref('alipay')

// 获取商品类型文本
const getItemTypeText = (type) => {
  const typeMap = {
    'product': '特产',
    'food': '美食',
    'room': '住宿'
  }
  return typeMap[type] || '商品'
}

// 获取订单状态文本
const getOrderStatusText = (status) => {
  return orderStore.orderStatusMap[status] || '未知状态'
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

// 安全的数字格式化函数
const safeToFixed = (value, digits = 2) => {
  const num = parseFloat(value)
  return isNaN(num) ? '0.00' : num.toFixed(digits)
}

// 支付
const handlePay = async () => {
  if (!orderInfo.value || orderInfo.value.status !== 'pending_payment') {
    ElMessage.error('订单状态不正确，无法支付')
    return
  }

  if (!paymentMethod.value) {
    ElMessage.warning('请选择支付方式')
    return
  }

  try {
    submitting.value = true
    
    // 模拟支付成功（因为不使用后端）
    ElMessage.success('支付成功！')
    
    // 清理 sessionStorage 中的待支付订单
    sessionStorage.removeItem('pendingOrder')
    
    // 跳转到支付成功页面
    router.push({
      name: 'PaymentSuccess',
      query: {
        order_id: orderInfo.value.id,
        order_no: orderInfo.value.order_no,
        amount: orderInfo.value.payment_amount
      }
    })
  } catch (error) {
    console.error('支付失败:', error)
    ElMessage.error('支付失败，请稍后再试')
  } finally {
    submitting.value = false
  }
}

// 取消订单
const handleCancel = () => {
  if (!orderInfo.value || orderInfo.value.status !== 'pending_payment') {
    ElMessage.error('只有待支付的订单可以取消')
    return
  }

  ElMessageBox.confirm('确定要取消该订单吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      submitting.value = true
      await orderStore.cancelUserOrder(orderInfo.value.id)
      
      // 取消成功，跳转到订单列表页
      ElMessageBox.alert('订单已取消', '提示', {
        confirmButtonText: '确定',
        callback: () => {
          router.push('/orders')
        }
      })
    } catch (error) {
      console.error('取消订单失败:', error)
      ElMessage.error('取消订单失败，请稍后再试')
    } finally {
      submitting.value = false
    }
  }).catch(() => {})
}

// 初始化
onMounted(async () => {
  if (!userStore.isLoggedIn) {
    router.push('/login?redirect=' + route.fullPath)
    return
  }

  try {
    // 首先尝试从 sessionStorage 获取待支付订单
    const pendingOrderStr = sessionStorage.getItem('pendingOrder')
    if (pendingOrderStr) {
      const pendingOrder = JSON.parse(pendingOrderStr)
      
      // 构造订单信息对象，确保数字类型正确
      orderInfo.value = {
        id: pendingOrder.id,
        order_no: `ORDER${pendingOrder.id}`,
        status: 'pending_payment',
        payment_amount: parseFloat(pendingOrder.total_price || 0), // 确保是数字
        created_at: new Date().toISOString(),
        items: [{
          id: pendingOrder.id,
          product_id: pendingOrder.productId,
          product_name: pendingOrder.name,
          name: pendingOrder.name, // 添加 name 字段
          image: pendingOrder.image,
          price: parseFloat(pendingOrder.price || 0), // 确保是数字
          quantity: parseInt(pendingOrder.quantity || 1), // 确保是数字
          total_price: parseFloat(pendingOrder.total_price || 0), // 确保是数字
          amount: parseFloat(pendingOrder.total_price || 0), // 添加 amount 字段作为备用
          item_type: pendingOrder.item_type || 'product'
        }]
      }
      
      loading.value = false
      return
    }

    // 如果没有待支付订单数据，显示错误
    loading.value = false
    ElMessage.error('没有找到订单信息')
    
  } catch (error) {
    console.error('获取订单失败:', error)
    ElMessage.error('获取订单失败')
    loading.value = false
  }
})
</script>

<style scoped>
/* 自定义样式 */
:deep(.el-radio-button__original-radio:checked + .el-radio-button__inner) {
  border-color: #16a34a;
  background-color: #16a34a;
  box-shadow: -1px 0 0 0 #16a34a;
}
</style>