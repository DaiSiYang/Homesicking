import request from '@/utils/request'

// 获取产品列表
export function getProductList(params) {
  return request({
    url: '/products/', // 不要包含 /api/v1
    method: 'get',
    params
  })
}

// 获取产品详情
export function getProductDetail(id) {
  return request({
    url: `/products/${id}/`,
    method: 'get'
  })
}

// 获取产品分类
export function getProductCategories() {
  return request({
    url: '/products/categories/',
    method: 'get'
  })
}

// 收藏/取消收藏产品
export function toggleProductFavorite(id) {
  return request({
    url: `/products/${id}/favorite/`,
    method: 'post'
  })
}