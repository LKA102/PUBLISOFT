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
            :src="post.users?.avatar_url || 'https://via.placeholder.com/40/CCCCCC/FFFFFF?text=AV'"
            alt="Avatar del autor"
            class="post-avatar"
          />
           </router-link>
          <div class="post-info">
            <span class="post-author">
              {{ post.users ? post.users.alias || post.users.email : 'Usuario Desconocido' }}
              <span v-if="post.users?.role === 'admin'" class="admin-badge">Admin</span>
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
          <template v-if="isImage(post.file_type)">
            <img :src="post.file_url" :alt="post.title" class="file-preview-image" />
          </template>
          <template v-else-if="isPdf(post.file_type)">
            <iframe :src="post.file_url" width="100%" height="400px" class="file-preview-pdf" frameborder="0"></iframe>
          </template>
          <template v-else>
            <a :href="post.file_url" target="_blank" rel="noopener noreferrer" class="file-link">
              <i class="fas fa-file-alt"></i> Ver Archivo ({{ post.file_type ? post.file_type.toUpperCase() : 'Archivo' }})
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
  // Asegurarse de que el usuario está autenticado antes de intentar cargar posts
  if (authStore.user) {
    await postStore.fetchUniqueCourses(); // Cargar cursos únicos
    await postStore.fetchUniqueCycles();   // Cargar ciclos únicos
    applyFilters(); // Cargar las publicaciones iniciales con el filtro de admin
  } else {
    // Si no está autenticado, redirigir al login (aunque el router guard debería manejar esto)
    router.push('/login');
  }
});

// onUnmounted para limpiar listeners, si hubiera
// Aquí no hay listeners específicos de DOM como en el Feed original
// pero si tuvieras suscripciones en tiempo real para recursos, irían aquí.
// Por ahora, asumimos que no hay necesidad específica de onUnmounted en Resources.vue
</script>

<style scoped>
/*
  IMPORTANTE:
  Los estilos que tenías en Feed.vue son bastante genéricos para el feed.
  Puedes copiarlos directamente aquí o, mejor aún, si son estilos compartidos
  entre Feed.vue y Resources.vue, deberías moverlos a un archivo CSS global
  (ej. src/assets/css/post-styles.css) e importarlo en ambos componentes,
  o en tu App.vue si son estilos muy generales.

  Por ahora, los pego directamente.
*/

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

/* Contenedor de previsualización de archivos */
.post-file-preview-container {
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid #eee;
  text-align: center;
}

/* Estilos para imágenes de previsualización */
.file-preview-image {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  margin-bottom: 10px;
}

/* Estilos para PDF de previsualización */
.file-preview-pdf {
  border: 1px solid #ddd;
  border-radius: 8px;
  width: 100%;
  min-height: 300px;
  max-height: 600px;
}

/* Estilos para enlaces de archivo */
.file-link {
  color: #1877f2;
  text-decoration: none;
  font-weight: bold;
  display: inline-flex;
  align-items: center;
  margin-top: 10px;
}

.file-link:hover {
  text-decoration: underline;
}

.file-link i {
  margin-right: 8px;
  font-size: 1.1em;
}
</style>