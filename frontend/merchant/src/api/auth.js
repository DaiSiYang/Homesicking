import request from '@/utils/request'

// 登录
export function login(data) {
  return request({
    url: '/api/v1/merchant/auth/login/',
    method: 'post',
    data
  })
}

// 注册
export function register(data) {
  return request({
    url: '/api/v1/merchant/auth/register/',
    method: 'post',
    data
  })
}

// 退出登录
export function logout() {
  return request({
    url: '/api/v1/merchant/auth/logout/',
    method: 'post'
  })
}

// 获取用户信息
export function getUserInfo() {
  return request({
    url: '/api/v1/merchant/user/info/',  // 修改路径
    method: 'get'
  })
}

// 更新用户信息
export function updateUserInfo(data) {
  return request({
    url: '/api/v1/merchant/user/info/',  // 修改路径
    method: 'put',
    data
  })
}

// 更新密码
export function updatePassword(data) {
  return request({
    url: '/merchant/user/password',
    method: 'put',
    data
  })
}

// 更新店铺信息
export function updateShopInfo(data) {
  return request({
    url: '/api/v1/merchant/shop/info',
    method: 'put',
    data
  })
}

// 上传头像
export function uploadAvatar(data) {
  return request({
    url: '/api/v1/merchant/user/avatar',
    method: 'post',
    data,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

// 修改密码
export const changeUserPassword = (data) => {
  return request({
    url: '/api/v1/merchant/user/change-password/',
    method: 'post',
    data
  })
}