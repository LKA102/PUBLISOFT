<template>
  <v-card class="mb-4 pa-3">
    <v-card-title>{{ publicacion.titulo }}</v-card-title>
    <v-card-subtitle>{{ publicacion.usuario }} - {{ fecha }}</v-card-subtitle>
    <v-btn color="error" small @click="$emit('eliminar', publicacion.id)">Eliminar</v-btn>
    <v-img v-if="esImagen" :src="publicacion.archivoUrl" height="200" class="my-2"/>
    <v-icon v-else class="my-2">mdi-file-document</v-icon>
    <RatingStars :valor="publicacion.rating" @rate="val => $emit('calificar', publicacion.id, val)" />
    <p class="mt-2">Promedio: {{ publicacion.rating.toFixed(2) }} ⭐ ({{ publicacion.votos }} votos)</p>
  </v-card>
</template>

<script setup>
import RatingStars from './RatingStars.vue';
import { computed } from 'vue';

const props = defineProps(['publicacion']);
const fecha = computed(() => new Date(props.publicacion.fecha).toLocaleDateString());
const esImagen = computed(() => props.publicacion.archivoUrl?.startsWith('blob:'));
</script>
