<template>
  <div class="food-detail container mx-auto py-8 px-4">
    <!-- 加载状态 -->
    <div v-if="loading" class="flex justify-center py-10">
      <el-skeleton :rows="15" animated />
    </div>

    <div v-else-if="!food" class="text-center py-10">
      <el-empty description="未找到该美食信息" />
    </div>

    <template v-else>
      <!-- 面包屑导航 -->
      <el-breadcrumb separator="/" class="mb-6">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item :to="{ path: '/foods' }">美食</el-breadcrumb-item>
        <el-breadcrumb-item>{{ food.name }}</el-breadcrumb-item>
      </el-breadcrumb>

      <!-- 美食基本信息 -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
        <!-- 美食图片轮播 -->
        <div class="food-gallery">
          <el-carousel :interval="4000" height="400px" indicator-position="outside">
            <el-carousel-item v-for="(image, index) in food.images" :key="index">
              <img :src="image" alt="美食图片" class="w-full h-full object-cover rounded-lg">
            </el-carousel-item>
          </el-carousel>
        </div>

        <!-- 美食信息 -->
        <div class="food-info">
          <div class="flex justify-between items-center mb-4">
            <h1 class="text-2xl font-bold">{{ food.name }}</h1>
            <el-button type="primary" @click="addToFavorites" :icon="Star" circle />
          </div>
          
          <div class="flex items-center mb-4">
            <el-rate v-model="food.rating" disabled text-color="#ff9900" />
            <span class="ml-2 text-orange-500">{{ food.rating }}分</span>
            <span class="ml-4 text-gray-500">{{ food.reviewCount }}条点评</span>
          </div>
          
          <p class="text-gray-600 mb-4">{{ food.category }} | {{ food.region }}</p>
          
          <div class="price-info mb-4 bg-gray-50 p-4 rounded-lg">
            <div class="flex items-center">
              <span class="text-gray-600 mr-2">价格:</span>
              <span class="text-red-500 text-2xl font-bold">¥{{ food.price }}/人</span>
            </div>
          </div>
          
          <div class="tags mb-4">
            <span class="text-gray-600 mr-2">特色标签:</span>
            <el-tag v-for="(tag, index) in food.tags" :key="index" class="mr-2 mb-2">
              {{ tag }}
            </el-tag>
          </div>
          
          <div class="address-info mb-4">
            <p class="text-gray-600"><strong>推荐餐厅:</strong> {{ food.recommendedRestaurant }}</p>
            <p class="text-gray-600"><strong>地址:</strong> {{ food.address }}</p>
            <p class="text-gray-600"><strong>营业时间:</strong> {{ food.businessHours }}</p>
          </div>
          
          <div class="action-buttons">
            <el-button type="primary" @click="makeReservation">在线预订</el-button>
            <el-button type="success" @click="viewLocation">查看位置</el-button>
          </div>
        </div>
      </div>

      <!-- 美食详情信息 -->
      <el-tabs class="mb-8" v-if="food">
        <el-tab-pane label="美食介绍">
          <div class="food-description mb-6">
            <h2 class="text-xl font-bold mb-4">详细介绍</h2>
            <div class="text-gray-700 leading-relaxed whitespace-pre-line">
              {{ food.description || '暂无介绍' }}
            </div>
          </div>
          
          <div class="food-making">
            <h2 class="text-xl font-bold mb-4">制作工艺</h2>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
              <div v-for="(step, index) in (food.makingProcess || [])" :key="index" class="making-step">
                <div class="step-number bg-primary text-white w-8 h-8 rounded-full flex items-center justify-center mb-2">
                  {{ index + 1 }}
                </div>
                <h3 class="font-bold mb-1">{{ step.title || '步骤' + (index + 1) }}</h3>
                <p class="text-gray-600 text-sm">{{ step.description || '制作步骤描述' }}</p>
              </div>
            </div>
          </div>
          
          <div class="food-ingredients">
            <h2 class="text-xl font-bold mb-4">主要食材</h2>
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div v-for="(ingredient, index) in (food.ingredients || [])" :key="index" class="ingredient-item p-3 border border-gray-200 rounded-lg text-center">
                <p class="font-bold">{{ ingredient.name || '未知食材' }}</p>
                <p class="text-gray-500 text-sm">{{ ingredient.description || '新鲜食材' }}</p>
              </div>
            </div>
          </div>
        </el-tab-pane>
        
        <el-tab-pane label="营养价值">
          <div class="nutrition-info">
            <h2 class="text-xl font-bold mb-4">营养成分表</h2>
            <el-table :data="food.nutritionFacts || []" stripe class="mb-6">
              <el-table-column prop="name" label="营养素" width="180" />
              <el-table-column prop="value" label="含量" />
              <el-table-column prop="dailyValue" label="每日参考值%" />
            </el-table>
            
            <div class="nutrition-description">
              <h3 class="font-bold mb-2">营养特点</h3>
              <p class="text-gray-700">{{ food.nutritionDescription || '营养丰富，口感独特' }}</p>
            </div>
          </div>
        </el-tab-pane>
        
        <el-tab-pane label="用户点评">
          <div class="reviews">
            <div class="review-summary flex items-center mb-6">
              <div class="rating-info mr-8">
                <p class="text-3xl font-bold text-orange-500">{{ food.rating || 0 }}</p>
                <p class="text-sm text-gray-500">综合评分</p>
              </div>
              <div class="rating-distribution flex-grow">
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
            
            <div v-if="(food.reviews || []).length === 0" class="text-center py-4">
              <el-empty description="暂无点评" />
            </div>
            <div v-else class="review-list">
              <div 
                v-for="(review, index) in (food.reviews || [])"
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
                  </div>
                </div>
              </div>
            </div>
            
            <div class="write-review mt-6">
              <el-button type="primary" @click="showReviewDialog = true">写点评</el-button>
            </div>
          </div>
        </el-tab-pane>
      </el-tabs>

      <!-- 相关美食推荐 -->
      <div class="related-foods">
        <h2 class="text-xl font-bold mb-4">相关美食推荐</h2>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div v-for="relatedFood in food.relatedFoods" :key="relatedFood.id" class="related-food-item">
            <el-card shadow="hover" class="h-full">
              <img :src="relatedFood.image" alt="相关美食" class="w-full h-32 object-cover rounded mb-2">
              <h3 class="text-lg font-bold mb-1">{{ relatedFood.name }}</h3>
              <div class="flex items-center mb-2">
                <el-rate v-model="relatedFood.rating" disabled :max="5" size="small" />
                <span class="ml-1 text-orange-500 text-sm">{{ relatedFood.rating }}</span>
              </div>
              <p class="text-red-500 font-bold mb-2">¥{{ relatedFood.price }}/人</p>
              <router-link :to="`/foods/${relatedFood.id}`">
                <el-button type="primary" size="small">查看详情</el-button>
              </router-link>
            </el-card>
          </div>
        </div>
      </div>
    </template>

    <!-- 评论对话框 -->
    <el-dialog
      v-model="showReviewDialog"
      title="写点评"
      width="500px"
    >
      <el-form :model="reviewForm" label-width="80px">
        <el-form-item label="评分">
          <el-rate v-model="reviewForm.rating" />
        </el-form-item>
        <el-form-item label="点评内容">
          <el-input
            v-model="reviewForm.content"
            type="textarea"
            :rows="4"
            placeholder="请分享您的用餐体验"
          />
        </el-form-item>
        <el-form-item label="上传图片">
          <el-upload
            action="#"
            list-type="picture-card"
            :auto-upload="false"
            :limit="5"
          >
            <el-icon><Plus /></el-icon>
          </el-upload>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showReviewDialog = false">取消</el-button>
          <el-button type="primary" @click="submitReview">提交</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 预订对话框 -->
    <el-dialog
      v-model="showReservationDialog"
      title="餐厅预订"
      width="500px"
    >
      <el-form :model="reservationForm" label-width="80px">
        <el-form-item label="日期">
          <el-date-picker 
            v-model="reservationForm.date" 
            type="date" 
            placeholder="选择日期"
            :disabled-date="disabledDate"
            class="w-full"
          />
        </el-form-item>
        <el-form-item label="时间">
          <el-time-picker
            v-model="reservationForm.time"
            format="HH:mm"
            placeholder="选择时间"
            class="w-full"
          />
        </el-form-item>
        <el-form-item label="人数">
          <el-input-number v-model="reservationForm.people" :min="1" :max="20" />
        </el-form-item>
        <el-form-item label="联系电话">
          <el-input v-model="reservationForm.phone" placeholder="请输入联系电话" />
        </el-form-item>
        <el-form-item label="备注">
          <el-input
            v-model="reservationForm.remarks"
            type="textarea"
            :rows="2"
            placeholder="如有特殊需求，请在此说明"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showReservationDialog = false">取消</el-button>
          <el-button type="primary" @click="submitReservation">提交预订</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Star, Plus } from '@element-plus/icons-vue'
