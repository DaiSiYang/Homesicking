<template>
  <div class="order-detail-container">
    <div class="page-header flex items-center mb-4">
      <el-button icon="ArrowLeft" text @click="$router.push('/orders')">返回</el-button>
      <h2 class="text-xl font-bold ml-2">订单详情</h2>
    </div>

    <el-card v-loading="loading">
      <template v-if="order">
        <!-- 订单基本信息 -->
        <el-descriptions title="订单信息" :column="2" border>
          <el-descriptions-item label="订单号">{{ order.id }}</el-descriptions-item>
          <el-descriptions-item label="下单时间">{{ order.created_at }}</el-descriptions-item>
          <el-descriptions-item label="订单状态">
            <el-tag :type="getStatusType(order.status)">
              {{ getStatusText(order.status) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="订单类型">
            <el-tag :type="order.type === 'product' ? 'success' : 'warning'">
              {{ order.type === 'product' ? '特产' : '民宿' }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="支付方式">{{ order.payment_method }}</el-descriptions-item>
          <el-descriptions-item label="支付时间" v-if="order.paid_at">{{ order.paid_at }}</el-descriptions-item>
        </el-descriptions>

        <!-- 客户信息 -->
        <el-descriptions title="客户信息" :column="2" border class="mt-6">
          <el-descriptions-item label="客户姓名">{{ order.customer.name }}</el-descriptions-item>
          <el-descriptions-item label="联系电话">{{ order.customer.phone }}</el-descriptions-item>
          <el-descriptions-item label="收货地址" :span="2" v-if="order.type === 'product'">
            {{ order.customer.address }}
          </el-descriptions-item>
        </el-descriptions>

        <!-- 商品信息 -->
        <div class="mt-6">
          <h3 class="text-lg font-medium mb-2">商品信息</h3>
          <el-table :data="order.items" style="width: 100%">
            <el-table-column label="商品图片" width="100">
              <template #default="scope">
                <el-image 
                  style="width: 60px; height: 60px" 
                  :src="scope.row.image" 
                  fit="cover"
                  :preview-src-list="[scope.row.image]"
                />
              </template>
            </el-table-column>
            <el-table-column prop="name" label="商品名称" min-width="200" />
            <el-table-column prop="price" label="单价" width="100">
              <template #default="scope">
                <span>¥{{ scope.row.price.toFixed(2) }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="quantity" label="数量" width="80" />
            <el-table-column label="小计" width="120">
              <template #default="scope">
                <span class="text-orange-500">¥{{ (scope.row.price * scope.row.quantity).toFixed(2) }}</span>
              </template>
            </el-table-column>
          </el-table>
        </div>

        <!-- 订单金额信息 -->
        <div class="flex justify-end mt-4">
          <div class="w-80">
            <div class="flex justify-between py-2">
              <span>商品总额：</span>
              <span>¥{{ calculateSubtotal().toFixed(2) }}</span>
            </div>
            <div class="flex justify-between py-2">
              <span>运费：</span>
              <span>¥{{ order.shipping_fee.toFixed(2) }}</span>
            </div>
            <div class="flex justify-between py-2 font-bold">
              <span>订单总额：</span>
              <span class="text-orange-500 text-xl">¥{{ order.total_amount.toFixed(2) }}</span>
            </div>
          </div>
        </div>

        <!-- 订单操作 -->
        <div class="flex justify-end mt-6">
          <el-button 
            v-if="order.status === 'pending'" 
            type="danger" 
            @click="cancelOrder"
          >
            取消订单
          </el-button>
          <el-button 
            v-if="order.status === 'paid' && order.type === 'product'" 
            type="primary" 
            @click="shipOrder"
          >
            发货
          </el-button>
          <el-button 
            v-if="order.status === 'shipping'" 
            type="success" 
            @click="completeOrder"
          >
            确认完成
          </el-button>
        </div>

        <!-- 订单日志 -->
        <div class="mt-6">
          <h3 class="text-lg font-medium mb-2">订单日志</h3>
          <el-timeline>
            <el-timeline-item
              v-for="(log, index) in order.logs"
              :key="index"
              :timestamp="log.time"
              :type="log.type"
            >
              {{ log.content }}
            </el-timeline-item>
          </el-timeline>
        </div>
      </template>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'

const route = useRoute()
const router = useRouter()
const loading = ref(true)
const order = ref(null)

// 获取订单详情
const fetchOrderDetail = async (orderId) => {
  loading.value = true
  try {
    const res = await getOrderDetail(orderId)
    if (res.code === 200) {
      order.value = res.data
    }
  } catch (error) {
    console.error('获取订单详情失败:', error)
    ElMessage.error('获取订单详情失败')
  } finally {
    loading.value = false
  }
}

// 取消订单
const cancelOrder = () => {
  ElMessageBox.confirm('确定要取消此订单吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await updateOrderStatus(order.value.id, 'cancelled')
      order.value.status = 'cancelled'
      ElMessage.success('订单已取消')
      fetchOrderDetail(order.value.id) // 重新获取订单详情
    } catch (error) {
      console.error('取消订单失败:', error)
      ElMessage.error('取消订单失败')
    }
  }).catch(() => {})
}

// 发货
const shipOrder = () => {
  ElMessageBox.confirm('确认商品已发货？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'info'
  }).then(async () => {
    try {
      await updateOrderStatus(order.value.id, 'shipping')
      order.value.status = 'shipping'
      ElMessage.success('已更新为发货状态')
      fetchOrderDetail(order.value.id) // 重新获取订单详情
    } catch (error) {
      console.error('发货失败:', error)
      ElMessage.error('发货失败')
    }
  }).catch(() => {})
}

// 完成订单
const completeOrder = () => {
  ElMessageBox.confirm('确认订单已完成？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'info'
  }).then(async () => {
    try {
      await updateOrderStatus(order.value.id, 'completed')
      order.value.status = 'completed'
      ElMessage.success('订单已完成')
      fetchOrderDetail(order.value.id) // 重新获取订单详情
    } catch (error) {
      console.error('完成订单失败:', error)
      ElMessage.error('完成订单失败')
    }
  }).catch(() => {})
}

// 计算商品小计
const calculateSubtotal = () => {
  if (!order.value || !order.value.items) return 0
  return order.value.items.reduce((sum, item) => sum + (item.price * item.quantity), 0)
}

// 获取状态类型
const getStatusType = (status) => {
  const types = {
    pending: 'warning',
    paid: 'primary',
    shipping: 'info',
    completed: 'success',
    cancelled: 'info'
  }
  return types[status] || 'info'
}

// 获取状态文本
const getStatusText = (status) => {
  const texts = {
    pending: '待付款',
    paid: '已付款',
    shipping: '配送中',
    completed: '已完成',
    cancelled: '已取消'
  }
  return texts[status] || '未知'
}

// 初始化
onMounted(() => {
  const orderId = route.params.id
  if (orderId) {
    fetchOrderDetail(orderId)
  } else {
    loading.value = false
    ElMessage.error('订单ID不存在')
    router.push('/orders')
  }
})
</script>

<style scoped>
.order-detail-container {
  padding: 20px;
}
</style>
