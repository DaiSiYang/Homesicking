import request from '@/utils/request'

// 获取民宿列表
export const getHomestayList = (params) => {
  return request({
    url: '/homestays/',
    method: 'get',
    params
  })
}

// 获取民宿详情
export const getHomestayDetail = (id) => {
  return request({
    url: `/homestays/${id}/`,
    method: 'get'
  })
}

// 更新民宿状态
export const updateHomestayStatus = (id, status) => {
  return request({
    url: `/homestays/${id}/status/`,
    method: 'patch',
    data: { status }
  })
}

// 审核民宿
export const reviewHomestay = (id, data) => {
  return request({
    url: `/homestays/${id}/review/`,
    method: 'post',
    data
  })
}