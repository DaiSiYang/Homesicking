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
      <el-breadcrumb separator="/" class="mb-6">
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
            <el-carousel-item v-for="(image, index) in product.gallery" :key="index">
              <img :src="image.imageUrl" :alt="image.caption" class="w-full h-full object-cover rounded-lg">
            </el-carousel-item>
          </el-carousel>
          
          <div class="image-thumbnails flex mt-4 gap-2 overflow-x-auto">
            <div
              v-for="(image, index) in product.gallery"
              :key="`thumb-${index}`"
              class="w-20 h-20 flex-shrink-0 cursor-pointer border-2"
              :class="{'border-green-500': currentImageIndex === index, 'border-transparent': currentImageIndex !== index}"
              @click="currentImageIndex = index"
            >
              <img :src="image.imageUrl" :alt="image.caption" class="w-full h-full object-cover">
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
          
          <div class="product-spec mb-6">
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
            <el-button type="primary" size="large" @click="addToCart">加入购物车</el-button>
            <el-button type="danger" size="large" @click="buyNow">立即购买</el-button>
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
      <div class="product-tabs mt-8">
        <el-tabs>
          <el-tab-pane label="产品详情">
            <div class="product-description mb-6">
              <h2 class="text-xl font-bold mb-4">产品介绍</h2>
              <div class="description-content text-gray-700 leading-relaxed whitespace-pre-line">
                {{ product.description }}
              </div>
            </div>
            
            <div class="product-images">
              <img 
                v-for="(image, index) in product.detailImages" 
                :key="index" 
                :src="image" 
                alt="产品详情图" 
                class="w-full mb-4 rounded-lg"
              >
            </div>
          </el-tab-pane>
          
          <el-tab-pane label="规格参数">
            <div class="specifications">
              <el-table :data="specTableData" stripe>
                <el-table-column prop="name" label="参数名" width="180" />
                <el-table-column prop="value" label="参数值" />
              </el-table>
            </div>
          </el-tab-pane>
          
          <el-tab-pane label="用户评价">
            <div class="reviews">
              <div class="review-summary flex items-center mb-6">
                <div class="rating-info mr-8">
                  <p class="text-3xl font-bold text-orange-500">{{ product.rating }}</p>
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
              
              <div v-if="product.reviews.length === 0" class="text-center py-4">
                <el-empty description="暂无评价" />
              </div>
              
              <div v-else class="review-list">
                <div 
                  v-for="(review, index) in product.reviews" 
                  :key="index"
                  class="review-item border-b border-gray-200 py-4 last:border-none"
                >
                  <div class="flex items-start">
                    <el-avatar :size="40" :src="review.user.avatar"></el-avatar>
                    <div class="ml-3 flex-1">
                      <div class="flex justify-between items-center mb-1">
                        <span class="font-bold">{{ review.user.name }}</span>
                        <span class="text-gray-500 text-sm">{{ review.date }}</span>
                      </div>
                      <div class="mb-2">
                        <el-rate v-model="review.rating" disabled text-color="#ff9900" />
                      </div>
                      <p class="text-base">{{ review.content }}</p>
                      <div v-if="review.images && review.images.length > 0" class="review-images flex gap-2 mt-2">
                        <el-image
                          v-for="(img, imgIndex) in review.images"
                          :key="imgIndex"
                          :src="img"
                          :preview-src-list="review.images"
                          class="w-16 h-16 object-cover rounded"
                        />
                      </div>
                      <div v-if="review.reply" class="official-reply mt-2 bg-gray-50 p-2 rounded text-sm">
                        <p class="text-gray-700"><span class="text-blue-600">商家回复：</span>{{ review.reply }}</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </el-tab-pane>
        </el-tabs>
      </div>
      
      <!-- 相关推荐 -->
      <div class="related-products mt-8">
        <h2 class="text-xl font-bold mb-4">相关推荐</h2>
        <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-4">
          <div v-for="item in product.relatedProducts" :key="item.id" class="related-item">
            <el-card shadow="hover" body-style="padding: 10px" class="h-full">
              <img :src="item.coverImage" alt="相关产品" class="w-full h-32 object-cover mb-2 rounded">
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
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
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

