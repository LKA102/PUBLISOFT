<template>
  <div class="feed-page">
    <PostUpload />
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

    <p v-if="postStore.loading" class="status-message">Cargando publicaciones...</p>
    <p v-else-if="postStore.error" class="error-message">Error al cargar publicaciones: {{ postStore.error }}</p>
    <p v-else-if="postStore.posts.length === 0" class="status-message">No hay publicaciones disponibles.</p>
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
import { onMounted, ref, computed, onUnmounted } from 'vue';
import { usePostStore } from '@modules/posts/stores/post';
import { useAuthStore } from '@modules/auth/stores/auth';
import { useRouter } from 'vue-router';
import TheHeader from '@/components/TheHeader.vue';
import PostUpload from '@modules/posts/components/PostUpload.vue';
import RatingStars from '@modules/ranking/components/RatingStars.vue';
import { useNotificationStore } from '@modules/notifications/stores/notification';

function debounce(fn, delay) {
  let timeoutId;
  return function(...args) {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn.apply(this, args), delay);
  };
}

// Stores
const postStore = usePostStore();
const authStore = useAuthStore();
const router = useRouter();
const notificationStore = useNotificationStore();

// Estados para filtros
const searchTerm = ref('');
const selectedCourse = ref('');
const selectedCycle = ref('');

// Estados UI
const dropdownOpen = ref(false);
const showNotifications = ref(false);

// Computed
const totalPages = computed(() => Math.ceil(postStore.total / postStore.itemsPerPage));
const currentItemsCount = computed(() => `${postStore.posts.length} de ${postStore.total}`);

const hasMore = computed(() => {
  return postStore.posts.length < postStore.total;
});

// Funciones de filtrado
const applyFilters = debounce(async () => {
  await postStore.fetchPosts({
    searchTerm: searchTerm.value || null,
    course: selectedCourse.value || null,
    cycle: selectedCycle.value || null,
    reset: true
  });
}, 300); 

const clearFilters = async () => {
  searchTerm.value = '';
  selectedCourse.value = '';
  selectedCycle.value = '';
  
  // Forzar una recarga completa con filtros null
  await postStore.fetchPosts({
    searchTerm: null,
    course: null,
    cycle: null,
    reset: true
  });
};

// Carga más posts al hacer scroll (scroll infinito)
const handleScroll = async () => {
  if (postStore.loading || postStore.posts.length >= postStore.total) return;
  
  const scrollPosition = window.innerHeight + window.scrollY;
  const documentHeight = document.body.offsetHeight;
  const nearBottom = scrollPosition >= documentHeight - 500;

  if (nearBottom) {
    await postStore.fetchPosts({
      page: postStore.currentPage + 1,
      searchTerm: searchTerm.value,
      course: selectedCourse.value,
      cycle: selectedCycle.value,
      reset: false
    });
  }
};

// Funciones de UI
const toggleDropdown = () => dropdownOpen.value = !dropdownOpen.value;
const toggleNotifications = async () => {
  showNotifications.value = !showNotifications.value;
  if (showNotifications.value) {
    await notificationStore.fetchNotifications(20);
  }
};
const markAllAsRead = async () => {
  await notificationStore.markAllAsRead();
  await notificationStore.fetchNotifications(20);
};
const handleLogout = async () => {
  await authStore.signOut();
  router.push('/login');
};
const handleClickOutside = (event) => {
  const dropdown = document.querySelector('.dropdown-container');
  if (dropdown && !dropdown.contains(event.target)) {
    dropdownOpen.value = false;
  }
};

// Helpers
const isImage = (fileType) => {
  if (!fileType) return false;
  return ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'].includes(fileType.toLowerCase());
};
const isPdf = (fileType) => fileType?.toLowerCase() === 'pdf';

// Ciclo de vida
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
        authorRole: 'student', // <-- Filtro específico
        reset: true
      });
      
      notificationStore.setupRealtimeNotifications();
    } catch (error) {
      console.error('Initialization error:', error);
    }
  }
});

