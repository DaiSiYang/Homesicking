<template>
  <div class="admin-layout ink-texture">
    <!-- 侧边栏 -->
    <div class="admin-sidebar" :class="{ 'is-collapsed': isCollapse }">
      <div class="logo-container">
        <div class="logo-content">
          <div class="logo-icon">
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2L2 7v10c0 5.55 3.84 9.739 9 11 5.16-1.261 9-5.45 9-11V7l-10-5z"/>
            </svg>
          </div>
          <div v-if="!isCollapse" class="logo-text">
            <h1>觅乡记</h1>
            <span>管理后台</span>
          </div>
        </div>
      </div>
      
      <!-- 菜单 -->
      <el-menu
        :default-active="activeMenu"
        class="sidebar-menu"
        :collapse="isCollapse"
        router
      >
        <el-menu-item v-for="route in routes" :key="route.path" :index="route.path">
          <el-icon><component :is="route.meta.icon" /></el-icon>
          <template #title>{{ route.meta.title }}</template>
        </el-menu-item>
      </el-menu>
      
      <!-- 底部装饰 -->
      <div class="sidebar-decoration">
        <div class="village-pattern"></div>
      </div>
    </div>
    
    <!-- 主内容区 -->
    <div class="admin-content">
      <!-- 头部 -->
      <div class="admin-header village-card">
        <div class="header-left">
          <el-button 
            link
            :icon="isCollapse ? 'Expand' : 'Fold'" 
            @click="toggleSidebar"
            class="toggle-btn"
          />
          <el-breadcrumb separator="/" class="breadcrumb">
            <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>{{ currentRoute.meta.title }}</el-breadcrumb-item>
          </el-breadcrumb>
        </div>
        
        <div class="header-right">
          <el-dropdown trigger="click" @command="handleCommand">
            <div class="user-dropdown">
              <el-avatar :size="36" :src="authStore.avatar" class="user-avatar" />
              <div class="user-info">
                <span class="username">{{ authStore.username }}</span>
                <span class="role">管理员</span>
              </div>
              <el-icon class="dropdown-icon"><ArrowDown /></el-icon>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="settings">
                  <el-icon><Setting /></el-icon>
                  系统设置
                </el-dropdown-item>
                <el-dropdown-item divided command="logout">
                  <el-icon><SwitchButton /></el-icon>
                  退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
      
      <!-- 主要内容 -->
      <div class="admin-main">
        <router-view v-slot="{ Component, route }">
          <transition name="fade" mode="out-in">
            <component :is="Component" :key="route.path" />
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

// 处理下拉菜单命令
const handleCommand = async (command) => {
  if (command === 'logout') {
    try {
      await ElMessageBox.confirm('确定要退出登录吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
      
      await authStore.logout()
      router.push('/login')
    } catch (error) {
      // 用户取消
    }
  } else if (command === 'settings') {
    router.push('/settings')
  }
}

onMounted(() => {
  // 修复：使用正确的方法名
  authStore.init()
})
</script>

<style scoped>
.admin-layout {
  display: flex;
  height: 100vh;
  background: var(--bg-primary);
}

/* 侧边栏样式 */
.admin-sidebar {
  width: 260px;
  background: linear-gradient(180deg, 
    var(--primary-color) 0%, 
    var(--primary-dark) 100%
  );
  transition: width 0.3s ease;
  position: relative;
  overflow: hidden;
}

.admin-sidebar.is-collapsed {
  width: 64px;
}

.logo-container {
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.logo-content {
  display: flex;
  align-items: center;
  color: white;
}

.logo-icon {
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 12px;
}

.logo-icon svg {
  width: 24px;
  height: 24px;
}

.logo-text h1 {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  line-height: 1;
}

.logo-text span {
  font-size: 12px;
  opacity: 0.8;
  display: block;
  margin-top: 2px;
}

.sidebar-menu {
  border: none;
  background: transparent;
  padding: 20px 0;
}

.sidebar-menu :deep(.el-menu-item) {
  color: rgba(255, 255, 255, 0.8);
  border-radius: 0 25px 25px 0;
  margin: 4px 20px 4px 0;
  transition: all 0.3s ease;
}

.sidebar-menu :deep(.el-menu-item:hover) {
  background: rgba(255, 255, 255, 0.1);
  color: white;
}

.sidebar-menu :deep(.el-menu-item.is-active) {
  background: rgba(255, 255, 255, 0.15);
  color: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.sidebar-decoration {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 100px;
  background: linear-gradient(to top, 
    rgba(0, 0, 0, 0.1) 0%, 
    transparent 100%
  );
}

.village-pattern {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  width: 60px;
  height: 20px;
  background: repeating-linear-gradient(
    90deg,
    rgba(255, 255, 255, 0.1) 0px,
    rgba(255, 255, 255, 0.1) 2px,
    transparent 2px,
    transparent 8px
  );
  border-radius: 10px;
}

/* 主内容区样式 */
.admin-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.admin-header {
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  margin: 16px 24px 0;
  border-radius: 12px;
  background: var(--bg-card);
  box-shadow: var(--shadow-soft);
}

.header-left {
  display: flex;
  align-items: center;
}

.toggle-btn {
  color: var(--primary-color);
  font-size: 18px;
  margin-right: 16px;
}

.breadcrumb {
  color: var(--text-secondary);
}

.header-right {
  display: flex;
  align-items: center;
}

.user-dropdown {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.user-dropdown:hover {
  background: var(--bg-secondary);
}

.user-avatar {
  border: 2px solid var(--border-light);
}

.user-info {
  margin: 0 12px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.username {
  font-weight: 500;
  color: var(--text-primary);
  line-height: 1;
}

.role {
  font-size: 12px;
  color: var(--text-muted);
  margin-top: 2px;
}

.dropdown-icon {
  color: var(--text-muted);
  transition: transform 0.3s ease;
}

.admin-main {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
  background: var(--bg-primary);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .admin-sidebar {
    position: fixed;
    left: 0;
    top: 0;
    z-index: 1000;
    transform: translateX(-100%);
    transition: transform 0.3s ease;
  }
  
  .admin-sidebar.is-open {
    transform: translateX(0);
  }
  
  .admin-content {
    margin-left: 0;
  }
  
  .admin-header {
    margin: 8px 16px 0;
    padding: 0 16px;
  }
  
  .admin-main {
    padding: 16px;
  }
}
</style>