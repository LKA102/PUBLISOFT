<template>
  <v-card class="mb-6" elevation="2">
    <!-- Encabezado -->
    <v-card-title class="d-flex justify-space-between align-center">
      <div>
        <span class="font-weight-bold">{{ publicacion.usuario }}</span>
        <span class="text-caption ml-2 text-grey">{{ fecha }}</span>
      </div>
      <v-btn icon small @click="$emit('eliminar', publicacion.id)">
        <v-icon color="grey">mdi-delete</v-icon>
      </v-btn>
    </v-card-title>

    <v-card-subtitle>{{ publicacion.titulo }}</v-card-subtitle>

    <!-- Previsualización del documento -->
    <div class="px-4 pb-2">
      <v-card outlined class="mb-3">
        <div class="d-flex align-center pa-3">
          <v-icon x-large color="blue" class="mr-3">mdi-file-document</v-icon>
          <div>
            <div class="font-weight-bold">Documento compartido</div>
            <div class="text-caption">Tipo: {{ tipoArchivo }}</div>
          </div>
          <v-spacer></v-spacer>
          <v-btn 
            color="primary" 
            small 
            :href="publicacion.archivoUrl" 
            download
            target="_blank"
          >
            <v-icon left>mdi-download</v-icon>
            Descargar
          </v-btn>
        </div>
        
        <!-- Previsualización para imágenes -->
        <v-img
          v-if="esImagen"
          :src="publicacion.archivoUrl"
          max-height="400"
          contain
          class="mx-auto"
        ></v-img>
        
        <!-- Previsualización para PDF (usando iframe) -->
        <iframe
          v-else-if="esPDF"
          :src="publicacion.archivoUrl"
          width="100%"
          height="500"
          frameborder="0"
          class="pdf-preview"
        ></iframe>
      </v-card>
    </div>

    <!-- Rating y acciones -->
    <v-card-actions class="d-flex justify-space-between px-4 pb-4">
      <div>
        <RatingStars :valor="publicacion.rating" @rate="val => $emit('calificar', publicacion.id, val)" />
        <span class="text-caption ml-2">{{ publicacion.rating.toFixed(1) }} ⭐ ({{ publicacion.votos }} votos)</span>
      </div>
    </v-card-actions>
  </v-card>
</template>

<script setup>
import RatingStars from './RatingStars.vue';
import { computed } from 'vue';

const props = defineProps(['publicacion']);
const emit = defineEmits(['eliminar', 'calificar']);

const fecha = computed(() => new Date(props.publicacion.fecha).toLocaleString());
const esImagen = computed(() => props.publicacion.archivoUrl?.startsWith('blob:') && 
  props.publicacion.archivoUrl?.match(/\.(jpeg|jpg|gif|png)$/i));
const esPDF = computed(() => props.publicacion.archivoUrl?.match(/\.pdf$/i));
const tipoArchivo = computed(() => {
  if (esImagen.value) return 'Imagen';
  if (esPDF.value) return 'PDF';
  return 'Documento';
});
</script>

<style scoped>
.v-card {
  width: 100%;
  border-radius: 8px;
}

.pdf-preview {
  border: none;
  margin-top: 8px;
}

.v-card__actions {
  border-top: 1px solid rgba(0, 0, 0, 0.12);
}
</style>