import request from '@/utils/request'

// 获取推荐乡村
export function getRecommendedVillages() {
  return request({
    url: '/villages/recommended/',
    method: 'get'
  })
}

// 获取推荐民宿
export function getRecommendedHomestays() {
  return request({
    url: '/homestays/',
    method: 'get',
    params: { is_recommended: true, page_size: 4 }
  })
}

// 获取推荐特产
export function getRecommendedProducts() {
  return request({
    url: '/products/',
    method: 'get',
    params: { is_featured: true, page_size: 4 }
  })
}

// 获取推荐美食
export function getRecommendedFoods() {
  return request({
    url: '/foods/',
    method: 'get',
    params: { is_featured: true, page_size: 4 }
  })
}