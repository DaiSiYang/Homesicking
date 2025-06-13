<template>
  <div class="product-detail-container">
    <div class="page-header flex justify-between items-center mb-4">
      <div class="flex items-center">
        <el-button icon="Back" @click="$router.back()" text>返回</el-button>
        <h2 class="text-xl font-bold">特产详情</h2>
      </div>
      <div>
        <el-button 
          v-if="product?.status === 'pending'"
          type="success" 
          @click="reviewProduct('approved')"
        >
          通过审核
        </el-button>
        <el-button 
          v-if="product?.status === 'pending'"
          type="danger" 
          @click="reviewProduct('rejected')"
        >
          拒绝审核
        </el-button>
        <el-button 
          v-if="product?.status !== 'pending'"
          :type="product?.status === 'active' ? 'warning' : 'success'" 
          @click="toggleProductStatus"
        >
          {{ product?.status === 'active' ? '下架商品' : '上架商品' }}
        </el-button>
      </div>
    </div>

    <el-card v-loading="loading" class="mb-4">
      <div v-if="product" class="product-info">
        <div class="flex flex-wrap">
          <!-- 商品图片 -->
          <div class="w-full lg:w-2/5 p-4">
            <el-carousel :interval="4000" type="card" height="300px">
              <el-carousel-item v-for="(image, index) in product.images" :key="index">
                <el-image 
                  style="width: 100%; height: 100%" 
                  :src="image" 
                  fit="cover" 
                />
              </el-carousel-item>
            </el-carousel>
          </div>
          
          <!-- 商品信息 -->
          <div class="w-full lg:w-3/5 p-4">
            <h3 class="text-xl font-bold mb-2">{{ product.name }}</h3>
            <div class="flex items-center mb-2">
              <el-tag :type="getStatusType(product.status)" class="mr-2">
                {{ getStatusText(product.status) }}
              </el-tag>
              <el-tag>{{ getCategoryText(product.category) }}</el-tag>
            </div>
            
            <div class="text-xl text-orange-500 font-bold mb-4">
              ¥{{ product.price.toFixed(2) }}
            </div>
            
            <el-descriptions :column="1" border>
              <el-descriptions-item label="商品ID">{{ product.id }}</el-descriptions-item>
              <el-descriptions-item label="所属商户">
                <div class="flex items-center">
                  <el-avatar :size="30" :src="product.merchant_logo" class="mr-2" />
                  {{ product.merchant_name }}
                </div>
              </el-descriptions-item>
              <el-descriptions-item label="库存数量">{{ product.stock }}</el-descriptions-item>
              <el-descriptions-item label="销售数量">{{ product.sales }}</el-descriptions-item>
              <el-descriptions-item label="上架时间">{{ product.created_at }}</el-descriptions-item>
              <el-descriptions-item label="更新时间">{{ product.updated_at }}</el-descriptions-item>
            </el-descriptions>
          </div>
        </div>
        
        <!-- 商品详情 -->
        <div class="mt-6">
          <el-tabs>
            <el-tab-pane label="商品详情">
              <div class="product-description">
                <h4 class="text-lg font-medium mb-2">商品描述</h4>
                <div class="bg-gray-50 p-4 rounded">
                  {{ product.description }}
                </div>
                
                <h4 class="text-lg font-medium mt-4 mb-2">商品特点</h4>
                <el-tag v-for="(feature, index) in product.features" :key="index" class="mr-2 mb-2">
                  {{ feature }}
                </el-tag>
                
                <h4 class="text-lg font-medium mt-4 mb-2">商品规格</h4>
                <el-table :data="product.specifications" style="width: 100%">
                  <el-table-column prop="name" label="规格名称" width="180" />
                  <el-table-column prop="value" label="规格值" />
                </el-table>
              </div>
            </el-tab-pane>
            
            <el-tab-pane label="评价信息">
              <div class="product-reviews">
                <div class="flex items-center mb-4">
                  <div class="text-3xl font-bold text-orange-500 mr-4">{{ product.rating }}</div>
                  <el-rate v-model="product.rating" disabled show-score text-color="#ff9900" />
                  <div class="ml-2 text-gray-500">共{{ product.review_count }}条评价</div>
                </div>
                
                <el-empty v-if="!reviews.length" description="暂无评价" />
                
                <div v-else class="reviews-list">
                  <div v-for="(review, index) in reviews" :key="index" class="review-item border-b pb-4 mb-4">
                    <div class="flex justify-between">
                      <div class="flex items-center">
                        <el-avatar :size="40" :src="review.user_avatar" />
                        <div class="ml-2">
                          <div>{{ review.user_name }}</div>
                          <div class="text-gray-500 text-sm">{{ review.created_at }}</div>
                        </div>
                      </div>
                      <el-rate v-model="review.rating" disabled />
                    </div>
                    <div class="mt-2">{{ review.content }}</div>
                    <div v-if="review.images && review.images.length" class="mt-2 flex flex-wrap">
                      <el-image
                        v-for="(image, imgIndex) in review.images"
                        :key="imgIndex"
                        style="width: 80px; height: 80px; margin: 5px;"
                        :src="image"
                        :preview-src-list="review.images"
                        fit="cover"
                      />
                    </div>
                  </div>
                </div>
              </div>
            </el-tab-pane>
          </el-tabs>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'

