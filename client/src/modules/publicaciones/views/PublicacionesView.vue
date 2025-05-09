<template>
  <v-app style="min-height: 100vh;">
    <!-- Barra superior -->
    <v-app-bar color="#1976D2" dark fixed app>
      <v-toolbar-title class="font-weight-bold">ApuntesCompartidos</v-toolbar-title>
      
      <v-spacer></v-spacer>
      
      <div class="mr-4 d-none d-sm-flex">
        <span class="mr-2">Bienvenido,</span>
        <span class="font-weight-bold">Usuario Demo</span>
      </div>
      
      <v-menu offset-y transition="slide-y-transition">
        <template v-slot:activator="{ on, attrs }">
          <v-btn icon v-bind="attrs" v-on="on">
            <v-avatar size="36" color="white">
              <v-icon dark>mdi-account</v-icon>
            </v-avatar>
          </v-btn>
        </template>
        
        <v-card width="250">
          <v-list dense>
            <v-list-item @click="menuAction('profile')">
              <v-list-item-icon>
                <v-icon>mdi-account</v-icon>
              </v-list-item-icon>
              <v-list-item-title>Mi Perfil</v-list-item-title>
            </v-list-item>
            
            <v-list-item @click="menuAction('settings')">
              <v-list-item-icon>
                <v-icon>mdi-cog</v-icon>
              </v-list-item-icon>
              <v-list-item-title>Configuración</v-list-item-title>
            </v-list-item>
            
            <v-divider></v-divider>
            
            <v-list-item @click="menuAction('logout')">
              <v-list-item-icon>
                <v-icon>mdi-logout</v-icon>
              </v-list-item-icon>
              <v-list-item-title>Cerrar Sesión</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-card>
      </v-menu>
    </v-app-bar>

    <v-main style="padding-top: 64px;">
      <v-container fluid class="pa-4" style="max-width: 800px; margin: 0 auto;">
        <!-- Área de publicación con skeleton loader -->
        <v-card class="mb-6" elevation="2" :loading="loading">
          <v-card-text class="text-center py-4">
            <p class="text-h6 mb-4">¿Tienes apuntes que quieras compartir?</p>
            <UploadForm @upload-complete="handleUploadComplete" />
          </v-card-text>
        </v-card>

        <!-- Lista de publicaciones con skeleton loader -->
        <template v-if="state.publicaciones.length > 0">
          <PublicationCard
            v-for="pub in state.publicaciones"
            :key="pub.id"
            :publicacion="pub"
            @eliminar="handleEliminar"
            @calificar="handleCalificar"
          />
        </template>
        <template v-else>
          <v-card v-for="n in 3" :key="`skeleton-${n}`" class="mb-4">
            <v-skeleton-loader type="card"></v-skeleton-loader>
          </v-card>
        </template>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import UploadForm from '../components/UploadForm.vue';
import PublicationCard from '../components/PublicationCard.vue';
import { usePublicaciones } from '../store/publicacionesStore';

const { state, cargar, eliminar, calificar } = usePublicaciones();
const loading = ref(false);

onMounted(async () => {
  loading.value = true;
  try {
    await cargar();
  } catch (error) {
    console.error('Error cargando publicaciones:', error);
  } finally {
    loading.value = false;
  }
});

const menuAction = (action) => {
  console.log(`Menú seleccionado: ${action}`);
};

const handleUploadComplete = async () => {
  loading.value = true;
  try {
    await cargar();
  } finally {
    loading.value = false;
  }
};

const handleEliminar = async (id) => {
  loading.value = true;
  try {
    await eliminar(id);
    await cargar();
  } finally {
    loading.value = false;
  }
};

const handleCalificar = async (id, estrellas) => {
  try {
    await calificar(id, estrellas);
  } catch (error) {
    console.error('Error calificando:', error);
  }
};
</script>

<style scoped>
.v-main {
  background-color: #f5f5f5;
  min-height: calc(100vh - 64px);
}

/* Transición suave para las cards */
.v-card {
  transition: opacity 0.3s ease;
}
</style>