<template>
  <v-app style="min-height: 100vh;">
    <!-- Barra superior -->
    <v-app-bar color="#1976D2" dark fixed app>
      <v-toolbar-title class="font-weight-bold">ApuntesCompartidos</v-toolbar-title>
    </v-app-bar>

    <v-main style="padding-top: 64px;">
      <v-container fluid class="pa-4" style="max-width: 800px; margin: 0 auto;">
        <!-- Área de publicación -->
        <v-card class="mb-6" elevation="2">
          <v-card-text class="text-center py-4">
            <p class="text-h6 mb-4">¿Tienes apuntes que quieras compartir?</p>
            <UploadForm @upload-complete="handleUploadComplete" />
          </v-card-text>
        </v-card>

        <!-- Estado cuando no hay publicaciones -->
        <v-card v-if="state.publicaciones.length === 0" class="mb-6" elevation="2">
          <v-card-text class="text-center py-8">
            <v-icon size="64" color="grey lighten-1">mdi-cloud-upload</v-icon>
            <h3 class="my-4">Aún no hay apuntes compartidos</h3>
            <p class="text-caption grey--text">Sé el primero en compartir tus apuntes</p>
          </v-card-text>
        </v-card>

        <!-- Lista de publicaciones (solo aparece cuando hay contenido) -->
        <template v-else>
          <PublicationCard
            v-for="pub in state.publicaciones"
            :key="pub.id"
            :publicacion="pub"
          />
        </template>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { usePublicaciones } from '../store/publicacionesStore'
import UploadForm from '../components/UploadForm.vue'
import PublicationCard from '../components/PublicationCard.vue'

const { state, cargar } = usePublicaciones()
cargar() // Carga las publicaciones al iniciar

const handleUploadComplete = () => {
  cargar() // Actualiza la lista después de subir
}
</script>