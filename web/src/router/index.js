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
    component: HomeView
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

export default router
