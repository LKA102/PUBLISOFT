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
      },
      {
      path: '/rate-mandatory', // ¡NUEVA RUTA para la valoración obligatoria!
      name: 'RateMandatory',
      // IMPORTANTE: Asegúrate que esta ruta al componente es la correcta en tu proyecto.
      // Si RateMandatoryPage.vue está en `src/components`, úsala. Si está en `src/views`, úsala.
      component: () => import('@/components/RateMandatoryPage.vue'), 
      meta: { requiresAuth: true, requiresStudentRating: true } // Marca esta ruta como requerimiento de estudiante
    },
    // Captura cualquier ruta no definida y redirige a Home
    { path: '/:pathMatch(.*)*', redirect: '/' } 
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

  // Paso 1: Si el store está en estado de carga inicial, espera a que se resuelva.
  // Esto asegura que `isAuthenticated`, `user.role` y `needsRating` sean precisos.
  if (authStore.isAuthLoading) {
    console.log(`RouterGuard: Esperando que authStore.isAuthLoading se resuelva para ${to.fullPath}...`);
    await new Promise(resolve => {
        const unsubscribe = authStore.$subscribe((mutation, state) => {
            if (!state.loading) { // Cuando el 'loading' global del store es false
                unsubscribe(); // Deja de observar una vez que el estado se resuelve
                resolve();
            }
        });
        // En caso de que el loading ya sea false cuando se ejecuta el beforeEeach
        // (por ejemplo, en navegaciones subsiguientes sin recarga completa)
        if (!authStore.isAuthLoading) {
            unsubscribe();
            resolve();
        }
    });
    console.log(`RouterGuard: authStore.isAuthLoading resuelto. Is Authenticated: ${authStore.isAuthenticated}, User Role: ${authStore.user?.role}, NeedsRating: ${authStore.needsRating}`);
  }

  // Obtener los estados relevantes después de asegurar que el store está cargado
  const isAuthenticated = authStore.isAuthenticated; 
  const isStudent = authStore.isStudent; // Usamos el getter `isStudent` del store
  const needsRating = authStore.needsRating; // Estado actualizado por `checkRatingRequirement`
  
  const requiresAuth = to.meta.requiresAuth;
  const isPublicRoute = to.meta.public; // Para rutas como login/register
  const requiredRole = to.meta.requiresRole; // Para roles específicos (ej. 'admin')
  const isRateMandatoryRoute = to.name === 'RateMandatory'; // Verifica si la ruta a la que va es la de rating

  // --- NUEVOS CONSOLE.LOG PARA DEPURACIÓN ESPECÍFICA ---
  console.log(`--- RouterGuard Depuración para ${to.fullPath} ---`);
  console.log(`  isAuthenticated: ${isAuthenticated}`);
  console.log(`  isStudent: ${isStudent}`);
  console.log(`  needsRating (del store): ${needsRating}`);
  console.log(`  requiresAuth (de la meta): ${requiresAuth}`);
  console.log(`  isPublicRoute (de la meta): ${isPublicRoute}`);
  console.log(`  isRateMandatoryRoute (nombre de la ruta actual): ${isRateMandatoryRoute}`);
  console.log(`  User Role (del store): ${authStore.user?.role}`);
  console.log(`-------------------------------------------`);

  // Lógica de Redirección ORDENADA POR PRIORIDAD:

  // 1. Si la ruta requiere autenticación y el usuario NO está autenticado
  if (requiresAuth && !isAuthenticated) {
    console.log("RouterGuard: Acceso no autorizado a ruta protegida. Redirigiendo a login.");
    return next({ name: 'Login', query: { redirect: to.fullPath } });
  } 
  
  // 2. Si el usuario ya está autenticado e intenta ir a una ruta pública (login/register)
  if (isPublicRoute && isAuthenticated) {
    console.log("RouterGuard: Usuario autenticado intentando acceder a ruta pública. Redirigiendo a feed.");
    return next({ name: 'Feed' });
  }

  // 3. Control de roles para rutas específicas (ej. /dashboard solo para admin)
  if (isAuthenticated && requiredRole && authStore.user?.role !== requiredRole) {
    console.warn(`RouterGuard: Acceso denegado. El rol del usuario "${authStore.user?.role}" no coincide con el rol requerido "${requiredRole}". Redirigiendo a Home.`);
    return next({ name: 'Home' }); 
  }

  // 4. Lógica de valoración obligatoria para estudiantes
  // Esto debe ir DESPUÉS de la autenticación y los roles generales
  if (isAuthenticated && isStudent) {
    console.log(`  Condición needsRating && !isRateMandatoryRoute: ${needsRating && !isRateMandatoryRoute}`);
    if (needsRating && !isRateMandatoryRoute) {
      // Si es estudiante, necesita valorar, y NO está en la página de valoración obligatoria
      console.log('RouterGuard: Estudiante necesita valorar un post. Redirigiendo a RateMandatory.');
      return next({ name: 'RateMandatory' });
    } else if (!needsRating && isRateMandatoryRoute) {
      // Si es estudiante, NO necesita valorar (ya cumplió), y está en la página de valoración obligatoria
      console.log('RouterGuard: Estudiante ya valoró. Redirigiendo fuera de RateMandatory.');
      return next({ name: 'Feed' }); // Redirige a la página principal del feed
    }
  }

  // Si ninguna de las condiciones anteriores redirige, permite el acceso a la ruta.
  console.log("RouterGuard: Permitido el acceso.");
  next();
});

export default router;