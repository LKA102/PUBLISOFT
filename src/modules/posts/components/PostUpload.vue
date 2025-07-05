<template>
  <div class="post-upload-container">
    <input
      type="text"
      placeholder="¿Qué apunte publicarás hoy?"
      class="upload-placeholder"
      @focus="openModal"
      readonly
    />

    <div v-if="isModalOpen" class="modal-overlay">
      <div class="post-upload-modal">
        <h3>Crear Nueva Publicación</h3>
        <form @submit.prevent="handleSubmit">
          <div class="form-group">
            <label for="post-title">Título:</label>
            <input type="text" id="post-title" v-model="post.title" required />
          </div>

          <div class="form-group">
            <label for="post-course">Curso:</label>
            <input type="text" id="post-course" v-model="post.course" required />
          </div>

          <div class="form-group">
            <label for="post-cycle">Ciclo:</label>
            <input type="text" id="post-cycle" v-model="post.cycle" placeholder="Ej: 2024-I" required />
          </div>

          <div class="form-group">
            <label for="post-file">Archivo (PDF, DOCX, PPT, JPG, PNG):</label>
            <input type="file" id="post-file" @change="handleFileChange" accept=".pdf,.doc,.docx,.ppt,.pptx,.jpg,.jpeg,.png,.gif" required />
            <p v-if="selectedFile" class="file-name">{{ selectedFile.name }}</p>
          </div>

          <div class="modal-actions">
            <button type="button" @click="closeModal" class="cancel-button">Cancelar</button>
            <button type="submit" :disabled="loading">
              <span v-if="loading">Subiendo...</span>
              <span v-else>Publicar</span>
            </button>
          </div>

          <p v-if="error" class="error-message">{{ error }}</p>
        </form>
        <button @click="closeModal" class="close-modal-button">&times;</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { usePostStore } from '@modules/posts/stores/post';
import { storeToRefs } from 'pinia';

const postStore = usePostStore();
const { loading, error } = storeToRefs(postStore);

const isModalOpen = ref(false); // Controla la visibilidad del modal
const post = ref({
  title: '',
  course: '',
  cycle: '',
});
const selectedFile = ref(null);

const openModal = () => {
  isModalOpen.value = true;
};

const closeModal = () => {
  isModalOpen.value = false;
  // Opcional: Limpiar el formulario al cerrar el modal
  post.value.title = '';
  post.value.course = '';
  post.value.cycle = '';
  selectedFile.value = null;
  const fileInput = document.getElementById('post-file');
  if (fileInput) fileInput.value = '';
};

const handleFileChange = (event) => {
  selectedFile.value = event.target.files.length > 0 ? event.target.files.item(0) : null;
};

const handleSubmit = async () => {
  if (!post.value.title || !post.value.course || !post.value.cycle) {
    alert('Por favor, completa todos los campos del formulario.');
    return;
  }
  if (!selectedFile.value) {
    alert('Por favor, selecciona un archivo para subir.');
    return;
  }

  await postStore.uploadPost(post.value, selectedFile.value);

  // Si no hubo error al subir, cerrar el modal
  if (!error.value) {
    closeModal();
  }
};
</script>

<style scoped>
.post-upload-container {
  margin-bottom: 20px;
}

/* Estilo para el input pequeño tipo Facebook */
.upload-placeholder {
  width: 100%;
  padding: 12px 15px;
  border: 1px solid #ddd;
  border-radius: 25px; /* Más redondeado */
  background-color: #f0f2f5; /* Fondo más claro */
  color: #65676b; /* Color de texto gris */
  font-size: 1em;
  cursor: pointer;
  box-sizing: border-box; /* Incluye padding y border en el ancho */
  transition: background-color 0.2s ease;
}

.upload-placeholder:hover {
  background-color: #e4e6eb; /* Ligeramente más oscuro al pasar el ratón */
}

.upload-placeholder:focus {
  outline: none;
  border-color: #1877f2; /* Borde azul al enfocar */
  box-shadow: 0 0 0 2px rgba(24, 119, 242, 0.2);
}

/* Estilos del modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6); /* Fondo oscuro semitransparente */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000; /* Asegura que esté por encima de todo */
}

.post-upload-modal {
  background-color: #ffffff;
  border-radius: 10px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
  padding: 25px;
  width: 90%;
  max-width: 550px; /* Ancho máximo del modal */
  position: relative;
  animation: fadeInScale 0.3s ease-out; /* Animación de entrada */
}

@keyframes fadeInScale {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

h3 {
  color: #333;
  margin-bottom: 20px;
  text-align: center;
  font-size: 1.5em;
}

.form-group {
  margin-bottom: 18px;
}

label {
  display: block;
  margin-bottom: 6px;
  font-weight: bold;
  color: #555;
  font-size: 0.9em;
}

input[type="text"],
input[type="file"] {
  width: calc(100% - 22px); /* Ajuste para padding y border */
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 6px;
  box-sizing: border-box;
  font-size: 1em;
}

input[type="file"] {
  padding: 0; /* Resetear padding para el input file */
}

input[type="file"]::file-selector-button {
  padding: 10px 15px;
  background-color: #e7f3ff; /* Azul claro de Facebook */
  color: #1877f2;
  border: 1px solid #cce5ff;
  border-radius: 6px;
  cursor: pointer;
  margin-right: 10px;
  transition: background-color 0.2s ease;
}

input[type="file"]::file-selector-button:hover {
  background-color: #d0e7ff;
}

.file-name {
  margin-top: 8px;
  font-size: 0.85em;
  color: #666;
  font-style: italic;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 25px;
}

button {
  padding: 10px 22px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1em;
  font-weight: bold;
  transition: background-color 0.2s ease, opacity 0.2s ease;
}

button:disabled {
  background-color: #a0c3ec;
  cursor: not-allowed;
  opacity: 0.7;
}

button:not(:disabled) {
  background-color: #1877f2; /* Azul principal */
  color: white;
}

button.cancel-button {
  background-color: #e4e6eb; /* Gris claro */
  color: #4b4f56;
}

button.cancel-button:hover {
  background-color: #d8dadf;
}

button:not(.cancel-button):hover:not(:disabled) {
  background-color: #166fe5; /* Azul más oscuro al pasar el ratón */
}

.error-message {
  color: #e53e3e;
  margin-top: 15px;
  font-size: 0.9em;
  text-align: center;
  background-color: #ffebeb;
  border: 1px solid #e53e3e;
  padding: 8px;
  border-radius: 5px;
}

.close-modal-button {
  position: absolute;
  top: 15px;
  right: 15px;
  background: none;
  border: none;
  font-size: 24px;
  line-height: 1;
  cursor: pointer;
  color: #777;
  padding: 5px;
  border-radius: 50%;
  transition: background-color 0.2s ease;
}

.close-modal-button:hover {
  background-color: #f0f2f5;
  color: #333;
}
</style>