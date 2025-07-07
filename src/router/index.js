// src/router/index.js

import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/modules/auth/stores/auth' // Asegúrate de que esta ruta es correcta

const routes = [
  {
    path: '/',
    name: 'Home',
    redirect: '/feed', // Redirige al feed por defecto
    children: [
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
        path: '/resources',
        name: 'Resources',
        component: () => import('@/modules/users/pages/Resources.vue'),
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
        component: () => import('@/modules/ranking/pages/Ranking.vue'), // Ruta corregida si usas @/
        meta: { requiresAuth: true }
      },
      {
        path: '/users/:userId',
        name: 'UserProfile',
        component: () => import('@/modules/users/pages/UserProfileView.vue'),
        meta: { requiresAuth: true }
      },
      // NUEVA RUTA PARA EL DASHBOARD DE ADMINISTRADOR
      {
        path: '/dashboard',
        name: 'Dashboard',
        component: () => import('@/modules/admi/pages/Dashboard.vue'),
        meta: { requiresAuth: true } // Requiere autenticación Y rol de admin
      }
    ]
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Guardia de navegación global
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore();

  // Si el store está en estado de carga (inicial o por alguna acción de auth)
  if (authStore.isAuthLoading) {
    console.log(`RouterGuard: Esperando que authStore.isAuthLoading se resuelva para ${to.fullPath}...`);
    // Espera hasta que el estado 'loading' del store cambie a false.
    // Esto asegura que `isAuthenticated` sea preciso antes de decidir la navegación.
    await new Promise(resolve => {
        const unsubscribe = authStore.$subscribe((mutation, state) => {
            if (!state.loading) { // Cuando el loading global del store es false
                unsubscribe(); // Deja de observar una vez que el estado se resuelve
                resolve();
            }
        });
        // Si por alguna razón el loading ya es false cuando se registra el $subscribe, resolvemos inmediatamente
        if (!authStore.isAuthLoading) {
            unsubscribe();
            resolve();
        }
    });
    console.log(`RouterGuard: authStore.isAuthLoading resuelto. Is Authenticated: ${authStore.isAuthenticated}, User Role: ${authStore.user?.role}`);
  }

  const isAuthenticated = authStore.isAuthenticated; 
  const requiresAuth = to.meta.requiresAuth;
  const isPublic = to.meta.public; // Define 'public' para rutas como login/register

  // Lógica de redirección
  if (requiresAuth && !isAuthenticated) {
    console.log("RouterGuard: Acceso no autorizado a ruta protegida. Redirigiendo a login.");
    // Añade la ruta a la que intentaba ir el usuario para redirigirlo de vuelta después del login
    return next({ name: 'Login', query: { redirect: to.fullPath } });
  } 
  
  if (isPublic && isAuthenticated) {
    console.log("RouterGuard: Usuario autenticado intentando acceder a ruta pública. Redirigiendo a feed.");
    return next({ name: 'Feed' });
  }

  // Si no se cumple ninguna de las condiciones anteriores, permite la navegación
  next();
});

export default router;