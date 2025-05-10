import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../modules/auth/store/authStore'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/publicaciones'
    },
    {
      path: '/login',
      name: 'Login',
      component: () => import('../modules/auth/views/LoginView.vue'),
      meta: { requiresGuest: true }
    },
    {
      path: '/publicaciones',
      name: 'Publicaciones',
      component: () => import('../modules/publicaciones/views/PublicacionesView.vue')
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: '/publicaciones'
    }
  ]
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  if (to.meta.requiresGuest && authStore.isAuthenticated) {
    next('/publicaciones') // Solo redirige si intenta acceder a login estando autenticado
  } else {
    next() // Permite el acceso en otros casos
  }
})

export default router