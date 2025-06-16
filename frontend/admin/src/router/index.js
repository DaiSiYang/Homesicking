import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../store/auth'

// 布局组件
const Layout = () => import('../components/Layout.vue')

// 路由配置
const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/auth/Login.vue'),
    meta: { title: '登录', requiresAuth: false }
  },
  {
    path: '/register',
    name: 'Register', 
    component: () => import('../views/auth/Register.vue'),
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
        component: () => import('../views/dashboard/index.vue'),
        meta: { title: '控制台', icon: 'Odometer' }
      },
      {
        path: 'users',
        name: 'Users',
        component: () => import('../views/users/index.vue'),
        meta: { title: '用户管理', icon: 'User' }
      },
      {
        path: 'merchants',
        name: 'Merchants',
        component: () => import('../views/merchants/index.vue'),
        meta: { title: '商户管理', icon: 'Shop' }
      },
      {
        path: 'merchants/:id',
        name: 'MerchantDetail',
        component: () => import('../views/merchants/detail.vue'),
        meta: { title: '商户详情', activeMenu: '/merchants' }
      },
      {
        path: 'products',
        name: 'Products',
        component: () => import('../views/products/index.vue'),
        meta: { title: '特产管理', icon: 'ShoppingBag' }
      },
      {
        path: 'products/:id',
        name: 'ProductDetail',
        component: () => import('../views/products/detail.vue'),
        meta: { title: '特产详情', activeMenu: '/products' }
      },
      {
        path: 'homestays',
        name: 'Homestays',
        component: () => import('../views/homestays/index.vue'),
        meta: { title: '民宿管理', icon: 'House' }
      },
      {
        path: 'homestays/:id',
        name: 'HomestayDetail',
        component: () => import('../views/homestays/detail.vue'),
        meta: { title: '民宿详情', activeMenu: '/homestays' }
      },
      {
        path: 'orders',
        name: 'Orders',
        component: () => import('../views/orders/index.vue'),
        meta: { title: '订单管理', icon: 'List' }
      },
      {
        path: 'orders/:id',
        name: 'OrderDetail',
        component: () => import('../views/orders/detail.vue'),
        meta: { title: '订单详情', activeMenu: '/orders' }
      },
      {
        path: 'content',
        name: 'Content',
        component: () => import('../views/content/index.vue'),
        meta: { title: '内容管理', icon: 'Document' }
      },
      {
        path: 'settings',
        name: 'Settings',
        component: () => import('../views/settings/index.vue'),
        meta: { title: '系统设置', icon: 'Setting' }
      }
    ]
  },
  // 404页面
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('../views/NotFound.vue'),
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
  document.title = to.meta.title ? `${to.meta.title} - 觅乡记管理后台` : '觅乡记管理后台'
  
  const authStore = useAuthStore()
  
  // 检查页面是否需要认证
  if (to.meta.requiresAuth && !authStore.isLoggedIn) {
    // 保存目标路由，登录后跳转
    next({ path: '/login', query: { redirect: to.fullPath } })
  } else {
    next()
  }
})

export default router