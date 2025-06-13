<template>
  <div class="admin-layout">
    <!-- 侧边栏 -->
    <div class="admin-sidebar" :class="{ 'is-collapsed': isCollapse }">
      <div class="logo-container flex items-center justify-center h-16 bg-gray-900">
        <h1 v-if="!isCollapse" class="text-xl font-bold text-white">觅乡记管理后台</h1>
        <h1 v-else class="text-xl font-bold text-white">觅</h1>
      </div>
      
      <!-- 菜单 -->
      <el-menu
        :default-active="activeMenu"
        class="sidebar-menu"
        background-color="#304156"
        text-color="#bfcbd9"
        active-text-color="#409EFF"
        :collapse="isCollapse"
        router
      >
        <el-menu-item v-for="route in routes" :key="route.path" :index="route.path">
          <el-icon><component :is="route.meta.icon" /></el-icon>
          <template #title>{{ route.meta.title }}</template>
        </el-menu-item>
      </el-menu>
    </div>
    
    <!-- 主内容区 -->
    <div class="admin-content">
      <!-- 头部 -->
      <div class="admin-header">
        <div class="flex items-center">
          <el-button 
            type="text" 
            :icon="isCollapse ? 'Expand' : 'Fold'" 
            @click="toggleSidebar"
          />
          <el-breadcrumb separator="/" class="ml-4">
            <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>{{ currentRoute.meta.title }}</el-breadcrumb-item>
          </el-breadcrumb>
        </div>
        
        <div class="flex items-center">
          <el-dropdown trigger="click" @command="handleCommand">
            <div class="flex items-center cursor-pointer">
              <el-avatar :size="32" :src="authStore.avatar" />
              <span class="ml-2">{{ authStore.username }}</span>
              <el-icon class="ml-1"><ArrowDown /></el-icon>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="settings">系统设置</el-dropdown-item>
                <el-dropdown-item divided command="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
      
      <!-- 主要内容 -->
      <div class="admin-main">
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
import { useAuthStore } from '../store/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
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
      authStore.logout()
      router.push('/login')
    }).catch(() => {})
  } else if (command === 'settings') {
    router.push('/settings')
  }
}

// 初始化
onMounted(() => {
  // 初始化认证状态
  authStore.init()
})
</script>

<style scoped>
.admin-layout {
  display: flex;
  min-height: 100vh;
}

.admin-sidebar {
  width: 220px;
  background-color: #304156;
  color: #fff;
  flex-shrink: 0;
  transition: width 0.3s;
}

.admin-sidebar.is-collapsed {
  width: 64px;
}

.admin-content {
  flex: 1;
  overflow-x: hidden;
}

.admin-header {
  height: 60px;
  background-color: #fff;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
  display: flex;
  align-items: center;
  padding: 0 20px;
  justify-content: space-between;
}

.admin-main {
  padding: 20px;
  background-color: #f0f2f5;
  min-height: calc(100vh - 60px);
}

.sidebar-menu {
  height: calc(100vh - 4rem);
  border-right: none;
}

.sidebar-menu:not(.el-menu--collapse) {
  width: 220px;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style> 