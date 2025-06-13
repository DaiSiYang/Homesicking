import request from '@/utils/request'

// 获取村庄列表
export function getVillageList(params) {
  return request({
    url: '/villages/',  // 移除 /api/v1 前缀
    method: 'get',
    params
  })
}

// 获取村庄详情
export function getVillageDetail(id) {
  return request({
    url: `/villages/${id}/`,  // 移除 /api/v1 前缀
    method: 'get'
  })
}

// 收藏/取消收藏村庄
export function toggleVillageFavorite(id) {
  return request({
    url: `/villages/${id}/favorite/`,  // 移除 /api/v1 前缀
    method: 'post'
  })
}