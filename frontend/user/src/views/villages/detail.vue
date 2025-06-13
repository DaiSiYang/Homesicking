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
          <el-carousel height="400px" indicator-position="outside" :interval="4000">
            <el-carousel-item v-for="(image, index) in village.gallery" :key="index">
              <img :src="image.imageUrl" :alt="image.caption" class="w-full h-full object-cover rounded-lg">
            </el-carousel-item>
          </el-carousel>
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
            <el-rate v-model="village.rating" disabled text-color="#ff9900" />
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
        
        <div v-if="village.attractions.length === 0" class="text-center py-6">
          <el-empty description="暂无景点信息" />
        </div>
        
        <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div v-for="attraction in village.attractions" :key="attraction.id" class="border rounded-lg overflow-hidden hover:shadow-lg transition-shadow">
            <img :src="attraction.coverImage" :alt="attraction.name" class="w-full h-48 object-cover">
            <div class="p-4">
              <h3 class="text-lg font-bold mb-2">{{ attraction.name }}</h3>
              <p class="text-gray-600 text-sm mb-3 line-clamp-2">{{ attraction.intro }}</p>
              <div class="flex justify-between items-center">
                <span class="text-orange-500">¥{{ attraction.ticketPrice }}</span>
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
        
        <div v-if="village.homestays.length === 0" class="text-center py-6">
          <el-empty description="暂无民宿信息" />
        </div>
        
        <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div v-for="homestay in village.homestays" :key="homestay.id" class="border rounded-lg overflow-hidden hover:shadow-lg transition-shadow">
            <img :src="homestay.coverImage" :alt="homestay.name" class="w-full h-48 object-cover">
            <div class="p-4">
              <h3 class="text-lg font-bold mb-2">{{ homestay.name }}</h3>
              <p class="text-gray-600 text-sm mb-3 line-clamp-2">{{ homestay.intro }}</p>
              <div class="flex justify-between items-center">
                <div>
                  <span class="text-red-500 font-bold">¥{{ homestay.lowestPrice }}</span>
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
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Star, StarFilled } from '@element-plus/icons-vue'
import { useUserStore } from '@/store/user'

const route = useRoute()
const userStore = useUserStore()
const villageId = route.params.id

// 页面状态
const loading = ref(true)
const village = ref(null)
const isFavorite = ref(false)

// 解析特色标签
const parsedFeatures = computed(() => {
  if (!village.value || !village.value.features) return []
  try {
    return JSON.parse(village.value.features)
  } catch (e) {
    return []
  }
})

// 获取乡村详情
const fetchVillageDetail = async () => {
  loading.value = true
  
  try {
    // 模拟API调用，实际项目中应替换为真实API
    setTimeout(() => {
      village.value = {
        id: villageId,
        name: '婺源篁岭',
        region: '华东-江西',
        address: '江西省上饶市婺源县',
        intro: '篁岭是江西省婺源县的一个古村落，距今已有近六百年历史，是一座建在千米高山之上的徽派古村落。',
        description: `<p>篁岭是江西省婺源县的一个古村落，距今已有近六百年历史，是一座建在千米高山之上的徽派古村落。篁岭因"晒秋"闻名遐迩，每到金秋时节，家家户户把收获的稻谷、红辣椒、南瓜等农作物摊晾在露台和房前屋后，形成一幅幅色彩斑斓的画卷。</p>
        <p>篁岭还是中国传统村落，保存着完好的明清古建筑群，古朴的徽派建筑与现代田园风光相结合，是摄影爱好者的天堂。</p>
        <p>村内有古戏台、祠堂等文化遗产，还有各种民俗活动和手工艺展示，让游客可以深入体验徽州文化的魅力。</p>`,
        coverImage: 'https://picsum.photos/id/1018/600/400',
        location: '29.151,117.934',
        features: '["古村落","晒秋","徽派建筑","民俗文化"]',
        views: 12580,
        rating: 4.7,
        gallery: [
          { imageUrl: 'https://picsum.photos/id/1018/600/400', caption: '篁岭全景' },
          { imageUrl: 'https://picsum.photos/id/1015/600/400', caption: '晒秋景观' },
          { imageUrl: 'https://picsum.photos/id/1019/600/400', caption: '徽派建筑' },
          { imageUrl: 'https://picsum.photos/id/1039/600/400', caption: '古村落风光' }
        ],
        attractions: [
          {
            id: 101,
            name: '篁岭古村',
            intro: '保存完好的明清古建筑群，是徽派建筑的代表。',
            coverImage: 'https://picsum.photos/id/1015/600/400',
            ticketPrice: 80
          },
          {
            id: 102,
            name: '晒秋广场',
            intro: '金秋时节，家家户户把收获的农作物摊晾在露台，形成色彩斑斓的画卷。',
            coverImage: 'https://picsum.photos/id/1019/600/400',
            ticketPrice: 0
          },
          {
            id: 103,
            name: '古戏台',
            intro: '明代建筑，至今仍有传统戏曲表演，是体验徽州文化的重要场所。',
            coverImage: 'https://picsum.photos/id/1039/600/400',
            ticketPrice: 0
          }
        ],
        homestays: [
          {
            id: 201,
            name: '篁岭山居',
            intro: '位于篁岭古村中心位置，徽派风格装修，可俯瞰整个村落美景。',
            coverImage: 'https://picsum.photos/id/1048/600/400',
            lowestPrice: 388
          },
          {
            id: 202,
            name: '晒秋小筑',
            intro: '紧邻晒秋广场，传统与现代结合的舒适民宿，秋季可观赏晒秋美景。',
            coverImage: 'https://picsum.photos/id/1037/600/400',
            lowestPrice: 428
          },
          {
            id: 203,
            name: '徽州院子',
            intro: '改建自百年老宅，保留原汁原味的徽派建筑风格，体验地道徽州生活。',
            coverImage: 'https://picsum.photos/id/1040/600/400',
            lowestPrice: 468
          }
        ]
      }
      
      // 模拟检查是否已收藏
      isFavorite.value = Math.random() > 0.5
      
      loading.value = false
    }, 1000)
  } catch (error) {
    ElMessage.error('获取乡村详情失败')
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
    // 模拟API调用，实际项目中应替换为真实API
    setTimeout(() => {
      isFavorite.value = !isFavorite.value
      ElMessage.success(isFavorite.value ? '收藏成功' : '已取消收藏')
    }, 300)
  } catch (error) {
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
  document.getElementById('homestays').scrollIntoView({ behavior: 'smooth' })
}

onMounted(() => {
  fetchVillageDetail()
})
</script> 