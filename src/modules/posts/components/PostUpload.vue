<template>
  <div class="post-upload-container">
    <div class="upload-input-wrapper">
      <img
        :src="authStore.user?.avatar_url || 'https://via.placeholder.com/40/CCCCCC/FFFFFF?text=AV'"
        alt="Avatar del usuario"
        class="user-avatar"
      />
      <input
        type="text"
        placeholder="¿Qué apunte publicarás hoy?"
        class="upload-placeholder"
        @focus="openModal"
        readonly
      />
    </div>

    <div v-if="isModalOpen" class="modal-overlay">
      <div class="post-upload-modal">
        <h3>Crear Nueva Publicación</h3>
        <form @submit.prevent="handleSubmit">
          <div class="form-group">
            <label for="post-title">Título:</label>
            <input type="text" id="post-title" v-model="post.title" required />
          </div>

          <div class="form-group">
            <label for="post-cycle">Ciclo:</label>
            <select id="post-cycle" v-model="selectedCycle" @change="fetchCoursesForCycle" required>
              <option value="" disabled>Selecciona un ciclo</option>
              <option v-for="cycle in uniqueCycles" :key="cycle" :value="cycle">{{ cycle }}</option>
            </select>
          </div>

          <div class="form-group">
            <label for="post-course">Curso:</label>
            <select id="post-course" v-model="post.course" :disabled="!selectedCycle || loadingCourses" required>
              <option value="" disabled>Selecciona un curso</option>
              <option v-if="loadingCourses">Cargando cursos...</option>
              <option v-for="course in filteredCourses" :key="course.course_code" :value="course.course_name">
                {{ course.course_code }} - {{ course.course_name }}
              </option>
            </select>
            <p v-if="!selectedCycle" class="hint-message">Selecciona un ciclo primero para ver los cursos.</p>
            <p v-if="selectedCycle && filteredCourses.length === 0 && !loadingCourses" class="hint-message">No se encontraron cursos para este ciclo.</p>
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
import { ref, onMounted, watch } from 'vue';
import { usePostStore } from '@modules/posts/stores/post';
import { useAuthStore } from '@modules/auth/stores/auth'; // Importa el authStore
import { storeToRefs } from 'pinia';
import { supabase } from '@/services/supabase';

// Agrega el authStore a las dependencias
const authStore = useAuthStore();

const postStore = usePostStore();
const { loading, error } = storeToRefs(postStore);

const isModalOpen = ref(false);
const post = ref({
  title: '',
  course: '',
  cycle: '', // Ahora el ciclo se manejará a través de selectedCycle y se asignará aquí al submit
});
const selectedFile = ref(null);

// Nuevos estados para ciclos y cursos
const allCoursesData = ref([]); // Almacenará todos los cursos de Supabase
const uniqueCycles = ref([]); // Almacenará los nombres de los ciclos únicos
const selectedCycle = ref(''); // El ciclo seleccionado por el usuario
const filteredCourses = ref([]); // Cursos filtrados por el ciclo seleccionado
const loadingCourses = ref(false); // Estado de carga para los cursos

// --- Funciones para manejar Ciclos y Cursos ---

// Función para obtener todos los cursos de Supabase y poblar los ciclos únicos
const fetchAllCourses = async () => {
  loadingCourses.value = true;
  try {
    const { data, error } = await supabase
      .from('courses_by_cycle') // Nombre de tu tabla en Supabase
      .select('cycle_name, course_code, course_name')
      .order('cycle_name', { ascending: true })
      .order('course_code', { ascending: true }); // Ordena para mejor visualización

    if (error) throw error;
    allCoursesData.value = data;

    // Extraer ciclos únicos
    const cycles = [...new Set(data.map(item => item.cycle_name))];
    uniqueCycles.value = cycles;

  } catch (err) {
    console.error('Error al cargar ciclos y cursos:', err.message);
    // Podrías mostrar un mensaje de error en la UI si lo deseas
  } finally {
    loadingCourses.value = false;
  }
};

// Función para filtrar cursos cuando se selecciona un ciclo
const fetchCoursesForCycle = () => {
  post.value.course = ''; // Resetear el curso seleccionado al cambiar de ciclo
  if (selectedCycle.value) {
    filteredCourses.value = allCoursesData.value.filter(course =>
      course.cycle_name === selectedCycle.value
    );
  } else {
    filteredCourses.value = [];
  }
};

