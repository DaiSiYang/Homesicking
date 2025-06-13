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
              <img :src="image.imageUrl" :alt="image.caption" class="w-full h-full object-cover rounded-lg">
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
        
        <div v-if="homestay.roomTypes.length === 0" class="text-center py-6">
          <el-empty description="暂无可预订房型" />
        </div>
        
        <div v-else>
          <el-card v-for="room in homestay.roomTypes" :key="room.id" class="mb-6">
            <div class="flex flex-col md:flex-row">
              <!-- 房型图片 -->
              <div class="md:w-1/4 mb-4 md:mb-0 md:mr-4">
                <img :src="room.coverImage" :alt="room.name" class="w-full h-40 object-cover rounded">
              </div>
              
              <!-- 房型信息 -->
              <div class="md:w-2/4">
                <h3 class="text-lg font-bold mb-2">{{ room.name }}</h3>
                <div class="flex flex-wrap gap-x-6 gap-y-2 text-sm text-gray-600 mb-3">
                  <div><i class="el-icon-user"></i> 最多{{ room.maxGuests }}人</div>
                  <div><i class="el-icon-house"></i> {{ room.area }}㎡</div>
                  <div><i class="el-icon-bed"></i> {{ room.bedType }}</div>
                  <div v-if="room.breakfast"><i class="el-icon-food"></i> 含早餐</div>
                </div>
                <p class="text-gray-600 text-sm mb-3 line-clamp-2">{{ room.description }}</p>
                <div class="text-xs text-gray-500">{{ room.cancellation }}</div>
              </div>
              
              <!-- 价格和预订 -->
              <div class="md:w-1/4 flex flex-col items-end justify-between">
                <div class="text-right">
                  <div v-if="room.discountPrice" class="mb-1">
                    <span class="text-gray-500 line-through text-sm">¥{{ room.price }}</span>
                  </div>
                  <div class="text-red-500 font-bold text-xl">
                    ¥{{ room.discountPrice || room.price }}
                  </div>
                  <div class="text-gray-500 text-xs">每晚/{{ dateRange ? calculateNights() + '晚' : '' }}</div>
                </div>
                
                <div class="mt-4">
                  <el-button 
                    type="primary" 
                    :disabled="!dateRange || room.available <= 0"
                    @click="handleBooking(room)"
                  >
                    {{ room.available > 0 ? '立即预订' : '已满房' }}
                  </el-button>
                </div>
              </div>
            </div>
          </el-card>
        </div>
      </div>
      
      <!-- 用户评价 -->
      <div class="mb-10">
        <h2 class="text-xl font-bold mb-4 border-b pb-2">用户评价</h2>
        
        <div v-if="homestay.reviews.length === 0" class="text-center py-6">
          <el-empty description="暂无评价" />
        </div>
        
        <div v-else>
          <div v-for="review in homestay.reviews" :key="review.id" class="mb-6 border-b pb-6">
            <div class="flex justify-between items-start mb-2">
              <div class="flex items-center">
                <img :src="review.userAvatar" :alt="review.userName" class="w-10 h-10 rounded-full mr-3">
                <div>
                  <div class="font-medium">{{ review.userName }}</div>
                  <div class="text-gray-500 text-xs">{{ review.createTime }}</div>
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
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Star, StarFilled } from '@element-plus/icons-vue'
import { useUserStore } from '@/store/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const homestayId = route.params.id

// 页面状态
const loading = ref(true)
const homestay = ref(null)
const isFavorite = ref(false)
const dateRange = ref(null)
const guestCount = ref(2)

// 解析设施特色
const parsedFeatures = computed(() => {
  if (!homestay.value || !homestay.value.features) return []
  try {
    return JSON.parse(homestay.value.features)
  } catch (e) {
    return []
  }
})

// 禁用过去的日期
const disabledDate = (time) => {
  return time.getTime() < Date.now() - 8.64e7 // 不能选择今天之前的日期
}

// 计算入住晚数
const calculateNights = () => {
  if (!dateRange.value || !dateRange.value[0] || !dateRange.value[1]) return 0
  const start = new Date(dateRange.value[0])
  const end = new Date(dateRange.value[1])
  return Math.round((end - start) / (1000 * 60 * 60 * 24))
}

