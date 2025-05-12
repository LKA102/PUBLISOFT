<template>
  <div>
    <v-file-input
      v-model="archivo"
      label="Selecciona tus apuntes (PDF, Word, imágenes)"
      prepend-icon="mdi-paperclip"
      outlined
      dense
      :rules="fileRules"
      accept=".pdf,.doc,.docx,.jpg,.jpeg,.png"
      @change="handleFileChange"
    ></v-file-input>

    <v-text-field
      v-model="titulo"
      label="Título (opcional)"
      outlined
      dense
      class="mb-3"
    ></v-text-field>

    <!-- Previsualización -->
    <v-card v-if="previewUrl" outlined class="mb-3">
      <v-img v-if="esImagen" :src="previewUrl" max-height="200" contain></v-img>
      <div v-else class="d-flex align-center pa-3">
        <v-icon x-large color="blue" class="mr-3">mdi-file-document</v-icon>
        <div>
          <div class="font-weight-bold">{{ archivo?.name }}</div>
          <div class="text-caption">Se convertirá a PDF</div>
        </div>
      </div>
    </v-card>

    <v-btn
      color="primary"
      block
      :disabled="!archivo"
      :loading="loading"
      @click="handleUpload"
    >
      Compartir apuntes
    </v-btn>

    <v-alert v-if="error" type="error" dense class="mt-3">
      {{ error }}
    </v-alert>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { usePublicaciones } from '../store/publicacionesStore';

const titulo = ref('');
const archivo = ref(null);
const previewUrl = ref(null);
const error = ref('');
const loading = ref(false);
const { subir } = usePublicaciones();

const esImagen = computed(() => {
  return archivo.value?.type.startsWith('image/');
});

const fileRules = [
  value => !value || 
    value.type === 'application/pdf' || 
    value.type === 'application/msword' ||
    value.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' ||
    value.type === 'image/jpeg' || 
    value.type === 'image/png' || 
    'Solo se permiten archivos PDF, Word o imágenes'
];

// DESPUÉS (Green Software)
const handleFileChange = async (file) => {
  if (!file) return;
  
  // Optimización para imágenes
  if (file.type.startsWith('image/')) {
    try {
      const optimizedImage = await compressImage(file);
      previewUrl.value = URL.createObjectURL(optimizedImage);
    } catch {
      previewUrl.value = URL.createObjectURL(file);
    }
  }
};

// Helper para compresión
async function compressImage(file, maxWidth = 800, quality = 0.7) {
  return new Promise((resolve) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      const img = new Image();
      img.src = e.target.result;
      img.onload = () => {
        const canvas = document.createElement('canvas');
        const scale = Math.min(maxWidth / img.width, 1);
        canvas.width = img.width * scale;
        canvas.height = img.height * scale;
        
        const ctx = canvas.getContext('2d');
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
        
        canvas.toBlob(
          (blob) => resolve(blob || file),
          'image/webp',
          quality
        );
      };
    };
    reader.readAsDataURL(file);
  });
}


const handleUpload = async () => {
  if (!archivo.value) return;
  
  loading.value = true;
  error.value = '';
  
  try {
    await subir({
      titulo: titulo.value,
      archivo: archivo.value,
      usuario: 'Usuario Demo'
    });
    
    titulo.value = '';
    archivo.value = null;
    previewUrl.value = null;
  } catch (err) {
    error.value = 'Error al subir el archivo: ' + err.message;
  } finally {
    loading.value = false;
  }
};
</script>