// --- Watcher para actualizar post.cycle cuando selectedCycle cambia ---
watch(selectedCycle, (newCycle) => {
  post.value.cycle = newCycle;
});

// --- Funciones del Modal ---
const openModal = async () => {
  isModalOpen.value = true;
  // Asegúrate de cargar los cursos solo una vez o cuando sea necesario
  if (uniqueCycles.value.length === 0) {
    await fetchAllCourses();
  }
  // Resetear la selección al abrir el modal
  selectedCycle.value = '';
  post.value.course = '';
  filteredCourses.value = [];
};

const closeModal = () => {
  isModalOpen.value = false;
  post.value.title = '';
  post.value.course = '';
  post.value.cycle = '';
  selectedFile.value = null;
  const fileInput = document.getElementById('post-file');
  if (fileInput) fileInput.value = '';
  
  // Resetear estados de selección de ciclo y curso
  selectedCycle.value = '';
  filteredCourses.value = [];
};

const handleFileChange = (event) => {
  selectedFile.value = event.target.files.length > 0 ? event.target.files.item(0) : null;
};

const handleSubmit = async () => {
  // Validaciones actualizadas
  if (!post.value.title || !post.value.course || !selectedCycle.value) { // Ahora validamos selectedCycle en lugar de post.cycle directamente
    alert('Por favor, completa todos los campos del formulario (Título, Ciclo y Curso).');
    return;
  }
  if (!selectedFile.value) {
    alert('Por favor, selecciona un archivo para subir.');
    return;
  }

  // Asignar el ciclo final al objeto post antes de subir
  post.value.cycle = selectedCycle.value;

  await postStore.uploadPost(post.value, selectedFile.value);

  if (!error.value) {
    closeModal();
  }
};

// --- Ciclo de Vida ---
onMounted(() => {
  // Opcional: Cargar los ciclos y cursos al montar el componente si el modal no es el único disparador
  // Aunque ya lo hacemos al abrir el modal, si este componente pudiera ser usado sin abrir el modal
  // y necesitara los datos, aquí sería un buen lugar. Por ahora, openModal es suficiente.
});
</script>
<style scoped>
.post-upload-container {
  margin-bottom: 20px;
}

.upload-input-wrapper {
  display: flex;
  align-items: center;
  gap: 10px;
  background-color:#fff;
  border-radius: 25px;
  padding: 8px 15px;
  transition: background-color 0.2s ease;
}

.upload-input-wrapper:hover {
  background-color: #e4e6eb;
}

.upload-input-wrapper img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #fff;
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
  /* Estilos para el input de "placeholder" */


.upload-placeholder {
  width: 100%;
  padding: 12px 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1em;
  color: #555;
  cursor: pointer;
  background-color: #f9f9f9;
  text-align: left;
}

.upload-placeholder:hover {
  background-color: #f0f0f0;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.post-upload-modal {
  background-color: #fff;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
  width: 90%;
  max-width: 500px;
  position: relative;
}

.post-upload-modal h3 {
  margin-top: 0;
  margin-bottom: 25px;
  color: #333;
  text-align: center;
  font-size: 1.8em;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #555;
}

.form-group input[type="text"],
.form-group input[type="file"],
.form-group select { /* Aplicar estilos a select también */
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 1em;
  box-sizing: border-box;
}

.form-group select:disabled {
  background-color: #e9e9e9;
  cursor: not-allowed;
}

.file-name {
  margin-top: 5px;
  font-size: 0.9em;
  color: #666;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 30px;
}

.cancel-button {
  background-color: #6c757d;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1em;
  transition: background-color 0.2s ease;
}

.cancel-button:hover {
  background-color: #5a6268;
}

.modal-actions button[type="submit"] {
  background-color: #28a745;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1em;
  transition: background-color 0.2s ease;
}

.modal-actions button[type="submit"]:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.modal-actions button[type="submit"]:hover:not(:disabled) {
  background-color: #218838;
}

.error-message {
  color: #dc3545;
  text-align: center;
  margin-top: 15px;
  font-size: 0.9em;
}

.close-modal-button {
  position: absolute;
  top: 15px;
  right: 15px;
  background: none;
  border: none;
  font-size: 1.8em;
  color: #999;
  cursor: pointer;
  transition: color 0.2s ease;
}

.close-modal-button:hover {
  color: #333;
}

/* Nuevos estilos para los mensajes de ayuda en los selects */
.hint-message {
  font-size: 0.85em;
  color: #888;
  margin-top: 5px;
}
</style>