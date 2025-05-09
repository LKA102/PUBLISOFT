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
      
      <!-- Menú de perfil FUNCIONAL -->
      <v-menu offset-y transition="slide-y-transition" :close-on-content-click="false">
        <template v-slot:activator="{ on, attrs }">
          <v-btn icon v-bind="attrs" v-on="on" data-testid="profile-menu-btn">
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
                <v-list-item-title>Usuario Demo</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list>
          
          <v-divider></v-divider>
          
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
      <v-container fluid class="pa-4" style="max-width: 800px; width: 100%; margin: 0 auto;">
        <!-- Área de publicación -->
        <v-card class="mb-6" elevation="2">
          <v-card-text class="text-center py-4">
            <p class="text-h6 mb-4">¿Tienes apuntes que quieras compartir?</p>
            <UploadForm />
          </v-card-text>
        </v-card>

        <!-- Lista de publicaciones -->
        <v-row>
          <v-col cols="12">
            <PublicationCard
              v-for="pub in state.publicaciones"
              :key="pub.id"
              :publicacion="pub"
              @eliminar="eliminar"
              @calificar="calificar"
            />
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref } from 'vue';
import UploadForm from '../components/UploadForm.vue';
import PublicationCard from '../components/PublicationCard.vue';
import { usePublicaciones } from '../store/publicacionesStore';

const { state, cargar, eliminar, calificar } = usePublicaciones();
cargar();

const menuAction = (action) => {
  console.log(`Menú seleccionado: ${action}`);
  // Aquí puedes agregar lógica para cada acción
};
</script>

<style scoped>
.v-main {
  background-color: #f5f5f5;
  min-height: calc(100vh - 64px);
}

.v-container {
  padding: 0 16px;
}

@media (min-width: 960px) {
  .v-container {
    padding: 0 24px;
  }
}
</style>