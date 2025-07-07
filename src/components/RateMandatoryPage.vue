<template>
  <div class="rate-mandatory-page-container">
    <div v-if="loadingPost" class="loading-state">
      <p>Cargando publicación para valorar...</p>
      <i class="fas fa-spinner fa-spin fa-2x"></i>
    </div>
    <div v-else-if="postToRate">
      <h2>¡Atención, Estudiante!</h2>
      <p>Por favor, valora esta publicación para continuar navegando.</p>
      
      <div class="post-item-to-rate">
        <div class="post-header">
          <img
            :src="postToRate.author_avatar_url || 'https://via.placeholder.com/40/CCCCCC/FFFFFF?text=AV'"
            alt="Avatar del autor"
            class="post-avatar"
          />
          <div class="post-info">
            <span class="post-author">{{ postToRate.author_alias || postToRate.author_email || 'Usuario Desconocido' }}</span>
            <span class="post-date">
              {{ new Date(postToRate.created_at).toLocaleDateString('es-ES', { day: '2-digit', month: 'long', year: 'numeric' }) }}
            </span>
          </div>
        </div>
        <h4 class="post-title"><strong>{{ postToRate.title }}</strong></h4>
        <p class="post-detail"><strong>Curso:</strong> {{ postToRate.course }}</p>
        <p class="post-detail"><strong>Ciclo:</strong> {{ postToRate.cycle }}</p>

        <div v-if="postToRate.file_url" class="post-file-preview-container">
          <template v-if="postToRate.thumbnail_url">
            <img :src="postToRate.thumbnail_url" :alt="postToRate.title" class="file-preview-thumbnail" />
            <a :href="postToRate.file_url" target="_blank" rel="noopener noreferrer" class="file-link-overlay">
              <i class="fas fa-eye"></i> Ver Completo
            </a>
          </template>
          <template v-else-if="isImage(postToRate.file_type)">
            <img :src="postToRate.file_url" :alt="postToRate.title" class="file-preview-image" />
            <a :href="postToRate.file_url" target="_blank" rel="noopener noreferrer" class="file-link-overlay">
              <i class="fas fa-eye"></i> Ver Completo
            </a>
          </template>
          <template v-else-if="isPdf(postToRate.file_type)">
            <div class="pdf-icon-preview">
              <i class="fas fa-file-pdf fa-5x"></i>
              <p>Documento PDF</p>
            </div>
            <a :href="postToRate.file_url" target="_blank" rel="noopener noreferrer" class="file-link-overlay">
              <i class="fas fa-eye"></i> Ver Completo
            </a>
          </template>
          <template v-else>
            <div class="generic-file-icon-preview">
              <i class="fas fa-file-alt fa-5x"></i>
              <p>Archivo {{ postToRate.file_type ? postToRate.file_type.toUpperCase() : '' }}</p>
            </div>
            <a :href="postToRate.file_url" target="_blank" rel="noopener noreferrer" class="file-link-overlay">
              <i class="fas fa-download"></i> Descargar Archivo
            </a>
          </template>
        </div>

        <div v-if="postToRate.file_url" class="file-download-action">
          <a :href="postToRate.file_url" target="_blank" rel="noopener noreferrer" class="download-button">
            <i class="fas fa-download"></i> Descargar Archivo Completo
          </a>
        </div>

        <div class="rating-section">
          <h3>Tu Valoración:</h3>
          <div class="stars">
            <i v-for="n in 5" :key="n" 
               :class="['fas fa-star', { 'active': n <= currentRating }]" 
               @click="setRating(n)"></i>
          </div>
          <button @click="submitRating" :disabled="currentRating === 0 || submitting" class="submit-rating-button">
            {{ submitting ? 'Enviando...' : 'Valorar y Continuar' }}
          </button>
          <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
        </div>
      </div>
    </div>
    <div v-else class="no-posts-found">
      <p>No hay publicaciones disponibles para valorar en este momento o ya las has valorado todas.</p>
      <p>Por favor, intenta más tarde o contacta a soporte si crees que esto es un error.</p>
      <button @click="authStore.signOut()" class="sign-out-button">Cerrar Sesión</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { supabase } from '@/services/supabase'; // Ajusta la ruta a tu archivo supabase.js
import { useAuthStore } from '@/modules/auth/stores/auth'; // Ajusta la ruta a tu auth store
import router from '@/router'; // Importar el router

