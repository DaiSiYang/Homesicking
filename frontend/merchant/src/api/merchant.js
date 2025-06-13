import request from '@/utils/request'

// 获取商户信息
export function getMerchantInfo() {
  return request({
    url: '/api/v1/merchant/profile/',
    method: 'get'
  })
}

// 更新商户信息
export function updateMerchantInfo(data) {
  return request({
    url: '/api/v1/merchant/profile/',
    method: 'put',
    data
  })
}

// 获取商户统计数据
export function getMerchantStatistics() {
  return request({
    url: '/api/v1/merchant/statistics/',
    method: 'get'
  })
}

// 获取收入统计
export function getIncomeStatistics(params) {
  return request({
    url: '/api/v1/merchant/statistics/income/',
    method: 'get',
    params
  })
}

// 上传商户Logo
export function uploadMerchantLogo(data) {
  return request({
    url: '/api/v1/merchant/upload/logo/',
    method: 'post',
    data,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

// 上传商户图片
export function uploadMerchantImage(data) {
  return request({
    url: '/api/v1/merchant/upload/image/',
    method: 'post',
    data,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

// 上传营业执照
export function uploadLicense(data) {
  return request({
    url: '/api/v1/merchant/upload/license/',
    method: 'post',
    data,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

// 获取通知设置
export function getNotificationSettings() {
  return request({
    url: '/api/v1/merchant/settings/notifications/',
    method: 'get'
  })
}

// 更新通知设置
export function updateNotificationSettings(data) {
  return request({
    url: '/api/v1/merchant/settings/notifications/',
    method: 'put',
    data
  })
}