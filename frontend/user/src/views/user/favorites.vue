<template>
  <div class="favorites-container">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-content">
        <div class="title-section">
          <h1 class="page-title">
            <el-icon class="title-icon"><Star /></el-icon>
            我的收藏
          </h1>
          <p class="page-subtitle">珍藏美好的乡村记忆</p>
        </div>
        
        <div class="header-stats">
          <div class="stat-card">
            <span class="stat-number">{{ totalFavorites }}</span>
            <span class="stat-label">总收藏</span>
          </div>
          <div class="stat-card">
            <span class="stat-number">{{ recentlyAdded }}</span>
            <span class="stat-label">本月新增</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 筛选和搜索区域 -->
    <div class="filter-section">
      <div class="filter-tabs">
        <el-segmented v-model="activeTab" :options="tabOptions" @change="handleTabChange" size="large" />
      </div>
      
      <div class="search-and-sort">
        <el-input
          v-model="searchKeyword"
          placeholder="搜索收藏内容..."
          prefix-icon="Search"
          clearable
          size="large"
          class="search-input"
          @input="handleSearch"
        />
        
        <el-select v-model="sortBy" placeholder="排序方式" size="large" class="sort-select">
          <el-option label="最近收藏" value="recent" />
          <el-option label="价格从低到高" value="price_asc" />
          <el-option label="价格从高到低" value="price_desc" />
          <el-option label="评分最高" value="rating" />
        </el-select>
      </div>
    </div>

    <!-- 收藏内容 -->
    <div class="favorites-content">
      <!-- 加载状态 -->
      <div v-if="loading" class="loading-container">
        <div class="loading-grid">
          <el-skeleton v-for="i in 8" :key="i" animated class="skeleton-card">
            <template #template>
              <el-skeleton-item variant="image" style="width: 100%; height: 200px; border-radius: 12px;" />
              <div style="padding: 20px;">
                <el-skeleton-item variant="h3" style="width: 80%; margin-bottom: 10px;" />
                <el-skeleton-item variant="text" style="width: 100%; margin-bottom: 8px;" />
                <el-skeleton-item variant="text" style="width: 60%;" />
              </div>
            </template>
          </el-skeleton>
        </div>
      </div>

      <!-- 空状态 -->
      <div v-else-if="filteredFavorites.length === 0" class="empty-state">
        <div class="empty-illustration">
          <el-icon :size="80"><Star /></el-icon>
        </div>
        <h3 class="empty-title">{{ getEmptyTitle() }}</h3>
        <p class="empty-description">{{ getEmptyDescription() }}</p>
        <el-button type="primary" size="large" @click="goToExplore" class="explore-btn">
          <el-icon><Compass /></el-icon>
          开始探索
        </el-button>
      </div>

      <!-- 收藏网格 -->
      <div v-else class="favorites-grid">
        <div 
          v-for="item in paginatedFavorites" 
          :key="item.id" 
          class="favorite-card"
          @click="viewDetail(item)"
        >
          <div class="card-image">
            <img :src="item.coverImage" :alt="item.name" />
            <div class="image-overlay">
              <el-button 
                type="danger" 
                circle 
                @click.stop="removeFavoriteItem(item)"
                class="remove-btn"
              >
                <el-icon><Delete /></el-icon>
              </el-button>
            </div>
            <el-tag :type="getTagType(item.type)" class="type-tag">{{ getTypeName(item.type) }}</el-tag>
          </div>
          
          <div class="card-content">
            <h3 class="item-title">{{ item.name }}</h3>
            <p class="item-description">{{ item.description }}</p>
            
            <div class="item-meta">
              <div v-if="item.location" class="location">
                <el-icon><MapPin /></el-icon>
                <span>{{ item.location }}</span>
              </div>
              <div class="favorite-date">
                <el-icon><Clock /></el-icon>
                <span>{{ formatDate(item.favoriteDate) }}</span>
              </div>
            </div>
            
            <div class="card-footer">
              <div class="price-rating">
                <div v-if="item.price" class="price">
                  <span class="currency">¥</span>
                  <span class="amount">{{ item.price }}</span>
                </div>
                <div v-if="item.rating" class="rating">
                  <el-rate v-model="item.rating" disabled size="small" />
                  <span class="rating-text">({{ item.reviewCount }})</span>
                </div>
              </div>
              
              <el-button type="primary" text class="view-btn">
                查看详情
                <el-icon><ArrowRight /></el-icon>
              </el-button>
            </div>
          </div>
        </div>
      </div>

      <!-- 分页 -->
      <div v-if="filteredFavorites.length > pageSize" class="pagination-wrapper">
        <el-pagination
          v-model:current-page="currentPage"
          :page-size="pageSize"
          :total="filteredFavorites.length"
          layout="prev, pager, next, jumper"
          background
          @current-change="handlePageChange"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  Star, 
  Delete, 
  Search, 
  MapPin, 
  Clock, 
  ArrowRight, 
  Compass 
} from '@element-plus/icons-vue'