onUnmounted(() => {
  notificationStore.unsubscribeRealtimeNotifications();
  document.removeEventListener('click', handleClickOutside);
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

/* In your FeedPage.vue <style scoped> section */


/* --- ESTILOS PARA PAGINACIÓN --- */
/* ... (tu código CSS existente aquí) ... */

/* Estilos de previsualización de archivos */
/* --- MODIFICACIONES IMPORTANTES AQUÍ --- */

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

/* ... (resto de tu código CSS existente) ... */
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
  /* Cambiado: Ahora los elementos internos se alinean en fila */
  /* Usa 'row' para alinear horizontalmente */
  flex-direction: row; 
  /* Permite que los elementos salten a la siguiente línea si no hay espacio */
  flex-wrap: wrap; 
  /* Espacio entre los elementos flexibles */
  gap: 15px; 
  /* Alinea los elementos al inicio (izquierda por defecto) */
  align-items: center; /* Alinea verticalmente los elementos en la fila */
  justify-content: space-between; /* Distribuye el espacio entre la barra de búsqueda y los filtros */
}

.search-bar {
  display: flex;
  gap: 10px;
  align-items: center;
  /* Permite que la barra de búsqueda ocupe el espacio disponible */
  flex-grow: 1; 
  /* Asegura que no sea más pequeño de lo necesario en ciertos casos */
  min-width: 250px; /* Ancho mínimo para la barra de búsqueda */
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
  /* Asegura que los botones no se encojan demasiado */
  flex-shrink: 0; 
}

.search-button:hover {
  background-color: #155bb5;
}

.clear-filters-button {
  background-color: #6c757d; /* Gris para limpiar filtros */
}

.clear-filters-button:hover {
  background-color: #5a6268;
}

.filter-dropdowns {
  display: flex;
  gap: 10px;
  /* Alinea los selectores al final (derecha) dentro de su contenedor */
  justify-content: flex-end; 
  /* Permite que los selectores ocupen el espacio restante o se envuelvan */
  flex-wrap: wrap; 
  /* Asegura que no se encojan demasiado y mantengan un ancho mínimo si es necesario */
  min-width: 200px; /* Ancho mínimo para el conjunto de dropdowns */
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
  appearance: none; /* Elimina estilos por defecto del sistema */
  background-image: url('data:image/svg+xml;charset=US-ASCII,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22292.4%22%20height%3D%22292.4%22%3E%3Cpath%20fill%3D%22%23ffffff%22%20d%3D%22M287%2069.4a17.6%2017.6%200%200%200-13.2-6.4H18.4c-4.9%200-9.2%202.2-12.8%206.4-3.6%204.2-4.7%209.7-3.2%2014.5l133.7%20163.6c2.7%203.4%206.7%205.5%2011.2%205.5s8.5-2.1%2011.2-5.5L287%2083.9c1.5-4.8.4-10.3-3.2-14.5z%22%2F%3E%3C%2Fsvg%3E');
  background-repeat: no-repeat;
  background-position: right 10px top 50%;
  background-size: 12px auto;
  padding-right: 30px; /* Espacio para el icono de flecha */
  /* Permite que los selectores se estiren o encojan de manera flexible */
  flex-grow: 1; 
  min-width: 120px; /* Ancho mínimo para cada selector individual */
}

.filter-select option{
  color: #333; /* Color del texto de las opciones */
  padding: 10px 15px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 1em;
  background-color:rgb(255, 255, 255);
  cursor: pointer;
  outline: none;
  appearance: none; /* Elimina estilos por defecto del sistema */
  background-image: url('data:image/svg+xml;charset=US-ASCII,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22292.4%22%20height%3D%22292.4%22%3E%3Cpath%20fill%3D%22%23ffffff%22%20d%3D%22M287%2069.4a17.6%2017.6%200%200%200-13.2-6.4H18.4c-4.9%200-9.2%202.2-12.8%206.4-3.6%204.2-4.7%209.7-3.2%2014.5l133.7%20163.6c2.7%203.4%206.7%205.5%2011.2%205.5s8.5-2.1%2011.2-5.5L287%2083.9c1.5-4.8.4-10.3-3.2-14.5z%22%2F%3E%3C%2Fsvg%3E');
  background-repeat: no-repeat;
  background-position: right 10px top 50%;
  background-size: 12px auto;
  padding-right: 30px; /* Espacio para el icono de flecha */
  /* Permite que los selectores se estiren o encojan de manera flexible */
  flex-grow: 1; 
  min-width: 120px; /* Ancho mínimo para cada selector individual */
}

.filter-select:hover {
  background-color: #155bb5;
  border-color: #155bb5;
}

/* --- Media Queries para Responsividad --- */
@media (max-width: 768px) {
  .filters-container {
    flex-direction: column; /* Vuelve a columna en pantallas pequeñas */
    align-items: stretch; /* Estira los elementos para ocupar todo el ancho */
  }

  .search-bar {
    width: 100%; /* La barra de búsqueda ocupa todo el ancho */
    min-width: unset; /* Elimina el min-width fijo */
  }

  .filter-dropdowns {
    width: 100%; /* Los dropdowns ocupan todo el ancho */
    justify-content: space-between; /* Distribuye espacio entre ellos si hay varios */
    min-width: unset; /* Elimina el min-width fijo */
  }

  .filter-select {
    width: 100%; /* Cada selector ocupa todo el ancho disponible */
    min-width: unset; /* Elimina el min-width fijo */
  }
}

@media (max-width: 480px) {
  .search-bar {
    flex-direction: column; /* Botones de búsqueda y limpiar se apilan */
    align-items: stretch;
  }
  .search-bar button {
    width: 100%; /* Los botones también ocupan el ancho completo */
  }
}
/* --- INICIO DE ESTILOS NUEVOS/MODIFICADOS PARA LOS ENLACES DE AUTOR EN EL FEED --- */
.post-author-link {
  display: flex; /* Permite alinear el avatar y el texto horizontalmente */
  align-items: center; /* Centra verticalmente el avatar y el texto */
  text-decoration: none; /* Elimina el subrayado predeterminado de los enlaces */
  color: inherit; /* Hereda el color del texto del padre para que el texto no sea azul por defecto */
}

/* Efecto al pasar el ratón sobre el enlace del autor */
.post-author-link:hover .post-author {
  text-decoration: underline; /* Subraya el alias/email */
  color: #1877f2; /* Cambia el color del texto a azul (similar a Facebook) */
}

.post-author-link:hover .post-avatar {
  filter: brightness(0.9); /* Oscurece ligeramente el avatar para un efecto visual */
}
/* --- FIN DE ESTILOS NUEVOS/MODIFICADOS --- */

/* --- ESTILOS DE NOTIFICACIONES (COPIADOS DE PROFILE.VUE) --- */
.notification-area {
  position: relative;
  display: flex;
  align-items: center;
}

.notification-icon {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.8em;
  color: #333;
  padding: 5px;
  border-radius: 50%;
  transition: background-color 0.2s ease;
}

.notification-icon:hover {
  background-color: #e0e0e0;
}

.notification-badge {
  position: absolute;
  top: -5px;
  right: -5px;
  background-color: #ff4d4f; /* Rojo */
  color: white;
  border-radius: 50%;
  padding: 3px 7px;
  font-size: 0.7em;
  font-weight: bold;
  pointer-events: none; /* Para que no interfiera con el click del icono */
}

.notifications-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  width: 300px;
  max-height: 400px; /* Limita la altura del dropdown */
  overflow-y: auto; /* Permite scroll si hay muchas notificaciones */
  z-index: 1000;
  padding: 10px;
  margin-top: 10px; /* Separación del botón */
}

