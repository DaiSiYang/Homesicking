import { defineStore } from 'pinia'
import { getCartList, addToCart, updateCartItem, removeFromCart, clearCart } from '@/api/cart'
import { ElMessage } from 'element-plus'

export const useCartStore = defineStore('cart', {
  state: () => ({
    cartItems: [],
    useMockData: false // 改为 false
  }),
  
  getters: {
    cartCount: (state) => state.totalQuantity,
    cartTotal: (state) => state.totalPrice,
    isEmpty: (state) => state.cartItems.length === 0
  },
  
  actions: {
    // 获取购物车列表
    async fetchCartItems() {
      this.loading = true
      try {
        if (this.useMockData) {
          // 使用模拟数据
          setTimeout(() => {
            this.cartItems = this.getMockCartItems()
            this.calculateTotals()
            this.loading = false
          }, 300)
          return Promise.resolve({ items: this.cartItems })
        } else {
          // 使用真实API
          const res = await getCartList()
          if (res.code === 200) {
            this.cartItems = res.data.items || []
            this.totalQuantity = res.data.total_quantity || 0
            this.totalPrice = res.data.total_price || 0
            return Promise.resolve(res.data)
          } else {
            return Promise.reject(res)
          }
        }
      } catch (error) {
        console.error('获取购物车失败:', error)
        // 如果API调用失败，切换到模拟数据
        if (!this.useMockData) {
          ElMessage.warning('API连接失败，切换到模拟数据模式')
          this.useMockData = true
          return this.fetchCartItems()
        } else {
          ElMessage.error('获取购物车失败')
          return Promise.reject(error)
        }
      } finally {
        if (!this.useMockData) {
          this.loading = false
        }
      }
    },
    
    // 添加商品到购物车
    async addToCart(item) {
      try {
        if (this.useMockData) {
          // 模拟添加商品
          const existingItem = this.cartItems.find(i => 
            i.productId === item.productId && 
            (i.skuName === item.skuName || (!i.skuName && !item.skuName))
          )
          
          if (existingItem) {
            existingItem.quantity += item.quantity
          } else {
            this.cartItems.push({
              ...item,
              id: Date.now().toString() // 生成一个临时ID
            })
          }
          
          this.calculateTotals()
          ElMessage.success('添加成功')
          return Promise.resolve({ item })
        } else {
          const res = await addToCart(item)
          if (res.code === 200) {
            ElMessage.success('添加成功')
            this.fetchCartItems()
            return Promise.resolve(res.data)
          } else {
            ElMessage.error(res.message || '添加失败')
            return Promise.reject(res)
          }
        }
      } catch (error) {
        console.error('添加失败:', error)
        ElMessage.error('添加失败')
        return Promise.reject(error)
      }
    },
    
    // 更新购物车商品数量
    async updateItemQuantity(id, quantity) {
      try {
        if (this.useMockData) {
          // 模拟更新数量
          const item = this.cartItems.find(i => i.id === id)
          if (item) {
            item.quantity = quantity
            this.calculateTotals()
          }
          return Promise.resolve({ item })
        } else {
          const res = await updateCartItem(id, { quantity })
          if (res.code === 200) {
            this.fetchCartItems()
            return Promise.resolve(res.data)
          } else {
            ElMessage.error(res.message || '更新失败')
            return Promise.reject(res)
          }
        }
      } catch (error) {
        console.error('更新失败:', error)
        ElMessage.error('更新失败')
        return Promise.reject(error)
      }
    },
    
    // 移除购物车商品
    async removeCartItem(id) {
      try {
        if (this.useMockData) {
          // 模拟移除商品
          this.cartItems = this.cartItems.filter(i => i.id !== id)
          this.calculateTotals()
          ElMessage.success('移除成功')
          return Promise.resolve({ success: true })
        } else {
          const res = await removeFromCart(id)
          if (res.code === 200) {
            ElMessage.success('移除成功')
            this.fetchCartItems()
            return Promise.resolve(res)
          } else {
            ElMessage.error(res.message || '移除失败')
            return Promise.reject(res)
          }
        }
      } catch (error) {
        console.error('移除失败:', error)
        ElMessage.error('移除失败')
        return Promise.reject(error)
      }
    },
    
    // 清空购物车
    async clearCartItems() {
      try {
        if (this.useMockData) {
          // 模拟清空购物车
          this.cartItems = []
          this.calculateTotals()
          ElMessage.success('购物车已清空')
          return Promise.resolve({ success: true })
        } else {
          const res = await clearCart()
          if (res.code === 200) {
            this.cartItems = []
            this.totalQuantity = 0
            this.totalPrice = 0
            ElMessage.success('购物车已清空')
            return Promise.resolve(res)
          } else {
            ElMessage.error(res.message || '清空购物车失败')
            return Promise.reject(res)
          }
        }
      } catch (error) {
        console.error('清空购物车失败:', error)
        ElMessage.error('清空购物车失败')
        return Promise.reject(error)
      }
    },
    
    // 计算总数量和总价格
    calculateTotals() {
      this.totalQuantity = this.cartItems.reduce((sum, item) => sum + item.quantity, 0)
      this.totalPrice = this.cartItems.reduce((sum, item) => sum + (item.price * item.quantity), 0)
    },
    
    // 获取模拟购物车数据
    getMockCartItems() {
      return [
        {
          id: '1',
          productId: '1',
          name: '云南野生菌礼盒',
          skuName: '精选礼盒装 300g',
          price: 168,
          coverImage: 'https://picsum.photos/id/292/600/400',
          quantity: 1
        },
        {
          id: '2',
          productId: '2',
          name: '婺源山茶油礼盒',
          skuName: '特级初榨 500ml',
          price: 138,
          coverImage: 'https://picsum.photos/id/493/600/400',
          quantity: 2
        }
      ]
    }
  }
})