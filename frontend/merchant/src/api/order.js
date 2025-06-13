import request from '@/utils/request'

// 获取订单列表
export function getOrderList(params) {
  return request({
    url: '/api/v1/merchant/orders/',
    method: 'get',
    params
  })
}

// 获取订单详情
export function getOrderDetail(id) {
  return request({
    url: `/api/v1/merchant/orders/${id}/`,
    method: 'get'
  })
}

// 更新订单状态
export function updateOrderStatus(id, status) {
  return request({
    url: `/api/v1/merchant/orders/${id}/status/`,
    method: 'put',
    data: { status }
  })
}

// 获取订单统计数据
export function getOrderStatistics(params) {
  return request({
    url: '/api/v1/merchant/orders/statistics/',
    method: 'get',
    params
  })
}

// 获取最近订单
export function getRecentOrders(limit = 5) {
  return request({
    url: '/api/v1/merchant/orders/recent/',
    method: 'get',
    params: { limit }
  })
}