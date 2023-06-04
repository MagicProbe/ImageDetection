import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginAndRegister/LoginView.vue'

const routes = [
  {
    path: '/login',
    name: 'login',
    component: LoginView
  },
  {
    path: '/register',
    name: 'register',
    component: () => import(/* webpackChunkName: "about" */ '../views/LoginAndRegister/RegisterView.vue')
  },
  {
    path: '/forgotpassword',
    name: 'forgotpassword',
    component: () => import(/* webpackChunkName: "about" */ '../views/LoginAndRegister/ForgotPassword.vue')
  },
  {
    path: '/validateemail',
    name: 'validateemail',
    component: () => import(/* webpackChunkName: "about" */ '../views/LoginAndRegister/ValidateEmail.vue')
  },
  {
    path: '/',
    name: 'home',
    component: HomeView,
    meta: { requiresAuth: true }
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// 全局前置守卫
router.beforeEach((to, from, next) => {
  // 判断是否需要验证登录状态
  if (to.matched.some(record => record.meta.requiresAuth)) {
    const idToken = localStorage.getItem('idToken')
    if (!idToken) {
      // 如果没有token，则重定向到登录页
      next({ name: 'login' })
    } else {
      // 如果有token，则允许通过
      next()
    }
  } else {
    // 不需要验证登录状态的页面直接放行
    next()
  }
})

export default router
