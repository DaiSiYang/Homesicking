import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('admin_token') || '',
    userInfo: JSON.parse(localStorage.getItem('admin_user_info') || '{}')
  }),

  getters: {
    isLoggedIn: (state) => !!state.token,
    username: (state) => state.userInfo.username || '',
    avatar: (state) => state.userInfo.avatar || ''
  },

  actions: {
    async login(credentials) {
      try {
        // 实际项目中应该调用API登录
        // const response = await axios.post('/api/admin/login', credentials)
        // const { token, user } = response.data

        // 模拟登录成功
        const token = 'admin_token_' + Date.now()
        const user = {
          id: 1,
          username: credentials.username,
          avatar: 'https://via.placeholder.com/100',
          role: 'admin'
        }

        // 保存到状态和本地存储
        this.token = token
        this.userInfo = user
        localStorage.setItem('admin_token', token)
        localStorage.setItem('admin_user_info', JSON.stringify(user))

        // 设置axios默认请求头
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`

        return { success: true }
      } catch (error) {
        console.error('登录失败:', error)
        return { success: false, message: error.message || '登录失败' }
      }
    },

    logout() {
      // 清除状态和本地存储
      this.token = ''
      this.userInfo = {}
      localStorage.removeItem('admin_token')
      localStorage.removeItem('admin_user_info')
      
      // 清除axios默认请求头
      delete axios.defaults.headers.common['Authorization']
    },

    async fetchUserInfo() {
      try {
        if (!this.token) return

        // 实际项目中应该调用API获取用户信息
        // const response = await axios.get('/api/admin/profile')
        // this.userInfo = response.data
        // localStorage.setItem('admin_user_info', JSON.stringify(response.data))

        // 模拟获取用户信息
        // 这里不做任何操作，因为我们已经有了用户信息
        
        return { success: true }
      } catch (error) {
        console.error('获取用户信息失败:', error)
        return { success: false, message: error.message || '获取用户信息失败' }
      }
    },

    init() {
      // 初始化认证状态
      if (this.token) {
        axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`
        this.fetchUserInfo()
      }
    }
  }
}) 