const router = useRouter()

// 响应式数据
const loading = ref(false)
const searchKeyword = ref('')
const activeTab = ref('all')
const sortBy = ref('recent')
const currentPage = ref(1)
const pageSize = 12

// 标签选项
const tabOptions = [
  { label: '全部', value: 'all' },
  { label: '乡村', value: 'village' },
  { label: '民宿', value: 'homestay' },
  { label: '特产', value: 'product' },
  { label: '美食', value: 'food' }
]

// 统计数据
const totalFavorites = ref(28)
const recentlyAdded = ref(5)

// 收藏数据
const favorites = ref([
  {
    id: 1,
    name: '篁岭古村',
    type: 'village',
    description: '中国最美乡村，梯田花海，徽派建筑',
    coverImage: 'https://picsum.photos/id/1015/400/300',
    location: '江西婺源',
    rating: 4.8,
    reviewCount: 1234,
    favoriteDate: '2024-01-15',
    price: null
  },
  {
    id: 2,
    name: '云端竹舍民宿',
    type: 'homestay',
    description: '隐于竹林深处的精品民宿，享受宁静时光',
    coverImage: 'https://picsum.photos/id/1018/400/300',
    location: '浙江安吉',
    rating: 4.9,
    reviewCount: 567,
    favoriteDate: '2024-01-10',
    price: 688
  },
  {
    id: 3,
    name: '婺源贡菊',
    type: 'product',
    description: '天然有机贡菊，清香甘甜，养生佳品',
    coverImage: 'https://picsum.photos/id/1060/400/300',
    location: '江西婺源',
    rating: 4.7,
    reviewCount: 890,
    favoriteDate: '2024-01-08',
    price: 68
  },
  {
    id: 4,
    name: '徽州毛豆腐',
    type: 'food',
    description: '传统徽州名菜，外酥内嫩，回味无穷',
    coverImage: 'https://picsum.photos/id/1080/400/300',
    location: '安徽黄山',
    rating: 4.6,
    reviewCount: 456,
    favoriteDate: '2024-01-05',
    price: 38
  }
  // 可以添加更多数据...
])

// 计算属性
const filteredFavorites = computed(() => {
  let result = favorites.value
  
  // 按类型筛选
  if (activeTab.value !== 'all') {
    result = result.filter(item => item.type === activeTab.value)
  }
  
  // 按关键词搜索
  if (searchKeyword.value) {
    const keyword = searchKeyword.value.toLowerCase()
    result = result.filter(item => 
      item.name.toLowerCase().includes(keyword) ||
      item.description.toLowerCase().includes(keyword) ||
      item.location.toLowerCase().includes(keyword)
    )
  }
  
  // 排序
  result.sort((a, b) => {
    switch (sortBy.value) {
      case 'recent':
        return new Date(b.favoriteDate) - new Date(a.favoriteDate)
      case 'price_asc':
        return (a.price || 0) - (b.price || 0)
      case 'price_desc':
        return (b.price || 0) - (a.price || 0)
      case 'rating':
        return (b.rating || 0) - (a.rating || 0)
      default:
        return 0
    }
  })
  
  return result
})

