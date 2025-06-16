<template>
  <div class="homestay-detail container mx-auto py-8 px-4">
    <div v-if="loading" class="flex justify-center py-10">
      <el-skeleton :rows="15" animated />
    </div>
    
    <div v-else-if="!homestay" class="text-center py-10">
      <el-empty description="未找到相关民宿信息" />
    </div>
    
    <div v-else>
      <!-- 面包屑导航 -->
      <el-breadcrumb separator="/" class="mb-6">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item :to="{ path: '/homestays' }">民宿</el-breadcrumb-item>
        <el-breadcrumb-item>{{ homestay.name }}</el-breadcrumb-item>
      </el-breadcrumb>
      
      <!-- 民宿基本信息 -->
      <div class="flex flex-col md:flex-row gap-6 mb-8">
        <!-- 图片轮播 -->
        <div class="md:w-3/5">
          <el-carousel height="400px" indicator-position="outside" :interval="4000">
            <el-carousel-item v-for="(image, index) in homestay.gallery" :key="index">
              <img :src="image.image_url" :alt="image.caption" class="w-full h-full object-cover rounded-lg">
            </el-carousel-item>
          </el-carousel>
        </div>
        
        <!-- 详细信息 -->
        <div class="md:w-2/5">
          <div class="flex justify-between items-start mb-4">
            <h1 class="text-3xl font-bold">{{ homestay.name }}</h1>
            <el-button 
              :icon="isFavorite ? 'Star' : 'StarFilled'" 
              :type="isFavorite ? 'default' : 'warning'"
              @click="toggleFavorite"
            >
              {{ isFavorite ? '已收藏' : '收藏' }}
            </el-button>
          </div>
          
          <div class="flex items-center mb-4">
            <el-rate v-model="homestay.rating" disabled text-color="#ff9900" />
            <span class="ml-2 text-orange-500">{{ homestay.rating }}分</span>
            <span class="ml-4 text-gray-500">{{ homestay.ordersCount }}人已预订</span>
          </div>
          
          <div class="mb-4">
            <span class="text-gray-700">所属乡村：</span>
            <router-link :to="`/villages/${homestay.villageId}`" class="text-blue-500">{{ homestay.villageName }}</router-link>
          </div>
          
          <div class="mb-4">
            <span class="text-gray-700">物业类型：</span>
            <span>{{ homestay.propertyType }}</span>
          </div>
          
          <div class="mb-4">
            <span class="text-gray-700">地址：</span>
            <span>{{ homestay.address }}</span>
          </div>
          
          <div class="mb-4">
            <span class="text-gray-700">入住/退房时间：</span>
            <span>{{ homestay.checkInTime }} / {{ homestay.checkOutTime }}</span>
          </div>
          
          <div class="mb-4">
            <span class="text-gray-700">设施特色：</span>
            <div class="flex flex-wrap gap-2 mt-2">
              <el-tag v-for="(feature, index) in parsedFeatures" :key="index" size="small">{{ feature }}</el-tag>
            </div>
          </div>
          
          <div class="mt-6">
            <el-button type="primary" @click="openMap">查看地图位置</el-button>
            <el-button type="success" @click="scrollToRooms">查看房型</el-button>
          </div>
        </div>
      </div>
      
      <!-- 民宿介绍 -->
      <div class="mb-10">
        <h2 class="text-xl font-bold mb-4 border-b pb-2">民宿介绍</h2>
        <div class="text-gray-700 leading-relaxed">
          <p class="mb-4">{{ homestay.intro }}</p>
          <div v-html="homestay.description"></div>
        </div>
      </div>
      
      <!-- 房型列表 -->
      <div class="mb-10" id="rooms">
        <h2 class="text-xl font-bold mb-4 border-b pb-2">可预订房型</h2>
        
        <!-- 日期选择器 -->
        <div class="mb-6 bg-gray-50 p-4 rounded-lg">
          <el-form :inline="true">
            <el-form-item label="入住日期">
              <el-date-picker
                v-model="dateRange"
                type="daterange"
                range-separator="至"
                start-placeholder="入住日期"
                end-placeholder="退房日期"
                :disabled-date="disabledDate"
                @change="handleDateChange"
              />
            </el-form-item>
            <el-form-item label="入住人数">
              <el-input-number v-model="guestCount" :min="1" :max="10" />
            </el-form-item>
          </el-form>
        </div>
        
        <!-- 房型列表 -->
        <div v-if="homestay.room_types && homestay.room_types.length === 0" class="text-center py-6">
          <el-empty description="暂无可预订房型" />
        </div>
        
        <div v-else-if="homestay.room_types">
          <el-card v-for="room in homestay.room_types" :key="room.id" class="mb-6">
            <div class="flex flex-col md:flex-row">
              <!-- 房型图片 -->
              <div class="md:w-1/4 mb-4 md:mb-0 md:mr-4">
                <img :src="room.cover_image" :alt="room.name" class="w-full h-40 object-cover rounded">
              </div>
              
              <!-- 房型信息 -->
              <div class="md:w-1/2 md:px-4">
                <h3 class="text-lg font-semibold mb-2">{{ room.name }}</h3>
                <div class="text-gray-600 mb-2">
                  <span class="mr-4">面积：{{ room.area }}㎡</span>
                  <span class="mr-4">床型：{{ room.bed_type }}</span>
                  <span>最多入住：{{ room.max_guests }}人</span>
                </div>
                <div v-if="room.breakfast" class="text-green-600 text-sm">
                  <el-icon><Check /></el-icon>
                  含早餐
                </div>
              </div>
              
              <!-- 价格和预订 -->
              <div class="md:w-1/4 flex flex-col justify-between">
                <div class="text-right">
                  <div v-if="room.discount_price" class="text-gray-400 line-through text-sm">¥{{ room.price }}</div>
                  <div class="text-2xl font-bold text-orange-500">¥{{ room.current_price }}</div>
                  <div class="text-gray-500 text-sm">每晚</div>
                </div>
                <el-button type="primary" @click="handleBooking(room)" class="mt-4">
                  立即预订
                </el-button>
              </div>
            </div>
          </el-card>
        </div>
      </div>
      
      <!-- 用户评价 -->
      <div class="mb-10">
        <h2 class="text-xl font-bold mb-4 border-b pb-2">用户评价</h2>
        
        <div v-if="!homestay.reviews || homestay.reviews.length === 0" class="text-center py-6">
          <el-empty description="暂无评价" />
        </div>
        
        <div v-else>
          <div v-for="review in homestay.reviews" :key="review.id" class="mb-6 border-b pb-6">
            <div class="flex justify-between items-start mb-2">
              <div class="flex items-center">
                <img :src="review.user_avatar || review.userAvatar" :alt="review.user_name || review.userName" class="w-10 h-10 rounded-full mr-3">
                <div>
                  <div class="font-medium">{{ review.user_name || review.userName }}</div>
                  <div class="text-gray-500 text-xs">{{ review.create_time || review.createTime }}</div>
                </div>
              </div>
              <el-rate v-model="review.rating" disabled text-color="#ff9900" />
            </div>
            <p class="text-gray-700 my-2">{{ review.content }}</p>
            <div v-if="review.reply" class="bg-gray-50 p-3 mt-2 text-sm">
              <div class="font-medium">商家回复：</div>
              <p class="text-gray-600">{{ review.reply }}</p>
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
import { getHomestayDetail, toggleHomestayFavorite } from '@/api/homestays'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const loading = ref(true)
const homestay = ref(null)
const isFavorite = ref(false)
const dateRange = ref([])
const guestCount = ref(2)

