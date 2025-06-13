import axios from 'axios'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/store/user'

// 创建axios实例
const request = axios.create({
  baseURL: 'http://localhost:8000/api/user', // 修改为正确的用户端API路径
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
request.interceptors.request.use(
  config => {
    const userStore = useUserStore()
    if (userStore.token) {
      config.headers.Authorization = `Bearer ${userStore.token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    console.error('响应错误:', error)
    
    if (error.response) {
      const { status, data } = error.response
      
      switch (status) {
        case 401:
          // 只有在明确的认证失败时才跳转登录页
          if (data?.code === 'TOKEN_EXPIRED' || data?.code === 'INVALID_TOKEN') {
            ElMessage.error('登录已过期，请重新登录')
            const userStore = useUserStore()
            userStore.resetState()
            window.location.href = '/login'
          }
          break
        case 403:
          ElMessage.error('没有权限访问')
          break
        case 404:
          // 404错误不应该导致跳转登录页
          console.warn('请求的资源不存在:', error.config?.url)
          break
        case 500:
          ElMessage.error('服务器内部错误')
          break
        default:
          ElMessage.error(data?.message || '请求失败')
      }
    } else {
      ElMessage.error('网络连接失败')
    }
    
    return Promise.reject(error)
  }
)

export default request