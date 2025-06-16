<template>
  <div class="homestays-container">
    <div class="page-header flex justify-between items-center mb-4">
      <h2 class="text-xl font-bold">民宿管理</h2>
      <el-button type="primary" @click="openAddDialog">添加民宿</el-button>
    </div>

    <!-- 搜索和筛选 -->
    <el-card class="mb-4">
      <div class="flex flex-wrap gap-4">
        <el-input
          v-model="searchQuery"
          placeholder="搜索民宿名称/商户名称"
          class="w-64"
          clearable
          @clear="fetchHomestays"
          @keyup.enter="fetchHomestays"
        >
          <template #append>
            <el-button :icon="Search" @click="fetchHomestays" />
          </template>
        </el-input>

        <el-select v-model="filterStatus" placeholder="状态筛选" class="w-32" @change="fetchHomestays">
          <el-option label="全部" value="" />
          <el-option label="上架中" value="active" />
          <el-option label="已下架" value="inactive" />
          <el-option label="待审核" value="pending" />
        </el-select>

        <el-select v-model="filterType" placeholder="类型筛选" class="w-40" @change="fetchHomestays">
          <el-option label="全部类型" value="" />
          <el-option label="整套出租" value="entire" />
          <el-option label="单间出租" value="single" />
          <el-option label="多人间" value="shared" />
        </el-select>
      </div>
    </el-card>

    <!-- 民宿列表 -->
    <el-card v-loading="loading">
      <el-table :data="homestays" style="width: 100%">
        <el-table-column label="图片" width="100">
          <template #default="scope">
            <el-image 
              style="width: 60px; height: 60px" 
              :src="scope.row.cover_image" 
              fit="cover"
            />
          </template>
        </el-table-column>
        <el-table-column prop="name" label="名称" min-width="150" />
        <el-table-column prop="merchant_name" label="所属商户" width="150" />
        <el-table-column prop="type" label="类型" width="100">
          <template #default="scope">
            <el-tag>{{ getTypeText(scope.row.type) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="price" label="价格/晚" width="100">
          <template #default="scope">
            <span class="text-orange-500">¥{{ parseFloat(scope.row.lowest_price || scope.row.price || 0).toFixed(2) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="capacity" label="可住人数" width="80" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="scope">
            <el-button-group>
              <el-button type="primary" size="small" text @click="viewHomestayDetail(scope.row)">
                详情
              </el-button>
              <!-- 在模板中更新函数名 -->
              <el-button 
                v-if="scope.row.status === 'pending'"
                type="success" 
                size="small" 
                text
                @click="handleReviewHomestay(scope.row, 'approved')"
              >
                通过
              </el-button>
              <el-button 
                v-if="scope.row.status === 'pending'"
                type="danger" 
                size="small" 
                text
                @click="handleReviewHomestay(scope.row, 'rejected')"
              >
                拒绝
              </el-button>
              <el-button 
                v-if="scope.row.status !== 'pending'"
                :type="scope.row.status === 'active' ? 'warning' : 'success'" 
                size="small" 
                text
                @click="toggleHomestayStatus(scope.row)"
              >
                {{ scope.row.status === 'active' ? '下架' : '上架' }}
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
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search } from '@element-plus/icons-vue'

// 导入API
import {
  getHomestayList,
  updateHomestayStatus,
  reviewHomestay as reviewHomestayApi  // 重命名导入的API函数
} from '@/api/homestay'

const router = useRouter()

// 数据
// 将硬编码的数组改为空数组
const homestays = ref([])

const loading = ref(false)
const searchQuery = ref('')
const filterStatus = ref('')
const filterType = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
// 将硬编码的total改为0
const total = ref(0)

// 获取民宿列表
// 删除这里的重复导入语句
// import {
//   getHomestayList,
//   updateHomestayStatus,
//   reviewHomestay
// } from '@/api/homestay'

// 更新fetchHomestays函数
const fetchHomestays = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value,
      search: searchQuery.value,
      status: filterStatus.value,
      type: filterType.value
    }
    
    const response = await getHomestayList(params)
    homestays.value = response.data.results
    total.value = response.data.count
  } catch (error) {
    console.error('获取民宿列表失败:', error)
    ElMessage.error('获取民宿列表失败')
  } finally {
    loading.value = false
  }
}

// 查看民宿详情
const viewHomestayDetail = (homestay) => {
  router.push(`/homestays/${homestay.id}`)
}

// 审核民宿 - 重命名本地函数
const handleReviewHomestay = async (homestay, action) => {
  try {
    await reviewHomestayApi(homestay.id, { action })
    ElMessage.success(`已${action === 'approved' ? '通过' : '拒绝'}民宿"${homestay.name}"的审核`)
    homestay.status = action === 'approved' ? 'active' : 'rejected'
    // 重新获取数据
    await fetchHomestays()
  } catch (error) {
    console.error('审核失败:', error)
    ElMessage.error('审核失败')
  }
}

// 切换民宿状态
const toggleHomestayStatus = (homestay) => {
  const newStatus = homestay.status === 'active' ? 'inactive' : 'active'
  homestay.status = newStatus
  ElMessage.success(`已${newStatus === 'active' ? '上架' : '下架'}民宿"${homestay.name}"`)
}

// 打开添加民宿对话框
const openAddDialog = () => {
  // 实际项目中应该打开添加民宿的对话框
  ElMessage.info('添加民宿功能待实现')
}

// 获取类型文本
const getTypeText = (type) => {
  const types = {
    'entire': '整套出租',
    'single': '单间出租',
    'shared': '多人间'
  }
  return types[type] || '未知'
}

// 获取状态类型
const getStatusType = (status) => {
  const types = {
    'active': 'success',
    'inactive': 'info',
    'pending': 'warning',
    'rejected': 'danger'
  }
  return types[status] || 'info'
}

// 获取状态文本
const getStatusText = (status) => {
  const texts = {
    'active': '上架中',
    'inactive': '已下架',
    'pending': '待审核',
    'rejected': '已拒绝'
  }
  return texts[status] || '未知'
}

// 分页处理
const handleSizeChange = (size) => {
  pageSize.value = size
  fetchHomestays()
}

const handleCurrentChange = (page) => {
  currentPage.value = page
  fetchHomestays()
}

// 初始化
fetchHomestays()
</script>

<style scoped>
.homestays-container {
  padding: 20px;
}
</style>