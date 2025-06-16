import axios from 'axios'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/store/auth'

const service = axios.create({
  baseURL: 'http://localhost:8000/api/v1/admin',  // 更新为新的API路径
  timeout: 10000
})

// 响应拦截器
service.interceptors.response.use(
  response => response.data,
  error => {
    ElMessage.error(error.response?.data?.message || '请求失败')
    return Promise.reject(error)
  }
)

export default service