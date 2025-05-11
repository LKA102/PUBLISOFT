<template>
  <v-menu offset-y transition="slide-y-transition">
    <template v-slot:activator="{ on, attrs }">
      <v-btn icon v-bind="attrs" v-on="on">
        <v-avatar size="36" color="white">
          <v-icon dark>mdi-account</v-icon>
        </v-avatar>
      </v-btn>
    </template>

    <v-card width="250">
      <v-list>
        <v-list-item>
          <v-list-item-avatar>
            <v-icon>mdi-account</v-icon>
          </v-list-item-avatar>
          <v-list-item-content>
            <v-list-item-title>{{ authStore.user.name }}</v-list-item-title>
            <v-list-item-subtitle>{{ authStore.user.email }}</v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-list>

      <v-divider></v-divider>

      <v-list dense>
        <v-list-item @click="handleAction('profile')">
          <v-list-item-icon>
            <v-icon>mdi-account</v-icon>
          </v-list-item-icon>
          <v-list-item-title>Mi Perfil</v-list-item-title>
        </v-list-item>

        <v-list-item @click="handleAction('logout')">
          <v-list-item-icon>
            <v-icon>mdi-logout</v-icon>
          </v-list-item-icon>
          <v-list-item-title>Cerrar Sesión</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-card>
  </v-menu>
</template>

<script setup>
import { useAuthStore } from '../store/authStore'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const handleAction = (action) => {
  if (action === 'logout') {
    authStore.logout()
    router.push('/login')
  } else {
    // Otras acciones como 'profile'
    console.log('Acción:', action)
  }
}
</script>