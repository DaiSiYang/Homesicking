<template>
  <div class="user-center container mx-auto py-8 px-4 bamboo-pattern">
    <h1 class="text-3xl font-serif font-bold mb-8 text-ink-500 ink-border pb-2">个人中心</h1>
    
    <div class="grid grid-cols-1 gap-6">
      <!-- 导航菜单 - 现在是全宽显示 -->
      <el-card class="navigation-card">
        <template #header>
          <div class="font-bold">我的服务</div>
        </template>
        <el-menu 
          router 
          :default-active="activeNav" 
          class="user-navigation"
          mode="horizontal"
        >
          <el-menu-item index="/orders">
            <el-icon><Tickets /></el-icon>
            <span>我的订单</span>
          </el-menu-item>
          <el-menu-item index="/user/favorites">
            <el-icon><Star /></el-icon>
            <span>我的收藏</span>
          </el-menu-item>
          <el-menu-item index="/user/coupons">
            <el-icon><Discount /></el-icon>
            <span>优惠券</span>
          </el-menu-item>
          <el-menu-item index="/user/address">
            <el-icon><Location /></el-icon>
            <span>收货地址</span>
          </el-menu-item>
          <el-menu-item index="/user/reviews">
            <el-icon><ChatLineRound /></el-icon>
            <span>我的评价</span>
          </el-menu-item>
          <el-menu-item index="/user/settings">
            <el-icon><Setting /></el-icon>
            <span>账号设置</span>
          </el-menu-item>
        </el-menu>
      </el-card>
      
      <!-- 内容区 -->
      <!-- 显示子路由内容 -->
      <router-view v-if="$route.path !== '/user'"></router-view>
      
      <!-- 默认显示用户中心首页内容 -->
      <template v-else>
        <div class="user-center">
          <div class="main-content">
            <!-- 订单概览 -->
            <el-card class="mb-6">
              <template #header>
                <div class="flex justify-between items-center">
                  <span class="font-bold">我的订单</span>
                  <el-button text type="primary" @click="goToOrders()">查看全部</el-button>
                </div>
              </template>
              
              <!-- 订单状态统计 -->
              <div class="order-status-bar flex justify-around mb-6">
                <div class="status-item cursor-pointer" @click="goToOrders('pending')">
                  <el-badge :value="orderStatusCounts.pending" :hidden="!orderStatusCounts.pending">
                    <el-icon :size="24"><Wallet /></el-icon>
                  </el-badge>
                  <span class="mt-2 block">待付款</span>
                </div>
                
                <div class="status-item cursor-pointer" @click="goToOrders('processing')">
                  <el-badge :value="orderStatusCounts.processing" :hidden="!orderStatusCounts.processing">
                    <el-icon :size="24"><Box /></el-icon>
                  </el-badge>
                  <span class="mt-2 block">待发货</span>
                </div>
                
                <div class="status-item cursor-pointer" @click="goToOrders('shipped')">
                  <el-badge :value="orderStatusCounts.shipped" :hidden="!orderStatusCounts.shipped">
                    <el-icon :size="24"><Van /></el-icon>
                  </el-badge>
                  <span class="mt-2 block">待收货</span>
                </div>
                
                <div class="status-item cursor-pointer" @click="goToOrders('review')">
                  <el-badge :value="orderStatusCounts.review" :hidden="!orderStatusCounts.review">
                    <el-icon :size="24"><ChatDotRound /></el-icon>
                  </el-badge>
                  <span class="mt-2 block">待评价</span>
                </div>
                
                <div class="status-item cursor-pointer" @click="goToOrders('completed')">
                  <el-badge :value="orderStatusCounts.completed" :hidden="!orderStatusCounts.completed">
                    <el-icon :size="24"><CircleCheck /></el-icon>
                  </el-badge>
                  <span class="mt-2 block">已完成</span>
                </div>
              </div>
              
              <!-- 最近订单 -->
              <div v-if="recentOrders.length > 0">
                <div v-for="order in recentOrders" :key="order.id" class="recent-order mb-4 p-4 border border-earth-100 rounded hover:bg-gray-50">
                  <div class="flex justify-between items-center mb-2">
                    <div class="text-gray-500">订单号：{{ order.orderNumber }}</div>
                    <el-tag :type="getOrderStatusType(order.status)">{{ getOrderStatusText(order.status) }}</el-tag>
                  </div>
                  
                  <div class="flex justify-between items-center">
                    <div class="flex items-center">
                      <div class="flex -space-x-2">
                        <el-image 
                          v-for="(product, index) in order.products.slice(0, 3)" 
                          :key="index"
                          :src="product.image"
                          class="w-10 h-10 rounded-full border-2 border-white"
                          fit="cover"
                        />
                      </div>
                      <div class="ml-4">
                        <div>共{{ order.totalItems }}件商品</div>
                        <div class="text-red-500 font-bold">¥{{ order.totalAmount }}</div>
                      </div>
                    </div>
                    
                    <div>
                      <el-button 
                        v-if="order.status === 'pending'" 
                        type="primary" 
                        size="small"
                        @click="payOrder(order.id)"
                      >去支付</el-button>
                      <el-button 
                        type="default" 
                        size="small"
                        @click="viewOrderDetail(order.id)"
                      >查看详情</el-button>
                    </div>
                  </div>
                </div>
              </div>
              
              <el-empty v-else description="暂无订单" />
            </el-card>
            
            <!-- 我的收藏 -->
            <el-card class="mb-6">
              <template #header>
                <div class="flex justify-between items-center">
                  <span class="font-bold">我的收藏</span>
                  <el-button text type="primary" @click="router.push('/favorites')">查看全部</el-button>
                </div>
              </template>
              
              <div v-if="favorites.length > 0" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-4">
                <div 
                  v-for="item in favorites" 
                  :key="item.id" 
                  class="favorite-item cursor-pointer"
                  @click="router.push(`/${item.category === '民宿' ? 'homestays' : 'products'}/${item.id}`)"
                >
                  <el-image 
                    :src="item.image" 
                    class="w-full h-24 object-cover rounded-md mb-2"
                    fit="cover"
                  />
                  <div class="truncate text-sm">{{ item.name }}</div>
                  <div class="text-red-500 text-sm">¥{{ item.price }}</div>
                </div>
              </div>
              
              <el-empty v-else description="暂无收藏" />
            </el-card>
            
            <!-- 最近浏览 -->
            <el-card>
              <template #header>
                <div class="flex justify-between items-center">
                  <span class="font-bold">最近浏览</span>
                  <el-button text type="primary">查看全部</el-button>
                </div>
              </template>
              
              <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-4">
                <div 
                  v-for="item in recentViews" 
                  :key="item.id" 
                  class="recent-view-item cursor-pointer"
                  @click="router.push(`/products/${item.id}`)"
                >
                  <el-image 
                    :src="item.image" 
                    class="w-full h-24 object-cover rounded-md mb-2"
                    fit="cover"
                  />
                  <div class="truncate text-sm">{{ item.name }}</div>
                  <div class="text-red-500 text-sm">¥{{ item.price }}</div>
                </div>
              </div>
            </el-card>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<style scoped>
