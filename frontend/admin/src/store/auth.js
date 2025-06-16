import { defineStore } from 'pinia'
import { login as loginApi, logout as logoutApi, register as registerApi } from '@/api/auth'
import request from '@/utils/request'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('admin_token') || '',
    userInfo: (() => {
      try {
        const stored = localStorage.getItem('admin_user_info')
        return stored && stored !== 'undefined' ? JSON.parse(stored) : {}
      } catch (error) {
        console.warn('Failed to parse admin_user_info from localStorage:', error)
        return {}
      }
    })()
  }),

  getters: {
    isLoggedIn: (state) => !!state.token,
    username: (state) => state.userInfo?.username || '',
    avatar: (state) => state.userInfo?.avatar || ''
  },

  actions: {
    async login(credentials) {
      try {
        const response = await loginApi(credentials)
        const data = response.data
        
        // 从后端响应中提取token和用户信息
        const token = data.token || data.access
        const user = {
          id: data.user_id,
          username: data.username,
          email: data.email,
          user_type: data.user_type,
          permissions: data.permissions
        }
    
        // 确保 token 和 user 对象存在
        if (!token) {
          throw new Error('登录令牌缺失')
        }
        if (!user.username) {
          throw new Error('用户信息缺失')
        }
    
        // 保存到状态和本地存储
        this.token = token
        this.userInfo = user
        localStorage.setItem('admin_token', token)
        localStorage.setItem('admin_user_info', JSON.stringify(user))
    
        // 设置请求头
        request.defaults.headers.common['Authorization'] = `Bearer ${token}`
    
        return { success: true }
      } catch (error) {
        console.error('登录失败:', error)
        return { success: false, message: error.response?.data?.message || error.message || '登录失败' }
      }
    },

    // 添加注册方法
    async register(userData) {
      try {
        const response = await registerApi(userData)
        const { token, user, message } = response.data

        // 注册成功后自动登录
        if (token && user) {
          this.token = token
          this.userInfo = user
          localStorage.setItem('admin_token', token)
          localStorage.setItem('admin_user_info', JSON.stringify(user))
          request.defaults.headers.common['Authorization'] = `Bearer ${token}`
        }

        return { success: true, message: message || '注册成功' }
      } catch (error) {
        console.error('注册失败:', error)
        return { 
          success: false, 
          message: error.response?.data?.message || error.response?.data?.error || '注册失败' 
        }
      }
    },

    async logout() {
      try {
        await logoutApi()
      } catch (error) {
        console.error('登出失败:', error)
      } finally {
        // 清除状态和本地存储
        this.token = ''
        this.userInfo = {}
        localStorage.removeItem('admin_token')
        localStorage.removeItem('admin_user_info')
        
        // 清除请求头
        delete request.defaults.headers.common['Authorization']
      }
    },

    async fetchUserInfo() {
      try {
        if (!this.token) return { success: false }

        const response = await request.get('/auth/profile/')
        this.userInfo = response.data
        localStorage.setItem('admin_user_info', JSON.stringify(response.data))
        
        return { success: true }
      } catch (error) {
        console.error('获取用户信息失败:', error)
        return { success: false, message: error.response?.data?.message || '获取用户信息失败' }
      }
    },

    init() {
      // 初始化认证状态
      if (this.token) {
        request.defaults.headers.common['Authorization'] = `Bearer ${this.token}`
        this.fetchUserInfo()
      }
    }
  }
})