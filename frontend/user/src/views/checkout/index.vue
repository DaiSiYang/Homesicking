<template>
  <div class="page-container py-8">
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-gray-800">确认订单</h1>
    </div>

    <el-skeleton :loading="loading" animated>
      <template #default>
        <div v-if="checkoutItems.length === 0" class="card p-10 text-center">
          <el-empty description="没有可结算的商品">
            <el-button type="primary" @click="$router.push('/cart')">返回购物车</el-button>
          </el-empty>
        </div>
        
        <template v-else>
          <!-- 联系信息表单 -->
          <div class="card mb-6 p-6">
            <h2 class="text-lg font-bold mb-4">联系人信息</h2>
            <el-form :model="contactForm" :rules="contactRules" ref="contactFormRef" label-width="100px">
              <el-form-item label="联系人姓名" prop="contact_name">
                <el-input v-model="contactForm.contact_name" placeholder="请输入联系人姓名" />
              </el-form-item>
              <el-form-item label="联系电话" prop="contact_phone">
                <el-input v-model="contactForm.contact_phone" placeholder="请输入联系电话" />
              </el-form-item>
              <el-form-item label="电子邮箱" prop="contact_email">
                <el-input v-model="contactForm.contact_email" placeholder="请输入电子邮箱（选填）" />
              </el-form-item>
              <el-form-item label="备注" prop="remark">
                <el-input 
                  v-model="contactForm.remark" 
                  type="textarea" 
                  placeholder="请输入备注信息（选填）" 
                  :rows="3"
                />
              </el-form-item>
            </el-form>
          </div>

          <!-- 订单商品 -->
          <div class="card mb-6">
            <div class="flex bg-gray-50 py-3 px-6 rounded-t-lg font-medium text-gray-600">
              <div class="flex-1">商品信息</div>
              <div class="w-32 text-center">单价</div>
              <div class="w-32 text-center">数量</div>
              <div class="w-32 text-center">小计</div>
            </div>

            <!-- 商品列表 -->
            <div v-for="item in checkoutItems" :key="item.id" class="border-b last:border-0 py-4 px-6">
              <div class="flex items-center">
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
                  <span class="text-red-600 font-medium">¥{{ item.item_price.toFixed(2) }}</span>
                </div>
                <div class="w-32 text-center">
                  <span>× {{ item.quantity }}</span>
                </div>
                <div class="w-32 text-center">
                  <span class="text-red-600 font-medium">¥{{ item.total_price.toFixed(2) }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- 订单汇总 -->
          <div class="card mb-6 p-6">
            <div class="flex justify-end">
              <div class="w-72">
                <div class="flex justify-between py-2">
                  <span class="text-gray-600">商品总额：</span>
                  <span class="text-gray-800">¥{{ totalAmount.toFixed(2) }}</span>
                </div>
                <div class="flex justify-between py-2">
                  <span class="text-gray-600">配送费：</span>
                  <span class="text-gray-800">¥0.00</span>
                </div>
                <div class="flex justify-between py-2 border-t border-gray-200 mt-2 pt-2">
                  <span class="text-gray-800 font-medium">实付金额：</span>
                  <span class="text-red-600 font-medium text-xl">¥{{ totalAmount.toFixed(2) }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- 提交按钮 -->
          <div class="flex justify-end mt-6">
            <el-button type="default" class="mr-4" @click="$router.push('/cart')">返回购物车</el-button>
            <el-button type="primary" :loading="submitting" @click="submitOrder">提交订单</el-button>
          </div>
        </template>
      </template>
    </el-skeleton>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useCartStore } from '@/store/cart'
import { useUserStore } from '@/store/user'
import { useOrderStore } from '@/store/order'

const route = useRoute()
const router = useRouter()
const cartStore = useCartStore()
const userStore = useUserStore()
const orderStore = useOrderStore()

const loading = ref(true)
const submitting = ref(false)
const contactFormRef = ref(null)
const checkoutItems = ref([])

// 联系信息表单
const contactForm = ref({
  contact_name: '',
  contact_phone: '',
  contact_email: '',
  remark: ''
})

// 表单验证规则
const contactRules = {
  contact_name: [
    { required: true, message: '请输入联系人姓名', trigger: 'blur' },
    { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
  ],
  contact_phone: [
    { required: true, message: '请输入联系电话', trigger: 'blur' },
    { pattern: /^1[3456789]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
  ],
  contact_email: [
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ]
}

// 计算总金额
const totalAmount = computed(() => {
  return checkoutItems.value.reduce((sum, item) => sum + item.total_price, 0)
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

// 提交订单
const submitOrder = () => {
  contactFormRef.value.validate(async (valid) => {
    if (!valid) {
      return false
    }

    if (checkoutItems.value.length === 0) {
      ElMessage.error('没有可结算的商品')
      return
    }

    try {
      submitting.value = true
      const cartIds = checkoutItems.value.map(item => item.id)
      
      const orderData = {
        cart_ids: cartIds,
        ...contactForm.value
      }

      // 添加调试信息
      console.log('提交订单数据:', orderData)
      console.log('购物车项:', checkoutItems.value)

      const result = await orderStore.submitOrder(orderData)
      
      // 创建订单成功，跳转到支付页面
      ElMessageBox.alert('订单创建成功，即将跳转到支付页面', '提示', {
        confirmButtonText: '确定',
        callback: () => {
          router.push({
            name: 'Payment',
            params: { id: result.order_id }
          })
        }
      })
    } catch (error) {
      console.error('提交订单失败:', error)
      console.error('错误详情:', error.response?.data) // 添加详细错误信息
      ElMessage.error('提交订单失败，请稍后再试')
    } finally {
      submitting.value = false
    }
  })
}

// 在 onMounted 中添加验证
onMounted(async () => {
  if (!userStore.isLoggedIn) {
    router.push('/login?redirect=/checkout')
    return
  }

  const cartIds = route.query.cart_ids
  if (!cartIds) {
    ElMessage.error('没有选择要结算的商品')
    router.push('/cart')
    return
  }

  try {
    await cartStore.fetchCartItems()
    
    // 解析购物车ID
    const ids = cartIds.split(',').map(id => parseInt(id))
    console.log('解析的购物车ID:', ids)
    
    // 根据ID筛选购物车项
    checkoutItems.value = cartStore.cartItems.filter(item => ids.includes(item.id))
    console.log('筛选后的购物车项:', checkoutItems.value)
    
    if (checkoutItems.value.length === 0) {
      ElMessage.error('选择的商品不存在或已失效')
      router.push('/cart')
      return
    }
    
    // 填充用户信息
    contactForm.value.contact_name = userStore.userInfo.username || ''
    contactForm.value.contact_phone = userStore.userInfo.phone || ''
    contactForm.value.contact_email = userStore.userInfo.email || ''
  } catch (error) {
    console.error('获取购物车失败:', error)
    ElMessage.error('获取购物车失败')
  } finally {
    loading.value = false
  }
})
</script>