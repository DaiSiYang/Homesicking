<template>
  <div class="min-h-screen rural-login-bg flex items-center justify-center p-4 relative overflow-hidden">
    <!-- 水墨风格背景装饰 -->
    <div class="absolute inset-0 opacity-20">
      <div class="absolute top-20 left-20 w-40 h-40 bg-gradient-to-br from-green-200 to-green-300 rounded-full blur-3xl animate-pulse"></div>
      <div class="absolute bottom-20 right-20 w-48 h-48 bg-gradient-to-br from-yellow-200 to-orange-200 rounded-full blur-3xl animate-pulse" style="animation-delay: 1s;"></div>
      <div class="absolute top-1/2 left-1/4 w-32 h-32 bg-gradient-to-br from-green-100 to-green-200 rounded-full blur-2xl animate-pulse" style="animation-delay: 2s;"></div>
    </div>
    
    <!-- 山水剪影装饰 -->
    <div class="absolute bottom-0 left-0 right-0 h-32 opacity-10">
      <svg viewBox="0 0 1200 120" class="w-full h-full">
        <path d="M0,60 C300,20 600,100 900,40 C1050,10 1150,80 1200,60 L1200,120 L0,120 Z" fill="currentColor" class="text-green-600"/>
      </svg>
    </div>
    
    <!-- 登录卡片 -->
    <div class="rural-card max-w-md w-full p-8 relative z-10">
      <!-- 头部 -->
      <div class="text-center mb-8">
        <div class="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-green-100 to-green-200 rounded-full mb-4">
          <svg viewBox="0 0 24 24" class="w-8 h-8 text-green-600">
            <path fill="currentColor" d="M12 2L2 7v10c0 5.55 3.84 9.739 9 11 5.16-1.261 9-5.45 9-11V7l-10-5z"/>
          </svg>
        </div>
        <h1 class="text-2xl font-bold text-gray-800 mb-2">觅乡记商户平台</h1>
        <p class="text-gray-600 text-sm">连接乡村，传承文化，共创美好</p>
      </div>
      
      <!-- 登录表单 -->
      <form @submit.prevent="handleLogin" class="space-y-6">
        <!-- 用户名输入 -->
        <div class="space-y-2">
          <label for="username" class="block text-sm font-medium text-gray-700">
            用户名
          </label>
          <div class="relative">
            <input
              id="username"
              v-model="form.username"
              type="text"
              required
              class="input-with-icon"
              placeholder="请输入用户名"
            />
            <div class="input-icon-left">
              <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
            </div>
          </div>
        </div>
        
        <!-- 密码输入 -->
        <div class="space-y-2">
          <label for="password" class="block text-sm font-medium text-gray-700">
            密码
          </label>
          <div class="relative">
            <input
              id="password"
              v-model="form.password"
              :type="showPassword ? 'text' : 'password'"
              required
              class="input-with-icon input-with-right-icon"
              placeholder="请输入密码"
            />
            <div class="input-icon-left">
              <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
            </div>
            <button
              type="button"
              @click="showPassword = !showPassword"
              class="input-icon-right"
            >
              <svg v-if="showPassword" class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
              <svg v-else class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L3 3m6.878 6.878L21 21" />
              </svg>
            </button>
          </div>
        </div>
        
        <!-- 记住我 -->
        <div class="flex items-center justify-between">
          <label class="flex items-center">
            <input
              v-model="form.remember"
              type="checkbox"
              class="w-4 h-4 text-green-600 border-gray-300 rounded focus:ring-green-500"
            />
            <span class="ml-2 text-sm text-gray-600">记住我</span>
          </label>
          <a href="#" class="text-sm text-green-600 hover:text-green-500 transition-colors">
            忘记密码？
          </a>
        </div>
        
        <!-- 登录按钮 -->
        <button
          type="submit"
          :disabled="loading"
          class="btn-primary w-full py-3 text-base font-medium"
        >
          <span v-if="loading" class="inline-flex items-center">
            <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            登录中...
          </span>
          <span v-else>立即登录</span>
        </button>
      </form>
      
      <!-- 注册链接 -->
      <div class="mt-6 text-center">
        <p class="text-sm text-gray-600">
          还没有账户？
          <router-link to="/register" class="text-green-600 hover:text-green-500 font-medium transition-colors">
            立即注册
          </router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/store/user'

const router = useRouter()
const userStore = useUserStore()

const loading = ref(false)
const showPassword = ref(false)

const form = reactive({
  username: '',
  password: '',
  remember: false
})

const handleLogin = async () => {
  if (!form.username || !form.password) {
    ElMessage.warning('请填写完整的登录信息')
    return
  }
  
  loading.value = true
  
  try {
    await userStore.loginUser({
      username: form.username,
      password: form.password,
      remember: form.remember
    })
    
    ElMessage.success('登录成功')
    router.push('/dashboard')
  } catch (error) {
    ElMessage.error(error.message || '登录失败，请检查用户名和密码')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.rural-login-bg {
  background: linear-gradient(135deg, 
    #F5F1E8 0%, 
    #E8DCC6 25%, 
    #F0EDE5 50%, 
    #E5E0D3 75%, 
    #F5F1E8 100%);
  position: relative;
}

.rural-login-bg::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: 
    radial-gradient(circle at 20% 80%, rgba(45, 80, 22, 0.03) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(127, 176, 105, 0.03) 0%, transparent 50%),
    radial-gradient(circle at 40% 40%, rgba(212, 165, 116, 0.02) 0%, transparent 50%);
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
    opacity: 0.2;
  }
  50% {
    transform: scale(1.1);
    opacity: 0.3;
  }
}

/* 自定义输入框样式 - 完全覆盖rural-input */
.input-with-icon {
  width: 100%;
  padding: 12px 16px 12px 48px !important; /* 左侧留出图标空间 */
  border: 2px solid rgba(45, 80, 22, 0.1);
  border-radius: 12px;
  background: var(--bg-card, #ffffff);
  color: var(--text-primary, #374151);
  font-size: 14px;
  transition: all 0.3s ease;
  font-family: inherit;
}

.input-with-right-icon {
  padding-right: 48px !important; /* 右侧也留出图标空间 */
}

.input-with-icon:focus {
  outline: none;
  border-color: var(--accent-bamboo, #7fb069);
  box-shadow: 0 0 0 3px rgba(127, 176, 105, 0.1);
}

.input-with-icon::placeholder {
  color: var(--text-muted, #9ca3af);
}

/* 图标定位 */
.input-icon-left {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  pointer-events: none;
  z-index: 10;
}

.input-icon-right {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  color: #9ca3af;
  transition: color 0.2s ease;
  z-index: 10;
}

.input-icon-right:hover {
  color: #6b7280;
}
</style>