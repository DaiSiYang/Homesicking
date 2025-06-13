<template>
  <div class="page-container py-8">
    <div class="mb-6 flex justify-between items-center">
      <h1 class="text-2xl font-bold text-gray-800">我的订单</h1>
      <div class="flex items-center">
        <!-- 订单类型筛选 -->
        <el-select v-model="filters.type" placeholder="订单类型" clearable>
          <el-option label="全部类型" value="" />
          <el-option label="特产订单" value="product" />
          <el-option label="美食订单" value="food" />
          <el-option label="住宿订单" value="room" />
        </el-select>
        
        <!-- 订单状态筛选 -->
        <el-select v-model="filters.status" placeholder="订单状态" clearable class="ml-4">
          <el-option label="全部状态" value="" />
          <el-option label="待支付" value="pending_payment" />
          <el-option label="已支付" value="paid" />
          <el-option label="已确认" value="confirmed" />
          <el-option label="已取消" value="canceled" />
          <el-option label="退款中" value="refunding" />
          <el-option label="已退款" value="refunded" />
          <el-option label="已完成" value="completed" />
        </el-select>
      </div>
    </div>

    <!-- 订单为空状态 -->
    <div v-if="orderStore.orders.length === 0 && !orderStore.loading" class="card p-10 text-center">
      <el-empty description="暂无订单">
        <el-button type="primary" @click="$router.push('/')">去购物</el-button>
      </el-empty>
    </div>

    <!-- 订单列表 -->
    <el-skeleton :loading="orderStore.loading" :rows="3" animated>
      <template #default>
        <div v-for="order in orderStore.orders" :key="order.id" class="card mb-6 overflow-hidden">
          <!-- 订单头部 -->
          <div class="flex justify-between px-6 py-4 bg-gray-50 border-b">
            <div>
              <span class="text-gray-500 mr-6">订单编号：{{ order.order_no }}</span>
              <span class="text-gray-500">下单时间：{{ formatDateTime(order.created_at) }}</span>
            </div>
            <div>
              <el-tag :type="getOrderStatusType(order.status)">
                {{ orderStore.orderStatusMap[order.status] }}
              </el-tag>
            </div>
          </div>
          
          <!-- 订单内容 -->
          <div class="p-6">
            <!-- 商品列表，只显示前2个 -->
            <div v-for="item in order.items.slice(0, 2)" :key="item.id" class="flex py-2">
              <img :src="item.image" alt="商品图片" class="w-16 h-16 object-cover rounded mr-4">
              <div class="flex-1">
                <div class="flex justify-between">
                  <h3 class="text-base font-medium text-gray-800">{{ item.name }}</h3>
                  <div class="text-right">
                    <div class="text-red-600 font-medium">¥{{ item.price.toFixed(2) }}</div>
                    <div class="text-gray-500">× {{ item.quantity }}</div>
                  </div>
                </div>
                <p class="text-sm text-gray-500 mt-1">
                  {{ getItemTypeText(item.item_type) }}
                  <span v-if="item.item_type === 'room' && item.check_in_date && item.check_out_date">
                    · {{ formatDate(item.check_in_date) }} 至 {{ formatDate(item.check_out_date) }}
                  </span>
                </p>
              </div>
            </div>
            
            <!-- 显示还有多少商品 -->
            <div v-if="order.items.length > 2" class="text-center text-gray-500 text-sm py-2">
              还有 {{ order.items.length - 2 }} 件商品
            </div>
            
            <!-- 订单金额和操作 -->
            <div class="flex justify-between items-center mt-4 pt-4 border-t">
              <div class="text-gray-600">
                共 <span class="text-red-600 font-medium">{{ getTotalQuantity(order) }}</span> 件商品，
                合计：<span class="text-red-600 font-medium text-lg">¥{{ order.total_amount.toFixed(2) }}</span>
              </div>
              <div class="flex space-x-3">
                <el-button type="default" @click="viewOrderDetail(order.id)">订单详情</el-button>
                
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
        </div>
        
        <!-- 分页 -->
        <div class="flex justify-center mt-6">
          <el-pagination
            :current-page="currentPage"
            :page-size="pageSize"
            :total="orderStore.orderCount"
            :page-sizes="[5, 10, 20, 50]"
            layout="total, sizes, prev, pager, next, jumper"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
          />
        </div>
      </template>
    </el-skeleton>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useUserStore } from '@/store/user'
import { useOrderStore } from '@/store/order'

const router = useRouter()
const userStore = useUserStore()
const orderStore = useOrderStore()

// 分页相关
const currentPage = ref(1)
const pageSize = ref(10)

// 筛选条件
const filters = reactive({
  type: '',
  status: ''
})

// 获取商品类型文本
const getItemTypeText = (type) => {
  const typeMap = {
    'product': '特产',
    'food': '美食',
    'room': '住宿'
  }
  return typeMap[type] || '商品'
}

// 获取订单状态类型对应的Element UI Tag类型
const getOrderStatusType = (status) => {
  const statusMap = {
    'pending_payment': 'warning',
    'paid': 'primary',
    'confirmed': 'primary',
    'canceled': 'info',
    'refunding': 'warning',
    'refunded': 'info',
    'completed': 'success'
  }
  return statusMap[status] || 'info'
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

// 获取订单总数量
const getTotalQuantity = (order) => {
  return order.items.reduce((sum, item) => sum + item.quantity, 0)
}

// 查看订单详情
const viewOrderDetail = (orderId) => {
  router.push(`/orders/${orderId}`)
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

// 处理页码变化
const handleCurrentChange = (page) => {
  currentPage.value = page
  fetchOrders()
}

// 处理每页条数变化
const handleSizeChange = (size) => {
  pageSize.value = size
  fetchOrders()
}

// 获取订单列表
const fetchOrders = async () => {
  try {
    orderStore.setPage(currentPage.value)
    orderStore.setPageSize(pageSize.value)
    
    const params = {
      ...filters
    }
    
    await orderStore.fetchOrders(params)
  } catch (error) {
    console.error('获取订单失败:', error)
  }
}

// 监听筛选条件变化
watch(filters, () => {
  currentPage.value = 1 // 重置页码
  fetchOrders()
}, { deep: true })

// 初始化
onMounted(async () => {
  if (!userStore.isLoggedIn) {
    router.push('/login?redirect=/orders')
    return
  }

  await fetchOrders()
})
</script>