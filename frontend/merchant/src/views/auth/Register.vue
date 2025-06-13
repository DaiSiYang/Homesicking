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
    
    <!-- 注册卡片 -->
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
      
      <!-- 注册表单 -->
      <form @submit.prevent="handleRegister" class="space-y-6">
        <!-- 商户名称 -->
        <div class="space-y-2">
          <label for="merchantName" class="block text-sm font-medium text-gray-700">
            商户名称
          </label>
          <div class="relative">
            <input
              id="merchantName"
              v-model="form.merchantName"
              type="text"
              required
              class="rural-input pl-12"
              placeholder="请输入商户名称"
            />
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center">
              <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
              </svg>
            </div>
          </div>
        </div>
        
        <!-- 用户名 -->
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
              class="rural-input pl-12"
              placeholder="请输入用户名"
            />
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center">
              <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
            </div>
          </div>
        </div>
        
        <!-- 邮箱 -->
        <div class="space-y-2">
          <label for="email" class="block text-sm font-medium text-gray-700">
            邮箱地址
          </label>
          <div class="relative">
            <input
              id="email"
              v-model="form.email"
              type="email"
              required
              class="rural-input pl-12"
              placeholder="请输入邮箱地址"
            />
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center">
              <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
            </div>
          </div>
        </div>
        
        <!-- 手机号 -->
        <div class="space-y-2">
          <label for="phone" class="block text-sm font-medium text-gray-700">
            手机号码
          </label>
          <div class="relative">
            <input
              id="phone"
              v-model="form.phone"
              type="tel"
              required
              class="rural-input pl-12"
              placeholder="请输入手机号码"
            />
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center">
              <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
              </svg>
            </div>
          </div>
        </div>
        
        <!-- 密码 -->
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
              class="rural-input pl-12 pr-12"
              placeholder="请输入密码"
            />
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center">
              <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
            </div>
            <button
              type="button"
              @click="showPassword = !showPassword"
              class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600"
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
        
        <!-- 确认密码 -->
        <div class="space-y-2">
          <label for="confirmPassword" class="block text-sm font-medium text-gray-700">
            确认密码
          </label>
          <div class="relative">
            <input
              id="confirmPassword"
              v-model="form.confirmPassword"
              :type="showConfirmPassword ? 'text' : 'password'"
              required
              class="rural-input pl-12 pr-12"
              placeholder="请再次输入密码"
            />
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center">
              <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
            </div>
            <button
              type="button"
              @click="showConfirmPassword = !showConfirmPassword"
              class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600"
            >
              <svg v-if="showConfirmPassword" class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
              <svg v-else class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L3 3m6.878 6.878L21 21" />
              </svg>
            </button>
          </div>
        </div>
        
        <!-- 商户类型 -->
        <div class="space-y-2">
          <label for="merchantType" class="block text-sm font-medium text-gray-700">
            商户类型
          </label>
          <div class="relative">
            <select
              id="merchantType"
              v-model="form.merchantType"
              required
              class="rural-input pl-12 appearance-none"
            >
              <option value="">请选择商户类型</option>
              <option value="homestay">民宿</option>
              <option value="restaurant">餐厅</option>
              <option value="shop">商店</option>
              <option value="service">服务</option>
              <option value="other">其他</option>
            </select>
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center">
              <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
              </svg>
            </div>
            <div class="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
              <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </div>
          </div>
        </div>
        
        <!-- 服务协议 -->
        <div class="flex items-center">
          <input
            id="agreement"
            v-model="form.agreement"
            type="checkbox"
            required
            class="w-4 h-4 text-green-600 border-gray-300 rounded focus:ring-green-500"
          />
          <label for="agreement" class="ml-2 block text-sm text-gray-700">
            我已阅读并同意
            <a href="#" class="text-green-600 hover:text-green-500">服务协议</a>
            和
            <a href="#" class="text-green-600 hover:text-green-500">隐私政策</a>
          </label>
        </div>
        
        <!-- 注册按钮 -->
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
            注册中...
          </span>
          <span v-else>注册</span>
        </button>
      </form>
      
      <!-- 登录链接 -->
      <div class="mt-6 text-center">
        <p class="text-sm text-gray-600">
          已有账户？
          <router-link
            to="/login"
            class="text-green-600 hover:text-green-500 font-medium transition-colors"
          >
            立即登录
          </router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store/user'
import { ElMessage } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()

const loading = ref(false)
const showPassword = ref(false)
const showConfirmPassword = ref(false)

const form = reactive({
  merchantName: '',
  username: '',
  email: '',
  phone: '',
  password: '',
  confirmPassword: '',
  merchantType: '',
  agreement: false
})

const handleRegister = async () => {
  // 验证表单
  if (!form.merchantName || !form.username || !form.email || !form.phone || !form.password || !form.confirmPassword || !form.merchantType) {
    ElMessage.warning('请填写完整的注册信息')
    return
  }
  
  if (form.password !== form.confirmPassword) {
    ElMessage.warning('两次输入的密码不一致')
    return
  }
  
  if (form.password.length < 6) {
    ElMessage.warning('密码长度不能少于6位')
    return
  }
  
  if (!form.agreement) {
    ElMessage.warning('请先同意服务协议和隐私政策')
    return
  }
  
  loading.value = true
  
  try {
    await userStore.registerUser({
      merchantName: form.merchantName,
      username: form.username,
      email: form.email,
      phone: form.phone,
      password: form.password,
      merchantType: form.merchantType
    })
    
    ElMessage.success('注册成功，请登录')
    router.push('/login')
  } catch (error) {
    ElMessage.error(error.message || '注册失败，请稍后重试')
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

/* 下拉框样式 */
select.rural-input {
  background-image: none;
}
</style>