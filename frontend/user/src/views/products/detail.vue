<template>
  <div class="product-detail container mx-auto py-8 px-4">
    <!-- 加载状态 -->
    <div v-if="loading" class="flex justify-center py-10">
      <el-skeleton :rows="15" animated />
    </div>

    <div v-else-if="!product" class="text-center py-10">
      <el-empty description="未找到该产品信息" />
    </div>

    <template v-else>
      <!-- 面包屑导航 -->
      <el-breadcrumb class="mb-6">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item :to="{ path: '/products' }">特产</el-breadcrumb-item>
        <el-breadcrumb-item>{{ product.name }}</el-breadcrumb-item>
      </el-breadcrumb>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <!-- 左侧：产品图片 -->
        <div class="product-gallery">
          <el-carousel 
            :initial-index="currentImageIndex" 
            trigger="click" 
            indicator-position="outside" 
            height="400px"
            @change="handleCarouselChange"
          >
            <el-carousel-item v-for="(image, index) in displayGallery" :key="index">
              <img :src="getImageUrl(image)" :alt="getImageCaption(image)" class="w-full h-full object-cover rounded-lg">
            </el-carousel-item>
          </el-carousel>
          
          <div class="image-thumbnails flex mt-4 gap-2 overflow-x-auto">
            <div
              v-for="(image, index) in displayGallery"
              :key="`thumb-${index}`"
              class="w-20 h-20 flex-shrink-0 cursor-pointer border-2"
              :class="{'border-green-500': currentImageIndex === index, 'border-transparent': currentImageIndex !== index}"
              @click="currentImageIndex = index"
            >
              <img :src="getImageUrl(image)" :alt="getImageCaption(image)" class="w-full h-full object-cover">
            </div>
          </div>
        </div>
        
        <!-- 右侧：产品信息 -->
        <div class="product-info">
          <h1 class="text-2xl font-bold mb-2">{{ product.name }}</h1>
          <p class="text-gray-500 mb-4">{{ product.category }} | {{ product.origin }}</p>
          
          <div class="price-section mb-6 bg-gray-50 p-4 rounded-lg">
            <div class="flex items-center mb-2">
              <span class="text-gray-500 mr-2">价格:</span>
              <span class="text-red-500 text-3xl font-bold">¥{{ selectedSku ? selectedSku.price : product.price }}</span>
              <span v-if="selectedSku && selectedSku.originalPrice" class="text-gray-400 line-through text-sm ml-2">¥{{ selectedSku.originalPrice }}</span>
              <span v-if="product.discountRate" class="ml-2 bg-red-500 text-white px-2 py-1 rounded text-sm">
                {{ product.discountRate }}折
              </span>
            </div>
            <div class="flex items-center text-sm text-gray-500">
              <span class="mr-4">销量: {{ product.soldCount }}</span>
              <span>评分: {{ product.rating }}分</span>
            </div>
          </div>
          
          <div class="product-spec mb-6" v-if="product.specifications && Object.keys(product.specifications).length > 0">
            <div class="grid grid-cols-2 gap-4">
              <div v-for="(spec, key) in product.specifications" :key="key" class="spec-item">
                <span class="text-gray-500">{{ key }}:</span>
                <span class="ml-1">{{ spec }}</span>
              </div>
            </div>
          </div>
          
          <div class="quantity-section mb-6">
            <p class="text-gray-500 mb-2">数量:</p>
            <div class="flex items-center">
              <el-input-number v-model="quantity" :min="1" :max="selectedSku ? selectedSku.stock : product.stock" :step="1" />
              <span class="ml-2 text-gray-500">库存: {{ selectedSku ? selectedSku.stock : product.stock }}件</span>
            </div>
          </div>
          
          <div class="action-buttons flex gap-4 mb-6">
            <el-button 
              type="primary" 
              size="large" 
              @click="addToCart"
              :disabled="!product || loading"
            >
              加入购物车
            </el-button>
            <el-button 
              type="danger" 
              size="large" 
              @click="buyNow"
              :disabled="!product || loading"
            >
              立即购买
            </el-button>
            <el-button 
              :type="isFavorite ? 'default' : 'warning'"
              @click="toggleFavorite"
            >
              <el-icon><component :is="isFavorite ? 'Star' : 'StarFilled'" /></el-icon>
              {{ isFavorite ? '已收藏' : '收藏' }}
            </el-button>
          </div>
          
          <div class="service-section text-sm text-gray-500 border-t border-gray-200 pt-4">
            <p class="mb-1"><el-icon><Check /></el-icon> 全场包邮</p>
            <p class="mb-1"><el-icon><Check /></el-icon> 正品保障</p>
            <p><el-icon><Check /></el-icon> 七天无理由退换</p>
          </div>
        </div>
      </div>
      
      <!-- 产品详情 -->
      <div class="product-tabs mt-8" v-if="product">
        <el-tabs>
          <el-tab-pane label="产品详情">
            <div class="product-description mb-6">
              <h2 class="text-xl font-bold mb-4">产品介绍</h2>
              <div class="description-content text-gray-700 leading-relaxed whitespace-pre-line">
                {{ product.description || '暂无产品介绍' }}
              </div>
            </div>
            
            <div class="product-images" v-if="product.detailImages && product.detailImages.length > 0">
              <img 
                v-for="(image, index) in product.detailImages" 
                :key="index" 
                :src="image" 
                alt="产品详情图" 
                class="w-full mb-4 rounded-lg"
              >
            </div>
            <div v-else class="text-center py-8 text-gray-500">
              暂无详情图片
            </div>
          </el-tab-pane>
          
          <el-tab-pane label="规格参数">
            <div class="specifications">
              <el-table v-if="specTableData && specTableData.length > 0" :data="specTableData" stripe>
                <el-table-column prop="name" label="参数名" width="180" />
                <el-table-column prop="value" label="参数值" />
              </el-table>
              <div v-else class="text-center py-8 text-gray-500">
                暂无规格参数
              </div>
            </div>
          </el-tab-pane>
          
          <el-tab-pane label="用户评价">
            <div class="reviews">
              <div class="review-summary flex items-center mb-6">
                <div class="rating-info mr-8">
                  <p class="text-3xl font-bold text-orange-500">{{ product.rating || 0 }}</p>
                  <p class="text-sm text-gray-500">综合评分</p>
                </div>
                <div class="rating-bars flex-grow">
                  <div v-for="(rate, index) in ratingDistribution" :key="index" class="rating-bar flex items-center mb-1">
                    <span class="text-sm mr-2 w-12">{{ 5-index }}星</span>
                    <div class="bg-gray-200 h-4 flex-grow rounded-full overflow-hidden">
                      <div 
                        class="bg-orange-500 h-full" 
                        :style="{ width: rate + '%' }"
                      ></div>
                    </div>
                    <span class="text-sm ml-2 w-12">{{ rate }}%</span>
                  </div>
                </div>
              </div>
              
              <div v-if="product.reviews && product.reviews.length > 0">
                <!-- 评价列表 -->
              </div>
              <div v-else class="text-center py-8 text-gray-500">
                暂无用户评价
              </div>
            </div>
          </el-tab-pane>
        </el-tabs>
      </div>
      
      <!-- 相关推荐 -->
      <div class="related-products mt-8" v-if="product && product.relatedProducts && product.relatedProducts.length > 0">
        <h2 class="text-xl font-bold mb-4">相关推荐</h2>
        <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-4">
          <div v-for="item in product.relatedProducts" :key="item.id" class="related-item">
            <el-card shadow="hover" body-style="padding: 10px" class="h-full">
              <img :src="item.coverImage || item.cover_image" alt="相关产品" class="w-full h-32 object-cover mb-2 rounded">
              <h3 class="text-sm font-bold mb-1 line-clamp-1">{{ item.name }}</h3>
              <p class="text-red-500 font-bold">¥{{ item.price }}</p>
              <router-link :to="`/products/${item.id}`">
                <el-button type="primary" size="small" text class="mt-1">查看详情</el-button>
              </router-link>
            </el-card>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getProductDetail, toggleProductFavorite } from '@/api/products'
