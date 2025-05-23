import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import PublicacionesView from '../modules/publicaciones/views/PublicacionesView.vue'
import notificaciones from '@/modules/notificaciones/views/notificaciones.vue'
import LoginView from '@/modules/auth/views/LoginView.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue'),
    },
    {
      path: '/publicaciones',
      name: 'Publicaciones',
      component: PublicacionesView,
    },
    {
      path: '/notificaciones',
      name: 'notificaciones',
      component: notificaciones,
    },
     {
      path: '/login',
      name: 'Login',
      component: LoginView,
    },

  ],
})

export default router
