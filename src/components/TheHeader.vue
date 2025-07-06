<template>
  <header class="app-header">
    <router-link v-if="showBackButton" :to="backRoute" class="back-to-previous">
      <i class="fas fa-arrow-left"></i> Volver
    </router-link>
    <h2 class="header-title">{{ headerTitle }}</h2>

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
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/modules/auth/stores/auth'; // Ajusta la ruta si es necesario
import { useNotificationStore } from '@/modules/notifications/stores/notification'; // Ajusta la ruta si es necesario

// Definir las props que el componente recibirá
const props = defineProps({
  headerTitle: {
    type: String,
    required: false,
    default: 'PUBLISOFT'
  },
  showBackButton: {
    type: Boolean,
    default: false
  },
  backRoute: {
    type: String,
    default: '/feed' // Ruta predeterminada para el botón de volver
  }
});

const router = useRouter();
const authStore = useAuthStore();
const notificationStore = useNotificationStore();

const dropdownOpen = ref(false);
const showNotifications = ref(false);

const toggleDropdown = () => {
  dropdownOpen.value = !dropdownOpen.value;
};

const toggleNotifications = () => {
  showNotifications.value = !showNotifications.value;
  if (showNotifications.value) {
    notificationStore.fetchNotifications(20);
  }
};

const markAllAsRead = async () => {
  await notificationStore.markAllAsRead();
  notificationStore.fetchNotifications(20);
};

const handleClickOutside = (event) => {
  const dropdown = document.querySelector('.dropdown-container');
  if (dropdown && !dropdown.contains(event.target)) {
    dropdownOpen.value = false;
  }
  const notificationDropdown = document.querySelector('.notification-area');
  if (notificationDropdown && !notificationDropdown.contains(event.target)) {
    showNotifications.value = false;
  }
};

const handleLogout = async () => {
  await authStore.signOut();
  router.push('/auth');
};

onMounted(() => {
  if (authStore.user) {
    notificationStore.setupRealtimeNotifications();
    notificationStore.fetchNotifications(20);
  }
  document.addEventListener('click', handleClickOutside);
});

onUnmounted(() => {
  notificationStore.unsubscribeRealtimeNotifications();
  document.removeEventListener('click', handleClickOutside);
});
</script>

<style scoped>
.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
  padding-bottom: 15px;
  border-bottom: 1px solid #e0e0e0;
  background-color: #fff; /* Fondo blanco para el header */
  padding: 10px 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.back-to-previous {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #1877f2;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.2s ease;
  margin-right: 20px; /* Espacio entre el botón de volver y el título */
}

.back-to-previous:hover {
  color: #155bb5;
}

.back-to-previous i {
  font-size: 1.2em;
}

.header-title {
  color: #333;
  margin: 0 auto; /* Centra el título si no hay botón de volver */
  font-size: 1.8em;
  font-weight: bold;
  flex-grow: 1; /* Permite que el título ocupe el espacio restante */
  text-align: center; /* Alinea el texto del título al centro */
}

.header-actions {
  position: relative;
  display: flex;
  gap: 15px;
  align-items: center;
  margin-left: auto; /* Empuja los elementos de acción a la derecha */
}

/* Notification Area */
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
  background-color: #ff4d4f;
  color: white;
  border-radius: 50%;
  padding: 3px 7px;
  font-size: 0.7em;
  font-weight: bold;
  pointer-events: none;
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
  max-height: 400px;
  overflow-y: auto;
  z-index: 1000;
  padding: 10px;
  margin-top: 10px;
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
  background-color: #e6f7ff;
  font-weight: 600;
}
.notifications-dropdown li small {
  display: block;
  font-size: 0.8em;
  color: #888;
  margin-top: 5px;
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
  background-color: #007bff;
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

/* Dropdown User Profile */
.dropdown-container {
  position: relative;
  display: inline-block;
  cursor: pointer;
  z-index: 100;
}
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
  color: #333;
}
.dropdown-arrow {
  margin-left: 8px;
  transition: transform 0.2s ease;
}
.dropdown-arrow.rotate-180 {
  transform: rotate(180deg);
}
.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  min-width: 180px;
  padding: 8px 0;
  z-index: 100;
  list-style: none;
  margin-top: 8px;
  overflow: hidden;
}
.dropdown-item {
  display: flex;
  align-items: center;
  padding: 10px 15px;
  color: #333;
  text-decoration: none;
  font-size: 0.95em;
  transition: background-color 0.2s ease, color 0.2s ease;
  width: 100%;
  text-align: left;
  border: none;
  background: none;
  cursor: pointer;
}
.dropdown-item:hover {
  background-color: #f0f2f5;
  color: #1877f2;
}
.dropdown-icon {
  margin-right: 10px;
  font-size: 1.1em;
  color: #606770;
}
.dropdown-item:hover .dropdown-icon {
  color: #1877f2;
}
.dropdown-item.logout-button-in-menu {
  color: #dc3545;
  border-top: 1px solid #eee;
  margin-top: 8px;
  padding-top: 10px;
}
.dropdown-item.logout-button-in-menu:hover {
  background-color: #fee2e2;
  color: #c82333;
}
.dropdown-item.logout-button-in-menu .dropdown-icon {
  color: #dc3545;
}
.dropdown-item.logout-button-in-menu:hover .dropdown-icon {
  color: #c82333;
}

/* Mensajes de estado (cargando, error, sin publicaciones) */
.status-message {
  text-align: center;
  color: #666;
  font-style: italic;
  padding: 5px; /* Más compacto para el dropdown */
}
.error-message {
  color: #e53e3e;
  font-weight: bold;
  text-align: center;
  padding: 5px; /* Más compacto para el dropdown */
}
</style>