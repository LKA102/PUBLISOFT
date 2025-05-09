<template>
  <v-container>
    <UploadForm />
    <PublicationCard
      v-for="pub in state.publicaciones"
      :key="pub.id"
      :publicacion="pub"
      @eliminar="eliminar"
      @calificar="calificar"
    />
  </v-container>
</template>

<script setup>
import UploadForm from '../components/UploadForm.vue';
import PublicationCard from '../components/PublicationCard.vue';
import { usePublicaciones } from '../store/publicacionesStore';

const { state, cargar, eliminar, calificar } = usePublicaciones();
cargar();
</script>
