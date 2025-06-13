import request from '@/utils/request'

// 获取收藏列表
export function getFavoriteList(params) {
  return request({
    url: '/favorites/',
    method: 'get',
    params
  })
}

// 移除收藏
export function removeFavorite(id, type) {
  return request({
    url: `/favorites/${id}/`,
    method: 'delete',
    data: { type }
  })
}