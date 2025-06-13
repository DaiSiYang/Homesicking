<template>
  <div>
    <!-- 英雄区域 -->
    <section class="relative h-96 overflow-hidden">
      <div class="absolute inset-0 bg-gradient-to-r from-primary-900/80 to-earth-800/60"></div>
      <div class="absolute inset-0 bg-cover bg-center" style="background-image: url('https://images.unsplash.com/photo-1528702748617-c64d49f918af?ixlib=rb-4.0.3')"></div>
      <div class="relative z-10 h-full flex items-center justify-center text-center text-white">
        <div class="max-w-4xl mx-auto px-4">
          <h1 class="text-5xl font-calligraphy mb-4 text-shadow-lg">觅乡记</h1>
          <div class="ink-border mx-auto w-32 mb-6"></div>
          <p class="text-xl mb-8 leading-relaxed">发现乡村之美，体验民俗文化<br>品尝地道美食，享受悠闲假期</p>
          <div class="flex justify-center space-x-4">
            <button class="btn-primary px-8 py-3" @click="$router.push('/villages')">
              开始探索
            </button>
            <button class="btn-outline border-white text-white hover:bg-white hover:text-primary-700 px-8 py-3">
              了解更多
            </button>
          </div>
        </div>
      </div>
    </section>

    <div class="page-container py-16">
      <!-- 分类导航 -->
      <section class="mb-16">
        <div class="text-center mb-12">
          <h2 class="text-3xl font-calligraphy text-ink-700 mb-4">探索乡村</h2>
          <div class="ink-border mx-auto"></div>
          <p class="text-ink-500 mt-4 max-w-2xl mx-auto">精选优质乡村资源，为您提供最地道的乡村体验</p>
        </div>
        
        <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
          <div v-for="category in categories" :key="category.id" 
               class="group card hover:scale-105 text-center cursor-pointer transition-all duration-300"
               @click="$router.push(category.link)">
            <div class="w-16 h-16 mx-auto mb-4 bg-gradient-to-br from-primary-100 to-earth-100 rounded-brush flex items-center justify-center group-hover:from-primary-200 group-hover:to-earth-200 transition-all duration-300">
              <el-icon :size="28" class="text-primary-600">
                <component :is="category.icon" />
              </el-icon>
            </div>
            <h3 class="text-lg font-medium text-ink-700 mb-2">{{ category.name }}</h3>
            <p class="text-ink-500 text-sm">{{ category.desc }}</p>
          </div>
        </div>
      </section>

      <!-- 热门推荐 -->
      <section class="mb-16">
        <div class="flex justify-between items-center mb-8">
          <div>
            <h2 class="text-2xl font-medium text-ink-700 mb-2">热门推荐</h2>
            <div class="ink-border"></div>
          </div>
          <el-button link class="text-primary-600 hover:text-primary-700" @click="$router.push('/products')">
            查看全部 →
          </el-button>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div v-for="product in featuredProducts" :key="product.id" 
               class="group card hover:shadow-brush cursor-pointer transition-all duration-300"
               @click="$router.push(`/products/${product.id}`)">
            <div class="relative overflow-hidden rounded-ink mb-4">
              <img :src="product.image" :alt="product.name" 
                   class="w-full h-48 object-cover group-hover:scale-105 transition-transform duration-300">
              <div class="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
            </div>
            <h3 class="text-lg font-medium text-ink-700 mb-2 group-hover:text-primary-600 transition-colors">{{ product.name }}</h3>
            <p class="text-ink-500 text-sm mb-3 line-clamp-2">{{ product.description }}</p>
            <div class="flex justify-between items-center">
              <span class="text-xl font-bold text-red-600">¥{{ product.price }}</span>
              <span class="text-xs text-ink-400 bg-earth-100 px-2 py-1 rounded-full">热销</span>
            </div>
          </div>
        </div>
      </section>

      <!-- 特色服务 -->
      <section class="mb-16">
        <div class="text-center mb-12">
          <h2 class="text-3xl font-calligraphy text-ink-700 mb-4">特色服务</h2>
          <div class="ink-border mx-auto"></div>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div class="text-center">
            <!-- 在特色服务部分 -->
            <div class="w-20 h-20 mx-auto mb-4 bg-gradient-to-br from-primary-100 to-bamboo-100 rounded-full flex items-center justify-center">
              <el-icon :size="32" class="text-primary-600"><Lock /></el-icon>
            </div>
            <h3 class="text-lg font-medium text-ink-700 mb-2">品质保证</h3>
            <p class="text-ink-500 text-sm">严格筛选，确保每一个推荐都值得信赖</p>
          </div>
          <div class="text-center">
            <div class="w-20 h-20 mx-auto mb-4 bg-gradient-to-br from-earth-100 to-primary-100 rounded-full flex items-center justify-center">
              <el-icon :size="32" class="text-primary-600"><Headset /></el-icon>
            </div>
            <h3 class="text-lg font-medium text-ink-700 mb-2">贴心服务</h3>
            <p class="text-ink-500 text-sm">24小时客服支持，让您的旅程无忧</p>
          </div>
          <div class="text-center">
            <div class="w-20 h-20 mx-auto mb-4 bg-gradient-to-br from-bamboo-100 to-earth-100 rounded-full flex items-center justify-center">
              <el-icon :size="32" class="text-primary-600"><Trophy /></el-icon>
            </div>
            <h3 class="text-lg font-medium text-ink-700 mb-2">优质体验</h3>
            <p class="text-ink-500 text-sm">精心设计的行程，带给您难忘的乡村体验</p>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import {
  House, ShoppingBag, Food, Suitcase, Lock, Headset, Trophy
} from '@element-plus/icons-vue'
import { getRecommendedProducts } from '@/api/recommendations'

