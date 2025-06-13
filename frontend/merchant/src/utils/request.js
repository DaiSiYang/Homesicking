import axios from 'axios'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/store/user'

// 创建axios实例
const service = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '',
  timeout: 15000
})

// 请求拦截器
service.interceptors.request.use(
  config => {
    // 从pinia获取token
    const userStore = useUserStore()
    if (userStore.token) {
      // 让每个请求携带token
      config.headers['Authorization'] = 'Bearer ' + userStore.token
    }
    return config
  },
  error => {
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  response => {
    const res = response.data
    
    // 如果返回的状态码不是2xx，则判断为错误
    if (res.code < 200 || res.code >= 300) {
      ElMessage({
        message: res.message || '请求错误',
        type: 'error',
        duration: 5 * 1000
      })
      
      // 401: 未登录或token过期
      if (res.code === 401) {
        // 重新登录
        const userStore = useUserStore()
        userStore.resetState()
        location.reload()
      }
      
      return Promise.reject(new Error(res.message || '请求错误'))
    } else {
      return res
    }
  },
  error => {
    console.error('响应错误:', error)
    ElMessage({
      message: error.message || '请求失败',
      type: 'error',
      duration: 5 * 1000
    })
    return Promise.reject(error)
  }
)

export default service