// 获取民宿详情
const fetchHomestayDetail = async () => {
  loading.value = true
  
  try {
    // 模拟API调用，实际项目中应替换为真实API
    setTimeout(() => {
      homestay.value = {
        id: homestayId,
        name: '篁岭山居',
        villageName: '婺源篁岭',
        villageId: 1,
        propertyType: '独栋房屋',
        address: '江西省上饶市婺源县篁岭古村23号',
        intro: '位于篁岭古村中心位置，徽派风格装修，可俯瞰整个村落美景。',
        description: `<p>篁岭山居位于篁岭古村中心位置，是一栋典型的徽派建筑，拥有300多年历史。整栋民宿经过精心修缮，保留了原有的建筑结构和特色，同时融入现代化的设施和服务。</p>
        <p>从民宿的窗户和露台可以俯瞰整个篁岭古村的美景，尤其是在晒秋时节，可以欣赏到村中晾晒的农作物形成的独特景观。</p>
        <p>民宿内设有传统茶室、阅读角落，提供免费的茶水和书籍，让您在体验徽州文化的同时，享受宁静舒适的住宿环境。</p>`,
        coverImage: 'https://picsum.photos/id/1048/600/400',
        location: '29.151,117.934',
        features: '["免费WiFi","空调","24小时热水","观景露台","免费早餐","停车场"]',
        checkInTime: '14:00',
        checkOutTime: '12:00',
        ordersCount: 256,
        rating: 4.8,
        gallery: [
          { imageUrl: 'https://picsum.photos/id/1048/600/400', caption: '民宿外观' },
          { imageUrl: 'https://picsum.photos/id/1037/600/400', caption: '客房内景' },
          { imageUrl: 'https://picsum.photos/id/1040/600/400', caption: '观景露台' },
          { imageUrl: 'https://picsum.photos/id/1044/600/400', caption: '公共区域' }
        ],
        roomTypes: [
          {
            id: 101,
            name: '标准双床房',
            coverImage: 'https://picsum.photos/id/1037/600/400',
            area: 25,
            price: 388,
            discountPrice: 348,
            bedType: '双人床',
            maxGuests: 2,
            description: '舒适的标准双床房，配备现代化设施，窗外可见村落美景。',
            facilities: '["空调","电视","独立卫浴","免费洗漱用品","电热水壶"]',
            breakfast: true,
            cancellation: '入住前24小时可免费取消',
            available: 3
          },
          {
            id: 102,
            name: '豪华大床房',
            coverImage: 'https://picsum.photos/id/1040/600/400',
            area: 35,
            price: 488,
            discountPrice: null,
            bedType: '大床',
            maxGuests: 2,
            description: '宽敞的豪华大床房，配备高品质床品和设施，提供更舒适的住宿体验。',
            facilities: '["空调","电视","独立卫浴","免费洗漱用品","电热水壶","迷你吧"]',
            breakfast: true,
            cancellation: '入住前24小时可免费取消',
            available: 1
          },
          {
            id: 103,
            name: '家庭套房',
            coverImage: 'https://picsum.photos/id/1044/600/400',
            area: 50,
            price: 688,
            discountPrice: 628,
            bedType: '大床+单人床',
            maxGuests: 3,
            description: '适合家庭入住的套房，拥有独立的客厅和卧室，提供更多私密空间。',
            facilities: '["空调","电视","独立卫浴","免费洗漱用品","电热水壶","迷你吧","沙发"]',
            breakfast: true,
            cancellation: '入住前48小时可免费取消',
            available: 0
          }
        ],
        reviews: [
          {
            id: 201,
            userName: '张先生',
            userAvatar: 'https://picsum.photos/id/1005/100/100',
            rating: 5,
            content: '环境非常好，房间干净整洁，服务也很周到。从露台可以看到整个村子的景色，特别是晚上的星空很美。早餐也很丰盛，推荐大家来住。',
            createTime: '2023-05-15',
            reply: '感谢您的好评，欢迎下次再来!'
          },
          {
            id: 202,
            userName: '李女士',
            userAvatar: 'https://picsum.photos/id/1006/100/100',
            rating: 4.5,
            content: '民宿位置很好，就在村中心，出行很方便。房间布置很有特色，能感受到浓浓的徽派风格。唯一的小缺点是隔音稍差，但总体很满意。',
            createTime: '2023-04-22',
            reply: '感谢您的反馈，我们会继续改进隔音问题，期待您的再次光临!'
          },
          {
            id: 203,
            userName: '王先生',
            userAvatar: 'https://picsum.photos/id/1012/100/100',
            rating: 4,
            content: '住宿体验不错，老板很热情，给我们介绍了很多当地的特色和景点。房间设施齐全，就是淡季人少，晚上有点安静过头了。',
            createTime: '2023-03-10',
            reply: null
          }
        ]
      }
      
      // 模拟检查是否已收藏
      isFavorite.value = Math.random() > 0.5
      
      loading.value = false
    }, 1000)
  } catch (error) {
    ElMessage.error('获取民宿详情失败')
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

// 处理日期变化
const handleDateChange = () => {
  // 实际项目中可以在这里调用API获取选定日期范围内的房型可用情况和价格
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
  document.getElementById('rooms').scrollIntoView({ behavior: 'smooth' })
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
  
  // 模拟添加到购物车或直接跳转到结算页面
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