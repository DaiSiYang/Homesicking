import { defineStore } from 'pinia'
import { login, register, logout, getUserInfo } from '@/api/auth'
import { ElMessage } from 'element-plus'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('merchant_token') || '',
    userInfo: (() => {
      try {
        const stored = localStorage.getItem('merchant_userInfo')
        return stored && stored !== 'undefined' ? JSON.parse(stored) : {}
      } catch (error) {
        console.warn('localStorage userInfo 解析失败:', error)
        localStorage.removeItem('merchant_userInfo')
        return {}
      }
    })()
  }),

  getters: {
    isLoggedIn: (state) => !!state.token,
    getUserInfo: (state) => state.userInfo
  },

  actions: {
    // 登录
    async loginUser(credentials) {
      try {
        const res = await login(credentials)
        if (res.code === 200) {
          // 适配新的后端数据结构
          const { token, user_id, username, email, user_type } = res.data
          this.setToken(token)
          // 构造用户信息对象
          const userInfo = {
            id: user_id,
            username: username,
            email: email,
            user_type: user_type,
            avatar: '', // 提供默认值避免undefined错误
            shopName: username // 使用username作为shopName的默认值
          }
          this.setUserInfo(userInfo)
          ElMessage.success('登录成功')
          return Promise.resolve(res)
        } else {
          ElMessage.error(res.message || '登录失败')
          return Promise.reject(res)
        }
      } catch (error) {
        console.error('登录失败:', error)
        ElMessage.error('登录失败，请检查网络连接')
        return Promise.reject(error)
      }
    },
    
    // 注册
    async registerUser(userData) {
      try {
        const res = await register(userData)
        // 接受2xx状态码作为成功
        if (res.code >= 200 && res.code < 300) {
          // 移除这里的成功提示，让注册页面统一处理
          return Promise.resolve(res)
        } else {
          return Promise.reject(res)
        }
      } catch (error) {
        console.error('注册失败:', error)
        return Promise.reject(error)
      }
    },
    
    // 获取用户信息
    async fetchUserInfo() {
      try {
        const res = await getUserInfo()
        if (res.code === 200) {
          this.setUserInfo(res.data)
          return Promise.resolve(res)
        } else {
          return Promise.reject(res)
        }
      } catch (error) {
        console.error('获取用户信息失败:', error)
        return Promise.reject(error)
      }
    },
    
    // 退出登录
    async logoutUser() {
      try {
        if (this.useMockData) {
          // 模拟退出
          this.resetState()
          ElMessage.success('已退出登录')
          return Promise.resolve({ code: 200 })
        } else {
          if (this.token) {
            await logout()
          }
          this.resetState()
          return Promise.resolve()
        }
      } catch (error) {
        console.error('退出登录失败:', error)
        this.resetState()
        return Promise.reject(error)
      }
    },
    
    // 设置Token
    setToken(token) {
      this.token = token
      localStorage.setItem('merchant_token', token)
    },
    
    // 设置用户信息
    setUserInfo(userInfo) {
      this.userInfo = userInfo
      localStorage.setItem('merchant_userInfo', JSON.stringify(userInfo))
    },
    
    // 重置状态
    resetState() {
      this.token = ''
      this.userInfo = {}
      localStorage.removeItem('merchant_token')
      localStorage.removeItem('merchant_userInfo')
    },
    
    // 更新用户信息
    async updateUserInfo(userData) {
      try {
        const res = await updateUserInfo(userData)
        if (res.code === 200) {
          this.setUserInfo(res.data)
          ElMessage.success('更新成功')
          return Promise.resolve(res)
        } else {
          ElMessage.error(res.message || '更新失败')
          return Promise.reject(res)
        }
      } catch (error) {
        console.error('更新用户信息失败:', error)
        ElMessage.error('更新失败，请检查网络连接')
        return Promise.reject(error)
      }
    }
  }
})