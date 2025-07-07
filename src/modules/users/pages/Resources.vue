<template>
  <div class="feed-page">
    

    <div class="filters-container">
      <div class="search-bar">
        <input
          type="text"
          v-model="searchTerm"
          placeholder="Buscar por título, curso o ciclo..."
          @keyup.enter="applyFilters"
        />
        <button @click="applyFilters" class="search-button">
          <i class="fas fa-search"></i> Buscar
        </button>
        <button v-if="searchTerm || selectedCourse || selectedCycle" @click="clearFilters" class="clear-filters-button">
          Limpiar Filtros
        </button>
      </div>

      <div class="filter-dropdowns">
        <select v-model="selectedCycle" @change="applyFilters" class="filter-select">
          <option value="">Todos los Ciclos</option>
          <option v-for="cycle in postStore.cycles" :key="cycle" :value="cycle">
            {{ cycle }}
          </option>
        </select>

        <select v-model="selectedCourse" @change="applyFilters" class="filter-select">
          <option value="">Todos los Cursos</option>
          <option v-for="course in postStore.courses" :key="course" :value="course">
            {{ course }}
          </option>
        </select>
      </div>
    </div>

    <p v-if="postStore.loading" class="status-message">Cargando recursos...</p>
    <p v-else-if="postStore.error" class="error-message">Error al cargar recursos: {{ postStore.error }}</p>
    <p v-else-if="postStore.posts.length === 0" class="status-message">No hay recursos disponibles.</p>
    <div v-else class="post-list">
      <div v-for="post in postStore.posts" :key="post.id" class="post-item">
        <div class="post-header">
          <router-link :to="`/users/${post.user_id}`" class="post-author-link">
          <img
            :src="post.avatar_url || 'https://via.placeholder.com/40/CCCCCC/FFFFFF?text=AV'"
            alt="Avatar del autor"
            class="post-avatar"
          />
           </router-link>
          <div class="post-info">
            <span class="post-author">
              {{ post.alias || post.email || 'Usuario Desconocido' }}
            </span>
            <span class="post-date">
              {{ new Date(post.created_at).toLocaleDateString('es-ES', { day: '2-digit', month: 'long', year: 'numeric' }) }}
            </span>
          </div>
        </div>

        <h4 class="post-title"><strong>{{ post.title }}</strong></h4>
        <p class="post-detail"><strong>Curso:</strong> {{ post.course }}</p>
        <p class="post-detail"><strong>Ciclo:</strong> {{ post.cycle }}</p>

    <div v-if="post.file_url" class="post-file-preview-container">
      <template v-if="post.thumbnail_url">
        <img :src="post.thumbnail_url" :alt="post.title" class="file-preview-thumbnail" />
        <a :href="post.file_url" target="_blank" rel="noopener noreferrer" class="file-link-overlay">
          <i class="fas fa-eye"></i> Ver Completo
        </a>
      </template>
      <template v-else-if="isImage(post.file_type)">
        <img :src="post.file_url" :alt="post.title" class="file-preview-image" />
        <a :href="post.file_url" target="_blank" rel="noopener noreferrer" class="file-link-overlay">
          <i class="fas fa-eye"></i> Ver Completo
        </a>
      </template>
      <template v-else-if="isPdf(post.file_type)">
        <div class="pdf-icon-preview">
          <i class="fas fa-file-pdf fa-5x"></i>
          <p>Documento PDF</p>
        </div>
        <a :href="post.file_url" target="_blank" rel="noopener noreferrer" class="file-link-overlay">
          <i class="fas fa-eye"></i> Ver Completo
        </a>
      </template>
      <template v-else>
        <div class="generic-file-icon-preview">
          <i class="fas fa-file-alt fa-5x"></i>
          <p>Archivo {{ post.file_type ? post.file_type.toUpperCase() : '' }}</p>
        </div>
        <a :href="post.file_url" target="_blank" rel="noopener noreferrer" class="file-link-overlay">
          <i class="fas fa-download"></i> Descargar Archivo
        </a>
      </template>
    </div>
    <RatingStars
          :post-id="post.id"
          :initial-average-rating="post.average_rating"
          :initial-user-rating="post.user_rating"
        />

      </div>
    </div>
    <div class="pagination-bar" v-if="totalPages > 1">
      <button 
        v-for="page in totalPages" 
        :key="page" 
        :class="{ 'active-page': page === postStore.currentPage }" 
        @click="changePage(page)"
        :disabled="page === postStore.currentPage"
      >
        {{ page }}
      </button>
    </div>

    <p class="page-status">
      Mostrando {{ postStore.posts.length }} de {{ postStore.total }} publicaciones
    </p>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from 'vue';
