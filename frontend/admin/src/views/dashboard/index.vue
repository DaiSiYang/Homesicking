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
      <el-card shadow="hover">
        <template #header>
          <div class="flex justify-between items-center">
            <span>订单统计</span>
            <el-radio-group v-model="orderChartType" size="small">
              <el-radio-button label="week">本周</el-radio-button>
              <el-radio-button label="month">本月</el-radio-button>
            </el-radio-group>
          </div>
        </template>
        <div class="h-80" ref="orderChartRef"></div>
      </el-card>
      
      <el-card shadow="hover">
        <template #header>
          <div class="flex justify-between items-center">
            <span>收入统计</span>
            <el-radio-group v-model="incomeChartType" size="small">
              <el-radio-button label="week">本周</el-radio-button>
              <el-radio-button label="month">本月</el-radio-button>
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
import { ref, reactive, onMounted, watch, onUnmounted } from 'vue'
import * as echarts from 'echarts/core'
import { LineChart, BarChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent
} from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'

// 注册必要的组件
echarts.use([
  TitleComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent,
  LineChart,
  BarChart,
  CanvasRenderer
])

// 图表引用
const orderChartRef = ref(null)
const incomeChartRef = ref(null)
let orderChart = null
let incomeChart = null

// 图表类型
const orderChartType = ref('week')
const incomeChartType = ref('week')

// 统计数据
const stats = reactive({
  userCount: 1568,
  userGrowth: 12.5,
  merchantCount: 245,
  merchantGrowth: 8.3,
  productCount: 1254,
  productGrowth: 15.2,
  homestayCount: 386,
  homestayGrowth: 10.8
})

// 最近活动
const recentActivities = ref([
  {
    content: '新商户"山水间农家乐"已通过审核',
    time: '2023-11-20 14:32:25',
    type: 'success'
  },
  {
    content: '用户"张三"提交了商户入驻申请',
    time: '2023-11-20 10:15:36',
    type: 'primary'
  },
  {
    content: '新增特产"葫芦峪蜂蜜"需要审核',
    time: '2023-11-19 16:45:12',
    type: 'warning'
  },
  {
    content: '用户"李四"投诉订单DD20230001',
    time: '2023-11-19 09:22:18',
    type: 'danger'
  },
  {
    content: '系统更新完成，版本号v1.2.5',
    time: '2023-11-18 22:30:00',
    type: 'info'
  }
])

// 待处理事项
const todos = ref([
  {
    title: '商户入驻申请审核',
    type: '商户管理',
    status: '待处理',
    time: '2023-11-20 10:15:36'
  },
  {
    title: '特产上架审核',
    type: '特产管理',
    status: '待处理',
    time: '2023-11-19 16:45:12'
  },
  {
    title: '用户投诉处理',
    type: '订单管理',
    status: '待处理',
    time: '2023-11-19 09:22:18'
  },
  {
    title: '系统安全更新',
    type: '系统管理',
    status: '进行中',
    time: '2023-11-18 22:30:00'
  }
])

// 获取待办事项类型颜色
const getTodoTypeColor = (type) => {
  const colors = {
    '商户管理': 'success',
    '特产管理': 'warning',
    '订单管理': 'danger',
    '系统管理': 'info'
  }
  return colors[type] || 'primary'
}

// 初始化订单图表
const initOrderChart = () => {
  if (!orderChartRef.value) return
  
  orderChart = echarts.init(orderChartRef.value)
  
  const option = {
    title: {
      text: '订单统计'
    },
    tooltip: {
      trigger: 'axis'
    },
    legend: {
      data: ['特产订单', '民宿订单', '总订单']
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
        : Array.from({ length: 30 }, (_, i) => `${i + 1}日`)
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        name: '特产订单',
        type: 'line',
        stack: '总量',
        data: orderChartType.value === 'week'
          ? [12, 13, 10, 16, 19, 23, 21]
          : Array.from({ length: 30 }, () => Math.floor(Math.random() * 20 + 10))
      },
      {
        name: '民宿订单',
        type: 'line',
        stack: '总量',
        data: orderChartType.value === 'week'
          ? [8, 9, 11, 13, 12, 17, 15]
          : Array.from({ length: 30 }, () => Math.floor(Math.random() * 15 + 5))
      },
      {
        name: '总订单',
        type: 'line',
        data: orderChartType.value === 'week'
          ? [20, 22, 21, 29, 31, 40, 36]
          : Array.from({ length: 30 }, () => Math.floor(Math.random() * 35 + 15))
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
    title: {
      text: '收入统计'
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    legend: {
      data: ['特产收入', '民宿收入', '总收入']
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: incomeChartType.value === 'week'
        ? ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        : Array.from({ length: 30 }, (_, i) => `${i + 1}日`)
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        name: '特产收入',
        type: 'bar',
        data: incomeChartType.value === 'week'
          ? [2200, 1800, 2100, 2400, 3000, 3500, 3100]
          : Array.from({ length: 30 }, () => Math.floor(Math.random() * 2000 + 1500))
      },
      {
        name: '民宿收入',
        type: 'bar',
        data: incomeChartType.value === 'week'
          ? [3000, 2800, 3200, 3800, 3500, 4200, 4000]
          : Array.from({ length: 30 }, () => Math.floor(Math.random() * 2500 + 2000))
      },
      {
        name: '总收入',
        type: 'line',
        data: incomeChartType.value === 'week'
          ? [5200, 4600, 5300, 6200, 6500, 7700, 7100]
          : Array.from({ length: 30 }, () => Math.floor(Math.random() * 4500 + 3500))
      }
    ]
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

// 窗口大小改变时重新调整图表大小
const handleResize = () => {
  orderChart?.resize()
  incomeChart?.resize()
}

onMounted(() => {
  // 初始化图表
  initOrderChart()
  initIncomeChart()
  
  // 监听窗口大小变化
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  // 移除事件监听
  window.removeEventListener('resize', handleResize)
  
  // 销毁图表实例
  orderChart?.dispose()
  incomeChart?.dispose()
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