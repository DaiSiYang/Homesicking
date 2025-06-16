import { defineStore } from 'pinia'
import { loginUser as apiLoginUser, registerUser as apiRegisterUser, getUserInfo as apiGetUserInfo, updateUserInfo as apiUpdateUserInfo, logout } from '@/api/auth'
import { ElMessage } from 'element-plus'

export const useUserStore = defineStore('user', {
  state: () => ({
    // 安全解析localStorage中的token
    token: (() => {
      try {
        const stored = localStorage.getItem('user_token')
        return (stored && stored !== 'undefined' && stored !== 'null') ? stored : ''
      } catch {
        return ''
      }
    })(),
    // 安全解析localStorage中的用户信息
    userInfo: (() => {
      try {
        const stored = localStorage.getItem('user_info')
        return (stored && stored !== 'undefined' && stored !== 'null') ? JSON.parse(stored) : {}
      } catch {
        return {}
      }
    })(),
    useMockData: false
  }),
  
  getters: {
    isLoggedIn: (state) => !!state.token || state.useMockData,
    userId: (state) => state.userInfo.id || '1',
    username: (state) => state.userInfo.username || '乡游爱好者',
  },
  
  actions: {
    // 登录
    // 修改 loginUser 方法中的错误处理
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
          const res = await apiLoginUser(credentials)  // 修改：使用正确的函数名
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
          } else {
            // 处理后端返回的错误响应
            const errorMessage = res.message || '登录失败'
            ElMessage.error(errorMessage)
            return Promise.reject(new Error(errorMessage))
          }
        }
      } catch (error) {
        console.error('登录失败:', error)
        
        // 区分不同类型的错误
        if (error.response) {
          // 后端返回了错误响应（如密码错误、用户不存在等）
          const errorMessage = error.response.data?.message || error.response.data?.detail || '登录失败'
          ElMessage.error(errorMessage)
          return Promise.reject(new Error(errorMessage))
        } else if (error.request) {
          // 网络连接问题
          if (!this.useMockData) {
            ElMessage.warning('网络连接失败，切换到模拟数据模式')
            this.useMockData = true
            return this.loginUser(credentials)
          }
        } else {
          // 其他错误
          ElMessage.error(error.message || '登录失败')
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
          const res = await apiRegisterUser(userData)
          // 修改这里：接受200和201作为成功响应
          if (res.code === 200 || res.code === 201) {
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
    validateToken() {
      if (!this.token || this.token === 'undefined' || this.token === 'null') {
        this.resetState()
        return false
      }
      return true
    },
    
    // 设置Token
    setToken(token) {
      this.token = token
      localStorage.setItem('user_token', token)
    },
    
    // 设置用户信息
    setUserInfo(userInfo) {
      this.userInfo = userInfo
      localStorage.setItem('user_info', JSON.stringify(userInfo))
    },
    
    // 重置状态
    resetState() {
      this.token = ''
      this.userInfo = {}
      localStorage.removeItem('user_token')
      localStorage.removeItem('user_info')
    },
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
})