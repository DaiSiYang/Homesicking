import request from '@/utils/request'

// 获取民宿列表
export const getHomestayList = (params) => {
  return request({
    url: '/api/v1/merchant/homestays/',
    method: 'get',
    params
  })
}

// 获取民宿详情
export const getHomestayDetail = (id) => {
  return request({
    url: `/api/v1/merchant/homestays/${id}/`,
    method: 'get'
  })
}

// 创建民宿
export const createHomestay = (data) => {
  return request({
    url: '/api/v1/merchant/homestays/',
    method: 'post',
    data
  })
}

// 更新民宿
export const updateHomestay = (id, data) => {
  return request({
    url: `/api/v1/merchant/homestays/${id}/`,
    method: 'put',
    data
  })
}

// 删除民宿
export const deleteHomestayById = (id) => {
  return request({
    url: `/api/v1/merchant/homestays/${id}/`,
    method: 'delete'
  })
}

// 更新民宿状态
export function updateHomestayStatus(id, status) {
  return request({
    url: `/api/v1/merchant/homestays/${id}/status/`,
    method: 'put',
    data: { status }
  })
}

// 上传民宿图片
export function uploadHomestayImage(data) {
  return request({
    url: '/api/v1/merchant/upload/homestay/',
    method: 'post',
    data,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}