import { usePostStore } from '@/modules/posts/stores/post'; // Usar '@/modules'
import { useAuthStore } from '@/modules/auth/stores/auth';   // Usar '@/modules'
import { useRouter } from 'vue-router';
// No necesitas TheHeader aquí, ya que se renderiza en App.vue o un layout superior
import PostUpload from '@/modules/posts/components/PostUpload.vue'; // Usar '@/modules'
import RatingStars from '@/modules/ranking/components/RatingStars.vue'; // Usar '@/modules'
// No necesitamos el notificationStore en Resources.vue a menos que quieras notificaciones específicas aquí
// import { useNotificationStore } from '@/modules/notifications/stores/notification'; 

const postStore = usePostStore();
const authStore = useAuthStore(); // Necesario para verificar si el usuario está logueado
const router = useRouter();

// Estados para la búsqueda y filtros
const searchTerm = ref('');
const selectedCourse = ref('');
const selectedCycle = ref('');

// La clave: la función applyFilters ahora pasa un parámetro `authorRole`
const applyFilters = () => {
  const filters = {
    searchTerm: searchTerm.value,
    course: selectedCourse.value,
    cycle: selectedCycle.value,
    authorRole: 'admin', // <-- FILTRO CLAVE: Solo publicaciones de admin
  };
  postStore.fetchPosts(filters);
};

const clearFilters = () => {
  searchTerm.value = '';
  selectedCourse.value = '';
  selectedCycle.value = '';
  applyFilters(); 
};

// Utilidades para previsualización de archivos
const isImage = (fileType) => {
  if (!fileType) return false;
  const lowerCaseType = fileType.toLowerCase();
  return ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'].includes(lowerCaseType);
};

const isPdf = (fileType) => {
  if (!fileType) return false;
  return fileType.toLowerCase() === 'pdf';
};

// --- Ciclo de Vida ---
onMounted(async () => {
  if (authStore.user) {
    try {
      await authStore.fetchUserProfile(authStore.user.id);
      await Promise.all([
        postStore.fetchUniqueCourses(),
        postStore.fetchUniqueCycles()
      ]);
      
      // Carga inicial solo para estudiantes
      await postStore.fetchPosts({
        authorRole: 'admin', // <-- Filtro específico
        reset: true
      });
      
      notificationStore.setupRealtimeNotifications();
    } catch (error) {
      console.error('Initialization error:', error);
    }
  }
});

const changePage = async (page) => {
  await postStore.fetchPosts({
    page,
    searchTerm: searchTerm.value,
    course: selectedCourse.value,
    cycle: selectedCycle.value,
    reset: true
  });
  window.scrollTo({ top: 0, behavior: 'smooth' });
};
</script>

<style scoped>
/* --- ESTILOS PARA PAGINACIÓN --- */
.pagination-bar {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin: 25px 0;
  flex-wrap: wrap;
}

.pagination-bar button {
  padding: 8px 12px;
  min-width: 36px;
  background-color: #f0f2f5;
  border: 1px solid #ddd;
  border-radius: 4px;
  color: #333;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.95em;
}

.pagination-bar button:hover {
  background-color: #e4e6eb;
  border-color: #ccc;
}

.pagination-bar button.active-page {
  background-color: #1877f2;
  color: white;
  border-color: #1877f2;
  font-weight: bold;
}

.page-status {
  text-align: center;
  color: #666;
  font-size: 0.9em;
  margin-top: 10px;
}

.pagination-bar button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  background-color: #1877f2;
  color: white;
}

/* Estilos generales del contenedor principal */
.feed-page {
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
  background-color: #f0f2f5;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0,0,0,0.05);
}

.filters-container {
  background-color: #fff;
  padding: 15px 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  margin-bottom: 20px;
  display: flex;
  flex-direction: row; 
  flex-wrap: wrap; 
  gap: 15px; 
  align-items: center;
  justify-content: space-between;
}

.search-bar {
  display: flex;
  gap: 10px;
  align-items: center;
  flex-grow: 1; 
  min-width: 250px; 
}

.search-bar input {
  flex-grow: 1;
  padding: 10px 15px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 1em;
  outline: none;
  transition: border-color 0.2s ease;
}

.search-bar input:focus {
  border-color: #1877f2;
}

.search-button, .clear-filters-button {
  padding: 10px 15px;
  background-color: #1877f2;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1em;
  display: flex;
  align-items: center;
  gap: 5px;
  transition: background-color 0.2s ease;
  flex-shrink: 0; 
}

