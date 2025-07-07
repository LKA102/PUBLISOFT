<template>
  <div class="post-upload-container">
    <div class="upload-input-wrapper">
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
            <label for="post-title">Título del Apunte:</label>
            <input type="text" id="post-title" v-model="post.title" placeholder="Ej: Resumen de Álgebra Lineal" required />
          </div>

          <div class="form-group">
            <label for="post-cycle">Ciclo:</label>
            <select id="post-cycle" v-model="selectedCycle" @change="fetchCoursesForCycle" required :disabled="loadingCourses">
              <option value="" disabled>Selecciona un ciclo</option>
              <option v-for="cycle in uniqueCycles" :key="cycle" :value="cycle">{{ cycle }}</option>
            </select>
            <p v-if="loadingCourses" class="hint-message">Cargando ciclos...</p>
            <p v-else-if="uniqueCycles.length === 0" class="hint-message">No se encontraron ciclos.</p>
          </div>

          <div class="form-group">
            <label for="post-course">Curso:</label>
            <select id="post-course" v-model="post.course" required :disabled="!selectedCycle || loadingCourses">
              <option value="" disabled>
                {{ !selectedCycle ? 'Selecciona un ciclo primero' : (loadingCourses ? 'Cargando cursos...' : 'Selecciona un curso') }}
              </option>
              <option v-for="course in filteredCourses" :key="course.course_code" :value="course.course_name">
                {{ course.course_code }} - {{ course.course_name }}
              </option>
            </select>
            <p v-if="!selectedCycle" class="hint-message">Selecciona un ciclo para ver los cursos.</p>
            <p v-else-if="loadingCourses" class="hint-message">Cargando cursos del ciclo...</p>
            <p v-else-if="filteredCourses.length === 0" class="hint-message">No se encontraron cursos para este ciclo.</p>
          </div>

          <div class="form-group">
            <label for="post-file">Archivo (PDF, DOCX, PPT, JPG, PNG):</label>
            <input type="file" id="post-file" @change="handleFileChange" accept=".pdf,.doc,.docx,.ppt,.pptx,.jpg,.jpeg,.png,.gif" required />
            <p v-if="selectedFile" class="file-name">{{ selectedFile.name }}</p>
            
            <p v-if="processingFile" class="processing-message">
              <i class="fas fa-spinner fa-spin"></i> Generando previsualización...
            </p>
            <p v-if="processedFileSize > 0" class="processed-info">
              Tamaño original: {{ formatBytes(originalFileSize) }} -> Miniatura generada: {{ formatBytes(processedFileSize) }}
            </p>
            <p v-if="processingTime > 0" class="processed-info">
              Tiempo de procesamiento: {{ processingTime.toFixed(2) }} ms
            </p>

            <div v-if="thumbnailUrl" class="thumbnail-preview">
                <h4>Miniatura generada:</h4>
                <img :src="thumbnailUrl" alt="Miniatura del documento" />
            </div>

          </div>

          <div class="modal-actions">
            <button type="button" @click="closeModal" class="cancel-button">Cancelar</button>
            <button type="submit" :disabled="loading || processingFile">
              <span v-if="loading">Subiendo...</span>
              <span v-else-if="processingFile">Procesando...</span>
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
import { ref, onMounted, watch, onUnmounted } from 'vue';
import { usePostStore } from '@modules/posts/stores/post';
import { useAuthStore } from '@modules/auth/stores/auth';
import { storeToRefs } from 'pinia';
import { supabase } from '@/services/supabase';
import { generatePdfThumbnail, formatBytes } from '@modules/posts/stores/pdfThumbnailGenerator'; // Ruta actualizada
import { processImageForThumbnail } from '@modules/posts/stores/imageProcessor'; // Importar nuevo procesador de imágenes

const authStore = useAuthStore();
const postStore = usePostStore();
const { loading, error } = storeToRefs(postStore);

const isModalOpen = ref(false);
const post = ref({
  title: '',
  course: '',
  cycle: '',
  // ¡Importante! Aquí vamos a agregar la thumbnail_url al objeto post
  thumbnail_url: null, // Inicializar como nulo
});
const selectedFile = ref(null); // Archivo principal a subir
const processingFile = ref(false);
const originalFileSize = ref(0);
const processedFileSize = ref(0);
const processingTime = ref(0);
const thumbnailUrl = ref(null); // URL temporal para la previsualización en el modal

const allCoursesData = ref([]);
const uniqueCycles = ref([]);
const selectedCycle = ref('');
const filteredCourses = ref([]);
const loadingCourses = ref(false);

