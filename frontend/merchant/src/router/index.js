import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/store/user'

// 布局组件
const Layout = () => import('@/components/Layout.vue')

// 路由配置
const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/auth/Login.vue'),
    meta: { title: '登录', requiresAuth: false }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/auth/Register.vue'),
    meta: { title: '注册', requiresAuth: false }
  },
  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    meta: { requiresAuth: true },
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/dashboard/index.vue'),
        meta: { title: '控制台', icon: 'Odometer' }
      },
      {
        path: 'products',
        name: 'Products',
        component: () => import('@/views/products/index.vue'),
        meta: { title: '特产管理', icon: 'ShoppingBag' }
      },
      {
        path: 'products/create',
        name: 'ProductCreate',
        component: () => import('@/views/products/create.vue'),
        meta: { title: '添加特产', activeMenu: '/products' }
      },
      {
        path: 'products/:id/edit',
        name: 'ProductEdit',
        component: () => import('@/views/products/edit.vue'),
        meta: { title: '编辑特产', activeMenu: '/products' }
      },
      {
        path: 'homestays',
        name: 'Homestays',
        component: () => import('@/views/homestays/index.vue'),
        meta: { title: '民宿管理', icon: 'House' }
      },
      {
        path: 'homestays/create',
        name: 'HomestayCreate',
        component: () => import('@/views/homestays/create.vue'),
        meta: { title: '添加民宿', activeMenu: '/homestays' }
      },
      {
        path: 'homestays/:id/edit',
        name: 'HomestayEdit',
        component: () => import('@/views/homestays/edit.vue'),
        meta: { title: '编辑民宿', activeMenu: '/homestays' }
      },
      {
        path: 'orders',
        name: 'Orders',
        component: () => import('@/views/orders/index.vue'),
        meta: { title: '订单管理', icon: 'List' }
      },
      {
        path: 'orders/:id',
        name: 'OrderDetail',
        component: () => import('@/views/orders/detail.vue'),
        meta: { title: '订单详情', activeMenu: '/orders' }
      },
      {
        path: 'profile',
        name: 'Profile',
        component: () => import('@/views/profile/index.vue'),
        meta: { title: '店铺信息', icon: 'Shop' }
      },
      {
        path: 'settings',
        name: 'Settings',
        component: () => import('@/views/settings/index.vue'),
        meta: { title: '账户设置', icon: 'Setting' }
      }
    ]
  },
  // 404页面
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFound.vue'),
    meta: { title: '页面不存在', requiresAuth: false }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 导航守卫
router.beforeEach((to, from, next) => {
  // 设置页面标题
  document.title = to.meta.title ? `${to.meta.title} - 觅乡记商户平台` : '觅乡记商户平台'
  
  const userStore = useUserStore()
  
  // 检查页面是否需要认证
  if (to.meta.requiresAuth && !userStore.isLoggedIn) {
    // 保存目标路由，登录后跳转
    next({ path: '/login', query: { redirect: to.fullPath } })
  } else {
    next()
  }
})

export default router 