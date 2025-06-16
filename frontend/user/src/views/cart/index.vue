<template>
  <div class="page-container py-8">
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-gray-800">我的购物车</h1>
    </div>

    <!-- 购物车为空状态 -->
    <div v-if="cartStore.isEmpty" class="card p-10 text-center">
      <el-empty description="购物车还是空的，去选购喜欢的商品吧~">
        <el-button type="primary" @click="$router.push('/')">去购物</el-button>
      </el-empty>
    </div>

    <!-- 购物车有商品 -->
    <div v-else>
      <div class="card mb-6">
        <div class="flex bg-gray-50 py-3 px-4 rounded-t-lg font-medium text-gray-600">
          <div class="w-16 text-center">
            <el-checkbox 
              v-model="isAllSelected" 
              @change="handleSelectAll"
              :indeterminate="isIndeterminate"
            />
          </div>
          <div class="flex-1">商品信息</div>
          <div class="w-32 text-center">单价</div>
          <div class="w-32 text-center">数量</div>
          <div class="w-32 text-center">小计</div>
          <div class="w-24 text-center">操作</div>
        </div>

        <el-skeleton :loading="cartStore.loading" :rows="3" animated>
          <template #default>
            <!-- 购物车项 -->
            <div v-for="item in cartStore.cartItems" :key="item.id" class="border-b last:border-0 py-4 px-4">
              <div class="flex items-center">
                <div class="w-16 text-center">
                  <el-checkbox v-model="selectedItems[item.id]" @change="updateSelectedStatus" />
                </div>
                <div class="flex-1">
                  <!-- 商品信息 -->
                  <div class="flex">
                    <img :src="item.item_image" alt="商品图片" class="w-20 h-20 object-cover rounded mr-4">
                    <div>
                      <h3 class="text-base font-medium text-gray-800 mb-2">{{ item.item_name }}</h3>
                      <p class="text-sm text-gray-500">
                        {{ getItemTypeText(item.item_type) }}
                        <span v-if="item.item_type === 'room'">
                          · {{ formatDate(item.check_in_date) }} 至 {{ formatDate(item.check_out_date) }}
                        </span>
                      </p>
                    </div>
                  </div>
                </div>
                <div class="w-32 text-center">
                  <span class="text-red-600 font-medium">¥{{ formatPrice(item.item_price) }}</span>
                </div>
                <div class="w-32 text-center">
                  <el-input-number 
                    v-model="item.quantity" 
                    :min="1" 
                    :max="99"
                    @change="(val) => handleQuantityChange(item.id, val)"
                    :disabled="item.item_type === 'room'"
                  />
                </div>
                <div class="w-32 text-center">
                  <span class="text-red-600 font-medium">¥{{ formatPrice(item.total_price) }}</span>
                </div>
                <div class="w-24 text-center">
                  <el-button type="danger" link @click="handleRemove(item.id)">删除</el-button>
                </div>
              </div>
            </div>
          </template>
        </el-skeleton>
      </div>

      <!-- 结算区域 -->
      <div class="flex justify-between items-center bg-white p-4 rounded-lg shadow">
        <div class="flex items-center">
          <el-checkbox 
            v-model="isAllSelected" 
            @change="handleSelectAll"
            :indeterminate="isIndeterminate"
          >全选</el-checkbox>
          <el-button type="danger" link class="ml-4" @click="handleClearCart">清空购物车</el-button>
        </div>
        <div class="flex items-center">
          <div class="mr-8">
            <span class="text-gray-600">已选商品 <span class="text-red-600 font-medium">{{ selectedCount }}</span> 件</span>
            <span class="mx-4 text-gray-400">|</span>
            <span class="text-gray-600">合计：<span class="text-red-600 font-medium text-xl">¥{{ totalPrice.toFixed(2) }}</span></span>
          </div>
          <el-button type="primary" size="large" :disabled="selectedCount === 0" @click="handleCheckout">
            去结算
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessageBox } from 'element-plus'
import { useCartStore } from '@/store/cart'
import { useUserStore } from '@/store/user'

const router = useRouter()
const cartStore = useCartStore()
const userStore = useUserStore()

// 选中的商品
const selectedItems = ref({})

// 是否全选
const isAllSelected = computed(() => {
  const cartItemIds = cartStore.cartItems.map(item => item.id)
  return cartItemIds.length > 0 && cartItemIds.every(id => selectedItems.value[id])
})

// 是否半选
const isIndeterminate = computed(() => {
  const selectedCount = Object.values(selectedItems.value).filter(Boolean).length
  return selectedCount > 0 && selectedCount < cartStore.cartItems.length
})

// 选中的商品数量
const selectedCount = computed(() => {
  return Object.entries(selectedItems.value)
    .filter(([_, isSelected]) => isSelected)
    .reduce((sum, [id]) => {
      const item = cartStore.cartItems.find(item => item.id == id)
      return sum + (item ? item.quantity : 0)
    }, 0)
})

// 选中的商品总价
const totalPrice = computed(() => {
  return Object.entries(selectedItems.value)
    .filter(([_, isSelected]) => isSelected)
    .reduce((sum, [id]) => {
      const item = cartStore.cartItems.find(item => item.id == id)
      return sum + (item ? item.total_price : 0)
    }, 0)
})

// 获取商品类型文本
const getItemTypeText = (type) => {
  const typeMap = {
    'product': '特产',
    'food': '美食',
    'room': '住宿'
  }
  return typeMap[type] || '商品'
}

// 格式化日期
const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
}

// 全选/取消全选
const handleSelectAll = (val) => {
  cartStore.cartItems.forEach(item => {
    selectedItems.value[item.id] = val
  })
}

// 更新选中状态
const updateSelectedStatus = () => {
  // 这个函数会在单个勾选框变化时触发，不需要额外逻辑
}

// 修改数量
const handleQuantityChange = async (id, quantity) => {
  try {
    await cartStore.updateItemQuantity(id, quantity)
  } catch (error) {
    console.error('更新数量失败:', error)
  }
}

// 删除商品
const handleRemove = (id) => {
  ElMessageBox.confirm('确定要移除该商品吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await cartStore.removeCartItem(id)
      // 移除已选中的项
      delete selectedItems.value[id]
    } catch (error) {
      console.error('删除失败:', error)
    }
  }).catch(() => {})
}

// 清空购物车
const handleClearCart = () => {
  ElMessageBox.confirm('确定要清空购物车吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await cartStore.clearCartItems()
      selectedItems.value = {}
    } catch (error) {
      console.error('清空购物车失败:', error)
    }
  }).catch(() => {})
}

// 去结算
const handleCheckout = () => {
  // 获取已选中的商品ID列表
  const selectedIds = Object.entries(selectedItems.value)
    .filter(([_, isSelected]) => isSelected)
    .map(([id]) => parseInt(id))

  if (selectedIds.length === 0) {
    ElMessageBox.alert('请选择要结算的商品', '提示')
    return
  }

  // 将选中的商品ID传递到结算页面
  router.push({
    name: 'Checkout',
    query: { cart_ids: selectedIds.join(',') }
  })
}

// 初始化
onMounted(async () => {
  if (!userStore.isLoggedIn) {
    router.push('/login?redirect=/cart')
    return
  }

  try {
    await cartStore.fetchCartItems()
    // 默认全选
    cartStore.cartItems.forEach(item => {
      selectedItems.value[item.id] = true
    })
  } catch (error) {
    console.error('获取购物车失败:', error)
  }
})

// 格式化价格的方法
const formatPrice = (price) => {
  return (price || 0).toFixed(2)
}
</script>