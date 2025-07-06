import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/modules/auth/stores/auth'

const routes = [
  { 
    path: '/', 
    name: 'Home', 
    component: () => import('@/modules/auth/pages/Login.vue'),
    meta: { public: true }
  },
  { 
    path: '/login', 
    name: 'Login', 
    component: () => import('@/modules/auth/pages/Login.vue'),
    meta: { public: true }
  },
  { 
    path: '/register', 
    name: 'Register', 
    component: () => import('@/modules/auth/pages/Register.vue'),
    meta: { public: true }
  },
  { 
    path: '/feed', 
    name: 'Feed', 
    component: () => import('@/modules/users/pages/Feed.vue'),
    meta: { requiresAuth: true }
  },
  { 
    path: '/myposts', 
    name: 'MyPublications', 
    component: () => import('@/modules/posts/pages/MyPublications.vue'),
    meta: { requiresAuth: true }
  },
  { 
    path: '/profile', 
    name: 'Profile', 
    component: () => import('@/modules/users/pages/Profile.vue'),
    meta: { requiresAuth: true }
  },
  { 
    path: '/notifications', 
    name: 'Notifications', 
    component: () => import('@/modules/notifications/pages/Notifications.vue'),
    meta: { requiresAuth: true }
  },
  { 
    path: '/ranking', 
    name: 'Ranking', 
    component: () => import('@modules/ranking/pages/Ranking.vue'),
    meta: { requiresAuth: true }
  },
  { 
    path: '/users/:userId', 
    name: 'UserProfile', 
    component: () => import('@/modules/users/pages/UserProfileView.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Guardia de navegación global
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  
  // Verificar autenticación solo si es necesario
  if (to.meta.requiresAuth) {
    if (!authStore.user) {
      // Intentar recuperar sesión si no hay usuario en el store
      try {
        const { data: { user } } = await supabase.auth.getUser()
        if (user) {
          authStore.setUser(user)
        } else {
          return next('/login?redirect=' + encodeURIComponent(to.fullPath))
        }
      } catch (error) {
        console.error('Error verificando sesión:', error)
        return next('/login?redirect=' + encodeURIComponent(to.fullPath))
      }
    }
    
    if (!authStore.isAuthenticated) {
      return next('/login?redirect=' + encodeURIComponent(to.fullPath))
    }
  }
  
  // Redirigir usuarios autenticados que intentan acceder a rutas públicas
  if (to.meta.public && authStore.isAuthenticated) {
    return next('/feed')
  }
  
  next()
})

export default router