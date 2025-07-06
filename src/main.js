// src/main.js
import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router'; // Si usas Vue Router
import { supabase } from '@/services/supabase'; // Tu archivo de configuración de Supabase
import { useAuthStore } from '@/modules/auth/stores/auth'; // Tu store de autenticación
// Asegúrate de que tu CSS de Tailwind se importa en algún lugar
import './assets/css/global.css'; // Añadido
import './assets/tailwind.css'; // La ruta correcta si el archivo está en src/assets/

const app = createApp(App);
const pinia = createPinia();

app.use(pinia);
app.use(router);

// *** LÓGICA CLAVE AQUÍ ***
// Escuchar cambios en el estado de autenticación de Supabase
supabase.auth.onAuthStateChange((event, session) => {
  const authStore = useAuthStore(); // Obtener la instancia del store

  if (session) {
    // Si hay una sesión, establecer el usuario en el store
    console.log('Auth state changed: LOGGED_IN', session.user);
    authStore.setUser(session.user); // Llama a la acción setUser que creamos
  } else {
    // Si no hay sesión (logout o no autenticado), limpiar el usuario
    console.log('Auth state changed: LOGGED_OUT');
    authStore.setUser(null);
  }
});

// Opcional: Cargar el usuario inicial si ya hay una sesión al cargar la app
// Esto es útil si el listener no se dispara inmediatamente al cargar
async function initializeAuth() {
  const { data: { user } } = await supabase.auth.getUser();
  const authStore = useAuthStore();
  if (user) {
    authStore.setUser(user);
  } else {
    authStore.setUser(null);
  }
}
initializeAuth().then(() => {
    app.mount('#app');
});

// app.mount('#app'); // Mueve esta línea dentro del .then() de initializeAuth