<template>
  <div class="notifications-page">
   
    <TheHeader
      :showBackButton="true"
      backRoute="/feed"
    />
    <h1>Todas tus Notificaciones</h1>
      <button v-if="notificationStore.notifications.length > 0 && notificationStore.unreadNotificationsCount > 0" @click="markAllAsRead" class="mark-read-button-page">
        Marcar todas como leídas
      </button>
    <div class="notification-list-container">
      <p v-if="notificationStore.loading" class="status-message">Cargando notificaciones...</p>
      <p v-else-if="notificationStore.error" class="error-message">{{ notificationStore.error }}</p>
      <ul v-else-if="notificationStore.notifications.length > 0" class="full-notification-list">
        <li v-for="notif in notificationStore.notifications" :key="notif.id" :class="{ 'unread': !notif.read }" class="notification-item-full">
          <div class="notification-content">
            <p>{{ notif.message }}</p>
            <small>{{ new Date(notif.created_at).toLocaleString('es-ES') }}</small>
          </div>
          <button v-if="!notif.read" @click="markNotificationAsRead(notif.id)" class="mark-single-read">
            <i class="fas fa-check-circle"></i>
          </button>
        </li>
      </ul>
      <p v-else class="status-message">No tienes notificaciones.</p>

      <div v-if="notificationStore.notifications.length > 0 && totalNotifications > itemsPerPage" class="pagination-controls">
        <button @click="prevPage" :disabled="currentPage === 1">Anterior</button>
        <span>Página {{ currentPage }} de {{ totalPages }}</span>
        <button @click="nextPage" :disabled="currentPage === totalPages">Siguiente</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, computed } from 'vue'; // <--- Añade 'computed' aquí
import { useNotificationStore } from '@modules/notifications/stores/notification'; // Asegúrate de que esta ruta sea correcta
import { useAuthStore } from '@modules/auth/stores/auth'; // Necesario para obtener el user_id
import { supabase } from '@/services/supabase'; // Importa supabase para operaciones directas (avatar, updateUser, admin delete)
import TheHeader from '@/components/TheHeader.vue'; // <-- ¡IMPORTA EL NUEVO COMPONENTE DE HEADER!

const notificationStore = useNotificationStore();
const authStore = useAuthStore();

// --- Paginación ---
const currentPage = ref(1);
const itemsPerPage = 10; // Puedes ajustar este número
const totalNotifications = ref(0); // Este valor se obtendrá de la DB

const totalPages = computed(() => Math.ceil(totalNotifications.value / itemsPerPage));

// Función para cargar notificaciones con paginación
const loadNotificationsPage = async () => {
  const userId = authStore.user?.id;
  if (!userId) return;

  notificationStore.loading = true; // Establece el loading
  notificationStore.error = null; // Limpia errores previos

  try {
    // Primero, obtén el conteo total para la paginación
    const { count, error: countError } = await supabase
      .from('notifications')
      .select('*', { count: 'exact', head: true })
      .eq('user_id', userId);

    if (countError) throw countError;
    totalNotifications.value = count;

    // Luego, obtén las notificaciones para la página actual
    const startIndex = (currentPage.value - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage - 1;

    const { data, error } = await supabase
      .from('notifications')
      .select('*')
      .eq('user_id', userId)
      .order('created_at', { ascending: false })
      .range(startIndex, endIndex);

    if (error) throw error;
    notificationStore.notifications = data; // Actualiza las notificaciones en el store (o en un estado local si prefieres)
  } catch (err) {
    notificationStore.error = err.message || 'Error al cargar notificaciones paginadas.';
    console.error('Error loading paginated notifications:', err.message);
  } finally {
    notificationStore.loading = false;
  }
};

// Acciones de paginación
const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--;
    loadNotificationsPage();
  }
};

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++;
    loadNotificationsPage();
  }
};

// --- Acciones de Notificaciones ---
const markAllAsRead = async () => {
  await notificationStore.markAllAsRead();
  loadNotificationsPage(); // Recargar la página actual para reflejar los cambios
};

const markNotificationAsRead = async (notificationId) => {
  try {
    const { error } = await supabase
      .from('notifications')
      .update({ read: true, updated_at: new Date().toISOString() })
      .eq('id', notificationId)
      .eq('user_id', authStore.user?.id); // Asegurar que solo actualiza las propias

    if (error) throw error;
    console.log(`Notificación ${notificationId} marcada como leída.`);
    loadNotificationsPage(); // Recargar la página para reflejar el cambio
  } catch (err) {
    console.error('Error marking single notification as read:', err.message);
  }
};


// --- Ciclo de Vida ---
onMounted(() => {
  // Asegúrate de que el usuario está cargado antes de intentar cargar notificaciones
  if (authStore.user?.id) {
    loadNotificationsPage();
    notificationStore.setupRealtimeNotifications(); // Mantener realtime para nuevas notificaciones
  } else {
    // Si el usuario no está cargado, espera a que el watcher de authStore.user en App.vue lo haga.
    // O puedes añadir un watcher aquí si es estrictamente necesario para esta página.
    watch(() => authStore.user, (newUser) => {
      if (newUser?.id) {
        loadNotificationsPage();
        notificationStore.setupRealtimeNotifications();
      }
    }, { immediate: true });
  }
});

onUnmounted(() => {
  notificationStore.unsubscribeRealtimeNotifications();
});
</script>

<style scoped>
.notifications-page {
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0,0,0,0.05);
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
}

.page-header h1 {
  margin: 0;
  font-size: 1.8em;
  color: #333;
}

.back-to-feed {
  display: flex;
  align-items: center;
  gap: 5px;
  text-decoration: none;
  color: #1877f2;
  font-weight: 500;
  transition: color 0.2s ease;
}

.back-to-feed:hover {
  color: #155bb5;
}

.mark-read-button-page {
  background-color: #28a745; /* Color verde para "marcar como leídas" */
  color: white;
  border: none;
  padding: 8px 15px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 0.9em;
  transition: background-color 0.2s ease;
}

.mark-read-button-page:hover {
  background-color: #218838;
}

.notification-list-container {
  margin-top: 20px;
}

.full-notification-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.notification-item-full {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #f9f9f9;
  padding: 15px;
  margin-bottom: 10px;
  border-radius: 6px;
  border: 1px solid #eee;
  transition: background-color 0.2s ease;
}

.notification-item-full.unread {
  background-color: #e6f7ff; /* Fondo para no leídas */
  border-color: #a7d9f6;
  font-weight: 600;
}

.notification-item-full:hover {
  background-color: #f0f0f0;
}

.notification-item-full.unread:hover {
  background-color: #d1edff;
}

.notification-content p {
  margin: 0 0 5px 0;
  color: #333;
}

.notification-content small {
  color: #666;
  font-size: 0.85em;
}

.mark-single-read {
  background: none;
  border: none;
  color: #28a745;
  cursor: pointer;
  font-size: 1.2em;
  margin-left: 10px;
  transition: color 0.2s ease;
}

.mark-single-read:hover {
  color: #218838;
}

.status-message,
.error-message {
  text-align: center;
  padding: 20px;
  color: #777;
}

.error-message {
  color: #d9534f;
}

.pagination-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
  gap: 15px;
}

.pagination-controls button {
  background-color: #1877f2;
  color: white;
  border: none;
  padding: 8px 15px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.pagination-controls button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.pagination-controls button:hover:not(:disabled) {
  background-color: #155bb5;
}

.pagination-controls span {
  font-weight: 600;
  color: #555;
}
</style>