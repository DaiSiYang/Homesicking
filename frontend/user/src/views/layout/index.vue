<template>
  <div class="layout">
    <!-- 顶部导航 -->
    <header class="bg-white/90 backdrop-blur-sm shadow-paper sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <!-- Logo和主导航 -->
          <div class="flex items-center">
            <div class="flex-shrink-0 flex items-center">
              <router-link to="/" class="flex items-center space-x-2">
                <div class="w-8 h-8 bg-primary-600 rounded-md flex items-center justify-center">
                  <span class="text-white font-calligraphy text-lg">觅</span>
                </div>
                <span class="text-2xl font-calligraphy text-primary-700">觅乡记</span>
              </router-link>
            </div>
            <nav class="ml-10 flex items-center space-x-1">
              <router-link to="/" class="nav-link" :class="{ 'nav-link-active': $route.path === '/' }">
                首页
              </router-link>
              <router-link to="/villages" class="nav-link" :class="{ 'nav-link-active': $route.path.includes('/villages') }">
                乡村
              </router-link>
              <router-link to="/homestays" class="nav-link" :class="{ 'nav-link-active': $route.path.includes('/homestays') }">
                民宿
              </router-link>
              <router-link to="/products" class="nav-link" :class="{ 'nav-link-active': $route.path.includes('/products') }">
                特产
              </router-link>
              <router-link to="/foods" class="nav-link" :class="{ 'nav-link-active': $route.path.includes('/foods') }">
                美食
              </router-link>
            </nav>
          </div>
          
          <!-- 用户相关 -->
          <div class="flex items-center space-x-4">
            <!-- 购物车 -->
            <router-link v-if="userStore.isLoggedIn" to="/cart" class="relative text-ink-500 hover:text-primary-600 transition-colors">
              <el-badge :value="cartStore.cartCount" class="item" v-if="cartStore.cartCount > 0">
                <el-icon :size="22"><ShoppingCart /></el-icon>
              </el-badge>
              <el-icon v-else :size="22"><ShoppingCart /></el-icon>
            </router-link>
            
            <!-- 收藏 -->
            <router-link v-if="userStore.isLoggedIn" to="/favorites" class="relative text-ink-500 hover:text-primary-600 transition-colors">
              <el-icon :size="22"><Star /></el-icon>
            </router-link>
            
            <!-- 用户菜单 -->
            <div v-if="userStore.isLoggedIn">
              <el-dropdown trigger="click">
                <div class="flex items-center cursor-pointer hover:bg-earth-50 px-3 py-2 rounded-ink transition-colors">
                  <div class="w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center mr-2">
                    <span class="text-primary-600 text-sm font-medium">{{ userStore.username?.charAt(0) }}</span>
                  </div>
                  <span class="text-sm font-medium text-ink-700 mr-1">{{ userStore.username }}</span>
                  <el-icon class="text-ink-400"><ArrowDown /></el-icon>
                </div>
                <template #dropdown>
                  <el-dropdown-menu class="shadow-brush border-earth-200">
                    <el-dropdown-item>
                      <router-link to="/profile" class="block w-full text-ink-600 hover:text-primary-600">
                        个人资料
                      </router-link>
                    </el-dropdown-item>
                    <el-dropdown-item>
                      <router-link to="/orders" class="block w-full text-ink-600 hover:text-primary-600">
                        我的订单
                      </router-link>
                    </el-dropdown-item>
                    <el-dropdown-item>
                      <router-link to="/favorites" class="block w-full text-ink-600 hover:text-primary-600">
                        我的收藏
                      </router-link>
                    </el-dropdown-item>
                    <el-dropdown-item divided @click="handleLogout" class="text-red-600 hover:text-red-700">
                      退出登录
                    </el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </div>
            
            <!-- 登录/注册 -->
            <div v-else class="flex space-x-3">
              <router-link to="/login" class="btn-outline text-sm px-4 py-2">
                登录
              </router-link>
              <router-link to="/register" class="btn-primary text-sm px-4 py-2">
                注册
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </header>
    
    <!-- 主内容区域 -->
    <main class="min-h-screen">
      <router-view />
    </main>
    
    <!-- 页脚 -->
    <footer class="bg-ink-800 text-white py-12 mt-16">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <!-- 装饰性顶部边框 -->
        <div class="w-full h-px bg-gradient-to-r from-transparent via-earth-400 to-transparent mb-8"></div>
        
        <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div>
            <div class="flex items-center space-x-2 mb-4">
              <div class="w-6 h-6 bg-primary-600 rounded flex items-center justify-center">
                <span class="text-white font-calligraphy text-sm">觅</span>
              </div>
              <h3 class="text-lg font-calligraphy text-white">觅乡记</h3>
            </div>
            <p class="text-gray-300 text-sm leading-relaxed">
              致力于为用户提供优质的乡村旅游服务，
              让您发现乡村之美，体验传统文化。
            </p>
          </div>
          
          <div>
            <h3 class="text-lg font-medium mb-4 text-earth-200">快速链接</h3>
            <ul class="space-y-2 text-sm">
              <li><router-link to="/" class="text-gray-300 hover:text-primary-400 transition-colors">首页</router-link></li>
              <li><router-link to="/villages" class="text-gray-300 hover:text-primary-400 transition-colors">乡村</router-link></li>
              <li><router-link to="/homestays" class="text-gray-300 hover:text-primary-400 transition-colors">民宿</router-link></li>
              <li><router-link to="/products" class="text-gray-300 hover:text-primary-400 transition-colors">特产</router-link></li>
              <li><router-link to="/foods" class="text-gray-300 hover:text-primary-400 transition-colors">美食</router-link></li>
            </ul>
          </div>
          
          <div>
            <h3 class="text-lg font-medium mb-4 text-earth-200">商家合作</h3>
            <ul class="space-y-2 text-sm">
              <li><a href="#" class="text-gray-300 hover:text-primary-400 transition-colors">商家入驻</a></li>
              <li><a href="#" class="text-gray-300 hover:text-primary-400 transition-colors">合作方式</a></li>
              <li><a href="#" class="text-gray-300 hover:text-primary-400 transition-colors">平台规则</a></li>
            </ul>
          </div>
          
          <div>
            <h3 class="text-lg font-medium mb-4 text-earth-200">联系我们</h3>
            <ul class="space-y-2 text-sm text-gray-300">
              <li>客服热线：400-123-4567</li>
              <li>邮箱：service@mixiangji.com</li>
              <li>地址：中国·乡村旅游示范区</li>
            </ul>
          </div>
        </div>
        
        <div class="border-t border-gray-700 mt-8 pt-8 text-center">
          <p class="text-gray-400 text-sm">
            © 2024 觅乡记. 保留所有权利. 
            <span class="mx-2">|</span>
            <a href="#" class="hover:text-primary-400 transition-colors">隐私政策</a>
            <span class="mx-2">|</span>
            <a href="#" class="hover:text-primary-400 transition-colors">服务条款</a>
          </p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessageBox } from 'element-plus'
import { ShoppingCart, ArrowDown, Phone, Message } from '@element-plus/icons-vue'
import { useUserStore } from '@/store/user'
import { useCartStore } from '@/store/cart'

const router = useRouter()
const userStore = useUserStore()
const cartStore = useCartStore()

// 退出登录
const handleLogout = () => {
  ElMessageBox.confirm('确定要退出登录吗?', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await userStore.logoutUser()
      router.push('/login')
    } catch (error) {
      console.error('退出登录失败:', error)
    }
  }).catch(() => {})
}

onMounted(async () => {
  // 如果用户已登录，获取购物车数据
  if (userStore.isLoggedIn) {
    try {
      await cartStore.fetchCartItems()
    } catch (error) {
      console.error('获取购物车失败:', error)
    }
  }
})
</script>

<style scoped>
.layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

main {
  flex: 1;
}
</style>