const fetchProductDetail = async () => {
  loading.value = true

  try {
    const productId = route.params.id
    const res = await getProductDetail(productId)
    
    if (res.code === 200) {
      product.value = res.data
      // 如果产品有SKU，设置默认选中第一个
      if (product.value.skus && product.value.skus.length > 0) {
        selectedSku.value = product.value.skus[0]
      }
    } else {
      ElMessage.error(res.message || '获取产品详情失败')
    }
  } catch (error) {
    console.error('获取产品详情失败:', error)
    ElMessage.error('获取产品详情失败')
  } finally {
    loading.value = false
  }
}

// 切换收藏状态
const toggleFavorite = async () => {
  if (!userStore.isLoggedIn) {
    ElMessage.warning('请先登录')
    return
  }
  
  try {
    const res = await toggleProductFavorite(product.value.id)
    if (res.code === 200) {
      isFavorite.value = !isFavorite.value
      ElMessage.success(isFavorite.value ? '收藏成功' : '已取消收藏')
    } else {
      ElMessage.error(res.message || '操作失败')
    }
  } catch (error) {
    console.error('收藏操作失败:', error)
    ElMessage.error('操作失败')
  }
}

// 规格参数表格数据
const specTableData = computed(() => {
  if (!product.value) return []
  return Object.entries(product.value.specifications).map(([name, value]) => ({
    name,
    value
  }))
})

// 评分分布数据（模拟）
const ratingDistribution = ref([70, 20, 8, 1.5, 0.5])

// 处理轮播图切换
const handleCarouselChange = (index) => {
  currentImageIndex.value = index
}

// 加入购物车
const addToCart = () => {
  if (!userStore.isLoggedIn) {
    ElMessageBox.confirm('加入购物车需要先登录，是否前往登录?', '提示', {
      confirmButtonText: '去登录',
      cancelButtonText: '取消',
      type: 'info'
    }).then(() => {
      router.push({
        path: '/login',
        query: { redirect: route.fullPath }
      })
    }).catch(() => {})
    return
  }
  
  // 检查库存
  const currentStock = selectedSku.value ? selectedSku.value.stock : product.value.stock
  if (quantity.value > currentStock) {
    ElMessage.warning(`库存不足，当前库存为${currentStock}`)
    return
  }
  
  // 添加到购物车
  const cartItem = {
    id: selectedSku.value ? selectedSku.value.id : product.value.id,
    productId: product.value.id,
    name: product.value.name,
    skuName: selectedSku.value ? selectedSku.value.name : '',
    price: selectedSku.value ? selectedSku.value.price : product.value.price,
    coverImage: product.value.gallery[0].imageUrl,
    quantity: quantity.value
  }
  
  cartStore.addToCart(cartItem)
  ElMessage.success('已加入购物车')
}

// 立即购买
const buyNow = () => {
  if (!userStore.isLoggedIn) {
    ElMessageBox.confirm('购买需要先登录，是否前往登录?', '提示', {
      confirmButtonText: '去登录',
      cancelButtonText: '取消',
      type: 'info'
    }).then(() => {
      router.push({
        path: '/login',
        query: { redirect: route.fullPath }
      })
    }).catch(() => {})
    return
  }
  
  // 检查库存
  const currentStock = selectedSku.value ? selectedSku.value.stock : product.value.stock
  if (quantity.value > currentStock) {
    ElMessage.warning(`库存不足，当前库存为${currentStock}`)
    return
  }
  
  // 添加到购物车并跳转到结算页面
  const cartItem = {
    id: selectedSku.value ? selectedSku.value.id : product.value.id,
    productId: product.value.id,
    name: product.value.name,
    skuName: selectedSku.value ? selectedSku.value.name : '',
    price: selectedSku.value ? selectedSku.value.price : product.value.price,
    coverImage: product.value.gallery[0].imageUrl,
    quantity: quantity.value
  }
  
  cartStore.addToCart(cartItem)
  router.push('/checkout?direct=true')
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