import request from '@/utils/request'

// 获取民宿列表
export function getHomestayList(params) {
  return request({
    url: '/homestays/',  // 移除 /api/v1 前缀
    method: 'get',
    params
  })
}

// 获取民宿详情
export function getHomestayDetail(id) {
  return request({
    url: `/homestays/${id}/`,  // 移除 /api/v1 前缀
    method: 'get'
  })
}

// 收藏/取消收藏民宿
export function toggleHomestayFavorite(id) {
  return request({
    url: `/homestays/${id}/favorite/`,  // 移除 /api/v1 前缀
    method: 'post'
  })
}