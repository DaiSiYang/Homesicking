import { defineStore } from 'pinia'
import { getOrderList, getOrderDetail, createOrder, cancelOrder } from '@/api/order'
import { createPayment } from '@/api/payment'
import { ElMessage } from 'element-plus'

export const useOrderStore = defineStore('order', {
  state: () => ({
    orders: [],
    currentOrder: null,
    loading: false,
    totalCount: 0,
    pageSize: 10,
    currentPage: 1
  }),
  
  getters: {
    // 获取订单总数
    orderCount: (state) => state.totalCount,
    
    // 订单状态显示
    orderStatusMap: () => ({
      'pending_payment': '待支付',
      'paid': '已支付',
      'confirmed': '已确认',
      'canceled': '已取消',
      'refunding': '退款中',
      'refunded': '已退款',
      'completed': '已完成'
    })
  },
  
  actions: {
    // 获取订单列表 - 支持sessionStorage
    async fetchOrders(params = {}) {
      this.loading = true
      try {
        // 检查是否有待处理的订单
        const pendingOrder = sessionStorage.getItem('pendingOrder')
        if (pendingOrder) {
          const orderData = JSON.parse(pendingOrder)
          // 将待处理订单添加到订单列表
          this.orders = [orderData, ...this.orders]
        }
        
        // 然后调用API获取其他订单
        const queryParams = {
          page: this.currentPage,
          page_size: this.pageSize,
          ...params
        }
        
        const res = await getOrderList(queryParams)
        if (res.code === 200) {
          this.orders = res.data.results || []
          this.totalCount = res.data.count || 0
          return Promise.resolve(res.data)
        } else {
          ElMessage.error(res.message || '获取订单失败')
          return Promise.reject(res)
        }
      } catch (error) {
        ElMessage.error('获取订单失败')
        return Promise.reject(error)
      } finally {
        this.loading = false
      }
    },
    
    // 获取订单详情
    async fetchOrderDetail(orderId) {
      this.loading = true
      try {
        const res = await getOrderDetail(orderId)
        if (res.code === 200) {
          this.currentOrder = res.data
          return Promise.resolve(res.data)
        } else {
          ElMessage.error(res.message || '获取订单详情失败')
          return Promise.reject(res)
        }
      } catch (error) {
        ElMessage.error('获取订单详情失败')
        return Promise.reject(error)
      } finally {
        this.loading = false
      }
    },
    
    // 创建订单
    async submitOrder(orderData) {
      this.loading = true
      try {
        const res = await createOrder(orderData)
        if (res.code === 200) {
          ElMessage.success('订单创建成功')
          return Promise.resolve(res.data)
        } else {
          ElMessage.error(res.message || '创建订单失败')
          return Promise.reject(res)
        }
      } catch (error) {
        ElMessage.error('创建订单失败')
        return Promise.reject(error)
      } finally {
        this.loading = false
      }
    },
    
    // 取消订单
    async cancelUserOrder(orderId) {
      try {
        const res = await cancelOrder(orderId)
        if (res.code === 200) {
          ElMessage.success('订单已取消')
          
          // 如果有当前订单，且是被取消的订单，更新状态
          if (this.currentOrder && this.currentOrder.id === orderId) {
            this.currentOrder.status = 'canceled'
          }
          
          // 更新订单列表中的状态
          const orderIndex = this.orders.findIndex(order => order.id === orderId)
          if (orderIndex !== -1) {
            this.orders[orderIndex].status = 'canceled'
          }
          
          return Promise.resolve(res)
        } else {
          ElMessage.error(res.message || '取消订单失败')
          return Promise.reject(res)
        }
      } catch (error) {
        ElMessage.error('取消订单失败')
        return Promise.reject(error)
      }
    },
    
    // 支付订单
    async payOrder(paymentData) {
      try {
        const res = await createPayment(paymentData)
        if (res.code === 200) {
          ElMessage.success('支付成功')
          return Promise.resolve(res.data)
        } else {
          ElMessage.error(res.message || '支付失败')
          return Promise.reject(res)
        }
      } catch (error) {
        ElMessage.error('支付失败')
        return Promise.reject(error)
      }
    },
    
    // 设置分页
    setPage(page) {
      this.currentPage = page
    },
    
    // 设置每页数量
    setPageSize(pageSize) {
      this.pageSize = pageSize
    }
  }
})