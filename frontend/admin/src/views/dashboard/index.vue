<template>
  <div class="dashboard-container">
    <h2 class="text-2xl font-bold mb-6">控制台</h2>
    
    <!-- 数据概览 -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
      <el-card shadow="hover" class="dashboard-card">
        <div class="flex items-center">
          <el-icon class="text-blue-500 text-3xl mr-4"><User /></el-icon>
          <div>
            <div class="text-gray-500">用户总数</div>
            <div class="text-2xl font-bold">{{ stats.userCount }}</div>
          </div>
        </div>
        <div class="mt-2 text-sm">
          <span class="text-green-500">
            <el-icon><CaretTop /></el-icon>
            {{ stats.userGrowth }}%
          </span>
          较上周
        </div>
      </el-card>
      
      <el-card shadow="hover" class="dashboard-card">
        <div class="flex items-center">
          <el-icon class="text-orange-500 text-3xl mr-4"><Shop /></el-icon>
          <div>
            <div class="text-gray-500">商户总数</div>
            <div class="text-2xl font-bold">{{ stats.merchantCount }}</div>
          </div>
        </div>
        <div class="mt-2 text-sm">
          <span class="text-green-500">
            <el-icon><CaretTop /></el-icon>
            {{ stats.merchantGrowth }}%
          </span>
          较上周
        </div>
      </el-card>
      
      <el-card shadow="hover" class="dashboard-card">
        <div class="flex items-center">
          <el-icon class="text-green-500 text-3xl mr-4"><ShoppingBag /></el-icon>
          <div>
            <div class="text-gray-500">特产数量</div>
            <div class="text-2xl font-bold">{{ stats.productCount }}</div>
          </div>
        </div>
        <div class="mt-2 text-sm">
          <span class="text-green-500">
            <el-icon><CaretTop /></el-icon>
            {{ stats.productGrowth }}%
          </span>
          较上周
        </div>
      </el-card>
      
      <el-card shadow="hover" class="dashboard-card">
        <div class="flex items-center">
          <el-icon class="text-purple-500 text-3xl mr-4"><House /></el-icon>
          <div>
            <div class="text-gray-500">民宿数量</div>
            <div class="text-2xl font-bold">{{ stats.homestayCount }}</div>
          </div>
        </div>
        <div class="mt-2 text-sm">
          <span class="text-green-500">
            <el-icon><CaretTop /></el-icon>
            {{ stats.homestayGrowth }}%
          </span>
          较上周
        </div>
      </el-card>
    </div>
    
    <!-- 图表区域 -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
      <!-- 订单统计图表 -->
      <el-card shadow="hover">
        <template #header>
          <div class="flex justify-between items-center">
            <span>订单统计</span>
            <el-radio-group v-model="orderChartType" size="small">
              <el-radio-button value="week">本周</el-radio-button>
              <el-radio-button value="month">本月</el-radio-button>
            </el-radio-group>
          </div>
        </template>
        <div class="h-80" ref="orderChartRef"></div>
      </el-card>
      
      <!-- 收入统计图表 -->
      <el-card shadow="hover">
        <template #header>
          <div class="flex justify-between items-center">
            <span>收入统计</span>
            <el-radio-group v-model="incomeChartType" size="small">
              <el-radio-button value="week">本周</el-radio-button>
              <el-radio-button value="month">本月</el-radio-button>
            </el-radio-group>
          </div>
        </template>
        <div class="h-80" ref="incomeChartRef"></div>
      </el-card>
    </div>
    
    <!-- 最近活动 -->
    <el-card shadow="hover" class="mb-6">
      <template #header>
        <div class="flex justify-between items-center">
          <span>最近活动</span>
          <el-button type="primary" text>查看全部</el-button>
        </div>
      </template>
      
      <el-timeline>
        <el-timeline-item
          v-for="(activity, index) in recentActivities"
          :key="index"
          :timestamp="activity.time"
          :type="activity.type"
        >
          {{ activity.content }}
        </el-timeline-item>
      </el-timeline>
    </el-card>
    
    <!-- 待处理事项 -->
    <el-card shadow="hover">
      <template #header>
        <div class="flex justify-between items-center">
          <span>待处理事项</span>
          <el-button type="primary" text>查看全部</el-button>
        </div>
      </template>
      
      <el-table :data="todos" style="width: 100%">
        <el-table-column prop="title" label="标题" min-width="200" />
        <el-table-column prop="type" label="类型" width="120">
          <template #default="scope">
            <el-tag :type="getTodoTypeColor(scope.row.type)">{{ scope.row.type }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.status === '待处理' ? 'danger' : 'info'">
              {{ scope.row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="time" label="时间" width="180" />
        <el-table-column label="操作" width="120" fixed="right">
          <template #default>
            <el-button type="primary" size="small" text>处理</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getDashboardStats, getRecentActivities, getTodoList } from '@/api/dashboard'

// 最近活动数据 - 确保始终是数组
// 删除第190-202行的重复声明
// const recentActivities = ref([
//   {
//     time: '2024-01-15 10:30',
//     type: 'primary',
//     content: '新用户注册：张三'
//   },
//   // ... 其他示例数据
// ])

// 待办事项 - 确保始终是数组
const todos = ref([])

// 统计数据 - 提供默认值
const stats = ref({
  userCount: 0,
  userGrowth: 0,
  merchantCount: 0,
  merchantGrowth: 0,
  productCount: 0,
  productGrowth: 0,
  homestayCount: 0,
  homestayGrowth: 0
})

// 图表类型控制
const orderChartType = ref('week')
const incomeChartType = ref('week')

// 待办事项


const loading = ref(false)
const orderChartRef = ref()
const incomeChartRef = ref()

// 获取待办事项类型颜色
const getTodoTypeColor = (type) => {
  const colorMap = {
    '审核': 'warning',
    '客服': 'info',
    '系统': 'danger',
    '运营': 'success'
  }
  return colorMap[type] || 'info'
}

// 获取统计数据
const fetchStats = async () => {
  try {
    const response = await getDashboardStats()
    if (response.data) {
      stats.value = response.data
    }
  } catch (error) {
    console.error('获取统计数据失败:', error)
    ElMessage.error('获取统计数据失败，请稍后重试')
  }
}

// 获取最近活动
const fetchActivities = async () => {
  try {
    const response = await getRecentActivities({ limit: 10 })
    // 确保数据结构正确
    if (response.data && response.data.results) {
      recentActivities.value = response.data.results
    } else {
      console.warn('获取最近活动数据格式异常:', response.data)
      recentActivities.value = []
    }
  } catch (error) {
    console.error('获取最近活动失败:', error)
    // 设置默认值防止组件错误
    recentActivities.value = []
    ElMessage.error('获取最近活动失败，请稍后重试')
  }
}

// 获取待办事项
const fetchTodos = async () => {
  try {
    const response = await getTodoList()
    if (response.data) {
      todos.value = response.data
    } else {
      todos.value = []
    }
  } catch (error) {
    console.error('获取待办事项失败:', error)
    todos.value = []
    ElMessage.error('获取待办事项失败，请稍后重试')
  }
}

// 初始化数据
const initData = async () => {
  loading.value = true
  try {
    await Promise.all([
      fetchStats(),
      fetchActivities(),
      fetchTodos()
    ])
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  initData()
})
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
}

.dashboard-card {
  transition: all 0.3s;
}

.dashboard-card:hover {
  transform: translateY(-5px);
}
</style>