const paginatedFavorites = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  const end = start + pageSize
  return filteredFavorites.value.slice(start, end)
})

// 方法
const handleTabChange = (value) => {
  activeTab.value = value
  currentPage.value = 1
}

const handleSearch = () => {
  currentPage.value = 1
}

const handlePageChange = (page) => {
  currentPage.value = page
  // 滚动到顶部
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const getTagType = (type) => {
  const typeMap = {
    village: 'success',
    homestay: 'primary',
    product: 'warning',
    food: 'danger'
  }
  return typeMap[type] || ''
}

const getTypeName = (type) => {
  const nameMap = {
    village: '乡村',
    homestay: '民宿',
    product: '特产',
    food: '美食'
  }
  return nameMap[type] || '其他'
}

const getEmptyTitle = () => {
  if (activeTab.value === 'all') {
    return searchKeyword.value ? '没有找到相关收藏' : '还没有收藏内容'
  }
  return `暂无${getTypeName(activeTab.value)}收藏`
}

const getEmptyDescription = () => {
  if (searchKeyword.value) {
    return '试试其他关键词或浏览推荐内容'
  }
  return '发现心仪的乡村体验，开始收藏吧'
}

const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  const now = new Date()
  const diff = now - date
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  
  if (days === 0) return '今天'
  if (days === 1) return '昨天'
  if (days < 7) return `${days}天前`
  if (days < 30) return `${Math.floor(days / 7)}周前`
  return date.toLocaleDateString()
}

const viewDetail = (item) => {
  const routeMap = {
    village: '/villages',
    homestay: '/homestays',
    product: '/products',
    food: '/foods'
  }
  const basePath = routeMap[item.type] || '/'
  router.push(`${basePath}/${item.id}`)
}

const removeFavoriteItem = async (item) => {
  try {
    await ElMessageBox.confirm(
      `确定要取消收藏「${item.name}」吗？`,
      '取消收藏',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    // 这里应该调用API删除收藏
    const index = favorites.value.findIndex(f => f.id === item.id)
    if (index > -1) {
      favorites.value.splice(index, 1)
      totalFavorites.value--
      ElMessage.success('已取消收藏')
    }
  } catch {
    // 用户取消操作
  }
}

const goToExplore = () => {
  router.push('/')
}

// 生命周期
onMounted(() => {
  // 这里可以调用API获取收藏数据
  console.log('收藏页面已加载')
})
</script>

<style scoped>
.favorites-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  min-height: 100vh;
}

/* 页面头部 */
.page-header {
  margin-bottom: 30px;
}

.header-content {
  background: white;
  border-radius: 20px;
  padding: 40px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.title-section {
  flex: 1;
}

.page-title {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 32px;
  font-weight: 700;
  margin: 0 0 8px;
  color: #2c3e50;
}

.title-icon {
  color: #f39c12;
  font-size: 36px;
}

.page-subtitle {
  font-size: 16px;
  color: #7f8c8d;
  margin: 0;
}

.header-stats {
  display: flex;
  gap: 30px;
}

.stat-card {
  text-align: center;
  padding: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 15px;
  color: white;
  min-width: 100px;
}

.stat-number {
  display: block;
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 14px;
  opacity: 0.9;
}

/* 筛选区域 */
.filter-section {
  background: white;
  border-radius: 15px;
  padding: 25px;
  margin-bottom: 30px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
}

.filter-tabs {
  margin-bottom: 20px;
  display: flex;
  justify-content: center;
}

.search-and-sort {
  display: flex;
  gap: 15px;
  align-items: center;
}

.search-input {
  flex: 1;
  max-width: 400px;
}

.sort-select {
  width: 150px;
}

/* 内容区域 */
.favorites-content {
  background: white;
  border-radius: 15px;
  padding: 30px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
}

/* 加载状态 */
.loading-container {
  padding: 20px 0;
}

.loading-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 25px;
}

