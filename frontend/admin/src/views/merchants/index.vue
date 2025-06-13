<template>
  <div class="merchants-container">
    <div class="page-header flex justify-between items-center mb-4">
      <h2 class="text-xl font-bold">商户管理</h2>
    </div>

    <!-- 搜索和筛选 -->
    <el-card class="mb-4">
      <div class="flex flex-wrap gap-4">
        <el-input
          v-model="searchQuery"
          placeholder="搜索商户名称/联系人/手机号"
          class="w-64"
          clearable
          @clear="fetchMerchants"
          @keyup.enter="fetchMerchants"
        >
          <template #append>
            <el-button :icon="Search" @click="fetchMerchants" />
          </template>
        </el-input>

        <el-select v-model="filterStatus" placeholder="状态筛选" class="w-32" @change="fetchMerchants">
          <el-option label="全部" value="" />
          <el-option label="待审核" value="pending" />
          <el-option label="已通过" value="approved" />
          <el-option label="已拒绝" value="rejected" />
          <el-option label="已禁用" value="disabled" />
        </el-select>

        <el-date-picker
          v-model="dateRange"
          type="daterange"
          range-separator="至"
          start-placeholder="入驻开始日期"
          end-placeholder="入驻结束日期"
          format="YYYY-MM-DD"
          value-format="YYYY-MM-DD"
          @change="fetchMerchants"
        />
      </div>
    </el-card>

    <!-- 商户列表 -->
    <el-card v-loading="loading">
      <el-table :data="merchants" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column label="Logo" width="80">
          <template #default="scope">
            <el-avatar :size="40" :src="scope.row.logo" />
          </template>
        </el-table-column>
        <el-table-column prop="name" label="商户名称" min-width="150" />
        <el-table-column prop="contact_person" label="联系人" width="100" />
        <el-table-column prop="contact_phone" label="联系电话" width="120" />
        <el-table-column prop="address" label="地址" min-width="200" show-overflow-tooltip />
        <el-table-column prop="created_at" label="入驻时间" width="160" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="getMerchantStatusType(scope.row.status)">
              {{ getMerchantStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="scope">
            <el-button-group>
              <el-button type="primary" size="small" text @click="viewMerchantDetail(scope.row)">
                详情
              </el-button>
              <el-button 
                v-if="scope.row.status === 'pending'"
                type="success" 
                size="small" 
                text
                @click="reviewMerchant(scope.row, 'approved')"
              >
                通过
              </el-button>
              <el-button 
                v-if="scope.row.status === 'pending'"
                type="danger" 
                size="small" 
                text
                @click="reviewMerchant(scope.row, 'rejected')"
              >
                拒绝
              </el-button>
              <el-button 
                v-if="scope.row.status === 'approved'"
                type="warning" 
                size="small" 
                text
                @click="toggleMerchantStatus(scope.row)"
              >
                {{ scope.row.status === 'disabled' ? '启用' : '禁用' }}
              </el-button>
            </el-button-group>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="flex justify-center mt-4">
        <el-pagination
          :current-page="currentPage"
          :page-size="pageSize"
          :page-sizes="[10, 20, 30, 50]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 商户详情抽屉 -->
    <el-drawer
      v-model="drawerVisible"
      title="商户详情"
      size="50%"
      destroy-on-close
    >
      <div v-if="currentMerchant" class="p-4">
        <div class="flex items-center mb-6">
          <el-avatar :size="80" :src="currentMerchant.logo" />
          <div class="ml-4">
            <h3 class="text-xl font-bold">{{ currentMerchant.name }}</h3>
            <p class="text-gray-500">ID: {{ currentMerchant.id }}</p>
          </div>
        </div>

        <el-tabs>
          <el-tab-pane label="基本信息">
            <el-descriptions :column="1" border>
              <el-descriptions-item label="商户名称">{{ currentMerchant.name }}</el-descriptions-item>
              <el-descriptions-item label="联系人">{{ currentMerchant.contact_person }}</el-descriptions-item>
              <el-descriptions-item label="联系电话">{{ currentMerchant.contact_phone }}</el-descriptions-item>
              <el-descriptions-item label="电子邮箱">{{ currentMerchant.email }}</el-descriptions-item>
              <el-descriptions-item label="详细地址">{{ currentMerchant.address }}</el-descriptions-item>
              <el-descriptions-item label="营业时间">{{ currentMerchant.business_hours }}</el-descriptions-item>
              <el-descriptions-item label="入驻时间">{{ currentMerchant.created_at }}</el-descriptions-item>
              <el-descriptions-item label="状态">
                <el-tag :type="getMerchantStatusType(currentMerchant.status)">
                  {{ getMerchantStatusText(currentMerchant.status) }}
                </el-tag>
              </el-descriptions-item>
            </el-descriptions>
          </el-tab-pane>
          
          <el-tab-pane label="营业执照">
            <div class="flex justify-center">
              <el-image
                style="width: 100%; max-width: 500px;"
                :src="currentMerchant.license"
                :preview-src-list="[currentMerchant.license]"
              />
            </div>
            <el-descriptions :column="1" border class="mt-4">
              <el-descriptions-item label="法人姓名">{{ currentMerchant.legal_person }}</el-descriptions-item>
              <el-descriptions-item label="统一社会信用代码">{{ currentMerchant.credit_code }}</el-descriptions-item>
            </el-descriptions>
          </el-tab-pane>
          
          <el-tab-pane label="商户照片">
            <el-image-group>
              <el-image
                v-for="(image, index) in currentMerchant.images"
                :key="index"
                style="width: 150px; height: 150px; margin: 5px;"
                :src="image"
                fit="cover"
              />
            </el-image-group>
          </el-tab-pane>
          
          <el-tab-pane label="商品列表">
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
            </el-table>
          </el-tab-pane>
        </el-tabs>
      </div>
    </el-drawer>

    <!-- 审核对话框 -->
    <el-dialog
      v-model="reviewDialogVisible"
      :title="reviewAction === 'approved' ? '通过商户审核' : '拒绝商户审核'"
      width="400px"
    >
      <div v-if="currentMerchant" class="flex items-center mb-4">
        <el-avatar :size="40" :src="currentMerchant.logo" />
        <div class="ml-2">
          <p class="font-bold">{{ currentMerchant.name }}</p>
          <p class="text-gray-500 text-sm">{{ currentMerchant.contact_person }}</p>
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
import { ref, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search } from '@element-plus/icons-vue'

// 数据
const merchants = ref([
  {
    id: 1,
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
  },
  {
    id: 2,
    name: '青山绿水民宿',
    logo: 'https://via.placeholder.com/100',
    contact_person: '李四',
    contact_phone: '13987654321',
    email: 'merchant002@example.com',
    address: '浙江省杭州市临安区天目山镇',
    business_hours: '08:00-20:00',
    created_at: '2023-10-18 14:25:36',
    legal_person: '李四',
    credit_code: '91330000XXXXXXXXXX',
    license: 'https://via.placeholder.com/800x600',
    images: [
      'https://via.placeholder.com/800x600',
      'https://via.placeholder.com/800x600'
    ],
    status: 'pending'
  },
  {
    id: 3,
    name: '田园风光小屋',
    logo: 'https://via.placeholder.com/100',
    contact_person: '王五',
    contact_phone: '13765432198',
    email: 'merchant003@example.com',
    address: '浙江省杭州市桐庐县',
    business_hours: '09:00-21:00',
    created_at: '2023-11-01 11:42:18',
    legal_person: '王五',
    credit_code: '91330000XXXXXXXXXX',
    license: 'https://via.placeholder.com/800x600',
    images: [
      'https://via.placeholder.com/800x600'
    ],
    status: 'rejected'
  }
])

const loading = ref(false)
const searchQuery = ref('')
const filterStatus = ref('')
const dateRange = ref([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(3)

// 商户详情相关
const drawerVisible = ref(false)
const currentMerchant = ref(null)
const merchantProducts = ref([])

// 审核相关
const reviewDialogVisible = ref(false)
const reviewAction = ref('approved')
const reviewLoading = ref(false)
const reviewForm = reactive({
  comment: ''
})

// 获取商户列表
const fetchMerchants = async () => {
  loading.value = true
  try {
    // 模拟API请求
    await new Promise(resolve => setTimeout(resolve, 500))
    // 实际项目中这里应该调用API获取数据
    loading.value = false
  } catch (error) {
    console.error('获取商户列表失败:', error)
    ElMessage.error('获取商户列表失败')
    loading.value = false
  }
}

// 查看商户详情
const viewMerchantDetail = async (merchant) => {
  currentMerchant.value = merchant
  drawerVisible.value = true
  
  try {
    // 模拟获取商户商品
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
  }
}

// 审核商户
const reviewMerchant = (merchant, action) => {
  currentMerchant.value = merchant
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
    const merchant = merchants.value.find(m => m.id === currentMerchant.value.id)
    if (merchant) {
      merchant.status = reviewAction.value
    }
    
    // 实际项目中这里应该调用API更新商户状态
    ElMessage.success(`已${reviewAction.value === 'approved' ? '通过' : '拒绝'}商户"${currentMerchant.value.name}"的审核`)
    reviewDialogVisible.value = false
  } catch (error) {
    console.error('审核失败:', error)
    ElMessage.error('审核失败')
  } finally {
    reviewLoading.value = false
  }
}

// 切换商户状态
const toggleMerchantStatus = (merchant) => {
  const newStatus = merchant.status === 'approved' ? 'disabled' : 'approved'
  const actionText = newStatus === 'approved' ? '启用' : '禁用'
  
  ElMessageBox.confirm(`确定要${actionText}商户"${merchant.name}"吗？`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      // 模拟API请求
      await new Promise(resolve => setTimeout(resolve, 300))
      
      // 更新本地状态
      merchant.status = newStatus
      ElMessage.success(`已${actionText}商户"${merchant.name}"`)
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

// 分页处理
const handleSizeChange = (size) => {
  pageSize.value = size
  fetchMerchants()
}

const handleCurrentChange = (page) => {
  currentPage.value = page
  fetchMerchants()
}

// 初始化
fetchMerchants()
</script>

<style scoped>
.merchants-container {
  padding: 20px;
}
</style> 