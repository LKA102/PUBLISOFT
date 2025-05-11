import { createRouter, createWebHistory } from 'vue-router'

// Importar las vistas
import HomeView from '../views/HomeView.vue'
import PublicacionesView from '../modules/publicaciones/views/PublicacionesView.vue'
import NotificacionesView from '../modules/notificaciones/views/notificaciones.vue' // Corregido el nombre de la variable

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),  // Usa la base URL configurada en Vite
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,  // Ruta principal que carga HomeView
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue'), // Ruta para la página About
    },
    {
      path: '/publicaciones',
      name: 'publicaciones',
      component: PublicacionesView,  // Ruta para publicaciones
    },
    {
      path: '/notificaciones',
      name: 'notificaciones',
      component: NotificacionesView, // Ruta para notificaciones
    },
  ],
})

export default router
