<template>
  <div class="homestays-container container mx-auto py-8 px-4">
    <h1 class="text-3xl font-bold mb-8 text-center">特色民宿</h1>
    
    <!-- 搜索和筛选区域 -->
    <div class="search-filter-container mb-8 bg-gray-50 p-4 rounded-lg">
      <el-form :inline="true" class="flex flex-wrap items-center">
        <el-form-item label="关键词">
          <el-input v-model="searchQuery" placeholder="搜索民宿名称" />
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
        <el-form-item label="价格">
          <el-select v-model="priceFilter" placeholder="价格范围">
            <el-option label="全部价格" value="" />
            <el-option label="¥0-200" value="0-200" />
            <el-option label="¥200-400" value="200-400" />
            <el-option label="¥400-600" value="400-600" />
            <el-option label="¥600-800" value="600-800" />
            <el-option label="¥800以上" value="800+" />
          </el-select>
        </el-form-item>
        <el-form-item label="评分">
          <el-select v-model="ratingFilter" placeholder="最低评分">
            <el-option label="全部评分" value="" />
            <el-option label="4.5分以上" value="4.5" />
            <el-option label="4分以上" value="4" />
            <el-option label="3.5分以上" value="3.5" />
            <el-option label="3分以上" value="3" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="searchHomestays">搜索</el-button>
          <el-button @click="resetFilters">重置</el-button>
        </el-form-item>
      </el-form>
    </div>
    
    <!-- 民宿列表 -->
    <div v-if="loading" class="flex justify-center py-10">
      <el-skeleton :rows="10" animated />
    </div>
    
    <div v-else-if="homestays.length === 0" class="text-center py-10">
      <el-empty description="暂无符合条件的民宿" />
    </div>
    
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="homestay in homestays" :key="homestay.id" class="homestay-card">
        <el-card class="h-full flex flex-col" shadow="hover">
          <div class="homestay-image relative mb-4">
            <img :src="cleanImageUrl(homestay.cover_image)" alt="民宿图片" class="w-full h-48 object-cover rounded" @error="handleImageError">
            <span v-if="homestay.is_featured" class="absolute top-2 left-2 bg-red-500 text-white text-xs px-2 py-1 rounded">特色民宿</span>
          </div>
          <h3 class="text-xl font-bold mb-2">{{ homestay.name }}</h3>
          <p class="text-gray-500 mb-2 text-sm">{{ homestay.village_name }} | {{ homestay.property_type }}</p>
          <div class="flex items-center mb-2">
            <el-rate :model-value="parseFloat(homestay.rating)" disabled text-color="#ff9900" />
            <span class="ml-2 text-orange-500 text-sm">{{ homestay.rating }}分</span>
          </div>
          <p class="text-sm text-gray-600 mb-4 flex-grow line-clamp-2">{{ homestay.intro }}</p>
          <div class="flex justify-between items-center">
            <div>
              <span class="text-red-500 font-bold">¥{{ homestay.lowest_price }}</span>
              <span class="text-gray-500 text-xs">起/晚</span>
            </div>
            <router-link :to="`/homestays/${homestay.id}`">
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
const priceFilter = ref('')
const ratingFilter = ref('')

// 分页参数
const currentPage = ref(1)
const pageSize = ref(12)
const total = ref(0)

// 数据加载状态
const loading = ref(true)

// 民宿数据
const homestays = ref([])

// 生命周期钩子
onMounted(() => {
  fetchHomestays()
})

// 获取民宿数据
// 在script setup中添加API导入
import { getHomestayList } from '@/api/homestays'

// 修改fetchHomestays函数
const fetchHomestays = async () => {
  loading.value = true
  
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value,
      search: searchQuery.value,
      region: regionFilter.value,
      price_range: priceFilter.value,
      min_rating: ratingFilter.value
    }
    
    const res = await getHomestayList(params)
    if (res.code === 200) {
      // 清理数据中的额外字符
      homestays.value = (res.data.results || []).map(homestay => ({
        ...homestay,
        cover_image: cleanImageUrl(homestay.cover_image)
      }))
      total.value = res.data.count || 0
    } else {
      ElMessage.error(res.message || '获取民宿数据失败')
    }
  } catch (error) {
    console.error('获取民宿数据失败:', error)
    ElMessage.error('获取民宿数据失败')
  } finally {
    loading.value = false
  }
}

// 清理图片URL的函数
const cleanImageUrl = (url) => {
  if (!url) return ''
  return url.replace(/[`\s]/g, '').trim()
}

// 图片加载错误处理
const handleImageError = (event) => {
  event.target.src = '/images/default-homestay.jpg' // 设置默认图片
}

// 搜索民宿
const searchHomestays = () => {
  currentPage.value = 1
  fetchHomestays()
}

// 重置筛选条件
const resetFilters = () => {
  searchQuery.value = ''
  regionFilter.value = ''
  priceFilter.value = ''
  ratingFilter.value = ''
  currentPage.value = 1
  fetchHomestays()
}

// 处理每页数量变化
const handleSizeChange = (val) => {
  pageSize.value = val
  fetchHomestays()
}

// 处理页码变化
const handleCurrentChange = (val) => {
  currentPage.value = val
  fetchHomestays()
}
</script>

<style scoped>
.homestay-card {
  transition: transform 0.3s ease;
}

.homestay-card:hover {
  transform: translateY(-5px);
}
</style>