const authStore = useAuthStore();
const postToRate = ref(null);
const loadingPost = ref(true);
const currentRating = ref(0);
const submitting = ref(false);
const errorMessage = ref('');

// Helper functions for file types
const isImage = (fileType) => ['image/jpeg', 'image/png', 'image/gif', 'image/webp'].includes(fileType);
const isPdf = (fileType) => fileType === 'application/pdf';

async function fetchRandomPost() {
  loadingPost.value = true;
  errorMessage.value = '';
  try {
    if (!authStore.user || authStore.user.role !== 'student') {
      console.error('Acceso denegado: Solo estudiantes pueden acceder a esta página obligatoria.');
      router.push({ name: 'Login' }); // Redirige a login si no es estudiante o no está logueado
      return;
    }

    // Asegúrate de que tu RPC get_random_unrated_post devuelve los campos necesarios
    // como 'file_type', 'thumbnail_url', 'author_alias', 'author_avatar_url'
    const { data, error } = await supabase.rpc('get_random_unrated_post', { p_user_id: authStore.user.id });

    if (error) throw error;

    if (data && data.length > 0) {
      postToRate.value = data[0];
    } else {
      postToRate.value = null; // No hay posts para valorar
      errorMessage.value = 'No se encontraron publicaciones disponibles para valorar en este momento o ya las has valorado todas.';
    }
  } catch (error) {
    console.error('Error fetching random post:', error.message);
    errorMessage.value = `Error al cargar la publicación: ${error.message}`;
    postToRate.value = null;
  } finally {
    loadingPost.value = false;
  }
}

function setRating(rating) {
  currentRating.value = rating;
}

async function submitRating() {
  if (currentRating.value === 0 || !postToRate.value) {
    errorMessage.value = 'Por favor, selecciona una valoración.';
    return;
  }

  submitting.value = true;
  errorMessage.value = '';
  try {
    // Inserta o actualiza el rating en tu tabla 'ratings'
    // Asumiendo que tu tabla se llama 'ratings' y tiene 'post_id', 'user_id', 'rating'
    // y que 'updated_at' se actualiza automáticamente.
    const { error } = await supabase.from('ratings').upsert(
      {
        post_id: postToRate.value.id,
        user_id: authStore.user.id,
        rating: currentRating.value
      },
      { onConflict: 'post_id,user_id' } // Si el usuario ya valoró este post, actualiza
    );

    if (error) throw error;

    console.log('Valoración enviada con éxito. Re-comprobando requerimiento.');
    // Si el rating fue exitoso, re-evalúa el requerimiento de rating y redirige
    await authStore.checkRatingRequirement(); // Esto actualizará authStore.needsRating

    if (!authStore.needsRating) { // Si ya no necesita rating, puede navegar
      console.log('Requerimiento de rating cumplido. Redirigiendo a Feed.');
      router.push({ name: 'Feed' }); // Redirige a la página principal del feed
    } else {
        // En un caso ideal, no debería llegar aquí si valoró un post.
        // Pero si por alguna razón `checkRatingRequirement` todavía devuelve true,
        // (ej. no hay suficientes posts únicos, o el timestamp no se actualizó inmediatamente),
        // reseteamos y cargamos otro post.
        console.log('Aún necesita valorar. Cargando otro post aleatorio.');
        currentRating.value = 0; // Resetear la valoración para el siguiente post
        await fetchRandomPost(); // Cargar otro post si por alguna razón aún lo necesita
        errorMessage.value = '¡Valoración enviada! Por favor, valora otra publicación si es necesario.';
    }

  } catch (error) {
    console.error('Error submitting rating:', error.message);
    errorMessage.value = `Error al enviar la valoración: ${error.message}`;
  } finally {
    submitting.value = false;
  }
}

onMounted(() => {
  // Asegurarse de que el usuario es un estudiante y que el store ya ha cargado su estado
  if (authStore.isAuthenticated && authStore.isStudent) {
    // La verificación real de needsRating se hace en el router guard.
    // Si llegamos a esta página, es porque el router ya determinó que needsRating es true.
    fetchRandomPost();
  } else {
    // Si no es un estudiante autenticado, no debería estar aquí, redirige
    router.push({ name: 'Home' }); 
  }
});
</script>

<style scoped>
/* Contenedor principal de la página de valoración obligatoria */
.rate-mandatory-page-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - 100px); /* Ajusta según el tamaño de tu header/footer */
  padding: 20px;
  background-color: #f0f2f5;
  font-family: 'Arial', sans-serif;
}

