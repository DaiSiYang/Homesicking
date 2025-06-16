<template>
  <div class="village-detail container mx-auto py-8 px-4">
    <div v-if="loading" class="flex justify-center py-10">
      <el-skeleton :rows="15" animated />
    </div>
    
    <div v-else-if="!village" class="text-center py-10">
      <el-empty description="未找到相关乡村信息" />
    </div>
    
    <div v-else>
      <!-- 面包屑导航 -->
      <el-breadcrumb separator="/" class="mb-6">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item :to="{ path: '/villages' }">乡村</el-breadcrumb-item>
        <el-breadcrumb-item>{{ village.name }}</el-breadcrumb-item>
      </el-breadcrumb>
      
      <!-- 乡村基本信息 -->
      <div class="flex flex-col md:flex-row gap-6 mb-8">
        <!-- 图片轮播 -->
        <div class="md:w-1/2">
          <el-carousel height="400px" indicator-position="outside" :interval="4000" v-if="village.gallery && village.gallery.length > 0">
            <el-carousel-item v-for="(image, index) in village.gallery" :key="index">
              <img :src="cleanImageUrl(image.image_url)" :alt="image.caption" class="w-full h-full object-cover rounded-lg">
            </el-carousel-item>
          </el-carousel>
          <div v-else class="h-96 bg-gray-200 rounded-lg flex items-center justify-center">
            <span class="text-gray-500">暂无图片</span>
          </div>
        </div>
        
        <!-- 详细信息 -->
        <div class="md:w-1/2">
          <div class="flex justify-between items-start mb-4">
            <h1 class="text-3xl font-bold">{{ village.name }}</h1>
            <el-button 
              :type="isFavorite ? 'default' : 'warning'"
              @click="toggleFavorite"
            >
              <el-icon><component :is="isFavorite ? 'Star' : 'StarFilled'" /></el-icon>
              {{ isFavorite ? '已收藏' : '收藏' }}
            </el-button>
          </div>
          
          <div class="flex items-center mb-4">
            <el-rate :model-value="parseFloat(village.rating)" disabled text-color="#ff9900" />
            <span class="ml-2 text-orange-500">{{ village.rating }}分</span>
            <span class="ml-4 text-gray-500">浏览量: {{ village.views }}</span>
          </div>
          
          <div class="mb-4">
            <span class="text-gray-700">地区：</span>
            <span>{{ village.region }}</span>
          </div>
          
          <div class="mb-4">
            <span class="text-gray-700">位置：</span>
            <span>{{ village.address }}</span>
          </div>
          
          <div class="mb-4">
            <span class="text-gray-700">特色标签：</span>
            <div class="flex flex-wrap gap-2 mt-2">
              <el-tag v-for="(tag, index) in parsedFeatures" :key="index" size="small">{{ tag }}</el-tag>
            </div>
          </div>
          
          <div class="mt-6">
            <el-button type="primary" @click="openMap">查看地图位置</el-button>
            <el-button type="success" @click="scrollToHomestays">查看住宿</el-button>
          </div>
        </div>
      </div>
      
      <!-- 乡村介绍 -->
      <div class="mb-10">
        <h2 class="text-xl font-bold mb-4 border-b pb-2">乡村介绍</h2>
        <div class="text-gray-700 leading-relaxed">
          <p class="mb-4">{{ village.intro }}</p>
          <div v-html="village.description"></div>
        </div>
      </div>
      
      <!-- 景点列表 -->
      <div class="mb-10" id="attractions">
        <h2 class="text-xl font-bold mb-4 border-b pb-2">景点推荐</h2>
        
        <div v-if="!village.attractions || village.attractions.length === 0" class="text-center py-6">
          <el-empty description="暂无景点信息" />
        </div>
        
        <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div v-for="attraction in village.attractions" :key="attraction.id" class="border rounded-lg overflow-hidden hover:shadow-lg transition-shadow">
            <img :src="cleanImageUrl(attraction.cover_image)" :alt="attraction.name" class="w-full h-48 object-cover">
            <div class="p-4">
              <h3 class="text-lg font-bold mb-2">{{ attraction.name }}</h3>
              <p class="text-gray-600 text-sm mb-3 line-clamp-2">{{ attraction.intro }}</p>
              <div class="flex justify-between items-center">
                <span class="text-orange-500">¥{{ attraction.ticket_price }}</span>
                <router-link :to="`/attractions/${attraction.id}`">
                  <el-button size="small">查看详情</el-button>
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 民宿列表 -->
      <div class="mb-10" id="homestays">
        <h2 class="text-xl font-bold mb-4 border-b pb-2">住宿推荐</h2>
        
        <div v-if="!village.homestays || village.homestays.length === 0" class="text-center py-6">
          <el-empty description="暂无民宿信息" />
        </div>
        
        <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div v-for="homestay in village.homestays" :key="homestay.id" class="border rounded-lg overflow-hidden hover:shadow-lg transition-shadow">
            <img :src="cleanImageUrl(homestay.cover_image)" :alt="homestay.name" class="w-full h-48 object-cover">
            <div class="p-4">
              <h3 class="text-lg font-bold mb-2">{{ homestay.name }}</h3>
              <p class="text-gray-600 text-sm mb-3 line-clamp-2">{{ homestay.intro }}</p>
              <div class="flex justify-between items-center">
                <div>
                  <span class="text-red-500 font-bold">¥{{ homestay.lowest_price }}</span>
                  <span class="text-gray-500 text-xs">起/晚</span>
                </div>
                <router-link :to="`/homestays/${homestay.id}`">
                  <el-button type="primary" size="small">查看详情</el-button>
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useUserStore } from '@/store/user'
import { getVillageDetail, toggleVillageFavorite } from '@/api/villages'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const loading = ref(true)
const village = ref(null)
const isFavorite = ref(false)

