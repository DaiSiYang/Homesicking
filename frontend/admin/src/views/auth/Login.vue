<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header text-center mb-8">
        <h1 class="text-3xl font-bold text-gray-800">觅乡记管理后台</h1>
        <p class="text-gray-500 mt-2">乡村旅游平台管理系统</p>
      </div>
      
      <el-form
        ref="loginFormRef"
        :model="loginForm"
        :rules="loginRules"
        label-position="top"
        @keyup.enter="handleLogin"
      >
        <el-form-item prop="username">
          <el-input
            v-model="loginForm.username"
            placeholder="用户名"
            prefix-icon="User"
            size="large"
          />
        </el-form-item>
        
        <el-form-item prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="密码"
            prefix-icon="Lock"
            show-password
            size="large"
          />
        </el-form-item>
        
        <el-form-item>
          <div class="flex items-center justify-between">
            <el-checkbox v-model="rememberMe">记住我</el-checkbox>
            <el-button type="text">忘记密码?</el-button>
          </div>
        </el-form-item>
        
        <el-form-item>
          <el-button
            type="primary"
            class="w-full"
            size="large"
            :loading="loading"
            @click="handleLogin"
          >
            登录
          </el-button>
        </el-form-item>
      </el-form>
      
      <div class="text-center text-gray-500 mt-4">
        <p>管理员账号: admin / 密码: admin123</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '../../store/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const loginFormRef = ref(null)
const loading = ref(false)
const rememberMe = ref(false)

// 登录表单数据
const loginForm = reactive({
  username: 'admin',
  password: 'admin123'
})

// 表单验证规则
const loginRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' }
  ]
}

// 处理登录
const handleLogin = async () => {
  if (!loginFormRef.value) return
  
  await loginFormRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        const result = await authStore.login(loginForm)
        
        if (result.success) {
          // 登录成功
          ElMessage.success('登录成功')
          
          // 如果有重定向地址，则跳转到重定向地址
          const redirectPath = route.query.redirect || '/'
          router.push(redirectPath)
        } else {
          ElMessage.error(result.message || '登录失败')
        }
      } catch (error) {
        console.error('登录出错:', error)
        ElMessage.error('登录失败，请稍后重试')
      } finally {
        loading.value = false
      }
    }
  })
}
</script>

<style scoped>
.login-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f0f2f5;
  background-image: url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMDAlIiBoZWlnaHQ9IjEwMCUiPjxkZWZzPjxwYXR0ZXJuIGlkPSJwYXR0ZXJuXzAiIHBhdHRlcm5Vbml0cz0idXNlclNwYWNlT25Vc2UiIHdpZHRoPSIxMCIgaGVpZ2h0PSIxMCIgcGF0dGVyblRyYW5zZm9ybT0icm90YXRlKDQ1KSI+PHJlY3QgeD0iMCIgeT0iMCIgd2lkdGg9IjQiIGhlaWdodD0iNCIgZmlsbD0iI2VlZWVmNyI+PC9yZWN0PjwvcGF0dGVybj48L2RlZnM+PHJlY3QgZmlsbD0iI2YwZjJmNSIgd2lkdGg9IjEwMCUiIGhlaWdodD0iMTAwJSI+PC9yZWN0PjxyZWN0IGZpbGw9InVybCgjcGF0dGVybl8wKSIgd2lkdGg9IjEwMCUiIGhlaWdodD0iMTAwJSIgb3BhY2l0eT0iMSI+PC9yZWN0Pjwvc3ZnPg==');
}

.login-card {
  width: 400px;
  padding: 40px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}
</style> 