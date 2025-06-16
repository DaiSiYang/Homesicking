import request from '@/utils/request'

// 获取仪表板统计数据
export const getDashboardStats = () => {
  return request({
    url: '/dashboard/stats/',
    method: 'get'
  })
}

// 获取最近活动
export const getRecentActivities = (params) => {
  return request({
    url: '/dashboard/activities/',
    method: 'get',
    params
  })
}

// 获取待办事项
export const getTodoList = () => {
  return request({
    url: '/dashboard/todos/',
    method: 'get'
  })
}