.search-button:hover {
  background-color: #155bb5;
}

.clear-filters-button {
  background-color: #6c757d; 
}

.clear-filters-button:hover {
  background-color: #5a6268;
}

.filter-dropdowns {
  display: flex;
  gap: 10px;
  justify-content: flex-end; 
  flex-wrap: wrap; 
  min-width: 200px;
}

.filter-select {
  color: white;
  padding: 10px 15px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 1em;
  background-color: #1877f2;
  cursor: pointer;
  outline: none;
  appearance: none; 
  background-image: url('data:image/svg+xml;charset=US-ASCII,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22292.4%22%20height%3D%22292.4%22%3E%3Cpath%20fill%3D%22%23ffffff%22%20d%3D%22M287%2069.4a17.6%2017.6%200%200%200-13.2-6.4H18.4c-4.9%200-9.2%202.2-12.8%206.4-3.6%204.2-4.7%209.7-3.2%2014.5l133.7%20163.6c2.7%203.4%206.7%205.5%2011.2%205.5s8.5-2.1%2011.2-5.5L287%2083.9c1.5-4.8.4-10.3-3.2-14.5z%22%2F%3E%3C%2Fsvg%3E');
  background-repeat: no-repeat;
  background-position: right 10px top 50%;
  background-size: 12px auto;
  padding-right: 30px; 
  flex-grow: 1; 
  min-width: 120px; 
}

.filter-select option{
  color: #333; 
  padding: 10px 15px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 1em;
  background-color:rgb(255, 255, 255);
  cursor: pointer;
  outline: none;
  appearance: none; 
  background-image: url('data:image/svg+xml;charset=US-ASCII,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22292.4%22%20height%3D%22292.4%22%3E%3Cpath%20fill%3D%22%23ffffff%22%20d%3D%22M287%2069.4a17.6%2017.6%200%200%200-13.2-6.4H18.4c-4.9%200-9.2%202.2-12.8%206.4-3.6%204.2-4.7%209.7-3.2%2014.5l133.7%20163.6c2.7%203.4%206.7%205.5%2011.2%205.5s8.5-2.1%2011.2-5.5L287%2083.9c1.5-4.8.4-10.3-3.2-14.5z%22%2F%3E%3C%2Fsvg%3E');
  background-repeat: no-repeat;
  background-position: right 10px top 50%;
  background-size: 12px auto;
  padding-right: 30px; 
  flex-grow: 1; 
  min-width: 120px; 
}

.filter-select:hover {
  background-color: #155bb5;
  border-color: #155bb5;
}

/* --- Media Queries para Responsividad --- */
@media (max-width: 768px) {
  .filters-container {
    flex-direction: column; 
    align-items: stretch;
  }

  .search-bar {
    width: 100%; 
    min-width: unset; 
  }

  .filter-dropdowns {
    width: 100%; 
    justify-content: space-between;
    min-width: unset; 
  }

  .filter-select {
    width: 100%; 
    min-width: unset;
  }
}

@media (max-width: 480px) {
  .search-bar {
    flex-direction: column; 
    align-items: stretch;
  }
  .search-bar button {
    width: 100%; 
  }
}
/* --- INICIO DE ESTILOS NUEVOS/MODIFICADOS PARA LOS ENLACES DE AUTOR EN EL FEED --- */
.post-author-link {
  display: flex; 
  align-items: center; 
  text-decoration: none; 
  color: inherit; 
}

/* Efecto al pasar el ratón sobre el enlace del autor */
.post-author-link:hover .post-author {
  text-decoration: underline; 
  color: #1877f2; 
}

.post-author-link:hover .post-avatar {
  filter: brightness(0.9); 
}
/* --- FIN DE ESTILOS NUEVOS/MODIFICADOS --- */

/* Badge para Admin */
.admin-badge {
  background-color: #ffc107; /* Color amarillo para destacar */
  color: #333;
  font-size: 0.7em;
  font-weight: bold;
  padding: 2px 6px;
  border-radius: 4px;
  margin-left: 8px;
  vertical-align: middle;
}


/* Mensajes de estado (cargando, error, sin publicaciones) */
.status-message {
  text-align: center;
  color: #666;
  font-style: italic;
  margin-top: 20px;
}

.error-message {
  color: #e53e3e;
  font-weight: bold;
  text-align: center;
  margin-top: 20px;
}

/* Lista de publicaciones */
.post-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* Ítem de publicación individual */
.post-item {
  background-color: #ffffff;
  border-radius: 10px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  padding: 20px;
  border: 1px solid #eee;
}

