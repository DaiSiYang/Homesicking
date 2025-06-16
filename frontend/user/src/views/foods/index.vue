<template>
  <div class="foods-container container mx-auto py-8 px-4">
    <h1 class="text-3xl font-bold mb-8 text-center">乡村特色美食</h1>
    
    <!-- 搜索和筛选区域 -->
    <div class="search-filter-container mb-8 bg-gray-50 p-4 rounded-lg">
      <el-form :inline="true" class="flex flex-wrap items-center">
        <el-form-item label="关键词">
          <el-input v-model="searchQuery" placeholder="搜索美食名称" />
        </el-form-item>
        <el-form-item label="分类">
          <el-select v-model="categoryFilter" placeholder="选择分类">
            <el-option label="全部分类" value="" />
            <el-option label="特色小吃" value="特色小吃" />
            <el-option label="农家菜" value="农家菜" />
            <el-option label="地方名菜" value="地方名菜" />
            <el-option label="风味甜点" value="风味甜点" />
            <el-option label="传统主食" value="传统主食" />
          </el-select>
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
          <el-button type="primary" @click="searchFoods">搜索</el-button>
          <el-button @click="resetFilters">重置</el-button>
        </el-form-item>
      </el-form>
    </div>
    
    <!-- 美食列表 -->
    <div v-if="loading" class="flex justify-center py-10">
      <el-skeleton :rows="10" animated />
    </div>
    
    <div v-else-if="foods.length === 0" class="text-center py-10">
      <el-empty description="暂无美食数据" />
    </div>
    
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="food in foods" :key="food.id" class="food-card">
        <el-card class="h-full flex flex-col" shadow="hover">
          <div class="food-image mb-4 relative">
            <img :src="food.cover_image || food.coverImage" alt="美食图片" class="w-full h-48 object-cover rounded">
            <div v-if="food.isPopular" class="absolute top-2 right-2 bg-red-500 text-white px-2 py-1 rounded text-sm">
              人气美食
            </div>
          </div>
          <h3 class="text-xl font-bold mb-2">{{ food.name }}</h3>
          <div class="flex items-center mb-2">
            <el-rate v-model="food.rating" disabled text-color="#ff9900" />
            <span class="ml-2 text-orange-500">{{ food.rating }}分</span>
          </div>
          <p class="text-gray-500 mb-2">{{ food.category }} | {{ food.region }}</p>
          <p class="text-sm text-gray-600 mb-4 flex-grow">{{ food.description }}</p>
          <div class="tags mb-4">
            <el-tag v-for="(tag, index) in food.tags" :key="index" size="small" class="mr-1 mb-1">
              {{ tag }}
            </el-tag>
          </div>
          <div class="flex justify-between items-center">
            <span class="price text-red-500 font-bold">¥{{ food.price }}/人</span>
            <router-link :to="`/foods/${food.id}`">
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
import { ref, onMounted, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { getFoodList } from '@/api/foods'

// 搜索和筛选参数
const searchQuery = ref('')
const categoryFilter = ref('') // 添加这个变量
const regionFilter = ref('') // 添加这个变量
const activeCategory = ref('all')
const selectedRegion = ref('all')

// 分页参数
const currentPage = ref(1)
const pageSize = ref(12)
const total = ref(0)

// 数据加载状态
const loading = ref(true)

// 美食数据
const foods = ref([])

// 分类数据
const categories = ref([
  { id: 'all', name: '全部' },
  { id: 'snack', name: '特色小吃' },
  { id: 'dish', name: '传统菜肴' },
  { id: 'dessert', name: '甜品糕点' },
  { id: 'drink', name: '饮品茶酒' }
])

// 地区数据
const regions = ref([
  { id: 'all', name: '全部地区' },
  { id: 'east', name: '华东' },
  { id: 'south', name: '华南' },
  { id: 'west', name: '华西' },
  { id: 'north', name: '华北' }
])

// 获取美食数据
const fetchFoods = async () => {
  loading.value = true
  
  try {
    const params = {
      page: currentPage.value,
      limit: pageSize.value,
      category: activeCategory.value === 'all' ? undefined : activeCategory.value,
      region: selectedRegion.value === 'all' ? undefined : selectedRegion.value,
      keyword: searchQuery.value
    }
    
    const res = await getFoodList(params)
    if (res.code === 200) {
      foods.value = res.data.results || []
      total.value = res.data.count || 0
    } else {
      ElMessage.error(res.message || '获取美食数据失败')
    }
  } catch (error) {
    console.error('获取美食数据失败:', error)
    ElMessage.error('获取美食数据失败')
  } finally {
    loading.value = false
  }
}

// 搜索美食
const searchFoods = () => {
  currentPage.value = 1
  fetchFoods()
}

// 切换分类
const handleCategoryChange = (category) => {
  activeCategory.value = category
  currentPage.value = 1
  fetchFoods()
}

// 切换地区
const handleRegionChange = (region) => {
  selectedRegion.value = region
  currentPage.value = 1
  fetchFoods()
}

// 分页变化
const handleCurrentChange = (page) => {
  currentPage.value = page
  fetchFoods()
}

// 添加缺失的 handleSizeChange 函数
const handleSizeChange = (val) => {
  pageSize.value = val
  currentPage.value = 1
  fetchFoods()
}

// 重置筛选条件
const resetFilters = () => {
  searchQuery.value = ''
  categoryFilter.value = ''
  regionFilter.value = ''
  activeCategory.value = 'all'
  selectedRegion.value = 'all'
  currentPage.value = 1
  fetchFoods()
}

// 生命周期钩子
onMounted(() => {
  fetchFoods()
})

// 监听搜索变化
watch(searchQuery, () => {
  searchFoods()
})
</script>

<style scoped>
.food-card {
  transition: transform 0.3s ease;
}

.food-card:hover {
  transform: translateY(-5px);
}
</style>