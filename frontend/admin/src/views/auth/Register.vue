<template>
  <div class="register-container ink-texture">
    <!-- 背景装饰 -->
    <div class="bg-decoration">
      <div class="bamboo-grove">
        <div class="bamboo" v-for="i in 8" :key="i"></div>
      </div>
    </div>
    
    <div class="register-form village-card">
      <div class="register-header">
        <div class="logo-section">
          <div class="logo-icon">
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/>
            </svg>
          </div>
          <h2 class="text-village-primary">管理员注册</h2>
          <p class="subtitle">加入觅乡记管理团队</p>
        </div>
      </div>
      
      <el-form
        ref="registerFormRef"
        :model="registerForm"
        :rules="registerRules"
        class="register-form-content"
        @keyup.enter="handleRegister"
      >
        <el-form-item prop="username">
          <el-input
            v-model="registerForm.username"
            placeholder="请输入用户名"
            size="large"
            prefix-icon="User"
            class="input-village"
          />
        </el-form-item>
        
        <el-form-item prop="email">
          <el-input
            v-model="registerForm.email"
            placeholder="请输入邮箱"
            size="large"
            prefix-icon="Message"
            type="email"
            class="input-village"
          />
        </el-form-item>
        
        <el-form-item prop="password">
          <el-input
            v-model="registerForm.password"
            type="password"
            placeholder="请输入密码"
            size="large"
            prefix-icon="Lock"
            show-password
            class="input-village"
          />
        </el-form-item>
        
        <el-form-item prop="confirmPassword">
          <el-input
            v-model="registerForm.confirmPassword"
            type="password"
            placeholder="请确认密码"
            size="large"
            prefix-icon="Lock"
            show-password
            class="input-village"
          />
        </el-form-item>
        
        <el-form-item>
          <el-button
            type="primary"
            size="large"
            style="width: 100%"
            :loading="loading"
            @click="handleRegister"
            class="btn-village"
          >
            {{ loading ? '注册中...' : '立即注册' }}
          </el-button>
        </el-form-item>
        
        <div class="register-footer">
          <span class="text-muted">已有账户？</span>
          <router-link to="/login" class="login-link text-village-primary">立即登录</router-link>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/store/auth'

const router = useRouter()
const authStore = useAuthStore()
const registerFormRef = ref()
const loading = ref(false)

const registerForm = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const validateConfirmPassword = (rule, value, callback) => {
  if (value !== registerForm.password) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

const registerRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, message: '用户名长度不能少于3个字符', trigger: 'blur' },
    { pattern: /^[a-zA-Z0-9_]+$/, message: '用户名只能包含字母、数字和下划线', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入有效的邮箱地址', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    { validator: validateConfirmPassword, trigger: 'blur' }
  ]
}

const handleRegister = async () => {
  try {
    await registerFormRef.value.validate()
    loading.value = true
    
    const result = await authStore.register({
      username: registerForm.username,
      email: registerForm.email,
      password: registerForm.password,
      confirm_password: registerForm.confirmPassword
    })
    
    if (result.success) {
      ElMessage.success(result.message || '注册成功')
      router.push('/dashboard')
    } else {
      ElMessage.error(result.message || '注册失败')
    }
  } catch (error) {
    console.error('注册表单验证失败:', error)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, 
    rgba(123, 160, 91, 0.1) 0%, 
    rgba(45, 90, 39, 0.05) 50%, 
    rgba(245, 243, 240, 0.8) 100%
  );
  position: relative;
  overflow: hidden;
}

/* 竹林背景 */
.bg-decoration {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
  z-index: 1;
}

.bamboo-grove {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 100%;
}

.bamboo {
  position: absolute;
  bottom: 0;
  width: 8px;
  background: linear-gradient(to top, 
    var(--secondary-color) 0%, 
    rgba(123, 160, 91, 0.3) 100%
  );
  border-radius: 4px 4px 0 0;
  opacity: 0.1;
}

.bamboo:nth-child(1) { left: 5%; height: 60%; }
.bamboo:nth-child(2) { left: 15%; height: 80%; }
.bamboo:nth-child(3) { left: 25%; height: 70%; }
.bamboo:nth-child(4) { left: 35%; height: 90%; }
.bamboo:nth-child(5) { right: 35%; height: 75%; }
.bamboo:nth-child(6) { right: 25%; height: 85%; }
.bamboo:nth-child(7) { right: 15%; height: 65%; }
.bamboo:nth-child(8) { right: 5%; height: 70%; }

.register-form {
  width: 420px;
  padding: 48px;
  position: relative;
  z-index: 2;
  backdrop-filter: blur(10px);
  background: rgba(255, 255, 255, 0.95);
}

.register-header {
  text-align: center;
  margin-bottom: 40px;
}

.logo-section {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.logo-icon {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, var(--secondary-color), var(--primary-color));
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16px;
  box-shadow: var(--shadow-medium);
}

.logo-icon svg {
  width: 32px;
  height: 32px;
  color: white;
}

.register-header h2 {
  margin: 0 0 8px 0;
  font-size: 28px;
  font-weight: 600;
  letter-spacing: 1px;
}

.subtitle {
  color: var(--text-secondary);
  margin: 0;
  font-size: 14px;
  font-style: italic;
}

.register-form-content {
  margin-top: 32px;
}

.register-footer {
  text-align: center;
  margin-top: 24px;
  padding-top: 20px;
  border-top: 1px solid var(--border-light);
}

.login-link {
  text-decoration: none;
  margin-left: 8px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.login-link:hover {
  text-decoration: underline;
  color: var(--primary-dark);
}

/* 响应式设计 */
@media (max-width: 480px) {
  .register-form {
    width: 90%;
    padding: 32px 24px;
  }
  
  .register-header h2 {
    font-size: 24px;
  }
}
</style>