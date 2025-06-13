<template>
  <div class="merchant-layout">
    <!-- 侧边栏 -->
    <div class="merchant-sidebar">
      <div class="logo-container">
        <div class="logo-content">
          <div class="logo-icon">
            <svg viewBox="0 0 24 24" class="w-8 h-8 text-white">
              <path fill="currentColor" d="M12 2L2 7v10c0 5.55 3.84 9.739 9 11 5.16-1.261 9-5.45 9-11V7l-10-5z"/>
              <path fill="var(--accent-bamboo)" d="M12 4.5L4.5 8.5v8c0 4.2 2.88 7.35 7.5 8.5 4.62-1.15 7.5-4.3 7.5-8.5v-8L12 4.5z"/>
            </svg>
          </div>
          <div class="logo-text">
            <h1 class="text-xl font-bold text-white mb-0">觅乡记</h1>
            <p class="text-xs text-green-200 opacity-80">商户平台</p>
          </div>
        </div>
      </div>
      
      <!-- 菜单 -->
      <el-menu
        :default-active="activeMenu"
        class="sidebar-menu"
        background-color="transparent"
        text-color="rgba(255,255,255,0.8)"
        active-text-color="#7FB069"
        :collapse="isCollapse"
        router
      >
        <el-menu-item v-for="route in routes" :key="route.path" :index="route.path" class="rural-menu-item">
          <el-icon><component :is="route.meta.icon" /></el-icon>
          <template #title>{{ route.meta.title }}</template>
        </el-menu-item>
      </el-menu>
    </div>
    
    <!-- 主内容区 -->
    <div class="merchant-content">
      <!-- 头部 -->
      <div class="merchant-header">
        <div class="flex items-center">
          <el-button 
            link
            :icon="isCollapse ? 'Expand' : 'Fold'" 
            @click="toggleSidebar"
            class="toggle-btn"
          />
          <el-breadcrumb separator="/" class="ml-4 rural-breadcrumb">
            <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>{{ currentRoute.meta.title }}</el-breadcrumb-item>
          </el-breadcrumb>
        </div>
        
        <div class="flex items-center">
          <el-dropdown trigger="click" @command="handleCommand" class="user-dropdown">
            <div class="flex items-center cursor-pointer p-2 rounded-lg hover:bg-green-50 transition-colors">
              <el-avatar :size="36" :src="userStore.userInfo?.avatar || ''" class="border-2 border-green-200" />
              <div class="ml-3 text-left">
                <div class="text-sm font-medium text-gray-700">{{ userStore.userInfo?.shopName || userStore.userInfo?.username || '商户' }}</div>
                <div class="text-xs text-gray-500">商户管理员</div>
              </div>
              <el-icon class="ml-2 text-gray-400"><ArrowDown /></el-icon>
            </div>
            <template #dropdown>
              <el-dropdown-menu class="rural-dropdown">
                <el-dropdown-item command="profile" class="rural-dropdown-item">
                  <el-icon class="mr-2"><User /></el-icon>
                  店铺信息
                </el-dropdown-item>
                <el-dropdown-item command="settings" class="rural-dropdown-item">
                  <el-icon class="mr-2"><Setting /></el-icon>
                  账户设置
                </el-dropdown-item>
                <el-dropdown-item divided command="logout" class="rural-dropdown-item text-red-600">
                  <el-icon class="mr-2"><SwitchButton /></el-icon>
                  退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
      
      <!-- 主要内容 -->
      <div class="merchant-main">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessageBox } from 'element-plus'
import { useUserStore } from '@/store/user'
import { ArrowDown, User, Setting, SwitchButton } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const isCollapse = ref(false)

// 获取可显示在侧边栏的路由
const routes = computed(() => {
  return router.options.routes
    .find(r => r.path === '/')
    .children
    .filter(item => item.meta && item.meta.icon)
})

// 当前激活的菜单
const activeMenu = computed(() => {
  return route.meta.activeMenu || route.path
})

// 当前路由
const currentRoute = computed(() => {
  return route
})

// 切换侧边栏
const toggleSidebar = () => {
  isCollapse.value = !isCollapse.value
}

// 下拉菜单命令处理
const handleCommand = (command) => {
  if (command === 'logout') {
    ElMessageBox.confirm('确定要退出登录吗?', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }).then(async () => {
      await userStore.logoutUser()
      router.push('/login')
    }).catch(() => {})
  } else if (command === 'profile') {
    router.push('/profile')
  } else if (command === 'settings') {
    router.push('/settings')
  }
}

// 获取用户信息
onMounted(async () => {
  if (userStore.isLoggedIn && !Object.keys(userStore.userInfo).length) {
    try {
      await userStore.fetchUserInfo()
    } catch (error) {
      console.error('获取用户信息失败:', error)
    }
  }
})
</script>

<style scoped>
.logo-container {
  height: 80px;
  background: linear-gradient(135deg, rgba(0,0,0,0.2), rgba(0,0,0,0.1));
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid rgba(127, 176, 105, 0.2);
  position: relative;
}

.logo-container::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 20%;
  right: 20%;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--accent-bamboo), transparent);
}

.logo-content {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-icon {
  position: relative;
}

.logo-text h1 {
  font-family: 'PingFang SC', serif;
  letter-spacing: 1px;
}

.rural-menu-item {
  margin: 4px 12px;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.rural-menu-item:hover {
  background: rgba(127, 176, 105, 0.15) !important;
}

.rural-menu-item.is-active {
  background: linear-gradient(135deg, rgba(127, 176, 105, 0.2), rgba(212, 165, 116, 0.1)) !important;
  border-left: 3px solid var(--accent-bamboo);
}

.toggle-btn {
  color: var(--primary-color) !important;
  padding: 8px;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.toggle-btn:hover {
  background: rgba(127, 176, 105, 0.1) !important;
}

.user-dropdown {
  border-radius: 12px;
}

.rural-dropdown {
  border-radius: 12px;
  box-shadow: var(--shadow-card);
  border: 1px solid rgba(45, 80, 22, 0.08);
}

.rural-dropdown-item {
  padding: 12px 16px;
  transition: all 0.3s ease;
  border-radius: 8px;
  margin: 4px;
}

.rural-dropdown-item:hover {
  background: rgba(127, 176, 105, 0.1);
}

.sidebar-menu {
  height: calc(100vh - 80px);
  border-right: none;
  padding-top: 20px;
}

.sidebar-menu:not(.el-menu--collapse) {
  width: 240px;
}
</style>