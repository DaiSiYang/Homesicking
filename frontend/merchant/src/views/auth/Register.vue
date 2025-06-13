<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 flex items-center justify-center p-4 relative overflow-hidden">
    <!-- 背景装饰 -->
    <div class="absolute inset-0 opacity-10">
      <div class="absolute top-20 left-20 w-32 h-32 bg-blue-200 rounded-full blur-xl"></div>
      <div class="absolute bottom-20 right-20 w-40 h-40 bg-indigo-200 rounded-full blur-xl"></div>
      <div class="absolute top-1/2 left-1/4 w-24 h-24 bg-cyan-200 rounded-full blur-lg"></div>
    </div>
    
    <!-- 注册卡片 -->
    <div class="bg-white/80 backdrop-blur-sm rounded-2xl shadow-xl border border-white/20 p-8 w-full max-w-md relative z-10">
      <!-- 头部 -->
      <div class="text-center mb-8">
        <h1 class="text-2xl font-bold text-gray-800 mb-2">商户注册</h1>
        <p class="text-gray-500 text-sm">创建您的商户账户，开始您的业务之旅</p>
      </div>
      
      <!-- 注册表单 -->
      <form @submit.prevent="handleRegister" class="space-y-6">
        <!-- 商户名称 -->
        <div class="space-y-2">
          <label for="merchantName" class="block text-sm font-medium text-gray-700">
            商户名称
          </label>
          <input
            id="merchantName"
            v-model="form.merchantName"
            type="text"
            required
            class="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-white/50 backdrop-blur-sm"
            placeholder="请输入商户名称"
          />
        </div>
        
        <!-- 用户名 -->
        <div class="space-y-2">
          <label for="username" class="block text-sm font-medium text-gray-700">
            用户名
          </label>
          <input
            id="username"
            v-model="form.username"
            type="text"
            required
            class="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-white/50 backdrop-blur-sm"
            placeholder="请输入用户名"
          />
        </div>
        
        <!-- 邮箱 -->
        <div class="space-y-2">
          <label for="email" class="block text-sm font-medium text-gray-700">
            邮箱地址
          </label>
          <input
            id="email"
            v-model="form.email"
            type="email"
            required
            class="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-white/50 backdrop-blur-sm"
            placeholder="请输入邮箱地址"
          />
        </div>
        
        <!-- 手机号 -->
        <div class="space-y-2">
          <label for="phone" class="block text-sm font-medium text-gray-700">
            手机号码
          </label>
          <input
            id="phone"
            v-model="form.phone"
            type="tel"
            required
            class="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-white/50 backdrop-blur-sm"
            placeholder="请输入手机号码"
          />
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
              class="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-white/50 backdrop-blur-sm"
              placeholder="请输入密码"
            />
            <button
              type="button"
              @click="showPassword = !showPassword"
              class="absolute inset-y-0 right-0 pr-3 flex items-center"
            >
              <svg v-if="showPassword" class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
              <svg v-else class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
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
              class="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-white/50 backdrop-blur-sm"
              placeholder="请再次输入密码"
            />
            <button
              type="button"
              @click="showConfirmPassword = !showConfirmPassword"
              class="absolute inset-y-0 right-0 pr-3 flex items-center"
            >
              <svg v-if="showConfirmPassword" class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
              <svg v-else class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
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
          <select
            id="merchantType"
            v-model="form.merchantType"
            required
            class="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-white/50 backdrop-blur-sm"
          >
            <option value="">请选择商户类型</option>
            <option value="homestay">民宿</option>
            <option value="restaurant">餐厅</option>
            <option value="shop">商店</option>
            <option value="service">服务</option>
            <option value="other">其他</option>
          </select>
        </div>
        
        <!-- 服务协议 -->
        <div class="flex items-center">
          <input
            id="agreement"
            v-model="form.agreement"
            type="checkbox"
            required
            class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
          />
          <label for="agreement" class="ml-2 block text-sm text-gray-700">
            我已阅读并同意
            <a href="#" class="text-blue-600 hover:text-blue-500">服务协议</a>
            和
            <a href="#" class="text-blue-600 hover:text-blue-500">隐私政策</a>
          </label>
        </div>
        
        <!-- 注册按钮 -->
        <button
          type="submit"
          :disabled="loading"
          class="w-full bg-gradient-to-r from-blue-600 to-indigo-600 text-white py-3 px-4 rounded-lg font-medium hover:from-blue-700 hover:to-indigo-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <span v-if="loading" class="flex items-center justify-center">
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
            class="text-blue-600 hover:text-blue-500 font-medium transition-colors"
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
/* 自定义样式 */
.backdrop-blur-sm {
  backdrop-filter: blur(4px);
}
</style>