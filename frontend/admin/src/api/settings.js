import request from '@/utils/request'

// 获取系统设置
export const getSystemSettings = () => {
  return request({
    url: '/settings/',
    method: 'get'
  })
}

// 更新系统设置
export const updateSystemSettings = (data) => {
  return request({
    url: '/settings/',
    method: 'patch',
    data
  })
}

// 上传文件
export const uploadFile = (file, type = 'image') => {
  const formData = new FormData()
  formData.append('file', file)
  formData.append('type', type)
  
  return request({
    url: '/settings/upload/',
    method: 'post',
    data: formData,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}