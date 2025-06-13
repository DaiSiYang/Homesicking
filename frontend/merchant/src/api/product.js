import request from '@/utils/request'

// 获取特产列表
export function getProductList(params) {
  return request({
    url: '/api/v1/merchant/products/',
    method: 'get',
    params
  })
}

// 获取特产详情
export function getProductDetail(id) {
  return request({
    url: `/api/v1/merchant/products/${id}/`,
    method: 'get'
  })
}

// 创建特产
export function createProduct(data) {
  return request({
    url: '/api/v1/merchant/products/',
    method: 'post',
    data
  })
}

// 更新特产
export function updateProduct(id, data) {
  return request({
    url: `/api/v1/merchant/products/${id}/`,
    method: 'put',
    data
  })
}

// 删除特产
export function deleteProduct(id) {
  return request({
    url: `/api/v1/merchant/products/${id}/`,
    method: 'delete'
  })
}

// 上传产品图片
export function uploadProductImage(data) {
  return request({
    url: '/api/v1/merchant/upload/product/',
    method: 'post',
    data,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}