// 轮播图数据
const banners = ref([
  {
    title: '古镇漫游',
    description: '探寻千年古镇，体验当地民俗文化',
    image: 'https://images.unsplash.com/photo-1528702748617-c64d49f918af?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80',
    link: '/villages'
  },
  {
    title: '民宿体验',
    description: '精选各地特色民宿，享受宁静舒适的住宿体验',
    image: 'https://images.unsplash.com/photo-1542718610-a1d656d1884c?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80',
    link: '/homestays'
  },
  {
    title: '地道美食',
    description: '品尝地方特色美食，感受舌尖上的乡村',
    image: 'https://images.unsplash.com/photo-1555126634-323283e090fa?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1064&q=80',
    link: '/foods'
  }
])

// 分类导航
const categories = ref([
  {
    id: 1,
    name: '乡村景点',
    desc: '发现自然之美',
    icon: 'House',
    link: '/villages'
  },
  {
    id: 2,
    name: '特色民宿',
    desc: '体验乡村生活',
    icon: 'Suitcase',
    link: '/homestays'
  },
  {
    id: 3,
    name: '乡村特产',
    desc: '购买当地好物',
    icon: 'ShoppingBag',
    link: '/products'
  },
  {
    id: 4,
    name: '乡村美食',
    desc: '品尝地方美食',
    icon: 'Food',
    link: '/foods'
  }
])

// 推荐产品
const featuredProducts = ref([])
const loading = ref(false)

// 获取推荐产品
const fetchFeaturedProducts = async () => {
  try {
    loading.value = true
    const response = await getRecommendedProducts()
    featuredProducts.value = response.data.results || response.data
  } catch (error) {
    console.error('获取推荐产品失败:', error)
    // 保留原有的模拟数据作为后备
    featuredProducts.value = [
      {
        id: 1,
        name: '云南野生菌礼盒',
        description: '精选云南高原野生食用菌，营养丰富，风味独特',
        price: 168,
        image: 'https://images.unsplash.com/photo-1607493739673-58db1b8d7738?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80'
      },
      {
        id: 2,
        name: '山茶油礼盒',
        description: '传统工艺压榨，不添加任何化学成分，健康食用油',
        price: 138,
        image: 'https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1061&q=80'
      },
      {
        id: 3,
        name: '手工腊肉',
        description: '农家自制，传统工艺腌制，肉质紧实，香味浓郁',
        price: 89,
        image: 'https://images.unsplash.com/photo-1625604086988-8e2506a35854?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80'
      },
      {
        id: 4,
        name: '蜂蜜礼盒',
        description: '百花蜜、洋槐蜜、枣花蜜等多种蜂蜜组合装',
        price: 198,
        image: 'https://images.unsplash.com/photo-1587049352851-8d4e89133924?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=880&q=80'
      }
    ]
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchFeaturedProducts()
})
</script>

<style scoped>
.text-shadow-lg {
  text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>