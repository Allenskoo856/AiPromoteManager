import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/Home.vue'),
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/Login.vue'),
      meta: { guest: true }
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/Register.vue'),
      meta: { guest: true }
    },
    {
      path: '/prompts',
      name: 'prompts',
      component: () => import('../views/prompts/List.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/prompts/create',
      name: 'prompt-create',
      component: () => import('../views/prompts/Create.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/prompts/:id',
      name: 'prompt-detail',
      component: () => import('../views/prompts/Detail.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/prompts/:id/edit',
      name: 'prompt-edit',
      component: () => import('../views/prompts/Edit.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/categories',
      name: 'categories',
      component: () => import('../views/categories/List.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/tags',
      name: 'tags',
      component: () => import('../views/tags/List.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('../views/Profile.vue'),
      meta: { requiresAuth: true }
    },
  ],
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  const isGuestOnly = to.matched.some(record => record.meta.guest)

  if (requiresAuth && !authStore.isLoggedIn) {
    next('/login')
  } else if (isGuestOnly && authStore.isLoggedIn) {
    next('/')
  } else {
    next()
  }
})

export default router 