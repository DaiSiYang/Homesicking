import request from '@/utils/request'

// 获取订单列表
export function getOrderList(params) {
  return request({
    url: '/orders/',
    method: 'get',
    params
  })
}

// 获取订单详情
export function getOrderDetail(id) {
  return request({
    url: `/orders/${id}/`,
    method: 'get'
  })
}

// 创建订单
export function createOrder(data) {
  return request({
    url: '/orders/create/',
    method: 'post',
    data
  })
}

// 取消订单
export function cancelOrder(id) {
  return request({
    url: `/orders/${id}/cancel/`,
    method: 'post'
  })
} 