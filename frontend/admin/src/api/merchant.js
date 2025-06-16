import request from '@/utils/request'

// 获取商户列表
export const getMerchantList = (params) => {
  return request({
    url: '/merchants/',
    method: 'get',
    params
  })
}

// 获取商户详情
export const getMerchantDetail = (id) => {
  return request({
    url: `/merchants/${id}/`,
    method: 'get'
  })
}

// 更新商户状态
export const updateMerchantStatus = (id, status) => {
  return request({
    url: `/merchants/${id}/status/`,
    method: 'patch',
    data: { status }
  })
}

// 审核商户
export const reviewMerchant = (id, data) => {
  return request({
    url: `/merchants/${id}/review/`,
    method: 'post',
    data
  })
}

// 获取商户产品
export const getMerchantProducts = (merchantId, params) => {
  return request({
    url: `/merchants/${merchantId}/products/`,
    method: 'get',
    params
  })
}