const fetchAllCourses = async () => { /* ... tu implementación actual ... */ 
  loadingCourses.value = true;
  try {
    const { data, error } = await supabase
      .from('courses_by_cycle')
      .select('cycle_name, course_code, course_name')
      .order('cycle_name', { ascending: true })
      .order('course_code', { ascending: true });

    if (error) throw error;
    allCoursesData.value = data;
    const cycles = [...new Set(data.map(item => item.cycle_name))];
    uniqueCycles.value = cycles;
  } catch (err) {
    console.error('Error al cargar ciclos y cursos:', err.message);
  } finally {
    loadingCourses.value = false;
  }
};

const fetchCoursesForCycle = () => { /* ... tu implementación actual ... */ 
  post.value.course = '';
  if (selectedCycle.value) {
    filteredCourses.value = allCoursesData.value.filter(course =>
      course.cycle_name === selectedCycle.value
    );
  } else {
    filteredCourses.value = [];
  }
};

watch(selectedCycle, (newCycle) => {
  post.value.cycle = newCycle;
});

const openModal = async () => {
  isModalOpen.value = true;
  if (uniqueCycles.value.length === 0) {
    await fetchAllCourses();
  }
  selectedCycle.value = '';
  post.value.course = '';
  post.value.title = ''; // Asegúrate de resetear el título también
  post.value.thumbnail_url = null; // Resetear la URL de la miniatura en el objeto post
  filteredCourses.value = [];

  selectedFile.value = null;
  processingFile.value = false;
  originalFileSize.value = 0;
  processedFileSize.value = 0;
  processingTime.value = 0;
  thumbnailUrl.value = null;
  const fileInput = document.getElementById('post-file');
  if (fileInput) fileInput.value = '';
};

const closeModal = () => {
  isModalOpen.value = false;
  post.value.title = '';
  post.value.course = '';
  post.value.cycle = '';
  post.value.thumbnail_url = null; // Resetear
  selectedFile.value = null;
  const fileInput = document.getElementById('post-file');
  if (fileInput) fileInput.value = '';
  
  selectedCycle.value = '';
  filteredCourses.value = [];

  processingFile.value = false;
  originalFileSize.value = 0;
  processedFileSize.value = 0;
  processingTime.value = 0;
  thumbnailUrl.value = null;
};

const handleFileChange = async (event) => {
  const file = event.target.files.length > 0 ? event.target.files.item(0) : null;
  selectedFile.value = null; 
  originalFileSize.value = 0;
  processedFileSize.value = 0;
  processingTime.value = 0;
  processingFile.value = false; 
  thumbnailUrl.value = null;
  post.value.thumbnail_url = null;

  if (file) {
    const fileExtension = file.name.split('.').pop().toLowerCase();
    const fileType = file.type.split('/')[0];

    if (fileExtension === 'pdf') {
      processingFile.value = true;
      originalFileSize.value = file.size;
      try {
        const { thumbnailBlob, processingTime: timeTaken, processedSize: newSize } = await generatePdfThumbnail(file);
        
        selectedFile.value = file; 
        
        // ****** FIX IS HERE ******
        const { data: { user } } = await supabase.auth.getUser(); // AWAIT this line!
        // **************************

        if (!user) { // Add a check in case user is not logged in or session expired
          throw new Error("No user found. Please log in again.");
        }

        const userId = user.id; // Access user.id directly
        const thumbnailPath = `${userId}/${Date.now()}_thumb.jpeg`;
        
        const { data: thumbUploadData, error: thumbUploadError } = await supabase.storage
          .from('thumbnails')
          .upload(thumbnailPath, thumbnailBlob, {
            cacheControl: '3600',
            upsert: false,
            contentType: 'image/jpeg'
          });

        if (thumbUploadError) throw thumbUploadError;

        const { data: publicUrlData } = supabase.storage
          .from('thumbnails')
          .getPublicUrl(thumbnailPath);

        post.value.thumbnail_url = publicUrlData.publicUrl;
        
        processedFileSize.value = newSize;
        processingTime.value = timeTaken;
        thumbnailUrl.value = URL.createObjectURL(thumbnailBlob);

      } catch (err) {
        console.error('Error durante el procesamiento/subida de miniatura PDF:', err);
        alert('Hubo un error al generar o subir la miniatura del PDF. El archivo principal se subirá, pero sin miniatura.');
        selectedFile.value = file;
        post.value.thumbnail_url = null;
      } finally {
        processingFile.value = false;
      }
    } 
    // ... similar fix for the image handling block ...
    else if (fileType === 'image' && ['jpg', 'jpeg', 'png', 'gif'].includes(fileExtension)) {
      processingFile.value = true;
      originalFileSize.value = file.size;

      try {
        const { processedBlob, processingTime: timeTaken, processedSize: newSize } = await processImageForThumbnail(file);
        
        selectedFile.value = file;
        
        // ****** FIX IS HERE ******
        const { data: { user } } = await supabase.auth.getUser(); // AWAIT this line!
        // **************************

        if (!user) { // Add a check
          throw new Error("No user found. Please log in again.");
        }

        const userId = user.id; // Access user.id directly
        const thumbnailPath = `${userId}/${Date.now()}_thumb.${processedBlob.type.split('/')[1]}`;

        const { data: thumbUploadData, error: thumbUploadError } = await supabase.storage
          .from('thumbnails')
          .upload(thumbnailPath, processedBlob, {
            cacheControl: '3600',
            upsert: false,
            contentType: processedBlob.type
          });

        if (thumbUploadError) throw thumbUploadError;

        const { data: publicUrlData } = supabase.storage
          .from('thumbnails')
          .getPublicUrl(thumbnailPath);

        post.value.thumbnail_url = publicUrlData.publicUrl;
        
        processedFileSize.value = newSize;
        processingTime.value = timeTaken;
        thumbnailUrl.value = URL.createObjectURL(processedBlob);

      } catch (err) {
        console.error('Error durante el procesamiento/subida de miniatura de imagen:', err);
        alert('Hubo un error al optimizar o subir la miniatura de la imagen. El archivo original se subirá, pero sin miniatura.');
        selectedFile.value = file;
        post.value.thumbnail_url = null;
      } finally {
        processingFile.value = false;
      }
    } 
    else {
      selectedFile.value = file;
      post.value.thumbnail_url = null;
    }
  }
};

