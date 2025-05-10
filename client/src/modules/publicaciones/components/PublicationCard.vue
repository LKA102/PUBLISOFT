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

    <!-- Vista previa del documento -->
    <div class="px-4 pb-2">
      <v-card outlined class="mb-3 preview-card" @click="showFullDocument = true">
        <div class="d-flex align-center pa-3">
          <v-icon x-large color="blue" class="mr-3">mdi-file-pdf-box</v-icon>
          <div>
            <div class="font-weight-bold">{{ publicacion.nombreOriginal }}</div>
            <div class="text-caption">Convertido a PDF</div>
          </div>
          <v-spacer></v-spacer>
          <v-btn 
            color="primary" 
            small 
            :href="publicacion.archivoUrl" 
            download
            target="_blank"
            @click.stop
          >
            <v-icon left>mdi-download</v-icon>
            Descargar
          </v-btn>
        </div>
        
        <!-- Miniaturas -->
        <v-img
          v-if="esImagen"
          :src="publicacion.previewUrl"
          height="150"
          contain
          class="mx-auto preview-image"
          loading="lazy"
        ></v-img>
        
        <!-- Previsualización para PDF -->
        <iframe
          v-else-if="esPDF"
          :src="publicacion.archivoUrl"
          width="100%"
          height="150"
          frameborder="0"
          class="pdf-preview"
          loading="lazy"
        ></iframe>
      </v-card>
    </div>

    <!-- Diálogo para vista completa -->
    <v-dialog v-model="showFullDocument" max-width="800">
      <v-card>
        <v-card-title class="d-flex justify-space-between">
          <span>{{ publicacion.titulo }}</span>
          <v-btn icon @click="showFullDocument = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>
        <v-card-text>
          <iframe
            :src="publicacion.archivoUrl"
            width="100%"
            height="500"
            frameborder="0"
          ></iframe>
        </v-card-text>
      </v-card>
    </v-dialog>

    <!-- Rating -->
    <v-card-actions class="d-flex justify-space-between px-4 pb-4">
      <div>
        <RatingStars :valor="publicacion.rating" @rate="val => $emit('calificar', publicacion.id, val)" />
        <span class="text-caption ml-2">{{ publicacion.rating.toFixed(1) }} ⭐ ({{ publicacion.votos }} votos)</span>
      </div>
    </v-card-actions>
  </v-card>
</template>

<script setup>
import { ref, computed } from 'vue'; // Añadido computed
import RatingStars from './RatingStars.vue';

const props = defineProps(['publicacion']);
const emit = defineEmits(['eliminar', 'calificar']);
const showFullDocument = ref(false);

const fecha = computed(() => new Date(props.publicacion.fecha).toLocaleString());

const esImagen = computed(() => {
  if (!props.publicacion.archivoUrl) return false;
  return props.publicacion.archivoUrl.startsWith('blob:image/') || 
         ['jpg', 'jpeg', 'png', 'webp'].some(ext => 
           props.publicacion.archivoUrl.includes(ext)
         );
});

const esPDF = computed(() => props.publicacion.archivoUrl?.match(/\.pdf$/i));

// Eliminado tipoArchivo ya que no se usa
</script>

<style scoped>
.preview-card {
  cursor: pointer;
  transition: all 0.3s ease;
}

.preview-card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.preview-image {
  border-top: 1px solid #eee;
  background-color: #f5f5f5;
}

.pdf-preview {
  border: none;
  margin-top: 8px;
}
</style>