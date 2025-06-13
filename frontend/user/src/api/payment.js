import request from '@/utils/request'

// 获取支付记录列表
export function getPaymentList(params) {
  return request({
    url: '/payment/',
    method: 'get',
    params
  })
}

// 创建支付
export function createPayment(data) {
  return request({
    url: '/payment/create/',
    method: 'post',
    data
  })
}

// 获取退款记录列表
export function getRefundList(params) {
  return request({
    url: '/payment/refund/',
    method: 'get',
    params
  })
}

// 申请退款
export function createRefund(data) {
  return request({
    url: '/payment/refund/create/',
    method: 'post',
    data
  })
} 