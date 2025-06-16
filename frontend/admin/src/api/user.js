import request from '@/utils/request'

// 获取用户列表
export const getUserList = (params) => {
  return request({
    url: '/users/',
    method: 'get',
    params
  })
}

// 获取用户详情
export const getUserDetail = (id) => {
  return request({
    url: `/users/${id}/`,
    method: 'get'
  })
}

// 更新用户状态
export const updateUserStatus = (id, status) => {
  return request({
    url: `/users/${id}/status/`,
    method: 'patch',
    data: { status }
  })
}

// 重置用户密码
export const resetUserPassword = (id, password) => {
  return request({
    url: `/users/${id}/reset-password/`,
    method: 'post',
    data: { password }
  })
}

// 获取用户订单
export const getUserOrders = (userId, params) => {
  return request({
    url: `/users/${userId}/orders/`,
    method: 'get',
    params
  })
}