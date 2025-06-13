<template>
  <div class="min-h-screen flex items-center justify-center ink-gradient py-12 px-4 sm:px-6 lg:px-8">
    <!-- 背景装饰 -->
    <div class="absolute inset-0 overflow-hidden">
      <div class="absolute top-10 left-10 w-32 h-32 bg-primary-100 rounded-full opacity-20 blur-xl"></div>
      <div class="absolute bottom-20 right-20 w-48 h-48 bg-earth-100 rounded-full opacity-30 blur-2xl"></div>
      <div class="absolute top-1/2 left-1/4 w-24 h-24 bg-bamboo-100 rounded-full opacity-25 blur-lg"></div>
    </div>
    
    <div class="max-w-md w-full space-y-8 relative z-10">
      <!-- 标题区域 -->
      <div class="text-center">
        <div class="mb-6">
          <h1 class="text-4xl font-calligraphy text-primary-700 mb-2">觅乡记</h1>
          <div class="ink-border mx-auto w-20"></div>
        </div>
        <h2 class="text-2xl font-medium text-ink-700 mb-2">欢迎回来</h2>
        <p class="text-ink-500">登录您的账户，继续您的乡村之旅</p>
      </div>
      
      <!-- 登录表单 -->
      <div class="card shadow-brush">
        <el-form 
          ref="loginForm" 
          :model="loginData" 
          :rules="loginRules" 
          label-position="top"
          class="space-y-6"
        >
          <el-form-item label="用户名/手机号" prop="username">
            <el-input 
              v-model="loginData.username" 
              placeholder="请输入用户名或手机号"
              prefix-icon="User"
              size="large"
              class="rounded-ink"
            />
          </el-form-item>
          
          <el-form-item label="密码" prop="password">
            <el-input 
              v-model="loginData.password" 
              type="password" 
              placeholder="请输入密码"
              prefix-icon="Lock"
              show-password
              size="large"
              class="rounded-ink"
            />
          </el-form-item>
          
          <div class="flex justify-between items-center">
            <el-checkbox v-model="loginData.remember" class="text-ink-600">
              记住我
            </el-checkbox>
            <el-button link class="text-primary-600 hover:text-primary-700" @click="$router.push('/forgot-password')">
              忘记密码？
            </el-button>
          </div>
          
          <el-button 
            type="primary" 
            class="w-full btn-primary" 
            size="large"
            :loading="loading" 
            @click="handleLogin"
          >
            登录
          </el-button>
          
          <div class="text-center pt-4 border-t border-earth-200">
            <span class="text-ink-500">还没有账号？</span>
            <el-button link class="text-primary-600 hover:text-primary-700 font-medium" @click="$router.push('/register')">
              立即注册
            </el-button>
          </div>
        </el-form>
      </div>
      
      <!-- 装饰性元素 -->
      <div class="text-center text-xs text-ink-400 space-y-2">
        <p>登录即表示您同意我们的服务条款和隐私政策</p>
        <div class="flex justify-center space-x-4">
          <span>安全</span>
          <span>•</span>
          <span>可靠</span>
          <span>•</span>
          <span>便捷</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { User, Lock } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/store/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const loginForm = ref(null)
const loading = ref(false)

// 登录表单数据
const loginData = reactive({
  username: '',
  password: '',
  remember: false
})

// 表单验证规则
const loginRules = {
  username: [
    { required: true, message: '请输入用户名或手机号', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6个字符', trigger: 'blur' }
  ]
}

// 处理登录
const handleLogin = () => {
  loginForm.value.validate(async (valid) => {
    if (!valid) return
    
    try {
      loading.value = true
      await userStore.loginUser(loginData)
      
      ElMessage.success('登录成功')
      
      // 获取重定向地址，如果没有则跳转到首页
      const redirectUrl = route.query.redirect || '/'
      router.push(redirectUrl)
    } catch (error) {
      console.error('登录失败:', error)
      ElMessage.error(error.message || '登录失败，请检查用户名和密码')
    } finally {
      loading.value = false
    }
  })
}
</script>

<style scoped>
.el-form-item {
  margin-bottom: 24px;
}

.el-form-item__label {
  color: #4a3f2f;
  font-weight: 500;
  margin-bottom: 8px;
}
</style>