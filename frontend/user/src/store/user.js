import { defineStore } from 'pinia'
import { login, register, logout } from '@/api/auth'  // 移除 getUserInfo 导入
import { ElMessage } from 'element-plus'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    userInfo: JSON.parse(localStorage.getItem('userInfo') || '{}'),
    useMockData: false // 确保设置为 false
  }),
  
  getters: {
    isLoggedIn: (state) => !!state.token || state.useMockData,
    userId: (state) => state.userInfo.id || '1',
    username: (state) => state.userInfo.username || '乡游爱好者',
  },
  
  actions: {
    // 登录
    async loginUser(credentials) {
      try {
        if (this.useMockData) {
          // 使用模拟数据
          const mockUser = {
            id: '1',
            username: credentials.username || '乡游爱好者',
            nickname: '乡游爱好者',
            email: credentials.username || 'user@example.com',
            avatar: 'https://picsum.photos/id/1005/200/200',
            phone: '13800138000',
            gender: '保密',
            birthday: '1990-01-01'
          }
          
          const mockToken = 'mock_token_' + Date.now()
          this.setToken(mockToken)
          this.setUserInfo(mockUser)
          
          ElMessage.success('登录成功')
          return Promise.resolve({ code: 200, data: { token: mockToken, user: mockUser } })
        } else {
          const res = await login(credentials)
          if (res.code === 200) {
            const { token, user_id, username, email, user_type } = res.data
            this.setToken(token)
            // 构造用户信息对象
            const userInfo = {
              id: user_id,
              username: username,
              email: email,
              user_type: user_type,
              // 添加其他默认字段
              nickname: username,
              avatar: '',
              phone: '',
              real_name: '',
              gender: '',
              birth_date: '',
              address: '',
              bio: ''
            }
            this.setUserInfo(userInfo)
            return Promise.resolve(res)
          }
        }
      } catch (error) {
        console.error('登录失败:', error)
        if (!this.useMockData) {
          ElMessage.warning('API连接失败，切换到模拟数据模式')
          this.useMockData = true
          return this.loginUser(credentials)
        }
        return Promise.reject(error)
      }
    },
    
    // 注册
    async registerUser(userData) {
      try {
        if (this.useMockData) {
          // 使用模拟数据
          const mockUser = {
            id: '1',
            username: userData.username,
            nickname: userData.nickname || userData.username,
            email: userData.email,
            avatar: 'https://picsum.photos/id/1005/200/200',
            phone: userData.phone || '',
            gender: '保密',
            birthday: ''
          }
          
          ElMessage.success('注册成功，请登录')
          return Promise.resolve({ code: 200, data: mockUser })
        } else {
          const res = await register(userData)
          if (res.code === 200) {
            return Promise.resolve(res)
          } else {
            return Promise.reject(res)
          }
        }
      } catch (error) {
        console.error('注册失败:', error)
        return Promise.reject(error)
      }
    },
    
    // 获取用户信息 - 直接从 store 返回，不调用 API
    getUserInfo() {
      if (this.useMockData || Object.keys(this.userInfo).length === 0) {
        // 如果是模拟模式或没有用户信息，返回模拟数据
        const mockUser = this.getMockUserInfo()
        this.setUserInfo(mockUser)
        return mockUser
      }
      return this.userInfo
    },
    
    // 更新用户信息
    updateUserInfo(newUserInfo) {
      const updatedInfo = { ...this.userInfo, ...newUserInfo }
      this.setUserInfo(updatedInfo)
      ElMessage.success('用户信息已更新')
      return Promise.resolve({ code: 200, data: updatedInfo })
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
          await logout()
        }
        this.resetState()
        return Promise.resolve()
      } catch (error) {
        console.error('退出登录失败:', error)
        this.resetState()
        return Promise.reject(error)
      }
    },
    
    // 设置Token
    setToken(token) {
      this.token = token
      localStorage.setItem('token', token)
    },
    
    // 设置用户信息
    setUserInfo(userInfo) {
      this.userInfo = userInfo
      localStorage.setItem('userInfo', JSON.stringify(userInfo))
    },
    
    // 重置状态
    resetState() {
      this.token = ''
      this.userInfo = {}
      localStorage.removeItem('token')
      localStorage.removeItem('userInfo')
    },
    
    // 获取模拟用户信息
    getMockUserInfo() {
      return {
        id: '1',
        username: '乡游爱好者',
        nickname: '乡游爱好者',
        email: 'user@example.com',
        avatar: 'https://picsum.photos/id/1005/200/200',
        phone: '13800138000',
        gender: '保密',
        birthday: '1990-01-01',
        real_name: '',
        birth_date: '',
        address: '',
        bio: ''
      }
    }
  }
})