.notifications-dropdown ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.notifications-dropdown li {
  padding: 10px;
  border-bottom: 1px solid #eee;
  cursor: pointer;
}

.notifications-dropdown li:last-child {
  border-bottom: none;
}

.notifications-dropdown li.unread {
  background-color: #e6f7ff; /* Fondo para no leídas */
  font-weight: 600;
}

.notifications-dropdown li small {
  display: block;
  font-size: 0.8em;
  color: #888;
  margin-top: 5px;
}

.status-message {
  text-align: center;
  padding: 15px;
  color: #666;
}

.error-message {
  text-align: center;
  padding: 15px;
  color: #d9534f;
}

.view-all-notifications-button {
  display: block;
  text-align: center;
  padding: 8px;
  margin: 10px 0;
  background-color: #f0f2f5;
  color: #1877f2;
  text-decoration: none;
  border-radius: 5px;
  transition: background-color 0.2s ease;
  font-size: 0.9em;
  width: 100%;
  box-sizing: border-box;
}

.view-all-notifications-button:hover {
  background-color: #e4e6eb;
}

.mark-read-button {
  background-color: #007bff; /* Azul primario */
  color: white;
  border: none;
  padding: 8px 15px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 0.9em;
  transition: background-color 0.2s ease;
  width: 100%;
  box-sizing: border-box;
}

