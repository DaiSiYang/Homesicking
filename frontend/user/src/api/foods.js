import request from '@/utils/request'

// 获取美食列表
export function getFoodList(params) {
  return request({
    url: '/foods/',  // 移除 /api/v1 前缀
    method: 'get',
    params
  })
}

// 获取美食详情
export function getFoodDetail(id) {
  return request({
    url: `/foods/${id}/`,  // 移除 /api/v1 前缀
    method: 'get'
  })
}