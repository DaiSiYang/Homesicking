<template>
  <div class="page-container py-8">
    <div class="card p-10 flex flex-col items-center">
      <el-icon :size="60" color="#67C23A" class="mb-6"><CircleCheckFilled /></el-icon>
      <h1 class="text-2xl font-bold text-green-600 mb-3">支付成功</h1>
      <p class="text-gray-600 mb-6">订单支付已完成，感谢您的购买！</p>
      
      <div class="w-full max-w-md bg-gray-50 p-6 rounded-lg mb-8">
        <div class="flex justify-between py-2 border-b border-gray-200">
          <span class="text-gray-600">订单编号：</span>
          <span class="text-gray-800">{{ orderNo }}</span>
        </div>
        <div class="flex justify-between py-2 border-b border-gray-200">
          <span class="text-gray-600">支付金额：</span>
          <span class="text-red-600 font-medium">¥{{ amount.toFixed(2) }}</span>
        </div>
        <div class="flex justify-between py-2">
          <span class="text-gray-600">支付时间：</span>
          <span class="text-gray-800">{{ currentTime }}</span>
        </div>
      </div>
      
      <div class="flex space-x-4">
        <el-button type="primary" @click="$router.push(`/orders/${orderId}`)">
          查看订单详情
        </el-button>
        <el-button type="default" @click="$router.push('/orders')">
          查看全部订单
        </el-button>
        <el-button type="default" @click="$router.push('/')">
          返回首页
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { CircleCheckFilled } from '@element-plus/icons-vue'
import { useUserStore } from '@/store/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const orderId = ref('')
const orderNo = ref('')
const amount = ref(0)
const currentTime = ref('')

// 格式化日期时间
const formatDateTime = (date) => {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  const seconds = String(date.getSeconds()).padStart(2, '0')
  
  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`
}

onMounted(() => {
  // 检查登录状态
  if (!userStore.isLoggedIn) {
    router.push('/login')
    return
  }
  
  // 获取URL参数
  orderId.value = route.query.order_id
  orderNo.value = route.query.order_no
  amount.value = parseFloat(route.query.amount || 0)
  
  // 设置当前时间
  currentTime.value = formatDateTime(new Date())
  
  // 如果没有订单信息，则跳转到订单列表
  if (!orderId.value || !orderNo.value) {
    router.push('/orders')
  }
})
</script> 