.user-center {
  max-width: 1200px;
  margin: 0 auto;
}

.main-content {
  width: 100%;
}

/* 自定义导航菜单样式，更符合乡村风格 */
:deep(.el-menu) {
  border-bottom: none;
  display: flex;
  justify-content: space-around;
  flex-wrap: wrap;
}

:deep(.el-menu-item) {
  height: 60px;
  line-height: 60px;
  color: #5c4f3d;
}

:deep(.el-menu-item.is-active) {
  color: #a18f78;
  border-bottom-color: #a18f78;
}

:deep(.el-menu-item:hover) {
  background-color: #f9f6f2;
}

.status-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  transition: all 0.3s ease;
}

.status-item:hover {
  color: #a18f78;
}

.favorite-item {
  transition: transform 0.3s ease;
}

.favorite-item:hover {
  transform: translateY(-5px);
}

.recent-view-item {
  transition: transform 0.3s ease;
}

.recent-view-item:hover {
  transform: translateY(-5px);
}

/* 乡村水墨画风格的背景纹理 */
.bamboo-pattern {
  background-color: #f9f6f2;
  background-image: linear-gradient(rgba(162, 145, 120, 0.05) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(162, 145, 120, 0.05) 1px, transparent 1px);
  background-size: 20px 20px;
}

