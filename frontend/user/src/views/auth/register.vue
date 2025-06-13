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
        <h2 class="text-2xl font-medium text-ink-700 mb-2">加入觅乡记</h2>
        <p class="text-ink-500">创建账户，开启您的乡村探索之旅</p>
      </div>
      
      <!-- 注册表单 -->
      <div class="card shadow-brush">
        <el-form 
          ref="registerForm" 
          :model="registerData" 
          :rules="registerRules" 
          label-position="top"
          class="space-y-6"
        >
          <el-form-item label="用户名" prop="username">
            <el-input 
              v-model="registerData.username" 
              placeholder="请输入用户名"
              prefix-icon="User"
              size="large"
              class="rounded-ink"
            />
          </el-form-item>
          
          <el-form-item label="手机号" prop="phone">
            <el-input 
              v-model="registerData.phone" 
              placeholder="请输入手机号"
              prefix-icon="Iphone"
              size="large"
              class="rounded-ink"
            />
          </el-form-item>
          
          <el-form-item label="邮箱" prop="email">
            <el-input 
              v-model="registerData.email" 
              placeholder="请输入邮箱"
              prefix-icon="Message"
              size="large"
              class="rounded-ink"
            />
          </el-form-item>
          
          <el-form-item label="密码" prop="password">
            <el-input 
              v-model="registerData.password" 
              type="password" 
              placeholder="请输入密码"
              prefix-icon="Lock"
              show-password
              size="large"
              class="rounded-ink"
            />
          </el-form-item>
          
          <el-form-item label="确认密码" prop="confirmPassword">
            <el-input 
              v-model="registerData.confirmPassword" 
              type="password" 
              placeholder="请再次输入密码"
              prefix-icon="Lock"
              show-password
              size="large"
              class="rounded-ink"
            />
          </el-form-item>
          
          <div class="flex items-start">
            <el-checkbox v-model="registerData.agreement" class="text-ink-600">
              我已阅读并同意<el-button link class="text-primary-600 hover:text-primary-700">《用户协议》</el-button>和<el-button link class="text-primary-600 hover:text-primary-700">《隐私政策》</el-button>
            </el-checkbox>
          </div>
          
          <el-button 
            type="primary" 
            class="w-full btn-primary" 
            size="large"
            :loading="loading" 
            @click="handleRegister"
          >
            注册
          </el-button>
          
          <div class="text-center pt-4 border-t border-earth-200">
            <span class="text-ink-500">已有账号？</span>
            <el-button link class="text-primary-600 hover:text-primary-700 font-medium" @click="$router.push('/login')">
              立即登录
            </el-button>
          </div>
        </el-form>
      </div>
      
      <!-- 装饰性元素 -->
      <div class="text-center text-xs text-ink-400 space-y-2">
        <p>注册即表示您同意我们的服务条款和隐私政策</p>
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
import { useRouter } from 'vue-router'
import { User, Lock, Iphone, Message } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/store/user'

const router = useRouter()
const userStore = useUserStore()
const registerForm = ref(null)
const loading = ref(false)

// 注册表单数据
const registerData = reactive({
  username: '',
  phone: '',
  email: '',
  password: '',
  confirmPassword: '',
  agreement: false
})

// 验证确认密码
const validatePass = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请再次输入密码'))
  } else if (value !== registerData.password) {
    callback(new Error('两次输入密码不一致'))
  } else {
    callback()
  }
}

// 表单验证规则
const registerRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3456789]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请再次输入密码', trigger: 'blur' },
    { validator: validatePass, trigger: 'blur' }
  ],
  agreement: [
    { 
      validator: (rule, value, callback) => {
        if (!value) {
          callback(new Error('请阅读并同意用户协议和隐私政策'))
        } else {
          callback()
        }
      }, 
      trigger: 'change' 
    }
  ]
}

// 处理注册
const handleRegister = async () => {
  registerForm.value.validate(async (valid) => {
    if (!valid) return
    
    try {
      loading.value = true
      
      await userStore.registerUser({
        username: registerData.username,
        password: registerData.password,
        confirm_password: registerData.confirmPassword,
        email: registerData.email,
        phone: registerData.phone,
        user_type: 'tourist'
      })
      
      ElMessage.success('注册成功，请登录')
      router.push('/login')
    } catch (error) {
      console.error('注册失败:', error)
      ElMessage.error(error.message || '注册失败，请稍后再试')
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