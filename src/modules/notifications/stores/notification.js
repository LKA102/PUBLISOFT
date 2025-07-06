// src/stores/notification.js
import { defineStore } from 'pinia';
import { supabase } from '@/services/supabase';
import { useAuthStore } from '@modules/auth/stores/auth'; // Necesitamos el usuario actual

export const useNotificationStore = defineStore('notification', {
  state: () => ({
    notifications: [],
    loading: false,
    error: null,
    // Para la escucha en tiempo real
    supabaseSubscription: null,
  }),
  getters: {
    unreadNotificationsCount: (state) => state.notifications.filter(n => !n.read).length,
  },
  actions: {
    async fetchNotifications(limit = null) {
      this.loading = true;
      this.error = null;
      const authStore = useAuthStore();
      const userId = authStore.user?.id;

      if (!userId) {
        this.error = 'Usuario no autenticado para cargar notificaciones.';
        this.loading = false;
        return;
      }

      try {
        let query = supabase
          .from('notifications')
          .select('*')
          .eq('user_id', userId)
          .order('created_at', { ascending: false });

        if (limit !== null) { // Aplica el límite si se proporciona
          query = query.limit(limit);
        }

        const { data, error } = await query;

        if (error) throw error;
        this.notifications = data;
      } catch (err) {
        this.error = err.message || 'Error al cargar notificaciones.';
        console.error('Error fetching notifications:', err.message);
      } finally {
        this.loading = false;
      }
    },

    async addNotification(notificationData) {
      this.loading = true; // Podrías tener un loading separado para esta acción
      this.error = null;
      try {
        const { error } = await supabase
          .from('notifications')
          .insert([notificationData]); // notificationData debe ser { user_id, sender_id, post_id, type, message }

        if (error) throw error;
        console.log('Notificación insertada exitosamente.');
        // No recargamos aquí inmediatamente, la suscripción en tiempo real se encargará
      } catch (err) {
        this.error = err.message || 'Error al agregar notificación.';
        console.error('Error adding notification:', err.message);
      } finally {
        this.loading = false;
      }
    },

    async markAllAsRead() {
      this.loading = true; // Podrías tener un loading separado
      this.error = null;
      const authStore = useAuthStore();
      const userId = authStore.user?.id;

      if (!userId) {
        this.error = 'Usuario no autenticado para marcar notificaciones.';
        this.loading = false;
        return;
      }

      try {
        const { error } = await supabase
          .from('notifications')
          .update({ read: true, updated_at: new Date().toISOString() }) // Añade updated_at si lo tienes
          .eq('user_id', userId)
          .eq('read', false); // Solo actualiza las no leídas

        if (error) throw error;
        console.log('Todas las notificaciones marcadas como leídas.');
        // Después de marcar como leídas, refresca la lista.
        // Podrías actualizar el estado localmente para una UI más rápida
        this.notifications = this.notifications.map(notif => ({ ...notif, read: true }));
        // O recargar desde la DB si prefieres la consistencia estricta:
        // await this.fetchNotifications();
      } catch (err) {
        this.error = err.message || 'Error al marcar notificaciones como leídas.';
        console.error('Error marking notifications as read:', err.message);
      } finally {
        this.loading = false;
      }
    },

    // --- Funciones para Realtime Notifications ---
    async setupRealtimeNotifications() {
      const authStore = useAuthStore();
      const userId = authStore.user?.id;

      if (!userId) {
        console.warn('No user ID found for realtime notifications setup.');
        return;
      }

      // Si ya hay una suscripción activa, la cerramos primero para evitar duplicados
      if (this.supabaseSubscription) {
        supabase.removeChannel(this.supabaseSubscription);
        this.supabaseSubscription = null;
      }

      console.log(`Setting up realtime notifications for user: ${userId}`);

      this.supabaseSubscription = supabase
        .channel(`notifications:user_id=eq.${userId}`) // Canal específico para el usuario
        .on('postgres_changes',
          { event: 'INSERT', schema: 'public', table: 'notifications', filter: `user_id=eq.${userId}` },
          (payload) => {
            console.log('Nueva notificación en tiempo real:', payload.new);
            // Agrega la nueva notificación al principio del array
            this.notifications.unshift(payload.new);
            // Podrías añadir una vibración o sonido aquí si estás en un contexto de app móvil
          }
        )
        .on('postgres_changes',
          { event: 'UPDATE', schema: 'public', table: 'notifications', filter: `user_id=eq.${userId}` },
          (payload) => {
            console.log('Notificación actualizada en tiempo real:', payload.new);
            // Encuentra y actualiza la notificación existente
            const index = this.notifications.findIndex(n => n.id === payload.new.id);
            if (index !== -1) {
              this.notifications[index] = payload.new;
            }
          }
        )
        .subscribe();
    },

    // Detener la suscripción cuando el store ya no sea necesario (o al cerrar sesión)
    unsubscribeRealtimeNotifications() {
      if (this.supabaseSubscription) {
        supabase.removeChannel(this.supabaseSubscription);
        this.supabaseSubscription = null;
        console.log('Realtime notifications unsubscribed.');
      }
    },
  },
});