const handleSubmit = async () => {
  if (!post.value.title || !post.value.course || !selectedCycle.value) {
    alert('Por favor, completa todos los campos del formulario (Título, Ciclo y Curso).');
    return;
  }
  if (!selectedFile.value) {
    alert('Por favor, selecciona un archivo para subir.');
    return;
  }

  if (processingFile.value) {
    alert('Por favor, espera a que el archivo termine de procesarse.');
    return;
  }

  post.value.cycle = selectedCycle.value;

  await postStore.uploadPost(post.value, selectedFile.value);

  if (!error.value) {
    closeModal();
  }
};

onMounted(() => {
    if (authStore.user && !authStore.userProfile) {
      authStore.fetchUserProfile(authStore.user.id);
    }
});

onUnmounted(() => {
  if (thumbnailUrl.value) {
    URL.revokeObjectURL(thumbnailUrl.value);
  }
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

.processing-message {
  color: #007bff;
  font-style: italic;
  margin-top: 10px;
}

.processing-message .fa-spinner {
  margin-right: 8px;
}

.processed-info {
  margin-top: 5px;
  font-size: 0.9em;
  color: #555;
}

.thumbnail-preview {
    margin-top: 20px;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 10px;
    background-color: #f9f9f9;
    text-align: center;
}

.thumbnail-preview h4 {
    margin-bottom: 10px;
    color: #333;
}

.thumbnail-preview img {
    max-width: 100%;
    height: auto;
    border: 1px solid #ccc;
    border-radius: 4px;
}

button[type="submit"]:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
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
  /* CAMBIO CLAVE 1: Permite que el modal se pegue más arriba si es muy largo */
  align-items: flex-start; /* Cambiado de 'center' a 'flex-start' */
  padding: 20px; /* Añade un poco de padding para que no toque los bordes de la pantalla */
  box-sizing: border-box; /* Asegura que el padding se incluya en el tamaño */
  overflow-y: auto; /* Permite desplazamiento en el overlay si el modal es aún más grande que la pantalla */
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
  
  /* CAMBIO CLAVE 2: Permitir desplazamiento interno si el contenido es demasiado alto */
  max-height: 90vh; /* Ajusta a un porcentaje de la altura del viewport. Puedes probar con 80vh o 90vh */
  overflow-y: auto; /* Agrega scroll vertical si el contenido excede el max-height */
  
  /* CAMBIO OPCIONAL: Ajustar padding para evitar que el scrollbar se superponga al contenido */
  padding-right: 35px; /* Un poco más de padding a la derecha para el scrollbar */
}

/* Ajusta el padding-right si tienes inputs con width: calc(100% - 22px); */
/* Por ejemplo, en los input[type="text"] y select */
input[type="text"],
input[type="file"],
select { /* Aplica esto a todos los inputs y selects */
  width: 100%; /* Ahora que el padding-right está en el modal, los inputs pueden ser 100% */
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 6px;
  box-sizing: border-box;
  font-size: 1em;
}

/* Asegúrate de que el padding-right no afecte la posición del botón de cerrar */
.close-modal-button {
  position: absolute;
  top: 15px;
  right: 15px; /* Mantenlo relativo al borde del modal, no del padding interno */
  /* ... otros estilos ... */
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