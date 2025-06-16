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
        <el-table-column prop="contact_phone" label="联系电话" width="130" />
        <el-table-column prop="address" label="地址" min-width="200" show-overflow-tooltip />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="getMerchantStatusType(scope.row.status)">
              {{ getMerchantStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="入驻时间" width="180" />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="scope">
            <el-button type="primary" size="small" text @click="viewMerchant(scope.row)">
              查看
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
              {{ scope.row.status === 'approved' ? '禁用' : '启用' }}
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="flex justify-center mt-4">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search } from '@element-plus/icons-vue'

// 响应式数据
const loading = ref(false)
const searchQuery = ref('')
const filterStatus = ref('')
const dateRange = ref([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

// 商户数据
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
    status: 'pending'
  }
])

// 获取商户列表
// 导入API函数
import { getMerchantList, reviewMerchant as reviewMerchantApi, updateMerchantStatus } from '@/api/merchant'



// 启用真实的API调用
const fetchMerchants = async () => {
  loading.value = true
  try {
    const response = await getMerchantList({
      page: currentPage.value,
      page_size: pageSize.value,
      search: searchQuery.value,
      status: filterStatus.value,
      start_date: dateRange.value?.[0],
      end_date: dateRange.value?.[1]
    })
    merchants.value = response.data.results
    total.value = response.data.count
  } catch (error) {
    console.error('获取商户列表失败:', error)
    ElMessage.error('获取商户列表失败')
  } finally {
    loading.value = false
  }
}

// 同样需要启用审核和状态更新的真实API调用
// 本地函数保持原名
const reviewMerchant = async (merchant, action) => {
  try {
    const actionText = action === 'approved' ? '通过' : '拒绝'
    await ElMessageBox.confirm(
      `确定要${actionText}商户"${merchant.name}"吗？`,
      '确认操作',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    // 调用重命名后的API函数
    await reviewMerchantApi(merchant.id, { action, comment: '' })
    
    merchant.status = action
    ElMessage.success(`${actionText}成功`)
  } catch (error) {
    if (error !== 'cancel') {
      console.error('审核失败:', error)
      ElMessage.error('操作失败')
    }
  }
}

// 切换商户状态
const toggleMerchantStatus = async (merchant) => {
  try {
    const newStatus = merchant.status === 'approved' ? 'disabled' : 'approved'
    const actionText = newStatus === 'disabled' ? '禁用' : '启用'
    
    await ElMessageBox.confirm(
      `确定要${actionText}商户"${merchant.name}"吗？`,
      '确认操作',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    // 这里应该调用真实的API
    // await updateMerchantStatus(merchant.id, { status: newStatus })
    
    merchant.status = newStatus
    ElMessage.success(`${actionText}成功`)
  } catch (error) {
    if (error !== 'cancel') {
      console.error('状态更新失败:', error)
      ElMessage.error('操作失败')
    }
  }
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