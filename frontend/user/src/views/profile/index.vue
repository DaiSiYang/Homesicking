<template>
  <div class="page-container py-8 bamboo-pattern">
    <div class="max-w-4xl mx-auto">
      <div class="card p-6 border-earth-200">
        <div class="flex items-center justify-between mb-6 ink-border pb-2">
          <h1 class="text-2xl font-serif font-bold text-ink-500">个人资料</h1>
          <el-button type="primary" @click="editMode = !editMode">
            {{ editMode ? '取消编辑' : '编辑资料' }}
          </el-button>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <!-- 头像区域 -->
          <div class="text-center">
            <div class="relative inline-block">
              <el-avatar :size="120" :src="userInfo.avatar" class="mb-4">
                <el-icon><User /></el-icon>
              </el-avatar>
              <el-button v-if="editMode" 
                        type="primary" 
                        size="small" 
                        circle 
                        class="absolute bottom-0 right-0"
                        @click="uploadAvatar">
                <el-icon><Camera /></el-icon>
              </el-button>
            </div>
            <h2 class="text-xl font-medium">{{ userInfo.username }}</h2>
            <p class="text-gray-500">{{ userInfo.email }}</p>
          </div>
          
          <!-- 基本信息 -->
          <div class="md:col-span-2">
            <el-form :model="userInfo" label-width="100px" :disabled="!editMode">
              <el-form-item label="用户名">
                <el-input v-model="userInfo.username" />
              </el-form-item>
              <el-form-item label="邮箱">
                <el-input v-model="userInfo.email" />
              </el-form-item>
              <el-form-item label="手机号">
                <el-input v-model="userInfo.phone" />
              </el-form-item>
              <el-form-item label="真实姓名">
                <el-input v-model="userInfo.real_name" />
              </el-form-item>
              <el-form-item label="性别">
                <el-select v-model="userInfo.gender" placeholder="请选择性别">
                  <el-option label="男" value="M" />
                  <el-option label="女" value="F" />
                  <el-option label="保密" value="" />
                </el-select>
              </el-form-item>
              <el-form-item label="生日">
                <el-date-picker v-model="userInfo.birth_date" 
                               type="date" 
                               placeholder="选择日期" />
              </el-form-item>
              <el-form-item label="地址">
                <el-input v-model="userInfo.address" type="textarea" :rows="3" />
              </el-form-item>
              <el-form-item label="个人简介">
                <el-input v-model="userInfo.bio" type="textarea" :rows="4" />
              </el-form-item>
              
              <el-form-item v-if="editMode">
                <el-button type="primary" @click="saveProfile" :loading="saving">
                  保存修改
                </el-button>
                <el-button @click="editMode = false">取消</el-button>
              </el-form-item>
            </el-form>
          </div>
        </div>
        
        <!-- 统计信息 - 水墨风格改造 -->
        <div class="mt-8 pt-6 border-t border-earth-200">
          <h3 class="text-lg font-serif font-medium mb-4 text-ink-500">我的统计</h3>
          <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div class="text-center p-4 bg-earth-100 rounded-lg transition-all hover:bg-earth-200">
              <div class="text-2xl font-bold text-primary-600">{{ stats.orders }}</div>
              <div class="text-earth-500">订单数量</div>
            </div>
            <div class="text-center p-4 bg-earth-100 rounded-lg transition-all hover:bg-earth-200">
              <div class="text-2xl font-bold text-primary-600">{{ stats.favorites }}</div>
              <div class="text-earth-500">收藏数量</div>
            </div>
            <div class="text-center p-4 bg-earth-100 rounded-lg transition-all hover:bg-earth-200">
              <div class="text-2xl font-bold text-primary-600">{{ stats.reviews }}</div>
              <div class="text-earth-500">评价数量</div>
            </div>
            <div class="text-center p-4 bg-earth-100 rounded-lg transition-all hover:bg-earth-200">
              <div class="text-2xl font-bold text-primary-600">{{ stats.points }}</div>
              <div class="text-earth-500">积分余额</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { User, Camera } from '@element-plus/icons-vue'
import { useUserStore } from '@/store/user'  // 导入 store

const userStore = useUserStore()  // 使用 store
const editMode = ref(false)
const saving = ref(false)
const loading = ref(false)

const userInfo = ref({
  username: '',
  email: '',
  phone: '',
  real_name: '',
  gender: '',
  birth_date: '',
  address: '',
  bio: '',
  avatar: ''
})

const stats = ref({
  orders: 0,
  favorites: 0,
  reviews: 0,
  points: 0
})

// 获取用户资料 - 从 store 获取
const fetchUserProfile = () => {
  try {
    const storeUserInfo = userStore.getUserInfo()
    userInfo.value = { ...userInfo.value, ...storeUserInfo }
  } catch (error) {
    console.error('获取用户资料失败:', error)
    ElMessage.error('获取用户资料失败')
  }
}

// 保存用户资料 - 保存到 store
const saveProfile = async () => {
  try {
    saving.value = true
    await userStore.updateUserInfo(userInfo.value)
    editMode.value = false
    ElMessage.success('保存成功')
  } catch (error) {
    console.error('保存失败:', error)
    ElMessage.error('保存失败')
  } finally {
    saving.value = false
  }
}

// 上传头像
const uploadAvatar = () => {
  // 实现头像上传逻辑
  ElMessage.info('头像上传功能待实现')
}

// 获取用户信息 - 从 store 获取
const fetchUserInfo = () => {
  try {
    loading.value = true
    const storeUserInfo = userStore.getUserInfo()
    userInfo.value = { ...userInfo.value, ...storeUserInfo }
  } catch (error) {
    console.error('获取用户信息失败:', error)
    ElMessage.error('获取用户信息失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchUserProfile()
})
</script>