// 解析设施特色
const parsedFeatures = computed(() => {
  if (!homestay.value?.facilities) return []
  try {
    return JSON.parse(homestay.value.facilities)
  } catch {
    return homestay.value.facilities.split(',').map(f => f.trim())
  }
})

// 获取民宿详情
const fetchHomestayDetail = async () => {
  loading.value = true
  try {
    const homestayId = route.params.id
    const res = await getHomestayDetail(homestayId)
    
    // 直接使用响应数据，不检查 res.code
    if (res && res.id) {
      homestay.value = res
      isFavorite.value = homestay.value.is_favorited || false
    } else {
      ElMessage.error('获取民宿详情失败')
      homestay.value = null
    }
  } catch (error) {
    console.error('获取民宿详情失败:', error)
    ElMessage.error('获取民宿详情失败')
    homestay.value = null
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
    const res = await toggleHomestayFavorite(homestay.value.id)
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

// 处理日期变化
const handleDateChange = () => {
  console.log('日期变化:', dateRange.value)
}

// 打开地图
const openMap = () => {
  if (homestay.value && homestay.value.location) {
    const [lat, lng] = homestay.value.location.split(',')
    window.open(`https://maps.google.com/maps?q=${lat},${lng}`, '_blank')
  }
}

// 滚动到房型区域
const scrollToRooms = () => {
  document.getElementById('rooms')?.scrollIntoView({ behavior: 'smooth' })
}

// 处理预订
const handleBooking = (room) => {
  if (!userStore.isLoggedIn) {
    ElMessageBox.confirm('预订需要先登录，是否前往登录?', '提示', {
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
  
  if (!dateRange.value || !dateRange.value[0] || !dateRange.value[1]) {
    ElMessage.warning('请先选择入住日期')
    return
  }
  
  ElMessage.success('已添加到订单，正在跳转...')
  setTimeout(() => {
    router.push({
      path: '/checkout',
      query: {
        homestayId: homestay.value.id,
        roomId: room.id,
        checkIn: dateRange.value[0].toISOString().split('T')[0],
        checkOut: dateRange.value[1].toISOString().split('T')[0],
        guests: guestCount.value
      }
    })
  }, 1000)
}

onMounted(() => {
  fetchHomestayDetail()
})
</script>