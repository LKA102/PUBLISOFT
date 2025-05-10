// Plugins
import { registerPlugins } from '@/plugins'
// Removed unused registerPlugins import

import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'

function initApp() {

  const app = createApp(App)

  app.use(createPinia())

  registerPlugins(app);

  app.mount('#app')

  // Opcional: Limpiar localStorage en desarrollo al iniciar
if (import.meta.env.MODE === 'development') {
  localStorage.clear()
}

}

initApp();
