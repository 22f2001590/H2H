import { createRouter, createWebHistory } from 'vue-router'
// import HomeView from '../views/HomeView.vue'
import index from '../views/index.vue'

import admin_login from '@/views/admin_login.vue'
import customer_login from '@/views/customer_login.vue'
import professional_login from '@/views/professional_login.vue'

import customer_signup from '@/views/customer_signup.vue'
import professional_signup from '@/views/professional_signup.vue'

import admin_dashboard from '@/views/admin_dashboard.vue'
import app_summary from '@/views/app_summary.vue'
import users from '@/views/users.vue'
import services from '@/views/services.vue'

import customer_dashboard from '@/views/customer_dashboard.vue'
import customer_history from '@/views/customer_history.vue'
// import customer_search from '@/views/customer_search.vue'
import user_profile from '@/views/user_profile.vue'

import professional_dashboard from '@/views/professional_dashboard.vue'
import professional_history from '@/views/professional_history.vue'




const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {path: '/', name: 'home', component: index,},
    {paht: '/logout', name: 'logout', component: index,},
    {path: '/admin_login',name: 'admin_login',component: admin_login,},
    {path: '/customer_login',name: 'customer_login',component: customer_login,},
    {path: '/professional_login',name: 'professional_login',component: professional_login,},
    {path: '/customer_signup',name: 'customer_signup',component: customer_signup,},
    {path: '/professional_signup',name: 'professional_signup',component: professional_signup,},
    {path: '/admin_dashboard',name: 'admin_dashboard',component: admin_dashboard,},
    {path: '/app_summary',name: 'app_summary',component: app_summary,},
    {path: '/users',name: 'users',component: users,},
    {path: '/services',name: 'services',component: services,},
    {path: '/customer_dashboard',name: 'customer_dashboard',component: customer_dashboard,},
    {path: '/professional_dashboard',name: 'professional_dashboard',component: professional_dashboard,},
    {path: '/customer_history/:id',name: 'customer_history',component: customer_history,},
    {path: '/professional_history/:id',name: 'professional_history',component: professional_history,},
    {path: '/user_profile/:id',name: 'user_profile',component: user_profile,},
  ],
})

export default router
