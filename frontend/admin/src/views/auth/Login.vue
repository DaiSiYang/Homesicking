<template>
  <div class="login-container ink-texture">
    <!-- 背景装饰 -->
    <div class="bg-decoration">
      <div class="bamboo-grove">
        <div class="bamboo" v-for="i in 8" :key="i"></div>
      </div>
    </div>
    
    <div class="login-form village-card">
      <div class="login-header">
        <div class="logo-section">
          <div class="logo-icon">
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2L2 7v10c0 5.55 3.84 9.739 9 11 5.16-1.261 9-5.45 9-11V7l-10-5z"/>
            </svg>
          </div>
          <h2 class="text-village-primary">觅乡记管理后台</h2>
          <p class="subtitle">寻觅乡村美好，记录田园时光</p>
        </div>
      </div>
      
      <el-form
        ref="loginFormRef"
        :model="loginForm"
        :rules="loginRules"
        class="login-form-content"
        @keyup.enter="handleLogin"
      >
        <el-form-item prop="username">
          <el-input
            v-model="loginForm.username"
            placeholder="请输入用户名"
            size="large"
            prefix-icon="User"
            class="input-village"
          />
        </el-form-item>
        
        <el-form-item prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="请输入密码"
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
            @click="handleLogin"
            class="btn-village"
          >
            {{ loading ? '登录中...' : '登录' }}
          </el-button>
        </el-form-item>
        
        <div class="login-footer">
          <span class="text-muted">还没有账户？</span>
          <router-link to="/register" class="register-link text-village-primary">立即注册</router-link>
        </div>
      </el-form>
      
      <!-- 移除这个演示信息区域 -->
      <!-- <div class="demo-info">
        <p class="text-muted">演示账户：admin / admin123</p>
      </div> -->
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
const loginFormRef = ref()
const loading = ref(false)

const loginForm = reactive({
  username: '',  // 清空默认用户名
  password: ''   // 清空默认密码
})

const loginRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, message: '用户名长度不能少于3个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6个字符', trigger: 'blur' }
  ]
}

const handleLogin = async () => {
  try {
    await loginFormRef.value.validate()
    loading.value = true
    
    const result = await authStore.login({
      username: loginForm.username,
      password: loginForm.password
    })
    
    if (result.success) {
      ElMessage.success(result.message || '登录成功')
      router.push('/dashboard')
    } else {
      ElMessage.error(result.message || '登录失败')
    }
  } catch (error) {
    console.error('登录表单验证失败:', error)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
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

.login-form {
  width: 420px;
  padding: 48px;
  position: relative;
  z-index: 2;
  backdrop-filter: blur(10px);
  background: rgba(255, 255, 255, 0.95);
}

.login-header {
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

.login-header h2 {
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

.login-form-content {
  margin-top: 32px;
}

.login-footer {
  text-align: center;
  margin-top: 24px;
  padding-top: 20px;
  border-top: 1px solid var(--border-light);
}

.register-link {
  text-decoration: none;
  margin-left: 8px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.register-link:hover {
  text-decoration: underline;
  color: var(--primary-dark);
}

/* 移除这个样式块 */
/*
.demo-info {
  text-align: center;
  margin-top: 20px;
  padding: 12px;
  background: var(--bg-secondary);
  border-radius: 8px;
  border-left: 3px solid var(--secondary-color);
}

.demo-info p {
  margin: 0;
  font-size: 12px;
}
*/

/* 响应式设计 */
@media (max-width: 480px) {
  .login-form {
    width: 90%;
    padding: 32px 24px;
  }
  
  .login-header h2 {
    font-size: 24px;
  }
}
</style>