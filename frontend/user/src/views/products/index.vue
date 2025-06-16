<template>
  <div class="products-container container mx-auto py-8 px-4">
    <h1 class="text-3xl font-bold mb-8 text-center">乡村特产</h1>
    
    <!-- 搜索和筛选区域 -->
    <div class="search-filter-container mb-8 bg-gray-50 p-4 rounded-lg">
      <el-form :inline="true" class="flex flex-wrap items-center">
        <el-form-item label="关键词">
          <el-input v-model="searchQuery" placeholder="搜索商品名称" />
        </el-form-item>
        <el-form-item label="分类">
          <el-select v-model="categoryFilter" placeholder="选择分类">
            <el-option label="全部分类" value="" />
            <el-option v-for="category in categories" :key="category.id" :label="category.name" :value="category.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="价格">
          <el-select v-model="priceFilter" placeholder="价格范围">
            <el-option label="全部价格" value="" />
            <el-option label="¥0-50" value="0-50" />
            <el-option label="¥50-100" value="50-100" />
            <el-option label="¥100-200" value="100-200" />
            <el-option label="¥200-500" value="200-500" />
            <el-option label="¥500以上" value="500+" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="searchProducts">搜索</el-button>
          <el-button @click="resetFilters">重置</el-button>
        </el-form-item>
      </el-form>
    </div>
    
    <!-- 分类标签 -->
    <div class="mb-8">
      <el-tabs v-model="activeCategory" @tab-click="handleCategoryChange">
        <el-tab-pane label="全部商品" name="all"></el-tab-pane>
        <el-tab-pane v-for="category in categories" :key="category.id" :label="category.name" :name="category.id.toString()"></el-tab-pane>
      </el-tabs>
    </div>
    
    <!-- 产品列表 -->
    <div v-if="loading" class="flex justify-center py-10">
      <el-skeleton :rows="10" animated />
    </div>
    
    <div v-else-if="products.length === 0" class="text-center py-10">
      <el-empty description="暂无符合条件的商品" />
    </div>
    
    <div v-else class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
      <div v-for="product in products" :key="product.id" class="product-card">
        <el-card class="h-full flex flex-col" shadow="hover" :body-style="{ padding: '0' }">
          <div class="relative">
            <img :src="product.cover_image || product.coverImage" alt="商品图片" class="w-full h-48 object-cover">
            <span v-if="product.isHot" class="absolute top-2 left-2 bg-red-500 text-white text-xs px-2 py-1 rounded">热卖</span>
            <span v-if="product.discount" class="absolute top-2 right-2 bg-orange-500 text-white text-xs px-2 py-1 rounded">{{ product.discount }}折</span>
          </div>
          <div class="p-4 flex flex-col flex-grow">
            <h3 class="text-base font-bold mb-2 line-clamp-2">{{ product.name }}</h3>
            <p class="text-gray-500 mb-2 text-xs">{{ product.origin }}</p>
            <p class="text-sm text-gray-600 mb-4 flex-grow line-clamp-2">{{ product.description }}</p>
            <div class="flex justify-between items-center">
              <div>
                <span class="text-red-500 font-bold">¥{{ product.price }}</span>
                <span v-if="product.originalPrice" class="text-gray-400 text-xs line-through ml-1">¥{{ product.originalPrice }}</span>
              </div>
              <el-button type="primary" size="small" @click="viewDetail(product.id)">查看详情</el-button>
            </div>
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
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getProductList, getProductCategories } from '@/api/products'

const router = useRouter()

// 搜索和筛选参数
const searchQuery = ref('')
const categoryFilter = ref('')
const priceFilter = ref('')
const activeCategory = ref('all')

// 分页参数
const currentPage = ref(1)
const pageSize = ref(12)
const total = ref(0)

// 数据加载状态
const loading = ref(true)

// 产品数据
const products = ref([])

// 分类数据
const categories = ref([
  { id: 1, name: '农产品' },
  { id: 2, name: '手工艺品' },
  { id: 3, name: '美食特产' },
  { id: 4, name: '茶叶' },
  { id: 5, name: '酒水' }
])

// 生命周期钩子
onMounted(() => {
  fetchCategories()
  fetchProducts()
})

// 获取产品数据
const fetchProducts = async () => {
  loading.value = true
  
  try {
    const params = {
      page: currentPage.value,
      limit: pageSize.value,
      category: activeCategory.value === 'all' ? undefined : activeCategory.value,
      keyword: searchQuery.value
    }
    
    const res = await getProductList(params)
    console.log('产品列表API返回数据:', res) // 添加调试日志
    
    if (res.code === 200) {
      products.value = res.data.results || []
      total.value = res.data.count || 0
      console.log('产品数据:', products.value) // 添加调试日志
    } else {
      ElMessage.error(res.message || '获取产品数据失败')
    }
  } catch (error) {
    console.error('获取产品数据失败:', error)
    ElMessage.error('获取产品数据失败')
  } finally {
    loading.value = false
  }
}

// 获取分类数据
const fetchCategories = async () => {
  try {
    const res = await getProductCategories()
    if (res.code === 200) {
      categories.value = [
        { id: 'all', name: '全部' },
        ...res.data
      ]
    }
  } catch (error) {
    console.error('获取分类数据失败:', error)
  }
}

// 搜索产品
const searchProducts = () => {
  currentPage.value = 1
  fetchProducts()
}

// 重置筛选条件
const resetFilters = () => {
  searchQuery.value = ''
  categoryFilter.value = ''
  priceFilter.value = ''
  activeCategory.value = 'all'
  currentPage.value = 1
  fetchProducts()
}

// 处理分类切换
const handleCategoryChange = (tab) => {
  categoryFilter.value = tab.name === 'all' ? '' : tab.name
  currentPage.value = 1
  fetchProducts()
}

// 处理每页数量变化
const handleSizeChange = (val) => {
  pageSize.value = val
  fetchProducts()
}

// 处理页码变化
const handleCurrentChange = (val) => {
  currentPage.value = val
  fetchProducts()
}

// 查看详情
const viewDetail = (id) => {
  if (!id) {
    ElMessage.error('商品ID无效')
    return
  }
  console.log('跳转到商品详情:', id) // 添加调试日志
  router.push(`/products/${id}`)
}
</script>

<style scoped>
.product-card {
  transition: transform 0.3s ease;
}

.product-card:hover {
  transform: translateY(-5px);
}
</style>