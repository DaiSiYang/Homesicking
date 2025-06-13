<template>
  <div class="merchant-detail-container">
    <div class="page-header flex justify-between items-center mb-4">
      <div class="flex items-center">
        <el-button icon="Back" @click="$router.back()" text>返回</el-button>
        <h2 class="text-xl font-bold">商户详情</h2>
      </div>
      <div>
        <el-button 
          v-if="merchant?.status === 'pending'"
          type="success" 
          @click="reviewMerchant('approved')"
        >
          通过审核
        </el-button>
        <el-button 
          v-if="merchant?.status === 'pending'"
          type="danger" 
          @click="reviewMerchant('rejected')"
        >
          拒绝审核
        </el-button>
        <el-button 
          v-if="merchant?.status === 'approved'"
          type="warning" 
          @click="toggleMerchantStatus"
        >
          {{ merchant?.status === 'disabled' ? '启用商户' : '禁用商户' }}
        </el-button>
      </div>
    </div>

    <el-card v-loading="loading" class="mb-4">
      <div v-if="merchant" class="merchant-info">
        <div class="flex items-center mb-6">
          <el-avatar :size="80" :src="merchant.logo" />
          <div class="ml-4">
            <h3 class="text-xl font-bold">{{ merchant.name }}</h3>
            <div class="flex items-center mt-1">
              <el-tag :type="getMerchantStatusType(merchant.status)" class="mr-2">
                {{ getMerchantStatusText(merchant.status) }}
              </el-tag>
              <span class="text-gray-500">ID: {{ merchant.id }}</span>
            </div>
          </div>
        </div>

        <el-tabs>
          <el-tab-pane label="基本信息">
            <el-descriptions :column="2" border>
              <el-descriptions-item label="商户名称">{{ merchant.name }}</el-descriptions-item>
              <el-descriptions-item label="联系人">{{ merchant.contact_person }}</el-descriptions-item>
              <el-descriptions-item label="联系电话">{{ merchant.contact_phone }}</el-descriptions-item>
              <el-descriptions-item label="电子邮箱">{{ merchant.email }}</el-descriptions-item>
              <el-descriptions-item label="详细地址" :span="2">{{ merchant.address }}</el-descriptions-item>
              <el-descriptions-item label="营业时间">{{ merchant.business_hours }}</el-descriptions-item>
              <el-descriptions-item label="入驻时间">{{ merchant.created_at }}</el-descriptions-item>
              <el-descriptions-item label="法人姓名">{{ merchant.legal_person }}</el-descriptions-item>
              <el-descriptions-item label="统一社会信用代码">{{ merchant.credit_code }}</el-descriptions-item>
            </el-descriptions>
          </el-tab-pane>
          
          <el-tab-pane label="营业执照">
            <div class="flex justify-center">
              <el-image
                style="width: 100%; max-width: 500px;"
                :src="merchant.license"
                :preview-src-list="[merchant.license]"
              />
            </div>
          </el-tab-pane>
          
          <el-tab-pane label="商户照片">
            <el-image-group>
              <el-image
                v-for="(image, index) in merchant.images"
                :key="index"
                style="width: 150px; height: 150px; margin: 5px;"
                :src="image"
                fit="cover"
              />
            </el-image-group>
          </el-tab-pane>
        </el-tabs>
      </div>
    </el-card>

    <!-- 商品列表 -->
    <el-card v-loading="productsLoading">
      <template #header>
        <div class="flex justify-between items-center">
          <span>商品列表</span>
        </div>
      </template>
      
      <el-table :data="merchantProducts" style="width: 100%">
        <el-table-column label="图片" width="100">
          <template #default="scope">
            <el-image 
              style="width: 60px; height: 60px" 
              :src="scope.row.image" 
              fit="cover"
            />
          </template>
        </el-table-column>
        <el-table-column prop="name" label="名称" min-width="150" />
        <el-table-column prop="type" label="类型" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.type === 'product' ? 'success' : 'warning'">
              {{ scope.row.type === 'product' ? '特产' : '民宿' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="price" label="价格" width="100">
          <template #default="scope">
            <span class="text-orange-500">¥{{ scope.row.price.toFixed(2) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.status === 'active' ? 'success' : 'info'">
              {{ scope.row.status === 'active' ? '上架中' : '已下架' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120" fixed="right">
          <template #default="scope">
            <el-button type="primary" size="small" text @click="viewProductDetail(scope.row)">
              详情
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 审核对话框 -->
    <el-dialog
      v-model="reviewDialogVisible"
      :title="reviewAction === 'approved' ? '通过商户审核' : '拒绝商户审核'"
      width="400px"
    >
      <div v-if="merchant" class="flex items-center mb-4">
        <el-avatar :size="40" :src="merchant.logo" />
        <div class="ml-2">
          <p class="font-bold">{{ merchant.name }}</p>
          <p class="text-gray-500 text-sm">{{ merchant.contact_person }}</p>
        </div>
      </div>
      
      <el-form :model="reviewForm" label-position="top">
        <el-form-item label="审核意见">
          <el-input
            v-model="reviewForm.comment"
            type="textarea"
            :rows="4"
            :placeholder="reviewAction === 'approved' ? '请输入通过意见（选填）' : '请输入拒绝原因（必填）'"
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="reviewDialogVisible = false">取消</el-button>
        <el-button 
          :type="reviewAction === 'approved' ? 'success' : 'danger'" 
          @click="confirmReview" 
          :loading="reviewLoading"
        >
          {{ reviewAction === 'approved' ? '确认通过' : '确认拒绝' }}
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'

const route = useRoute()
const router = useRouter()
const merchantId = route.params.id

// 数据
const merchant = ref(null)
const loading = ref(true)
const merchantProducts = ref([])
const productsLoading = ref(false)

// 审核相关
const reviewDialogVisible = ref(false)
const reviewAction = ref('approved')
const reviewLoading = ref(false)
const reviewForm = reactive({
  comment: ''
})

// 获取商户详情
const fetchMerchantDetail = async () => {
  loading.value = true
  try {
    // 模拟API请求
    await new Promise(resolve => setTimeout(resolve, 500))
    
    // 模拟数据 - 实际项目中应该从API获取
    merchant.value = {
      id: merchantId,
      name: '山水间农家乐',
      logo: 'https://via.placeholder.com/100',
      contact_person: '张三',
      contact_phone: '13812345678',
      email: 'merchant001@example.com',
      address: '浙江省杭州市临安区太湖源镇',
      business_hours: '09:00-18:00',
      created_at: '2023-10-15 09:32:45',
      legal_person: '张三',
      credit_code: '91330000XXXXXXXXXX',
      license: 'https://via.placeholder.com/800x600',
      images: [
        'https://via.placeholder.com/800x600',
        'https://via.placeholder.com/800x600',
        'https://via.placeholder.com/800x600'
      ],
      status: 'approved'
    }
  } catch (error) {
    console.error('获取商户详情失败:', error)
    ElMessage.error('获取商户详情失败')
  } finally {
    loading.value = false
  }
}

// 获取商户商品
const fetchMerchantProducts = async () => {
  productsLoading.value = true
  try {
    // 模拟API请求
    await new Promise(resolve => setTimeout(resolve, 300))
    
    // 模拟数据
    merchantProducts.value = [
      {
        id: 1,
        name: '葫芦峪蜂蜜',
        image: 'https://via.placeholder.com/200x200',
        type: 'product',
        price: 128.00,
        status: 'active'
      },
      {
        id: 2,
        name: '手工竹编',
        image: 'https://via.placeholder.com/200x200',
        type: 'product',
        price: 99.00,
        status: 'active'
      },
      {
        id: 3,
        name: '青山绿水民宿双人间',
        image: 'https://via.placeholder.com/200x200',
        type: 'homestay',
        price: 388.00,
        status: 'active'
      }
    ]
  } catch (error) {
    console.error('获取商户商品失败:', error)
    ElMessage.error('获取商户商品失败')
  } finally {
    productsLoading.value = false
  }
}

// 查看商品详情
const viewProductDetail = (product) => {
  const path = product.type === 'product' 
    ? `/products/${product.id}` 
    : `/homestays/${product.id}`
  router.push(path)
}

// 审核商户
const reviewMerchant = (action) => {
  reviewAction.value = action
  reviewForm.comment = ''
  reviewDialogVisible.value = true
}

// 确认审核
const confirmReview = async () => {
  if (reviewAction.value === 'rejected' && !reviewForm.comment) {
    ElMessage.warning('请输入拒绝原因')
    return
  }
  
  reviewLoading.value = true
  try {
    // 模拟API请求
    await new Promise(resolve => setTimeout(resolve, 800))
    
    // 更新本地状态
    merchant.value.status = reviewAction.value
    
    // 实际项目中这里应该调用API更新商户状态
    ElMessage.success(`已${reviewAction.value === 'approved' ? '通过' : '拒绝'}商户"${merchant.value.name}"的审核`)
    reviewDialogVisible.value = false
  } catch (error) {
    console.error('审核失败:', error)
    ElMessage.error('审核失败')
  } finally {
    reviewLoading.value = false
  }
}

// 切换商户状态
const toggleMerchantStatus = () => {
  const newStatus = merchant.value.status === 'approved' ? 'disabled' : 'approved'
  const actionText = newStatus === 'approved' ? '启用' : '禁用'
  
  ElMessageBox.confirm(`确定要${actionText}商户"${merchant.value.name}"吗？`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      // 模拟API请求
      await new Promise(resolve => setTimeout(resolve, 300))
      
      // 更新本地状态
      merchant.value.status = newStatus
      ElMessage.success(`已${actionText}商户"${merchant.value.name}"`)
    } catch (error) {
      console.error('操作失败:', error)
      ElMessage.error('操作失败')
    }
  }).catch(() => {})
}

// 获取商户状态类型
const getMerchantStatusType = (status) => {
  const types = {
    pending: 'warning',
    approved: 'success',
    rejected: 'danger',
    disabled: 'info'
  }
  return types[status] || 'info'
}

// 获取商户状态文本
const getMerchantStatusText = (status) => {
  const texts = {
    pending: '待审核',
    approved: '已通过',
    rejected: '已拒绝',
    disabled: '已禁用'
  }
  return texts[status] || '未知'
}

onMounted(() => {
  fetchMerchantDetail()
  fetchMerchantProducts()
})
</script>

<style scoped>
.merchant-detail-container {
  padding: 20px;
}

.merchant-info {
  margin-bottom: 20px;
}
</style> 