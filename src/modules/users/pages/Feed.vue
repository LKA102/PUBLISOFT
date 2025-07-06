<template>
  <div class="feed-page">
    <header class="feed-header">
      <h2 class="header-title">PUBLISOFT</h2>

      <div class="header-actions">
        <div class="notification-area">
          <button @click="toggleNotifications" class="notification-icon">
            <i class="fas fa-bell"></i>
            <span v-if="notificationStore.unreadNotificationsCount > 0" class="notification-badge">
              {{ notificationStore.unreadNotificationsCount }}
            </span>
          </button>
          <div v-if="showNotifications" class="notifications-dropdown">
            <p v-if="notificationStore.loading" class="status-message">Cargando notificaciones...</p>
            <p v-else-if="notificationStore.error" class="error-message">{{ notificationStore.error }}</p>
            <ul v-else-if="notificationStore.notifications.length > 0">
              <li v-for="notif in notificationStore.notifications" :key="notif.id" :class="{ 'unread': !notif.read }">
                {{ notif.message }}
                <br>
                <small>{{ new Date(notif.created_at).toLocaleString('es-ES') }}</small>
              </li>
            </ul>
            <p v-else class="status-message">No hay notificaciones.</p>

            <router-link to="/notifications" class="view-all-notifications-button">
              Ver todas las notificaciones ({{ notificationStore.notifications.length }} mostradas)
            </router-link>

            <button v-if="notificationStore.notifications.length > 0 && notificationStore.unreadNotificationsCount > 0"
                    @click="markAllAsRead" class="mark-read-button">
              Marcar todas como leídas
            </button>
          </div>
        </div>
        <div v-if="authStore.user" class="dropdown-container" @click="toggleDropdown">
          <button class="profile-dropdown-toggle">
            <img
              :src="authStore.user?.avatar_url || 'https://via.placeholder.com/40/CCCCCC/FFFFFF?text=AV'"
              alt="Avatar del usuario"
              class="profile-avatar"
            />
            <span class="profile-alias">
              {{ authStore.user?.alias || 'Mi Perfil' }}
            </span>
            <i class="fas fa-caret-down dropdown-arrow" :class="{ 'rotate-180': dropdownOpen }"></i>
          </button>

          <div v-if="dropdownOpen" class="dropdown-menu">
            <router-link to="/profile" class="dropdown-item">
              <i class="fas fa-user-circle dropdown-icon"></i> Mi Perfil
            </router-link>
            <router-link to="/ranking" class="dropdown-item">
              <i class="fas fa-trophy dropdown-icon"></i> Ranking
            </router-link>
            <button @click="handleLogout" :disabled="authStore.loading" class="dropdown-item logout-button-in-menu">
              <i class="fas fa-sign-out-alt dropdown-icon"></i> Cerrar Sesión
            </button>
          </div>
        </div>
      </div>
    </header>

    <PostUpload />
    <p v-if="postStore.loading" class="status-message">Cargando publicaciones...</p>
    <p v-else-if="postStore.error" class="error-message">Error al cargar publicaciones: {{ postStore.error }}</p>
    <p v-else-if="postStore.posts.length === 0" class="status-message">No hay publicaciones disponibles.</p>
    <div v-else class="post-list">
      <div v-for="post in postStore.posts" :key="post.id" class="post-item">
        <div class="post-header">
          <img
            :src="post.users?.avatar_url || 'https://via.placeholder.com/40/CCCCCC/FFFFFF?text=AV'"
            alt="Avatar del autor"
            class="post-avatar"
          />
          <div class="post-info">
            <span class="post-author">
              {{ post.users ? post.users.alias || post.users.email : 'Usuario Desconocido' }}
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
import { onMounted, ref } from 'vue'; // Importa 'ref'
import { usePostStore } from '@modules/posts/stores/post';
import { useAuthStore } from '@modules/auth/stores/auth';
import { useRouter } from 'vue-router';

import PostUpload from '@modules/posts/components/PostUpload.vue'
import RatingStars from '@modules/ranking/components/RatingStars.vue'
import { useNotificationStore } from '@modules/notifications/stores/notification'; // Asegúrate de que esta ruta sea correcta

const postStore = usePostStore();
const authStore = useAuthStore();
const router = useRouter();
const notificationStore = useNotificationStore(); // INSTANCIAR EL STORE

const dropdownOpen = ref(false); // Estado para controlar la visibilidad del desplegable
// --- Estados Locales para Notificaciones ---
const showNotifications = ref(false); // PARA CONTROLAR LA VISIBILIDAD DEL DROPDOWN DE NOTIFICACIONES

const toggleDropdown = () => {
  dropdownOpen.value = !dropdownOpen.value;
};

// --- Funciones de Notificaciones ---
const toggleNotifications = () => {
  showNotifications.value = !showNotifications.value;
  if (showNotifications.value) {
    // Cargar un máximo de 20 notificaciones para el dropdown
    notificationStore.fetchNotifications(20);
  }
};

const markAllAsRead = async () => {
  await notificationStore.markAllAsRead();
  // Después de marcar como leídas, recargamos con el límite del dropdown
  notificationStore.fetchNotifications(20);
};


// Cierra el desplegable si se hace clic fuera
const handleClickOutside = (event) => {
  const dropdown = document.querySelector('.dropdown-container');
  if (dropdown && !dropdown.contains(event.target)) {
    dropdownOpen.value = false;
  }
};

const handleLogout = async () => {
  await authStore.signOut();
  router.push('/login');
};

// --- Ciclo de Vida ---
onMounted(async () => {
  if (authStore.user) {
    await postStore.fetchPosts();
    // Iniciar las notificaciones en tiempo real al cargar el feed
    notificationStore.setupRealtimeNotifications();
    // Opcional: cargar las notificaciones iniciales para el badge (sin el dropdown abierto)
    await notificationStore.fetchNotifications(20); // Carga inicial para el contador
  }
});

onUnmounted(() => {
  // Asegúrate de desuscribirte de las notificaciones al salir del Feed
  notificationStore.unsubscribeRealtimeNotifications();
});

const isImage = (fileType) => {
  if (!fileType) return false;
  const lowerCaseType = fileType.toLowerCase();
  return ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'].includes(lowerCaseType);
};

const isPdf = (fileType) => {
  if (!fileType) return false;
  return fileType.toLowerCase() === 'pdf';
};

onMounted(async () => {
  await authStore.fetchUserProfile(authStore.user?.id); 
  await postStore.fetchPosts();
  // Agrega el event listener al montar el componente
  document.addEventListener('click', handleClickOutside);
});

// Limpia el event listener al desmontar el componente
import { onUnmounted } from 'vue';
onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
});
</script>

<style scoped>
/* Mantén tus estilos existentes y agrega/modifica estos */

/* Estilos generales del contenedor principal */
.feed-page {
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
  background-color: #f0f2f5;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0,0,0,0.05);
}


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