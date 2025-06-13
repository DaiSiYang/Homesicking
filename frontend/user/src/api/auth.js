import request from '@/utils/request'

// 用户登录
export function login(data) {
  return request({
    url: '/auth/login/',
    method: 'post',
    data
  })
}

// 用户注册
export function register(data) {
  return request({
    url: '/auth/register/',
    method: 'post',
    data
  })
}

// 用户登出
export function logout() {
  return request({
    url: '/auth/logout/',
    method: 'post'
  })
}

// 获取用户信息


// 更新用户信息
export function updateUserInfo(data) {
  return request({
    url: '/profile/update/',
    method: 'patch',
    data
  })
}

// 修改密码
export function changePassword(data) {
  return request({
    url: '/auth/change-password/',
    method: 'post',
    data
  })
}