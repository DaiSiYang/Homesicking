<template>
  <div class="users-container">
    <div class="page-header flex justify-between items-center mb-4">
      <h2 class="text-xl font-bold">用户管理</h2>
    </div>

    <!-- 搜索和筛选 -->
    <el-card class="mb-4">
      <div class="flex flex-wrap gap-4">
        <el-input
          v-model="searchQuery"
          placeholder="搜索用户名/手机号/邮箱"
          class="w-64"
          clearable
          @clear="fetchUsers"
          @keyup.enter="fetchUsers"
        >
          <template #append>
            <el-button :icon="Search" @click="fetchUsers" />
          </template>
        </el-input>

        <el-select v-model="filterStatus" placeholder="状态筛选" class="w-32" @change="fetchUsers">
          <el-option label="全部" value="" />
          <el-option label="正常" value="active" />
          <el-option label="禁用" value="disabled" />
        </el-select>

        <el-date-picker
          v-model="dateRange"
          type="daterange"
          range-separator="至"
          start-placeholder="注册开始日期"
          end-placeholder="注册结束日期"
          format="YYYY-MM-DD"
          value-format="YYYY-MM-DD"
          @change="fetchUsers"
        />
      </div>
    </el-card>

    <!-- 用户列表 -->
    <el-card v-loading="loading">
      <el-table :data="users" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column label="头像" width="80">
          <template #default="scope">
            <el-avatar :size="40" :src="scope.row.avatar" />
          </template>
        </el-table-column>
        <el-table-column prop="username" label="用户名" width="120" />
        <el-table-column prop="nickname" label="昵称" width="120" />
        <el-table-column prop="phone" label="手机号" width="120" />
        <el-table-column prop="email" label="邮箱" min-width="180" />
        <el-table-column prop="created_at" label="注册时间" width="160" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.status === 'active' ? 'success' : 'danger'">
              {{ scope.row.status === 'active' ? '正常' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="scope">
            <el-button-group>
              <el-button type="primary" size="small" text @click="viewUserDetail(scope.row)">
                详情
              </el-button>
              <el-button 
                :type="scope.row.status === 'active' ? 'danger' : 'success'" 
                size="small" 
                text
                @click="toggleUserStatus(scope.row)"
              >
                {{ scope.row.status === 'active' ? '禁用' : '启用' }}
              </el-button>
              <el-button type="warning" size="small" text @click="resetUserPassword(scope.row)">
                重置密码
              </el-button>
            </el-button-group>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="flex justify-center mt-4">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 30, 50]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          @size-change="fetchUsers"
          @current-change="fetchUsers"
        />
      </div>
    </el-card>

    <!-- 用户详情抽屉 -->
    <el-drawer
      v-model="drawerVisible"
      title="用户详情"
      size="50%"
      destroy-on-close
    >
      <div v-if="currentUser" class="p-4">
        <div class="flex items-center mb-6">
          <el-avatar :size="80" :src="currentUser.avatar" />
          <div class="ml-4">
            <h3 class="text-xl font-bold">{{ currentUser.nickname || currentUser.username }}</h3>
            <p class="text-gray-500">ID: {{ currentUser.id }}</p>
          </div>
        </div>

        <el-descriptions :column="1" border>
          <el-descriptions-item label="用户名">{{ currentUser.username }}</el-descriptions-item>
          <el-descriptions-item label="昵称">{{ currentUser.nickname }}</el-descriptions-item>
          <el-descriptions-item label="手机号">{{ currentUser.phone }}</el-descriptions-item>
          <el-descriptions-item label="邮箱">{{ currentUser.email }}</el-descriptions-item>
          <el-descriptions-item label="注册时间">{{ currentUser.created_at }}</el-descriptions-item>
          <el-descriptions-item label="最后登录时间">{{ currentUser.last_login_time }}</el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="currentUser.status === 'active' ? 'success' : 'danger'">
              {{ currentUser.status === 'active' ? '正常' : '禁用' }}
            </el-tag>
          </el-descriptions-item>
        </el-descriptions>

        <div class="mt-6">
          <h4 class="text-lg font-medium mb-2">用户订单</h4>
          <el-table :data="userOrders" style="width: 100%">
            <el-table-column prop="id" label="订单号" width="120" />
            <el-table-column prop="type" label="类型" width="80">
              <template #default="scope">
                <el-tag :type="scope.row.type === 'product' ? 'success' : 'warning'">
                  {{ scope.row.type === 'product' ? '特产' : '民宿' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="title" label="商品名称" min-width="180" />
            <el-table-column prop="amount" label="金额" width="100">
              <template #default="scope">
                <span class="text-orange-500">¥{{ scope.row.amount.toFixed(2) }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="status" label="状态" width="100">
              <template #default="scope">
                <el-tag :type="getOrderStatusType(scope.row.status)">
                  {{ getOrderStatusText(scope.row.status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="created_at" label="下单时间" width="160" />
          </el-table>
        </div>
      </div>
    </el-drawer>

    <!-- 重置密码对话框 -->
    <el-dialog
      v-model="resetPasswordDialogVisible"
      title="重置用户密码"
      width="400px"
    >
      <div v-if="currentUser" class="flex items-center mb-4">
        <el-avatar :size="40" :src="currentUser.avatar" />
        <div class="ml-2">
          <p class="font-bold">{{ currentUser.username }}</p>
          <p class="text-gray-500 text-sm">{{ currentUser.email }}</p>
        </div>
      </div>
      
      <el-form :model="resetPasswordForm" label-position="top">
        <el-form-item label="新密码">
          <el-input
            v-model="resetPasswordForm.password"
            type="password"
            placeholder="请输入新密码"
            show-password
          />
        </el-form-item>
        <el-form-item label="确认密码">
          <el-input
            v-model="resetPasswordForm.confirmPassword"
            type="password"
            placeholder="请再次输入新密码"
            show-password
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="resetPasswordDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmResetPassword" :loading="resetPasswordLoading">
          确认重置
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search } from '@element-plus/icons-vue'
import { 
  getUserList, 
  getUserDetail, 
  updateUserStatus, 
  resetUserPassword, 
  getUserOrders 
} from '@/api/user'

// 数据
const users = ref([])
const loading = ref(false)
const searchQuery = ref('')
const filterStatus = ref('')
const dateRange = ref([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

// 用户详情相关
const drawerVisible = ref(false)
const currentUser = ref(null)
const userOrders = ref([])

// 重置密码相关
const resetPasswordDialogVisible = ref(false)
const resetPasswordLoading = ref(false)
const resetPasswordForm = reactive({
  password: '',
  confirmPassword: ''
})

// 获取用户列表
const fetchUsers = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value,
      search: searchQuery.value,
      status: filterStatus.value,
      start_date: dateRange.value[0],
      end_date: dateRange.value[1]
    }
    
    const response = await getUserList(params)
    // 修改这两行以匹配后端返回的数据结构
    users.value = response.data.users  // 改为 users
    total.value = response.data.pagination.total_count  // 改为 pagination.total_count
  } catch (error) {
    console.error('获取用户列表失败:', error)
    ElMessage.error('获取用户列表失败')
  } finally {
    loading.value = false
  }
}

// 查看用户详情
const viewUserDetail = async (user) => {
  currentUser.value = user
  drawerVisible.value = true
  
  try {
    const response = await getUserOrders(user.id)
    userOrders.value = response.data.results
  } catch (error) {
    console.error('获取用户订单失败:', error)
    ElMessage.error('获取用户订单失败')
  }
}

// 更新用户状态
const handleStatusChange = async (user, status) => {
  try {
    await updateUserStatus(user.id, status)
    ElMessage.success('状态更新成功')
    await fetchUsers()
  } catch (error) {
    console.error('操作失败:', error)
    ElMessage.error('操作失败')
    // 恢复原状态
    user.status = user.status === 'active' ? 'disabled' : 'active'
  }
}

// 重置密码
const handleResetPassword = async () => {
  if (resetPasswordForm.password !== resetPasswordForm.confirmPassword) {
    ElMessage.error('两次输入的密码不一致')
    return
  }
  
  resetPasswordLoading.value = true
  try {
    await resetUserPassword(currentUser.value.id, resetPasswordForm.password)
    ElMessage.success('密码重置成功')
    resetPasswordDialogVisible.value = false
    resetPasswordForm.password = ''
    resetPasswordForm.confirmPassword = ''
  } catch (error) {
    console.error('重置密码失败:', error)
    ElMessage.error('重置密码失败')
  } finally {
    resetPasswordLoading.value = false
  }
}

// 搜索
const handleSearch = () => {
  currentPage.value = 1
  fetchUsers()
}

// 重置搜索
const handleReset = () => {
  searchQuery.value = ''
  filterStatus.value = ''
  dateRange.value = []
  currentPage.value = 1
  fetchUsers()
}

// 分页变化
const handlePageChange = (page) => {
  currentPage.value = page
  fetchUsers()
}

// 页面大小变化
const handleSizeChange = (size) => {
  pageSize.value = size
  currentPage.value = 1
  fetchUsers()
}

// 初始化
onMounted(() => {
  fetchUsers()
})
</script>

<style scoped>
.users-container {
  padding: 20px;
}
</style>