// 清理图片URL的函数
const cleanImageUrl = (url) => {
  if (!url) return ''
  return url.replace(/[`\s]/g, '') // 移除反引号和空格
}

// 解析特色标签
const parsedFeatures = computed(() => {
  if (!village.value?.features) return []
  
  // 如果 features 是数组，直接返回
  if (Array.isArray(village.value.features)) {
    return village.value.features
  }
  
  // 如果 features 不是字符串，返回空数组
  if (typeof village.value.features !== 'string') {
    return []
  }
  
  try {
    return JSON.parse(village.value.features)
  } catch {
    return village.value.features.split(',').map(f => f.trim())
  }
})

// 获取乡村详情
const fetchVillageDetail = async () => {
  loading.value = true
  try {
    const villageId = route.params.id
    const res = await getVillageDetail(villageId)
    
    // 检查返回的数据类型
    if (res && res.id) {
      // 如果返回的是民宿数据（包含 merchant_id），重定向到民宿详情页
      if (res.merchant_id) {
        ElMessage.warning('检测到民宿数据，正在跳转到民宿详情页...')
        router.push(`/homestays/${res.id}`)
        return
      }
      
      // 确保数据结构完整
      village.value = {
        ...res,
        attractions: res.attractions || [],
        homestays: res.homestays || [],
        gallery: res.gallery || []
      }
      isFavorite.value = village.value.is_favorited || false
    } else {
      ElMessage.error('获取乡村详情失败')
      village.value = null
    }
  } catch (error) {
    console.error('获取乡村详情失败:', error)
    ElMessage.error('获取乡村详情失败')
    village.value = null
  } finally {
    loading.value = false
  }
}

// 收藏/取消收藏
const toggleFavorite = async () => {
  if (!userStore.isLoggedIn) {
    ElMessage.warning('请先登录')
    return
  }
  
  try {
    const res = await toggleVillageFavorite(village.value.id)
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

// 打开地图
const openMap = () => {
  if (village.value && village.value.location) {
    const [lat, lng] = village.value.location.split(',')
    window.open(`https://maps.google.com/maps?q=${lat},${lng}`, '_blank')
  }
}

// 滚动到民宿区域
const scrollToHomestays = () => {
  document.getElementById('homestays')?.scrollIntoView({ behavior: 'smooth' })
}

onMounted(() => {
  fetchVillageDetail()
})
</script>