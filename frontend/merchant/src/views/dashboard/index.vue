<template>
  <div class="dashboard-container">
    <div class="page-title">控制台概览</div>
    
    <!-- 数据概览 -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <div class="stat-card">
        <div class="flex items-center justify-between">
          <div>
            <div class="stat-icon products">
              <el-icon class="text-xl"><Goods /></el-icon>
            </div>
            <div class="text-gray-500 text-sm mb-1">特产总数</div>
            <div class="text-2xl font-bold text-gray-800">{{ statistics.productCount }}</div>
            <div class="text-xs text-green-600 mt-1">↗ +12% 较上月</div>
          </div>
          <div class="w-16 h-16 opacity-10">
            <svg viewBox="0 0 64 64" class="w-full h-full text-green-600">
              <path fill="currentColor" d="M32 8L8 20v24c0 11.1 7.68 19.48 18 22 10.32-2.52 18-10.9 18-22V20L32 8z"/>
            </svg>
          </div>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="flex items-center justify-between">
          <div>
            <div class="stat-icon homestays">
              <el-icon class="text-xl"><House /></el-icon>
            </div>
            <div class="text-gray-500 text-sm mb-1">民宿总数</div>
            <div class="text-2xl font-bold text-gray-800">{{ statistics.homestayCount }}</div>
            <div class="text-xs text-orange-600 mt-1">↗ +8% 较上月</div>
          </div>
          <div class="w-16 h-16 opacity-10">
            <svg viewBox="0 0 64 64" class="w-full h-full text-orange-600">
              <path fill="currentColor" d="M32 4L4 20v36h56V20L32 4z"/>
            </svg>
          </div>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="flex items-center justify-between">
          <div>
            <div class="stat-icon orders">
              <el-icon class="text-xl"><List /></el-icon>
            </div>
            <div class="text-gray-500 text-sm mb-1">订单总数</div>
            <div class="text-2xl font-bold text-gray-800">{{ statistics.orderCount }}</div>
            <div class="text-xs text-purple-600 mt-1">↗ +15% 较上月</div>
          </div>
          <div class="w-16 h-16 opacity-10">
            <svg viewBox="0 0 64 64" class="w-full h-full text-purple-600">
              <path fill="currentColor" d="M8 12h48l-4 32H12L8 12z"/>
            </svg>
          </div>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="flex items-center justify-between">
          <div>
            <div class="stat-icon income">
              <el-icon class="text-xl"><Money /></el-icon>
            </div>
            <div class="text-gray-500 text-sm mb-1">总收入(元)</div>
            <div class="text-2xl font-bold text-gray-800">{{ statistics.totalIncome }}</div>
            <div class="text-xs text-teal-600 mt-1">↗ +23% 较上月</div>
          </div>
          <div class="w-16 h-16 opacity-10">
            <svg viewBox="0 0 64 64" class="w-full h-full text-teal-600">
              <circle cx="32" cy="32" r="28" fill="currentColor"/>
            </svg>
          </div>
        </div>
      </div>
    </div>

    <!-- 图表和最近订单 -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- 收入趋势图 -->
      <div class="rural-card p-6">
        <h3 class="text-lg font-semibold text-gray-800 mb-4 flex items-center">
          <div class="w-1 h-6 bg-gradient-to-b from-green-500 to-green-600 rounded-full mr-3"></div>
          收入趋势
        </h3>
        <div class="h-64 flex items-center justify-center text-gray-500">
          <!-- 这里可以集成图表库如 ECharts -->
          <div class="text-center">
            <svg class="w-16 h-16 mx-auto mb-4 text-gray-300" fill="currentColor" viewBox="0 0 20 20">
              <path d="M2 11a1 1 0 011-1h2a1 1 0 011 1v5a1 1 0 01-1 1H3a1 1 0 01-1-1v-5zM8 7a1 1 0 011-1h2a1 1 0 011 1v9a1 1 0 01-1 1H9a1 1 0 01-1-1V7zM14 4a1 1 0 011-1h2a1 1 0 011 1v12a1 1 0 01-1 1h-2a1 1 0 01-1-1V4z"></path>
            </svg>
            <p>收入趋势图表</p>
          </div>
        </div>
      </div>
      
      <!-- 最近订单 -->
      <div class="rural-card p-6">
        <h3 class="text-lg font-semibold text-gray-800 mb-4 flex items-center">
          <div class="w-1 h-6 bg-gradient-to-b from-orange-500 to-orange-600 rounded-full mr-3"></div>
          最近订单
        </h3>
        <div class="space-y-3">
          <div v-for="order in recentOrders" :key="order.id" class="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
            <div class="flex items-center">
              <div class="w-10 h-10 bg-gradient-to-br from-green-100 to-green-200 rounded-lg flex items-center justify-center mr-3">
                <el-icon class="text-green-600"><ShoppingBag /></el-icon>
              </div>
              <div>
                <div class="font-medium text-gray-800">订单 #{{ order.orderNumber }}</div>
                <div class="text-sm text-gray-500">{{ order.customerName }}</div>
              </div>
            </div>
            <div class="text-right">
              <div class="font-semibold text-gray-800">¥{{ order.amount }}</div>
              <div class="text-xs" :class="getStatusColor(order.status)">{{ order.status }}</div>
            </div>
          </div>
        </div>
        <div class="mt-4 text-center">
          <router-link to="/orders" class="btn-secondary inline-block">
            查看全部订单
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted, watch } from 'vue'
import * as echarts from 'echarts'
import { getMerchantStatistics, getIncomeStatistics } from '@/api/merchant'
import { getRecentOrders } from '@/api/order'
import { ElMessage } from 'element-plus'

