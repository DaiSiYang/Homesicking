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
          placeholder="搜索订单号/客户名"
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
        <el-table-column prop="id" label="订单号" width="120" />
        <el-table-column prop="type" label="类型" width="80">
          <template #default="scope">
            <el-tag :type="scope.row.type === 'product' ? 'success' : 'warning'">
              {{ scope.row.type === 'product' ? '特产' : '民宿' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="title" label="商品名称" min-width="180" />
        <el-table-column prop="customer_name" label="客户" width="100" />
        <el-table-column prop="amount" label="金额" width="100">
          <template #default="scope">
            <span class="text-orange-500">¥{{ scope.row.amount.toFixed(2) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="下单时间" width="160" />
        <el-table-column label="操作" width="120" fixed="right">
          <template #default="scope">
            <el-button type="primary" size="small" text @click="viewOrderDetail(scope.row)">
              查看详情
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="flex justify-center mt-4">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 30, 50]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          @size-change="fetchOrders"
          @current-change="fetchOrders"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Search } from '@element-plus/icons-vue'
import { getOrderList } from '@/api/order'

const router = useRouter()
const loading = ref(false)
const searchQuery = ref('')
const filterStatus = ref('')
const filterType = ref('')
const dateRange = ref([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

// 订单数据
const orders = ref([])

// 获取订单列表
const fetchOrders = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      limit: pageSize.value,
      search: searchQuery.value,
      status: filterStatus.value,
      type: filterType.value,
      start_date: dateRange.value?.[0],
      end_date: dateRange.value?.[1]
    }
    
    const res = await getOrderList(params)
    if (res.code === 200) {
      orders.value = res.data.results || res.data.list || []
      total.value = res.data.total || res.data.count || 0
    }
  } catch (error) {
    console.error('获取订单列表失败:', error)
    ElMessage.error('获取订单列表失败')
  } finally {
    loading.value = false
  }
}

// 查看订单详情
const viewOrderDetail = (order) => {
  router.push(`/orders/${order.id}`)
}

// 获取状态类型
const getStatusType = (status) => {
  const types = {
    pending: 'warning',
    paid: 'primary',
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
    completed: '已完成',
    cancelled: '已取消'
  }
  return texts[status] || '未知'
}

// 初始化
onMounted(() => {
  fetchOrders()
})
</script>

<style scoped>
.orders-container {
  padding: 20px;
}
</style>