import { getFoodDetail } from '@/api/foods'

const route = useRoute()
const loading = ref(true)
const food = ref(null)
const showReviewDialog = ref(false)
const showReservationDialog = ref(false)

// 评分分布（模拟数据）
const ratingDistribution = ref([75, 15, 8, 1.5, 0.5])

// 评论表单
const reviewForm = ref({
  rating: 5,
  content: '',
  images: []
})

// 预订表单
const reservationForm = ref({
  date: '',
  time: '',
  people: 2,
  phone: '',
  remarks: ''
})

// 获取美食详情
onMounted(() => {
  fetchFoodDetail()
})

const fetchFoodDetail = async () => {
  loading.value = true

  try {
    const foodId = route.params.id
    const res = await getFoodDetail(foodId)
    
    if (res.code === 200) {
      const rawData = res.data
      
      // 添加更严格的数据验证
      let ingredients = []
      try {
        if (rawData.ingredients && typeof rawData.ingredients === 'string') {
          const parsed = JSON.parse(rawData.ingredients)
          ingredients = Array.isArray(parsed) ? parsed.map(name => ({ 
            name: name || '未知食材', 
            description: '' 
          })) : []
        }
      } catch (e) {
        console.warn('解析ingredients失败:', e)
        ingredients = []
      }
      
      food.value = {
        id: rawData.id || 0,
        name: rawData.name || '未知美食',
        images: rawData.gallery && Array.isArray(rawData.gallery) && rawData.gallery.length > 0 
          ? rawData.gallery.map(item => item.image_url || '').filter(Boolean)
          : [rawData.cover_image || '/default-food.jpg'],
        price: rawData.current_price || rawData.price || 0,
        rating: parseFloat(rawData.rating) || 0,
        reviewCount: rawData.views || 0,
        category: rawData.category_name || '特色美食',
        region: rawData.village_name || '未知地区',
        description: rawData.description || '暂无介绍',
        ingredients: ingredients,
        recommendedRestaurant: rawData.merchant_name || '暂无推荐餐厅',
        address: rawData.village_name || '地址待更新',
        businessHours: '09:00-21:00',
        tags: rawData.category_name ? [rawData.category_name] : ['特色美食'],
        makingProcess: [
          {
            title: '食材准备',
            description: '精选优质食材'
          },
          {
            title: '传统工艺',
            description: rawData.intro || '采用传统制作工艺'
          },
          {
            title: '精心制作',
            description: '匠心独运，精心制作'
          }
        ],
        // 添加缺失的字段
        nutritionFacts: [],
        nutritionDescription: '营养丰富，口感独特',
        reviews: [],
        relatedFoods: []
      }
    } else {
      ElMessage.error(res.message || '获取美食详情失败')
    }
  } catch (error) {
    console.error('获取美食详情失败:', error)
    ElMessage.error('获取美食详情失败')
  } finally {
    loading.value = false
  }
}