import { useCartStore } from '@/store/cart'
import { useUserStore } from '@/store/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const cartStore = useCartStore()
const loading = ref(true)
const product = ref(null)
const quantity = ref(1)
const currentImageIndex = ref(0)
const isFavorite = ref(false)
const selectedSku = ref(null)

// 获取产品详情
onMounted(() => {
  fetchProductDetail()
})

// 计算属性：处理图片展示数据
const displayGallery = computed(() => {
  if (!product.value) return []
  
  // 如果有gallery数据，使用gallery
  if (product.value.gallery && product.value.gallery.length > 0) {
    return product.value.gallery
  }
  
  // 如果没有gallery，使用cover_image作为默认图片
  if (product.value.cover_image) {
    return [{
      imageUrl: cleanImageUrl(product.value.cover_image),
      image_url: cleanImageUrl(product.value.cover_image),
      url: cleanImageUrl(product.value.cover_image),
      caption: product.value.name || '产品图片'
    }]
  }
  
  return []
})

// 清理图片URL中的反引号和空格
const cleanImageUrl = (url) => {
  if (!url) return ''
  return url.replace(/`/g, '').trim()
}

// 获取图片URL的函数
const getImageUrl = (image) => {
  // 尝试多种可能的字段名
  const url = image.imageUrl || image.image_url || image.url || image.src || ''
  return cleanImageUrl(url)
}

// 获取图片说明的函数
const getImageCaption = (image) => {
  return image.caption || image.alt || image.title || '产品图片'
}

const fetchProductDetail = async () => {
  loading.value = true
  try {
    const res = await getProductDetail(route.params.id)
    console.log('产品详情API响应:', res) // 添加调试日志
    
    if (res && res.code === 200 && res.data && res.data.id) {
      product.value = res.data
      
      // 从localStorage读取收藏状态
      const favorites = JSON.parse(localStorage.getItem('favorites') || '[]')
      isFavorite.value = favorites.includes(product.value.id)
      
      console.log('产品数据:', product.value)
      console.log('图库数据:', displayGallery.value)
    } else {
      console.error('产品详情获取失败:', res)
      ElMessage.error(res?.message || '获取产品详情失败')
      product.value = null
      // 跳转回产品列表页面
      router.push('/products')
    }
  } catch (error) {
    console.error('获取产品详情失败:', error)
    ElMessage.error('获取产品详情失败')
    product.value = null
    // 跳转回产品列表页面
    router.push('/products')
  } finally {
    loading.value = false
  }
}

// 切换收藏状态 - 纯前端操作
const toggleFavorite = () => {
  const existingFavorites = JSON.parse(localStorage.getItem('favorites') || '[]')
  
  if (isFavorite.value) {
    // 取消收藏
    const updatedFavorites = existingFavorites.filter(item => item.id !== product.value.id)
    localStorage.setItem('favorites', JSON.stringify(updatedFavorites))
    isFavorite.value = false
    ElMessage.success('已取消收藏')
  } else {
    // 添加收藏
    const favoriteItem = {
      id: product.value.id,
      name: product.value.name,
      price: product.value.current_price || product.value.price,
      image: cleanImageUrl(product.value.cover_image) || (product.value.gallery && product.value.gallery[0]?.image_url ? cleanImageUrl(product.value.gallery[0].image_url) : ''),
      addTime: new Date().toISOString(),
      type: 'product'
    }
    
    existingFavorites.push(favoriteItem)
    localStorage.setItem('favorites', JSON.stringify(existingFavorites))
    isFavorite.value = true
    ElMessage.success('已添加到收藏')
  }
}

// 规格参数表格数据
const specTableData = computed(() => {
  if (!product.value || !product.value.specifications) return []
  try {
    return Object.entries(product.value.specifications).map(([name, value]) => ({
      name,
      value
    }))
  } catch (error) {
    console.error('规格参数解析错误:', error)
    return []
  }
})

// 评分分布数据（模拟）
const ratingDistribution = ref([70, 20, 8, 1.5, 0.5])

// 处理轮播图切换
const handleCarouselChange = (index) => {
  currentImageIndex.value = index
}

// 加入购物车 - 纯前端操作
// 添加到购物车
const addToCart = async () => {
  // 检查产品数据是否已加载
  if (!product.value) {
    ElMessage.error('产品信息加载中，请稍后再试')
    return
  }

  // 检查库存
  const currentStock = selectedSku.value ? selectedSku.value.stock : product.value.stock
  if (quantity.value > currentStock) {
    ElMessage.warning(`库存不足，当前库存为${currentStock}`)
    return
  }

  const cartItem = {
    id: Date.now(),
    productId: product.value.id,
    name: product.value.name,
    price: selectedSku.value ? selectedSku.value.price : product.value.current_price || product.value.price,
    quantity: quantity.value,
    image: cleanImageUrl(product.value.cover_image) || (product.value.gallery && product.value.gallery[0]?.image_url ? cleanImageUrl(product.value.gallery[0].image_url) : ''),
    addTime: new Date().toISOString()
  }

  // 获取现有购物车数据
  const existingCart = JSON.parse(localStorage.getItem('cart') || '[]')
  
  // 检查是否已存在相同商品
  const existingItemIndex = existingCart.findIndex(item => item.productId === product.value.id)
  
  if (existingItemIndex > -1) {
    // 如果已存在，更新数量
    existingCart[existingItemIndex].quantity += quantity.value
  } else {
    // 如果不存在，添加新商品
    existingCart.push(cartItem)
  }
  
  // 保存到localStorage
  localStorage.setItem('cart', JSON.stringify(existingCart))
  
  ElMessage.success('已加入购物车')
}

// 立即购买 - 纯前端操作
const buyNow = () => {
  // 检查产品数据是否已加载
  if (!product.value) {
    ElMessage.error('产品信息未加载，请稍后再试')
    return
  }

  // 检查库存
  if (product.value.stock < quantity.value) {
    ElMessage.error('库存不足')
    return
  }

  // 创建订单项，确保数字类型
  const orderItem = {
    id: Date.now(),
    productId: product.value.id,
    name: product.value.name,
    price: parseFloat(product.value.price), // 确保是数字
    quantity: parseInt(quantity.value), // 确保是数字
    image: product.value.image,
    total_price: parseFloat(product.value.price) * parseInt(quantity.value), // 确保是数字
    item_type: 'product'
  }

  // 保存到sessionStorage用于支付页面
  sessionStorage.setItem('pendingOrder', JSON.stringify(orderItem))

  // 直接跳转到支付页面，不带参数
  router.push('/payment')
}
</script>

<style scoped>
.thumbnail-item {
  transition: border-color 0.2s ease;
}

.thumbnail-item:hover {
  border-color: #409EFF;
}

.line-clamp-1 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.related-item {
  transition: transform 0.3s ease;
}

.related-item:hover {
  transform: translateY(-5px);
}
</style>