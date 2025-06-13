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
import { ref, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search } from '@element-plus/icons-vue'

// 数据
const users = ref([
  {
    id: 1,
    username: 'user001',
    nickname: '张三',
    phone: '13812345678',
    email: 'user001@example.com',
    avatar: 'https://via.placeholder.com/100',
    created_at: '2023-10-15 09:32:45',
    last_login_time: '2023-11-20 15:30:45',
    status: 'active'
  },
  {
    id: 2,
    username: 'user002',
    nickname: '李四',
    phone: '13987654321',
    email: 'user002@example.com',
    avatar: 'https://via.placeholder.com/100',
    created_at: '2023-10-18 14:25:36',
    last_login_time: '2023-11-19 10:15:22',
    status: 'active'
  },
  {
    id: 3,
    username: 'user003',
    nickname: '王五',
    phone: '13765432198',
    email: 'user003@example.com',
    avatar: 'https://via.placeholder.com/100',
    created_at: '2023-11-01 11:42:18',
    last_login_time: '2023-11-18 16:45:30',
    status: 'disabled'
  }
])

const loading = ref(false)
const searchQuery = ref('')
const filterStatus = ref('')
const dateRange = ref([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(3)

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
    // 模拟API请求
    await new Promise(resolve => setTimeout(resolve, 500))
    // 实际项目中这里应该调用API获取数据
    loading.value = false
  } catch (error) {
    console.error('获取用户列表失败:', error)
    ElMessage.error('获取用户列表失败')
    loading.value = false
  }
}

// 查看用户详情
const viewUserDetail = async (user) => {
  currentUser.value = user
  drawerVisible.value = true
  
  try {
    // 模拟获取用户订单
    await new Promise(resolve => setTimeout(resolve, 300))
    
    // 模拟数据
    userOrders.value = [
      {
        id: 'DD20230001',
        type: 'product',
        title: '葫芦峪蜂蜜',
        amount: 128.00,
        status: 'completed',
        created_at: '2023-11-20 14:32:25'
      },
      {
        id: 'DD20230002',
        type: 'homestay',
        title: '青山绿水民宿双人间',
        amount: 388.00,
        status: 'paid',
        created_at: '2023-11-19 09:15:42'
      }
    ]
  } catch (error) {
    console.error('获取用户订单失败:', error)
    ElMessage.error('获取用户订单失败')
  }
}

// 切换用户状态
const toggleUserStatus = (user) => {
  const newStatus = user.status === 'active' ? 'disabled' : 'active'
  const actionText = newStatus === 'active' ? '启用' : '禁用'
  
  ElMessageBox.confirm(`确定要${actionText}用户"${user.username}"吗？`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      // 模拟API请求
      await new Promise(resolve => setTimeout(resolve, 300))
      
      // 更新本地状态
      user.status = newStatus
      ElMessage.success(`已${actionText}用户"${user.username}"`)
    } catch (error) {
      console.error('操作失败:', error)
      ElMessage.error('操作失败')
    }
  }).catch(() => {})
}

// 重置用户密码
const resetUserPassword = (user) => {
  currentUser.value = user
  resetPasswordForm.password = ''
  resetPasswordForm.confirmPassword = ''
  resetPasswordDialogVisible.value = true
}

// 确认重置密码
const confirmResetPassword = async () => {
  if (!resetPasswordForm.password) {
    ElMessage.warning('请输入新密码')
    return
  }
  
  if (resetPasswordForm.password !== resetPasswordForm.confirmPassword) {
    ElMessage.warning('两次输入的密码不一致')
    return
  }
  
  resetPasswordLoading.value = true
  try {
    // 模拟API请求
    await new Promise(resolve => setTimeout(resolve, 800))
    
    // 实际项目中这里应该调用API重置密码
    ElMessage.success(`已重置用户"${currentUser.value.username}"的密码`)
    resetPasswordDialogVisible.value = false
  } catch (error) {
    console.error('重置密码失败:', error)
    ElMessage.error('重置密码失败')
  } finally {
    resetPasswordLoading.value = false
  }
}

// 获取订单状态类型
const getOrderStatusType = (status) => {
  const types = {
    pending: 'warning',
    paid: 'primary',
    completed: 'success',
    cancelled: 'info'
  }
  return types[status] || 'info'
}

// 获取订单状态文本
const getOrderStatusText = (status) => {
  const texts = {
    pending: '待付款',
    paid: '已付款',
    completed: '已完成',
    cancelled: '已取消'
  }
  return texts[status] || '未知'
}

// 初始化
fetchUsers()
</script>

<style scoped>
.users-container {
  padding: 20px;
}
</style> 