.loading-state {
  text-align: center;
  font-size: 1.2em;
  color: #555;
}

/* Estilos para el contenedor del post a valorar (similar a post-item en FeedPage) */
.post-item-to-rate {
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  padding: 25px;
  margin-bottom: 20px;
  width: 100%;
  max-width: 600px; /* Ancho máximo para legibilidad */
}

h2 {
  color: #333;
  margin-bottom: 10px;
  text-align: center;
}

p {
  color: #666;
  text-align: center;
  margin-bottom: 20px;
}

/* Estilos de encabezado de post (reutilizados) */
.post-header {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

.post-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
  margin-right: 10px;
}

.post-info {
  display: flex;
  flex-direction: column;
}

.post-author {
  font-weight: bold;
  color: #333;
}

.post-date {
  font-size: 0.85em;
  color: #888;
}

/* Estilos del cuerpo del post (reutilizados) */
.post-title {
  color: #0056b3;
  margin-top: 10px;
  margin-bottom: 10px;
  font-size: 1.3em;
}

.post-detail {
  color: #555;
  margin-bottom: 5px;
}

/* Sección de Valoración */
.rating-section {
  text-align: center;
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.rating-section h3 {
  margin-bottom: 15px;
  color: #333;
}

.stars {
  font-size: 2em;
  color: #ccc; /* Color por defecto de estrellas inactivas */
  margin-bottom: 20px;
}

.stars .fa-star {
  cursor: pointer;
  transition: color 0.2s ease;
}

.stars .fa-star.active {
  color: #ffc107; /* Color dorado para estrellas activas */
}

.submit-rating-button {
  padding: 12px 25px;
  background-color: #007bff; /* Azul primario */
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1.1em;
  transition: background-color 0.2s ease;
}

.submit-rating-button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.submit-rating-button:hover:not(:disabled) {
  background-color: #0056b3; /* Azul más oscuro al pasar el ratón */
}

.error-message {
  color: #dc3545; /* Rojo para mensajes de error */
  margin-top: 10px;
}

/* Estilos para cuando no hay posts para valorar */
.no-posts-found {
    text-align: center;
    padding: 30px;
    background-color: white;
    border-radius: 10px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.sign-out-button {
  margin-top: 20px;
  padding: 10px 20px;
  background-color: #dc3545; /* Rojo para el botón de cerrar sesión */
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
.sign-out-button:hover {
  background-color: #c82333; /* Rojo más oscuro al pasar el ratón */
}

/* --- REUTILIZACIÓN DE ESTILOS DE PREVISUALIZACIÓN DE ARCHIVOS --- */
/* Cópialos directamente desde FeedPage.vue para asegurar consistencia */

.post-file-preview-container {
    margin-top: 15px;
    padding-top: 15px;
    border-top: 1px solid #eee;
    text-align: center;
    position: relative;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    min-height: 150px;
    overflow: hidden;
}

.file-preview-thumbnail {
    max-width: 100%;
    height: auto;
    max-height: 250px;
    display: block;
    object-fit: contain;
    border-radius: 8px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    margin: 0 auto 10px auto;
}

.file-preview-image {
    max-width: 100%;
    height: auto;
    border-radius: 8px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    margin-bottom: 10px;
}

.file-link-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    color: white;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-decoration: none;
    font-weight: bold;
    opacity: 0;
    transition: opacity 0.3s ease;
    border-radius: 8px;
}

.post-file-preview-container:hover .file-link-overlay {
    opacity: 1;
}

.file-link-overlay i {
    margin-bottom: 8px;
    font-size: 1.5em;
}

.pdf-icon-preview, .generic-file-icon-preview {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 150px;
  border: 1px dashed #ccc;
  border-radius: 8px;
  background-color: #f9f9f9;
  color: #666;
}

.pdf-icon-preview i {
  margin-bottom: 10px;
  color: #d9534f;
}

.generic-file-icon-preview i {
  margin-bottom: 10px;
  color: #6c757d;
}

.pdf-icon-preview p, .generic-file-icon-preview p {
  font-size: 0.9em;
  margin: 0;
}

.file-download-action {
  text-align: center;
  margin-top: 20px;
  padding-top: 15px;
  border-top: 1px solid #eee;
}

.download-button {
  display: inline-flex;
  align-items: center;
  padding: 10px 20px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1em;
  text-decoration: none;
  transition: background-color 0.2s ease;
}

.download-button i {
  margin-right: 8px;
}

.download-button:hover {
  background-color: #218838;
}
</style>