// 图表引用
const orderChartRef = ref(null)
const incomeChartRef = ref(null)
let orderChart = null
let incomeChart = null

// 图表类型
const orderChartType = ref('week')
const incomeChartType = ref('week')

// 统计数据
const statistics = reactive({
  productCount: 0,
  homestayCount: 0,
  orderCount: 0,
  totalIncome: 0
})

// 最近订单
const recentOrders = ref([])
const loading = ref(false)

// 获取统计数据
const fetchStatistics = async () => {
  try {
    const res = await getMerchantStatistics()
    if (res.code === 200) {
      Object.assign(statistics, res.data)
    }
  } catch (error) {
    console.error('获取统计数据失败:', error)
  }
}

// 获取订单图表数据
const fetchOrderChartData = async (type) => {
  try {
    const res = await getOrderStatistics({ type })
    if (res.code === 200) {
      updateOrderChart(res.data)
    }
  } catch (error) {
    console.error('获取订单图表数据失败:', error)
  }
}

// 获取收入图表数据
const fetchIncomeChartData = async (type) => {
  try {
    const res = await getIncomeStatistics({ type })
    if (res.code === 200) {
      updateIncomeChart(res.data)
    }
  } catch (error) {
    console.error('获取收入图表数据失败:', error)
  }
}

// 获取最近订单
const fetchRecentOrders = async () => {
  try {
    loading.value = true
    const res = await getRecentOrders({ limit: 10 })
    if (res.code === 200) {
      recentOrders.value = res.data.list || res.data.results || []
    }
  } catch (error) {
    console.error('获取最近订单失败:', error)
    ElMessage.error('获取最近订单失败')
  } finally {
    loading.value = false
  }
}

// 获取订单状态类型
const getOrderStatusType = (status) => {
  switch (status) {
    case 'completed':
    case '已完成':
      return 'success'
    case 'paid':
    case '已付款':
    case 'pending':
    case '待发货':
      return 'warning'
    case 'cancelled':
    case '已取消':
      return 'danger'
    default:
      return 'info'
  }
}

// 初始化订单图表
const initOrderChart = () => {
  if (!orderChartRef.value) return
  
  orderChart = echarts.init(orderChartRef.value)
  
  const option = {
    tooltip: {
      trigger: 'axis'
    },
    legend: {
      data: ['特产订单', '民宿订单']
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: orderChartType.value === 'week' 
        ? ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        : Array.from({length: 30}, (_, i) => `${i + 1}日`)
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        name: '特产订单',
        type: 'line',
        stack: 'Total',
        data: orderChartType.value === 'week'
          ? [5, 7, 3, 8, 6, 9, 10]
          : Array.from({length: 30}, () => Math.floor(Math.random() * 10) + 1)
      },
      {
        name: '民宿订单',
        type: 'line',
        stack: 'Total',
        data: orderChartType.value === 'week'
          ? [3, 2, 4, 6, 2, 5, 8]
          : Array.from({length: 30}, () => Math.floor(Math.random() * 8) + 1)
      }
    ]
  }
  
  orderChart.setOption(option)
}

// 初始化收入图表
const initIncomeChart = () => {
  if (!incomeChartRef.value) return
  
  incomeChart = echarts.init(incomeChartRef.value)
  
  const option = {
    tooltip: {
      trigger: 'axis',
      formatter: '{b}<br />{a}: ¥{c}'
    },
    xAxis: {
      type: 'category',
      data: incomeChartType.value === 'week' 
        ? ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        : Array.from({length: 30}, (_, i) => `${i + 1}日`)
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        name: '收入',
        type: 'bar',
        data: incomeChartType.value === 'week'
          ? [820, 932, 901, 934, 1290, 1330, 1320]
          : Array.from({length: 30}, () => Math.floor(Math.random() * 1000) + 500)
      }
    ],
    color: ['#67c23a']
  }
  
  incomeChart.setOption(option)
}

// 监听图表类型变化
watch(orderChartType, () => {
  initOrderChart()
})

watch(incomeChartType, () => {
  initIncomeChart()
})

// 监听窗口大小变化
const handleResize = () => {
  orderChart && orderChart.resize()
  incomeChart && incomeChart.resize()
}

onMounted(() => {
  fetchStatistics()
  fetchRecentOrders()
  initOrderChart()
  initIncomeChart()
  window.addEventListener('resize', handleResize)
})

// 组件卸载时移除事件监听
onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  orderChart && orderChart.dispose()
  incomeChart && incomeChart.dispose()
})

const getStatusColor = (status) => {
  const colors = {
    '待付款': 'text-orange-600',
    '待发货': 'text-blue-600',
    '已发货': 'text-green-600',
    '已完成': 'text-gray-600',
    '已取消': 'text-red-600'
  }
  return colors[status] || 'text-gray-600'
}
</script>

<style scoped>
.dashboard-container {
  padding: 0;
}
</style>