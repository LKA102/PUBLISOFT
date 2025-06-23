// Plugins
import { registerPlugins } from '@/plugins'
import axios from '@/axios'
// Removed unused registerPlugins import

import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'

async function initApp() {

  const app = createApp(App)

  app.use(createPinia())

  registerPlugins(app);

  app.mount('#app')

  // const response = await axios.post('/auth/login', { "email": "prueba@gmail.com", "password": "1234"})
  // console.log(response)

  // Opcional: Limpiar localStorage en desarrollo al iniciar
if (import.meta.env.MODE === 'development') {
  localStorage.clear()
}

}

initApp();
