import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/store/user'

// 布局组件
const Layout = () => import('@/views/layout/index.vue')

// 路由配置
const routes = [
  {
    path: '/',
    component: Layout,
    children: [
      {
        path: '',
        name: 'Home',
        component: () => import('@/views/home/index.vue'),
        meta: { title: '首页', requiresAuth: false }
      },
      {
        path: 'villages',
        name: 'Villages',
        component: () => import('@/views/villages/index.vue'),
        meta: { title: '乡村', requiresAuth: false }
      },
      {
        path: 'villages/:id',
        name: 'VillageDetail',
        component: () => import('@/views/villages/detail.vue'),
        meta: { title: '乡村详情', requiresAuth: false }
      },
      {
        path: 'attractions/:id',
        name: 'AttractionDetail',
        component: () => import('@/views/attractions/detail.vue'),
        meta: { title: '景点详情', requiresAuth: false }
      },
      {
        path: 'homestays',
        name: 'Homestays',
        component: () => import('@/views/homestays/index.vue'),
        meta: { title: '民宿', requiresAuth: false }
      },
      {
        path: 'homestays/:id',
        name: 'HomestayDetail',
        component: () => import('@/views/homestays/detail.vue'),
        meta: { title: '民宿详情', requiresAuth: false }
      },
      {
        path: 'products',
        name: 'Products',
        component: () => import('@/views/products/index.vue'),
        meta: { title: '特产', requiresAuth: false }
      },
      {
        path: 'products/:id',
        name: 'ProductDetail',
        component: () => import('@/views/products/detail.vue'),
        meta: { title: '特产详情', requiresAuth: false }
      },
      {
        path: 'foods',
        name: 'Foods',
        component: () => import('@/views/foods/index.vue'),
        meta: { title: '美食', requiresAuth: false }
      },
      {
        path: 'foods/:id',
        name: 'FoodDetail',
        component: () => import('@/views/foods/detail.vue'),
        meta: { title: '美食详情', requiresAuth: false }
      },
      // 购物车和订单相关路由
      {
        path: 'cart',
        name: 'Cart',
        component: () => import('@/views/cart/index.vue'),
        meta: { title: '购物车', requiresAuth: true }
      },
      {
        path: 'checkout',
        name: 'Checkout',
        component: () => import('@/views/checkout/index.vue'),
        meta: { title: '确认订单', requiresAuth: true }
      },
      {
        path: 'orders',
        name: 'Orders',
        component: () => import('@/views/orders/index.vue'),
        meta: { title: '我的订单', requiresAuth: true }
      },
      {
        path: 'orders/:id',
        name: 'OrderDetail',
        component: () => import('@/views/orders/detail.vue'),
        meta: { title: '订单详情', requiresAuth: true }
      },
      {
        path: 'payment/:id',
        name: 'Payment',
        component: () => import('@/views/payment/index.vue'),
        meta: { title: '支付', requiresAuth: true }
      },
      {
        path: 'payment/success',
        name: 'PaymentSuccess',
        component: () => import('@/views/payment/success.vue'),
        meta: { title: '支付成功', requiresAuth: true }
      },
      // 用户中心路由
      {
        path: 'user',
        name: 'UserCenter',
        component: () => import('@/views/user/index.vue'),
        meta: { title: '个人中心', requiresAuth: true },
        children: [
          // 在适当位置添加这些路由
          {
            path: '/profile',
            name: 'Profile',
            component: () => import('@/views/profile/index.vue'),
            meta: { title: '个人资料', requiresAuth: true }
          },
          {
            path: '/favorites',
            name: 'Favorites',
            component: () => import('@/views/favorites/index.vue'),
            meta: { title: '我的收藏', requiresAuth: true }
          }
        ]
      }
    ]
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/auth/login.vue'),
    meta: { title: '登录', requiresAuth: false }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/auth/register.vue'),
    meta: { title: '注册', requiresAuth: false }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/error/404.vue'),
    meta: { title: '页面不存在', requiresAuth: false }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  }
})

// 路由守卫
router.beforeEach((to, from, next) => {
  // 设置页面标题
  document.title = to.meta.title ? `${to.meta.title} - 觅乡记` : '觅乡记 - 发现乡村之美'
  
  // 权限验证
  if (to.meta.requiresAuth) {
    const userStore = useUserStore()
    if (!userStore.isLoggedIn) {
      next({ name: 'Login', query: { redirect: to.fullPath } })
      return
    }
  }
  
  next()
})

export default router