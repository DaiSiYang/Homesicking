<template>
  <div class="orders-container">
    <div class="page-header flex justify-between items-center mb-4">
      <h2 class="text-xl font-bold">订单管理</h2>
    </div>

    <!-- 搜索和筛选 -->
    <el-card class="mb-4">
      <div class="flex flex-wrap gap-4">
        <el-input
          v-model="searchQuery"
          placeholder="搜索订单号/用户名/商户名"
          class="w-64"
          clearable
          @clear="fetchOrders"
          @keyup.enter="fetchOrders"
        >
          <template #append>
            <el-button :icon="Search" @click="fetchOrders" />
          </template>
        </el-input>

        <el-select v-model="filterStatus" placeholder="订单状态" class="w-32" @change="fetchOrders">
          <el-option label="全部" value="" />
          <el-option label="待付款" value="pending" />
          <el-option label="已付款" value="paid" />
          <el-option label="已完成" value="completed" />
          <el-option label="已取消" value="cancelled" />
          <el-option label="已退款" value="refunded" />
        </el-select>

        <el-select v-model="filterType" placeholder="订单类型" class="w-32" @change="fetchOrders">
          <el-option label="全部" value="" />
          <el-option label="特产" value="product" />
          <el-option label="民宿" value="homestay" />
        </el-select>

        <el-date-picker
          v-model="dateRange"
          type="daterange"
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          format="YYYY-MM-DD"
          value-format="YYYY-MM-DD"
          @change="fetchOrders"
        />
      </div>
    </el-card>

    <!-- 订单列表 -->
    <el-card v-loading="loading">
      <el-table :data="orders" style="width: 100%">
        <el-table-column prop="order_id" label="订单号" width="180" />
        <el-table-column prop="type" label="类型" width="80">
          <template #default="scope">
            <el-tag :type="scope.row.type === 'product' ? 'success' : 'warning'">
              {{ scope.row.type === 'product' ? '特产' : '民宿' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="title" label="商品名称" min-width="180" show-overflow-tooltip />
        <el-table-column prop="user_name" label="用户" width="120" />
        <el-table-column prop="merchant_name" label="商户" width="120" />
        <el-table-column prop="amount" label="金额" width="100">
          <template #default="scope">
            <span class="text-orange-500">¥{{ scope.row.amount.toFixed(2) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="下单时间" width="160" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="getOrderStatusType(scope.row.status)">
              {{ getOrderStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="scope">
            <el-button-group>
              <el-button type="primary" size="small" text @click="viewOrderDetail(scope.row)">
                详情
              </el-button>
              <el-button 
                v-if="scope.row.status === 'pending'" 
                type="danger" 
                size="small" 
                text
                @click="cancelOrder(scope.row)"
              >
                取消
              </el-button>
              <el-button 
                v-if="scope.row.status === 'paid'" 
                type="success" 
                size="small" 
                text
                @click="completeOrder(scope.row)"
              >
                完成
              </el-button>
              <el-button 
                v-if="scope.row.status === 'paid'" 
                type="warning" 
                size="small" 
                text
                @click="refundOrder(scope.row)"
              >
                退款
              </el-button>
            </el-button-group>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="flex justify-center mt-4">
        <el-pagination
          :current-page="currentPage"
          :page-size="pageSize"
          :page-sizes="[10, 20, 30, 50]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search } from '@element-plus/icons-vue'

const router = useRouter()

// 数据
const orders = ref([
  {
    id: 1,
    order_id: 'DD20230001',
    type: 'product',
    title: '葫芦峪蜂蜜',
    user_id: 101,
    user_name: '张三',
    merchant_id: 1,
    merchant_name: '山水间农家乐',
    amount: 128.00,
    quantity: 1,
    status: 'completed',
    created_at: '2023-11-20 14:32:25',
    paid_at: '2023-11-20 14:35:18',
    completed_at: '2023-11-21 10:15:30'
  },
  {
    id: 2,
    order_id: 'DD20230002',
    type: 'homestay',
    title: '青山绿水民宿双人间',
    user_id: 102,
    user_name: '李四',
    merchant_id: 2,
    merchant_name: '青山绿水民宿',
    amount: 388.00,
    quantity: 1,
    status: 'paid',
    created_at: '2023-11-19 09:15:42',
    paid_at: '2023-11-19 09:20:15',
    completed_at: null
  },
  {
    id: 3,
    order_id: 'DD20230003',
    type: 'product',
    title: '手工竹编',
    user_id: 103,
    user_name: '王五',
    merchant_id: 1,
    merchant_name: '山水间农家乐',
    amount: 99.00,
    quantity: 1,
    status: 'pending',
    created_at: '2023-11-21 16:45:30',
    paid_at: null,
    completed_at: null
  }
])

const loading = ref(false)
const searchQuery = ref('')
const filterStatus = ref('')
const filterType = ref('')
const dateRange = ref([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(3)

// 获取订单列表
const fetchOrders = async () => {
  loading.value = true
  try {
    // 模拟API请求
    await new Promise(resolve => setTimeout(resolve, 500))
    // 实际项目中这里应该调用API获取数据
    loading.value = false
  } catch (error) {
    console.error('获取订单列表失败:', error)
    ElMessage.error('获取订单列表失败')
    loading.value = false
  }
}

// 查看订单详情
const viewOrderDetail = (order) => {
  router.push(`/orders/${order.id}`)
}

// 取消订单
const cancelOrder = (order) => {
  ElMessageBox.confirm(`确定要取消订单 ${order.order_id} 吗？`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      // 模拟API请求
      await new Promise(resolve => setTimeout(resolve, 300))
      
      // 更新本地状态
      order.status = 'cancelled'
      ElMessage.success(`已取消订单 ${order.order_id}`)
    } catch (error) {
      console.error('操作失败:', error)
      ElMessage.error('操作失败')
    }
  }).catch(() => {})
}

// 完成订单
const completeOrder = (order) => {
  ElMessageBox.confirm(`确定要将订单 ${order.order_id} 标记为已完成吗？`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      // 模拟API请求
      await new Promise(resolve => setTimeout(resolve, 300))
      
      // 更新本地状态
      order.status = 'completed'
      order.completed_at = new Date().toISOString().replace('T', ' ').substring(0, 19)
      ElMessage.success(`已将订单 ${order.order_id} 标记为已完成`)
    } catch (error) {
      console.error('操作失败:', error)
      ElMessage.error('操作失败')
    }
  }).catch(() => {})
}

// 退款订单
const refundOrder = (order) => {
  ElMessageBox.confirm(`确定要对订单 ${order.order_id} 进行退款吗？`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      // 模拟API请求
      await new Promise(resolve => setTimeout(resolve, 300))
      
      // 更新本地状态
      order.status = 'refunded'
      ElMessage.success(`已对订单 ${order.order_id} 进行退款`)
    } catch (error) {
      console.error('操作失败:', error)
      ElMessage.error('操作失败')
    }
  }).catch(() => {})
}

// 获取订单状态类型
const getOrderStatusType = (status) => {
  const types = {
    'pending': 'warning',
    'paid': 'primary',
    'completed': 'success',
    'cancelled': 'info',
    'refunded': 'danger'
  }
  return types[status] || 'info'
}

// 获取订单状态文本
const getOrderStatusText = (status) => {
  const texts = {
    'pending': '待付款',
    'paid': '已付款',
    'completed': '已完成',
    'cancelled': '已取消',
    'refunded': '已退款'
  }
  return texts[status] || '未知'
}

// 分页处理
const handleSizeChange = (size) => {
  pageSize.value = size
  fetchOrders()
}

const handleCurrentChange = (page) => {
  currentPage.value = page
  fetchOrders()
}

// 初始化
fetchOrders()
</script>

<style scoped>
.orders-container {
  padding: 20px;
}
</style> 