<template>
  <v-app style="min-height: 100vh;">
    <v-app-bar color="#1976D2" dark fixed app>
      <v-toolbar-title class="font-weight-bold">ApuntesCompartidos</v-toolbar-title>
    </v-app-bar>

    <v-main style="padding-top: 64px;">
      <v-container fluid class="pa-4" style="max-width: 500px; margin: 0 auto;">
        <v-card class="mb-6" elevation="2">
          <v-card-title class="text-center py-4">
            <span class="text-h5">Iniciar Sesión</span>
          </v-card-title>

          <v-card-text>
            <AuthForm 
              :is-login="true" 
              @submit="handleLogin"
              :initial-email="demoCredentials.email"
              :initial-password="demoCredentials.password"
            />
          </v-card-text>
        </v-card>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '../store/authStore'
import AuthForm from '../components/AuthForm.vue'
import { computed } from 'vue'
import { onMounted } from 'vue'


const authStore = useAuthStore()
const router = useRouter()

onMounted(() => {
  // Solo en desarrollo, fuerza logout al cargar la vista de login
  if (import.meta.env.MODE === 'development') {
    authStore.logout()
  } else {
    authStore.initialize() // En producción, carga el estado persistente
  }
})

// Credenciales demo solo en desarrollo
const demoCredentials = computed(() => {
  return import.meta.env.MODE === 'development' 
    ? { email: 'demo@example.com', password: 'demo123' }
    : { email: '', password: '' }
})

const handleLogin = async (formData) => {
  const success = await authStore.login(formData.email, formData.password)
  if (success) {
    router.push('/publicaciones')
  }
}
</script>