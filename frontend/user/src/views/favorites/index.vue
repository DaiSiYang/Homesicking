<template>
  <div class="page-container py-8 bg-warm-gray-50">
    <div class="max-w-6xl mx-auto px-4">
      <!-- 页面标题区域 -->
      <div class="mb-8 border-b border-warm-gray-200 pb-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center">
            <div class="ink-border mr-4">
              <h1 class="text-2xl font-bold text-earth-800">我的收藏</h1>
            </div>
            <p class="text-warm-gray-600">珍藏您喜爱的乡村美景与特产</p>
          </div>
          <div class="bamboo-pattern p-1 rounded-lg">
            <el-select 
              v-model="activeTab" 
              @change="fetchFavorites" 
              class="w-32 bg-white rounded-md"
              placeholder="选择分类"
            >
              <el-option label="全部收藏" value="all" />
              <el-option label="乡村风光" value="village" />
              <el-option label="特色民宿" value="homestay" />
              <el-option label="乡村特产" value="product" />
              <el-option label="地方美食" value="food" />
            </el-select>
          </div>
        </div>
      </div>
      
      <!-- 内容区域 -->
      <div v-loading="loading" class="min-h-96">
        <!-- 空状态 -->
        <div v-if="favorites.length === 0" class="text-center py-16 bg-warm-gray-100 rounded-lg shadow-inner">
          <!-- 替换这里的img标签为Element Plus的图标组件 -->
          <el-empty 
            description="" 
            :image-size="128" 
            class="mb-4"
          >
            <template #image>
              <el-icon :size="64" class="text-warm-gray-400 mb-2">
                <Star />
              </el-icon>
            </template>
          </el-empty>
          <p class="text-warm-gray-600 mb-4">您还没有收藏任何内容</p>
          <el-button type="primary" class="bg-earth-700 hover:bg-earth-800" @click="goExplore">去探索乡村之美</el-button>
        </div>
        
        <!-- 收藏列表 -->
        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div 
            v-for="item in favorites" 
            :key="item.id" 
            class="bg-white rounded-lg overflow-hidden shadow-md hover:shadow-lg transition-shadow duration-300 border border-warm-gray-200"
          >
            <!-- 图片区域 -->
            <div class="relative overflow-hidden group">
              <img 
                :src="item.image || item.cover_image" 
                :alt="item.name || item.title" 
                class="w-full h-52 object-cover transition-transform duration-500 group-hover:scale-105"
              >
              
              <!-- 类型标签 -->
              <div class="absolute top-3 right-3 z-10">
                <div class="bamboo-pattern p-0.5 rounded">
                  <el-tag 
                    :type="getTypeColor(item.content_type)" 
                    size="small" 
                    class="border-0 text-xs font-medium"
                  >
                    {{ getTypeName(item.content_type) }}
                  </el-tag>
                </div>
              </div>
              
              <!-- 操作按钮 -->
              <div class="absolute top-0 left-0 w-full h-full bg-black bg-opacity-0 group-hover:bg-opacity-20 transition-all duration-300 flex items-center justify-center opacity-0 group-hover:opacity-100">
                <el-button 
                  type="danger" 
                  size="small" 
                  circle 
                  class="mr-2 bg-white bg-opacity-90"
                  @click.stop="handleRemoveFavorite(item.id, item.content_type)"
                >
                  <el-icon><Delete /></el-icon>
                </el-button>
                <el-button 
                  type="primary" 
                  size="small" 
                  class="bg-earth-700 hover:bg-earth-800 border-0"
                  @click.stop="viewDetail(item)"
                >
                  查看详情
                </el-button>
              </div>
            </div>
            
            <!-- 内容区域 -->
            <div class="p-4">
              <h3 
                class="text-lg font-medium mb-2 line-clamp-1 text-earth-900 cursor-pointer hover:text-earth-700"
                @click="viewDetail(item)"
              >
                {{ item.name || item.title }}
              </h3>
              
              <p class="text-warm-gray-600 text-sm mb-3 line-clamp-2 h-10">
                {{ item.description || item.content || '探索乡村之美，品味自然生活' }}
              </p>
              
              <!-- 价格/评分区域 -->
              <div class="flex justify-between items-center border-t border-warm-gray-100 pt-3 mt-2">
                <div v-if="item.price" class="text-red-600 font-bold">
                  <span class="text-xs">¥</span>{{ item.price }}
                </div>
                <div v-else-if="item.rating" class="flex items-center">
                  <el-rate v-model="item.rating" disabled size="small" />
                  <span class="ml-1 text-xs text-warm-gray-500">({{ item.rating }})</span>
                </div>
                <div v-else class="text-xs text-warm-gray-500">
                  <i class="el-icon-view mr-1"></i>{{ item.views || 0 }} 浏览
                </div>
                
                <div class="text-xs text-warm-gray-400">
                  {{ formatDate(item.created_at) }}
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 分页 -->
        <div v-if="total > pageSize" class="flex justify-center mt-8">
          <el-pagination
            v-model:current-page="currentPage"
            v-model:page-size="pageSize"
            :total="total"
            :page-sizes="[12, 24, 48]"
            layout="total, sizes, prev, pager, next, jumper"
            @current-change="fetchFavorites"
            @size-change="fetchFavorites"
            background
            class="pagination-earth"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Delete, Star } from '@element-plus/icons-vue'