// 添加到收藏
const addToFavorites = () => {
  ElMessage.success('已添加到收藏')
}

// 在线预订
const makeReservation = () => {
  showReservationDialog.value = true
}

// 查看位置
const viewLocation = () => {
  ElMessage.info('正在打开地图查看位置')
  // 在实际应用中，这里可能会打开地图组件或跳转到地图页面
}

// 禁用日期（今天之前的日期不可选）
const disabledDate = (time) => {
  return time.getTime() < Date.now() - 8.64e7 // 8.64e7 = 一天的毫秒数
}

// 提交评论
const submitReview = () => {
  if (!reviewForm.value.content) {
    ElMessage.warning('请输入点评内容')
    return
  }
  
  // 模拟提交评论
  ElMessage.success('点评提交成功')
  showReviewDialog.value = false
  
  // 重置表单
  reviewForm.value = {
    rating: 5,
    content: '',
    images: []
  }
}

// 提交预订
const submitReservation = () => {
  if (!reservationForm.value.date || !reservationForm.value.time) {
    ElMessage.warning('请选择预订日期和时间')
    return
  }
  
  if (!reservationForm.value.phone) {
    ElMessage.warning('请输入联系电话')
    return
  }
  
  // 模拟提交预订
  ElMessage.success('预订提交成功，商家会尽快与您联系确认')
  showReservationDialog.value = false
  
  // 重置表单
  reservationForm.value = {
    date: '',
    time: '',
    people: 2,
    phone: '',
    remarks: ''
  }
}
</script>

<style scoped>
.making-step {
  transition: transform 0.3s ease;
}

.making-step:hover {
  transform: translateY(-5px);
}

.ingredient-item {
  transition: all 0.3s ease;
}

.ingredient-item:hover {
  border-color: #409EFF;
  background-color: #f0f9ff;
}

.related-food-item {
  transition: transform 0.3s ease;
}

.related-food-item:hover {
  transform: translateY(-5px);
}

.bg-primary {
  background-color: #409EFF;
}
</style>