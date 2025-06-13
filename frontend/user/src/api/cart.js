import request from '@/utils/request'

// 获取购物车列表
export function getCartList() {
  return request({
    url: '/cart/', // 不要包含 /api/v1
    method: 'get'
  })
}

// 添加到购物车
export function addToCart(data) {
  return request({
    url: '/cart/',
    method: 'post',
    data
  })
}

// 更新购物车商品
export function updateCartItem(id, data) {
  return request({
    url: `/cart/${id}/`,
    method: 'patch',
    data
  })
}

// 删除购物车商品
export function removeFromCart(id) {
  return request({
    url: `/cart/${id}/`,
    method: 'delete'
  })
}

// 清空购物车
export function clearCart() {
  return request({
    url: '/cart/clear/',
    method: 'post'
  })
}