import { getFavoriteList, removeFavorite } from '@/api/favorites'
import { useRouter } from 'vue-router'

const router = useRouter()

const loading = ref(false)
const activeTab = ref('all')
const favorites = ref([])
const currentPage = ref(1)
const pageSize = ref(12)
const total = ref(0)

// 获取收藏列表
const fetchFavorites = async () => {
  try {
    loading.value = true
    const params = {
      page: currentPage.value,
      page_size: pageSize.value
    }
    if (activeTab.value !== 'all') {
      params.content_type = activeTab.value
    }
    
    const response = await getFavoriteList(params)
    favorites.value = response.data.results || response.data
    total.value = response.data.count || 0
  } catch (error) {
    console.error('获取收藏列表失败:', error)
    ElMessage.error('获取收藏列表失败')
  } finally {
    loading.value = false
  }
}

// 移除收藏
const handleRemoveFavorite = async (id, type) => {
  try {
    await ElMessageBox.confirm('确定要取消收藏吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await removeFavorite(id, type)
    ElMessage.success('已取消收藏')
    fetchFavorites()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('取消收藏失败:', error)
      ElMessage.error('取消收藏失败')
    }
  }
}

// 查看详情
const viewDetail = (item) => {
  const routeMap = {
    village: '/villages',
    homestay: '/homestays',
    product: '/products',
    food: '/foods'
  }
  const basePath = routeMap[item.content_type]
  if (basePath) {
    router.push(`${basePath}/${item.content_id || item.id}`)
  }
}

// 获取类型颜色
const getTypeColor = (type) => {
  const colorMap = {
    village: 'success',
    homestay: 'primary',
    product: 'warning',
    food: 'danger'
  }
  return colorMap[type] || 'info'
}

// 获取类型名称
const getTypeName = (type) => {
  const nameMap = {
    village: '乡村',
    homestay: '民宿',
    product: '特产',
    food: '美食'
  }
  return nameMap[type] || '未知'
}

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

// 去探索
const goExplore = () => {
  router.push('/')
}

onMounted(() => {
  fetchFavorites()
})
</script>

<style scoped>
/* 水墨边框效果 */
.ink-border {
  position: relative;
  display: inline-block;
  padding: 0 0.5rem;
}

.ink-border::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, rgba(0,0,0,0), rgba(0,0,0,0.7), rgba(0,0,0,0));
}

/* 竹纹背景 */
.bamboo-pattern {
  background-color: rgba(245, 245, 240, 0.8);
  background-image: linear-gradient(rgba(76, 125, 76, 0.05) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(76, 125, 76, 0.05) 1px, transparent 1px);
  background-size: 20px 20px;
  background-position: center center;
}

/* 自定义分页样式 */
.pagination-earth :deep(.el-pager li.is-active) {
  background-color: #5c6f52;
  color: white;
}

.pagination-earth :deep(.el-pager li:hover) {
  color: #5c6f52;
}

/* 暖色背景 */
.bg-warm-gray-50 {
  background-color: #f7f3ed;
}

.bg-warm-gray-100 {
  background-color: #f0ebe4;
}

.text-warm-gray-400 {
  color: #9c9389;
}

.text-warm-gray-500 {
  color: #857f77;
}

.text-warm-gray-600 {
  color: #6e6860;
}

.border-warm-gray-100 {
  border-color: #f0ebe4;
}

.border-warm-gray-200 {
  border-color: #e5dfd6;
}

.text-earth-700 {
  color: #5c6f52;
}

.text-earth-800 {
  color: #4a5a43;
}

.text-earth-900 {
  color: #384433;
}

.bg-earth-700 {
  background-color: #5c6f52;
}

.hover\:bg-earth-800:hover {
  background-color: #4a5a43;
}
</style>