<template>
  <div class="villages-container container mx-auto py-8 px-4">
    <h1 class="text-3xl font-bold mb-8 text-center">探索美丽乡村</h1>
    
    <!-- 搜索和筛选区域 -->
    <div class="search-filter-container mb-8 bg-gray-50 p-4 rounded-lg">
      <el-form :inline="true" class="flex flex-wrap items-center">
        <el-form-item label="关键词">
          <el-input v-model="searchQuery" placeholder="搜索乡村名称" />
        </el-form-item>
        <el-form-item label="地区">
          <el-select v-model="regionFilter" placeholder="选择地区">
            <el-option label="全部地区" value="" />
            <el-option label="华东" value="华东" />
            <el-option label="华南" value="华南" />
            <el-option label="华北" value="华北" />
            <el-option label="西南" value="西南" />
            <el-option label="西北" value="西北" />
            <el-option label="东北" value="东北" />
            <el-option label="华中" value="华中" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="searchVillages">搜索</el-button>
          <el-button @click="resetFilters">重置</el-button>
        </el-form-item>
      </el-form>
    </div>
    
    <!-- 乡村列表 -->
    <div v-if="loading" class="flex justify-center py-10">
      <el-skeleton :rows="10" animated />
    </div>
    
    <div v-else-if="villages.length === 0" class="text-center py-10">
      <el-empty description="暂无乡村数据" />
    </div>
    
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="village in villages" :key="village.id" class="village-card">
        <el-card class="h-full flex flex-col" shadow="hover">
          <div class="village-image mb-4">
            <img :src="village.coverImage" alt="村庄图片" class="w-full h-48 object-cover rounded">
          </div>
          <h3 class="text-xl font-bold mb-2">{{ village.name }}</h3>
          <p class="text-gray-500 mb-2">{{ village.region }}</p>
          <p class="text-sm text-gray-600 mb-4 flex-grow">{{ village.description }}</p>
          <div class="flex justify-between items-center">
            <el-rate v-model="village.rating" disabled text-color="#ff9900" />
            <router-link :to="`/villages/${village.id}`">
              <el-button type="primary" size="small">查看详情</el-button>
            </router-link>
          </div>
        </el-card>
      </div>
    </div>
    
    <!-- 分页 -->
    <div class="pagination-container flex justify-center mt-8">
      <el-pagination
        :current-page="currentPage"
        :page-size="pageSize"
        :page-sizes="[12, 24, 36, 48]"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

// 搜索和筛选参数
const searchQuery = ref('')
const regionFilter = ref('')

// 分页参数
const currentPage = ref(1)
const pageSize = ref(12)
const total = ref(0)

// 数据加载状态
const loading = ref(true)

// 村庄数据
const villages = ref([])

// 生命周期钩子
onMounted(() => {
  fetchVillages()
})

// 获取村庄数据
// 在script setup中添加API导入
import { getVillageList } from '@/api/villages'

// 修改fetchVillages函数
const fetchVillages = async () => {
  loading.value = true
  
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value,
      search: searchQuery.value,
      region: regionFilter.value
    }
    
    const res = await getVillageList(params)
    if (res.code === 200) {
      villages.value = res.data.results || []
      total.value = res.data.count || 0
    } else {
      ElMessage.error(res.message || '获取乡村数据失败')
    }
  } catch (error) {
    console.error('获取乡村数据失败:', error)
    ElMessage.error('获取乡村数据失败')
  } finally {
    loading.value = false
  }
}

// 搜索村庄
const searchVillages = () => {
  currentPage.value = 1
  fetchVillages()
}

// 重置筛选条件
const resetFilters = () => {
  searchQuery.value = ''
  regionFilter.value = ''
  currentPage.value = 1
  fetchVillages()
}

// 处理每页数量变化
const handleSizeChange = (val) => {
  pageSize.value = val
  fetchVillages()
}

// 处理页码变化
const handleCurrentChange = (val) => {
  currentPage.value = val
  fetchVillages()
}
</script>

<style scoped>
.village-card {
  transition: transform 0.3s ease;
}

.village-card:hover {
  transform: translateY(-5px);
}
</style>