/* Encabezado de la publicación (autor, fecha) */
.post-header {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

/* Avatar del autor de la publicación */
.post-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 10px;
  object-fit: cover;
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
  color: #777;
}

/* Título, curso y ciclo de la publicación */
.post-title {
  margin-top: 0;
  margin-bottom: 10px;
  color: #1877f2;
  font-size: 1.3em;
}

.post-detail {
  margin-bottom: 5px;
  color: #333;
  font-size: 0.95em;
}
/* Contenedor de previsualización de archivos - MODIFICADO */
.post-file-preview-container {
    margin-top: 15px;
    padding-top: 15px;
    border-top: 1px solid #eee;
    text-align: center;
    position: relative; /* ¡CRÍTICO! Necesario para posicionar el overlay correctamente */
    display: flex;      /* Usa flexbox para centrar el contenido */
    flex-direction: column; /* Alinea los elementos verticalmente */
    justify-content: center; /* Centra el contenido verticalmente */
    align-items: center;   /* Centra el contenido horizontalmente */
    min-height: 150px;     /* Asegura un espacio mínimo, ajusta si es necesario */
    overflow: hidden;      /* Previene desbordamientos si la imagen es muy grande */
}

/* NUEVO: Estilos para imágenes de miniaturas (usado por `post.thumbnail_url`) */
.file-preview-thumbnail {
    max-width: 100%;       /* Asegura que no se desborde del contenedor */
    height: auto;          /* Mantiene la relación de aspecto */
    max-height: 250px;     /* Altura máxima para las miniaturas, ajusta a tu gusto */
    display: block;        /* Para que se comporte como un bloque y respete márgenes */
    object-fit: contain;   /* Escala la imagen para que quepa completamente dentro de sus límites */
    border-radius: 8px;    /* Consistente con otros elementos */
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); /* Consistente con otros elementos */
    margin: 0 auto 10px auto; /* Centra horizontalmente y añade margen inferior */
}

/* Estilos para imágenes de previsualización (para cuando no hay miniatura y es una imagen original) - EXISTENTE */
.file-preview-image {
    max-width: 100%;
    height: auto;
    border-radius: 8px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    margin-bottom: 10px;
}

/* NUEVO: Estilos para el enlace/overlay que aparece sobre la miniatura */
.file-link-overlay {
    position: absolute; /* Posicionamiento absoluto respecto a .post-file-preview-container */
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5); /* Fondo semitransparente oscuro */
    color: white;
    display: flex;
    flex-direction: column; /* Icono y texto apilados */
    justify-content: center;
    align-items: center;
    text-decoration: none;
    font-weight: bold;
    opacity: 0; /* Por defecto está oculto */
    transition: opacity 0.3s ease; /* Transición suave para el efecto hover */
    border-radius: 8px; /* Coincide con el border-radius de la miniatura */
}

/* Muestra el overlay al pasar el ratón por el contenedor */
.post-file-preview-container:hover .file-link-overlay {
    opacity: 1; /* Se hace visible al hacer hover */
}

/* Sección de acción de descarga */
.file-download-action {
  text-align: center;
  margin-top: 20px; /* Espacio superior para separarlo de la previsualización */
  padding-top: 15px; /* Padding superior para el botón */
  border-top: 1px solid #eee; /* Línea divisoria */
}

.download-button {
  display: inline-flex; /* Permite icono y texto en línea */
  align-items: center; /* Alinea verticalmente icono y texto */
  padding: 10px 20px;
  background-color: #28a745; /* Un verde para el botón de descarga */
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1em;
  text-decoration: none; /* Elimina el subrayado del enlace */
  transition: background-color 0.2s ease;
}

.download-button i {
  margin-right: 8px; /* Espacio entre el icono y el texto */
}

.download-button:hover {
  background-color: #218838; /* Verde más oscuro al pasar el ratón */
}

.file-link-overlay i {
    margin-bottom: 8px; /* Espacio entre el icono y el texto */
    font-size: 1.5em; /* Tamaño del icono */
}

/* Estilos para PDF de previsualización (cuando se muestra el icono PDF, no la miniatura de imagen) - EXISTENTE */
.file-preview-pdf {
    border: 1px solid #ddd;
    border-radius: 8px;
    width: 100%;
    min-height: 300px;
    max-height: 600px;
    /* Esto era para el iframe, no aplica si usas un icono como fallback */
    /* Si lo que quieres es el icono de PDF, la clase no se usará aquí directamente */
}
</style>