.skeleton-card {
  border-radius: 15px;
  overflow: hidden;
}

/* 空状态 */
.empty-state {
  text-align: center;
  padding: 80px 20px;
}

.empty-illustration {
  color: #d1d5db;
  margin-bottom: 20px;
}

.empty-title {
  font-size: 24px;
  font-weight: 600;
  color: #374151;
  margin: 0 0 10px;
}

.empty-description {
  font-size: 16px;
  color: #6b7280;
  margin: 0 0 30px;
}

.explore-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  border-radius: 25px;
  padding: 12px 30px;
  font-size: 16px;
}

/* 收藏网格 */
.favorites-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 25px;
  margin-bottom: 40px;
}

.favorite-card {
  background: white;
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  cursor: pointer;
  border: 1px solid #f0f0f0;
}

.favorite-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
}

.card-image {
  position: relative;
  height: 220px;
  overflow: hidden;
}

.card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.favorite-card:hover .card-image img {
  transform: scale(1.05);
}

.image-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.favorite-card:hover .image-overlay {
  opacity: 1;
}

.remove-btn {
  background: rgba(255, 255, 255, 0.9);
  border: none;
  color: #e74c3c;
}

.remove-btn:hover {
  background: white;
  transform: scale(1.1);
}

.type-tag {
  position: absolute;
  top: 12px;
  left: 12px;
  z-index: 2;
  font-weight: 600;
}

.card-content {
  padding: 20px;
}

.item-title {
  font-size: 18px;
  font-weight: 600;
  color: #2c3e50;
  margin: 0 0 8px;
  line-height: 1.3;
}

.item-description {
  color: #7f8c8d;
  font-size: 14px;
  line-height: 1.5;
  margin: 0 0 15px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.item-meta {
  display: flex;
  gap: 15px;
  margin-bottom: 15px;
  font-size: 12px;
  color: #95a5a6;
}

.location, .favorite-date {
  display: flex;
  align-items: center;
  gap: 4px;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.price {
  display: flex;
  align-items: baseline;
  gap: 2px;
}

.currency {
  font-size: 14px;
  color: #e74c3c;
  font-weight: 500;
}

.amount {
  font-size: 20px;
  font-weight: 700;
  color: #e74c3c;
}

.rating {
  display: flex;
  align-items: center;
  gap: 5px;
}

.rating-text {
  font-size: 12px;
  color: #95a5a6;
}

.view-btn {
  color: #667eea;
  font-weight: 600;
}

.view-btn:hover {
  color: #5a67d8;
}

/* 分页 */
.pagination-wrapper {
  display: flex;
  justify-content: center;
  padding-top: 20px;
  border-top: 1px solid #f0f0f0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .favorites-container {
    padding: 10px;
  }
  
  .header-content {
    flex-direction: column;
    gap: 20px;
    padding: 30px 20px;
  }
  
  .header-stats {
    width: 100%;
    justify-content: center;
  }
  
  .search-and-sort {
    flex-direction: column;
  }
  
  .search-input {
    max-width: none;
  }
  
  .favorites-grid {
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 20px;
  }
  
  .filter-tabs {
    overflow-x: auto;
    padding-bottom: 10px;
  }
}

@media (max-width: 480px) {
  .favorites-grid {
    grid-template-columns: 1fr;
  }
  
  .page-title {
    font-size: 24px;
  }
  
  .stat-card {
    padding: 15px;
    min-width: 80px;
  }
  
  .stat-number {
    font-size: 20px;
  }
}
</style>