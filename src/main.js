import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router';
import { supabase } from '@/services/supabase';
import { useAuthStore } from '@/stores/auth';

// Importar CSS
import './assets/css/global.css'; // Añadido
import './assets/tailwind.css'; // Existente

const app = createApp(App);
const pinia = createPinia();

app.use(pinia);
app.use(router);

// Lógica de autenticación (se mantiene igual)
supabase.auth.onAuthStateChange((event, session) => {
  const authStore = useAuthStore();
  if (session) {
    authStore.setUser(session.user);
  } else {
    authStore.setUser(null);
  }
});

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