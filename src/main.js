// src/main.js
import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router'; // Importa tu Vue Router
import { supabase } from '@/services/supabase'; // Tu archivo de configuración de Supabase
import { useAuthStore } from '@/modules/auth/stores/auth'; // Tu store de autenticación

// Importa tus archivos CSS principales
import './assets/css/global.css'; // Asegúrate de que esta ruta es correcta
import './assets/tailwind.css'; // Asegúrate de que esta ruta es correcta
// Si tienes otros archivos CSS, impórtalos aquí:
// import './assets/styles/global.css'; 
// import './assets/styles/variables.css'; 
// import './assets/styles/forms.css'; 
// import './assets/styles/buttons.css'; 
// import '@fortawesome/fontawesome-free/css/all.css'; // Para los iconos de Font Awesome si los usas

async function initializeAndMountApp() {
  const app = createApp(App);
  const pinia = createPinia();

  app.use(pinia); // Primero, usa Pinia para que los stores estén disponibles

  const authStore = useAuthStore(); // Obtener la instancia del authStore
  
  // *** CRUCIAL: Inicializar el estado de autenticación ANTES de montar el router ***
  console.log('main.js: Iniciando inicialización de autenticación...');
  await authStore.initializeAuth(); 
  console.log('main.js: Autenticación inicializada. User:', authStore.user);

  // *** Escuchar cambios de autenticación en tiempo real después de la inicialización ***
  // Esto es para reaccionar a login/logout/refresh de token mientras la app está corriendo
  supabase.auth.onAuthStateChange(async (event, session) => {
    console.log('main.js: onAuthStateChange - Event:', event, 'Session:', session);
    // Usa la acción setUser del store para actualizar el estado, que a su vez cargará el perfil
    await authStore.setUser(session ? session.user : null); 
  });

  app.use(router); // Ahora, usa el router, el cual ya tendrá el estado de autenticación inicial listo

  app.mount('#app'); // Monta la aplicación en el DOM
  console.log('main.js: Aplicación Vue montada.');
}

// Llama a la función de inicialización asíncrona
initializeAndMountApp();