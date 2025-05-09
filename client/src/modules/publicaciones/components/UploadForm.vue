<template>
  <v-card class="pa-4 mb-4">
    <v-form @submit.prevent="handleUpload">
      <v-text-field v-model="titulo" label="Título" required></v-text-field>
      <v-file-input v-model="archivo" label="Selecciona archivo" required></v-file-input>
      <v-btn type="submit" color="primary">Subir</v-btn>
    </v-form>
  </v-card>
</template>

<script setup>
import { ref } from 'vue';
import { usePublicaciones } from '../store/publicacionesStore';

const titulo = ref('');
const archivo = ref(null);
const { subir } = usePublicaciones();

const handleUpload = async () => {
  if (!titulo.value || !archivo.value) return;
  await subir({ titulo: titulo.value, archivo: archivo.value, usuario: 'anónimo' });
  titulo.value = '';
  archivo.value = null;
};
</script>
