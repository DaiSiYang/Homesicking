import request from '@/utils/request'

// 获取产品列表
export const getProductList = (params) => {
  return request({
    url: '/products/',
    method: 'get',
    params
  })
}

// 获取产品详情
export const getProductDetail = (id) => {
  return request({
    url: `/products/${id}/`,
    method: 'get'
  })
}

// 更新产品状态
export const updateProductStatus = (id, status) => {
  return request({
    url: `/products/${id}/status/`,
    method: 'patch',
    data: { status }
  })
}

// 删除产品
export const deleteProduct = (id) => {
  return request({
    url: `/products/${id}/`,
    method: 'delete'
  })
}

// 批量操作产品
export const batchUpdateProducts = (ids, action, data = {}) => {
  return request({
    url: '/products/batch/',
    method: 'post',
    data: {
      ids,
      action,
      ...data
    }
  })
}

// 获取产品评价
export const getProductReviews = (productId, params) => {
  return request({
    url: `/products/${productId}/reviews/`,
    method: 'get',
    params
  })
}