.ink-border {
  border-bottom: 2px solid #e8e0d5;
}
</style>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Wallet, Box, Van, ChatDotRound, CircleCheck } from '@element-plus/icons-vue'
import { useUserStore } from '@/store/user'  // 添加这一行

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()  // 添加这一行

// 当前激活的导航项
const activeNav = computed(() => {
  return route.path
})

// 订单状态统计
const orderStatusCounts = ref({
  pending: 2,
  processing: 1,
  shipped: 0,
  completed: 9,
  review: 3
})

// 最近订单
const recentOrders = ref([
  {
    id: 1,
    orderNumber: 'MXJ20230615001',
    status: 'pending',
    totalItems: 3,
    totalAmount: 380,
    products: [
      { image: 'https://picsum.photos/id/1060/100/100' },
      { image: 'https://picsum.photos/id/1061/100/100' },
      { image: 'https://picsum.photos/id/1062/100/100' }
    ]
  },
  {
    id: 2,
    orderNumber: 'MXJ20230612002',
    status: 'processing',
    totalItems: 1,
    totalAmount: 688,
    products: [
      { image: 'https://picsum.photos/id/1048/100/100' }
    ]
  },
  {
    id: 3,
    orderNumber: 'MXJ20230610003',
    status: 'completed',
    totalItems: 2,
    totalAmount: 156,
    products: [
      { image: 'https://picsum.photos/id/1082/100/100' },
      { image: 'https://picsum.photos/id/1080/100/100' }
    ]
  }
])

// 收藏列表
const favorites = ref([
  {
    id: 1,
    name: '婺源贡菊',
    category: '农副产品',
    price: 68,
    image: 'https://picsum.photos/id/1060/200/200'
  },
  {
    id: 2,
    name: '篁岭山景民宿',
    category: '民宿',
    price: 388,
    image: 'https://picsum.photos/id/1048/200/200'
  },
  {
    id: 3,
    name: '徽州毛豆腐',
    category: '美食',
    price: 38,
    image: 'https://picsum.photos/id/1080/200/200'
  }
])

// 最近浏览
const recentViews = ref([
  {
    id: 1,
    name: '云南普洱茶',
    price: 128,
    image: 'https://picsum.photos/id/1061/200/200'
  },
  {
    id: 2,
    name: '丽江纳西烤鱼',
    price: 68,
    image: 'https://picsum.photos/id/1083/200/200'
  },
  {
    id: 3,
    name: '景德镇青花瓷',
    price: 299,
    image: 'https://picsum.photos/id/1065/200/200'
  },
  {
    id: 4,
    name: '云端竹舍',
    price: 688,
    image: 'https://picsum.photos/id/1054/200/200'
  }
])

// 获取订单状态对应的标签类型
const getOrderStatusType = (status) => {
  const statusMap = {
    'pending': 'warning',
    'processing': 'primary',
    'shipped': 'info',
    'completed': 'success',
    'canceled': 'danger',
    'review': ''
  }
  return statusMap[status] || ''
}

// 获取订单状态对应的文字
const getOrderStatusText = (status) => {
  const statusMap = {
    'pending': '待付款',
    'processing': '待发货',
    'shipped': '待收货',
    'completed': '已完成',
    'canceled': '已取消',
    'review': '待评价'
  }
  return statusMap[status] || '未知状态'
}

// 跳转到订单列表（可带状态筛选）
const goToOrders = (status) => {
  router.push({
    path: '/orders',
    query: status ? { status } : {}
  })
}

// 查看订单详情
const viewOrderDetail = (orderId) => {
  router.push(`/orders/${orderId}`)
}

// 支付订单
const payOrder = (orderId) => {
  router.push(`/payment/${orderId}`)
}

onMounted(() => {
  // 实际应用中，这里会从API获取用户数据
  console.log('用户中心组件已挂载')
  // 移除这行调用，因为用户信息已经在store初始化时加载
  // userStore.fetchUserInfo()  // 删除这一行
  
  // 或者改为直接获取用户信息（如果需要的话）
  // const userInfo = userStore.getUserInfo()
})
</script>