const route = useRoute()
const router = useRouter()
const productId = route.params.id

// 数据
const product = ref(null)
const loading = ref(true)
const reviews = ref([])

// 获取特产详情
const fetchProductDetail = async () => {
  loading.value = true
  try {
    // 模拟API请求
    await new Promise(resolve => setTimeout(resolve, 500))
    
    // 模拟数据 - 实际项目中应该从API获取
    product.value = {
      id: productId,
      name: '葫芦峪蜂蜜',
      images: [
        'https://via.placeholder.com/800x600',
        'https://via.placeholder.com/800x600',
        'https://via.placeholder.com/800x600'
      ],
      price: 128.00,
      stock: 100,
      sales: 58,
      category: 'food',
      status: 'active',
      created_at: '2023-10-15 09:32:45',
      updated_at: '2023-10-20 14:25:36',
      merchant_id: 1,
      merchant_name: '山水间农家乐',
      merchant_logo: 'https://via.placeholder.com/100',
      description: '葫芦峪蜂蜜采自深山野花，蜂农采用传统工艺，不加任何添加剂，保留了蜂蜜的原始风味和营养价值。具有色泽金黄，质地细腻，口感醇厚的特点。富含多种维生素和矿物质，具有润肺止咳、调节肠胃等功效。',
      features: ['纯天然', '无添加', '深山野花', '传统工艺'],
      specifications: [
        { name: '净含量', value: '500g/瓶' },
        { name: '保质期', value: '24个月' },
        { name: '储存方法', value: '常温避光保存' },
        { name: '产地', value: '浙江省杭州市临安区太湖源镇' }
      ],
      rating: 4.8,
      review_count: 26
    }
    
    // 获取评价
    fetchReviews()
  } catch (error) {
    console.error('获取特产详情失败:', error)
    ElMessage.error('获取特产详情失败')
  } finally {
    loading.value = false
  }
}

// 获取评价
const fetchReviews = async () => {
  try {
    // 模拟API请求
    await new Promise(resolve => setTimeout(resolve, 300))
    
    // 模拟数据
    reviews.value = [
      {
        id: 1,
        user_id: 101,
        user_name: '张三',
        user_avatar: 'https://via.placeholder.com/100',
        rating: 5,
        content: '蜂蜜质量非常好，口感醇厚，甜度适中，包装也很精美，很满意的一次购买！',
        created_at: '2023-11-10 15:23:45',
        images: [
          'https://via.placeholder.com/400x300',
          'https://via.placeholder.com/400x300'
        ]
      },
      {
        id: 2,
        user_id: 102,
        user_name: '李四',
        user_avatar: 'https://via.placeholder.com/100',
        rating: 4,
        content: '蜂蜜味道不错，但是快递包装可以再加强一些，有一点漏出来了。',
        created_at: '2023-11-05 09:12:36',
        images: []
      }
    ]
  } catch (error) {
    console.error('获取评价失败:', error)
    ElMessage.error('获取评价失败')
  }
}

// 审核特产
const reviewProduct = (action) => {
  ElMessageBox.confirm(
    `确定要${action === 'approved' ? '通过' : '拒绝'}特产"${product.value.name}"的审核吗？`,
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: action === 'approved' ? 'success' : 'warning'
    }
  ).then(async () => {
    try {
      // 模拟API请求
      await new Promise(resolve => setTimeout(resolve, 300))
      
      // 更新本地状态
      product.value.status = action === 'approved' ? 'active' : 'rejected'
      ElMessage.success(`已${action === 'approved' ? '通过' : '拒绝'}特产"${product.value.name}"的审核`)
    } catch (error) {
      console.error('操作失败:', error)
      ElMessage.error('操作失败')
    }
  }).catch(() => {})
}

// 切换特产状态
const toggleProductStatus = () => {
  const newStatus = product.value.status === 'active' ? 'inactive' : 'active'
  const actionText = newStatus === 'active' ? '上架' : '下架'
  
  ElMessageBox.confirm(`确定要${actionText}特产"${product.value.name}"吗？`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      // 模拟API请求
      await new Promise(resolve => setTimeout(resolve, 300))
      
      // 更新本地状态
      product.value.status = newStatus
      ElMessage.success(`已${actionText}特产"${product.value.name}"`)
    } catch (error) {
      console.error('操作失败:', error)
      ElMessage.error('操作失败')
    }
  }).catch(() => {})
}

// 获取分类文本
const getCategoryText = (category) => {
  const categories = {
    'agricultural': '农产品',
    'handicraft': '手工艺品',
    'food': '食品',
    'other': '其他'
  }
  return categories[category] || '未知'
}

// 获取状态类型
const getStatusType = (status) => {
  const types = {
    'active': 'success',
    'inactive': 'info',
    'pending': 'warning',
    'rejected': 'danger'
  }
  return types[status] || 'info'
}

// 获取状态文本
const getStatusText = (status) => {
  const texts = {
    'active': '上架中',
    'inactive': '已下架',
    'pending': '待审核',
    'rejected': '已拒绝'
  }
  return texts[status] || '未知'
}

onMounted(() => {
  fetchProductDetail()
})
</script>

<style scoped>
.product-detail-container {
  padding: 20px;
}

.product-description {
  line-height: 1.6;
}
</style> 