.mark-read-button:hover {
  background-color: #0056b3;
}
/* --- FIN ESTILOS DE NOTIFICACIONES --- */

/* Estilos del encabezado del feed */
.feed-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
  padding-bottom: 15px;
  border-bottom: 1px solid #e0e0e0;
}

.header-title {
  color: #333;
  margin: 0;
  font-size: 1.8em;
  font-weight: bold;
}

.header-actions {
  position: relative; /* Importante para el posicionamiento del desplegable */
  display: flex;
  gap: 15px;
  align-items: center;
}

/* Contenedor del desplegable */
.dropdown-container {
  position: relative;
  display: inline-block;
  cursor: pointer;
  z-index: 100; /* Asegura que el desplegable esté por encima de otros elementos */
}

/* Botón que activa el desplegable (avatar + alias + flecha) */
.profile-dropdown-toggle {
  display: flex;
  align-items: center;
  background-color: transparent;
  border: none;
  padding: 5px 10px;
  border-radius: 20px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.profile-dropdown-toggle:hover {
  background-color: #e4e6eb;
}

.profile-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
  margin-right: 8px;
  border: 1px solid #ddd;
}

.profile-alias {
  font-weight: bold;
  font-size: 0.95em;
  white-space: nowrap;
  color: #333; /* Color para el texto del alias */
}

.dropdown-arrow {
  margin-left: 8px;
  transition: transform 0.2s ease;
}

.dropdown-arrow.rotate-180 {
  transform: rotate(180deg);
}

/* Estilos del menú desplegable */
.dropdown-menu {
  position: absolute;
  top: 100%; /* Coloca el menú debajo del botón */
  right: 0; /* Alinea el menú a la derecha del botón */
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  min-width: 180px; /* Ancho mínimo para el menú */
  padding: 8px 0;
  z-index: 100; /* Asegura que esté por encima de otros elementos */
  list-style: none; /* Eliminar viñetas si fuera una ul */
  margin-top: 8px; /* Espacio entre el botón y el menú */
  overflow: hidden; /* Para border-radius */
}

.dropdown-item {
  display: flex;
  align-items: center;
  padding: 10px 15px;
  color: #333;
  text-decoration: none;
  font-size: 0.95em;
  transition: background-color 0.2s ease, color 0.2s ease;
  width: 100%; /* Asegura que ocupe todo el ancho del desplegable */
  text-align: left; /* Alinea el texto a la izquierda */
  border: none; /* Quita el borde de los botones */
  background: none; /* Quita el fondo de los botones */
  cursor: pointer;
}

.dropdown-item:hover {
  background-color: #f0f2f5;
  color: #1877f2;
}

.dropdown-icon {
  margin-right: 10px;
  font-size: 1.1em;
  color: #606770; /* Color predeterminado para los iconos */
}

/* Color para el icono al hacer hover */
.dropdown-item:hover .dropdown-icon {
  color: #1877f2;
}

/* Estilos específicos para el botón de cerrar sesión dentro del menú */
.dropdown-item.logout-button-in-menu {
  color: #dc3545; /* Color rojo para cerrar sesión */
  border-top: 1px solid #eee; /* Separador */
  margin-top: 8px;
  padding-top: 10px;
}

.dropdown-item.logout-button-in-menu:hover {
  background-color: #fee2e2; /* Fondo rojo claro al pasar el ratón */
  color: #c82333;
}

.dropdown-item.logout-button-in-menu .dropdown-icon {
  color: #dc3545; /* Color rojo para el icono de cerrar sesión */
}

.dropdown-item.logout-button-in-menu:hover .dropdown-icon {
  color: #c82333;
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