// src/stores/rating.js
import { defineStore } from 'pinia';
import { supabase } from '@/services/supabase'; // Asegúrate de que esta ruta sea correcta
import { useAuthStore } from '@modules/auth/stores/auth';// Para obtener el user_id
import { usePostStore } from '@modules/posts/stores/post'; // Para refrescar los posts después de calificar

export const useRatingStore = defineStore('rating', {
  state: () => ({
    loading: false,
    error: null,
  }),
  actions: {
    async submitRating(postId, ratingValue) {
      this.loading = true;
      this.error = null;
      const authStore = useAuthStore();
      const postStore = usePostStore(); // Instancia el postStore para refrescar
      const userId = authStore.user?.id;

      if (!userId) {
        this.error = 'Usuario no autenticado.';
        this.loading = false;
        return { success: false, error: this.error };
      }

      try {
        const { data: existingRating, error: fetchError } = await supabase
          .from('ratings')
          .select('*')
          .eq('user_id', userId)
          .eq('post_id', postId)
          .single();

        if (fetchError && fetchError.code !== 'PGRST116') { // PGRST116 means no rows found
          throw fetchError;
        }

        let result;
        if (existingRating) {
          result = await supabase
            .from('ratings')
            .update({ rating: ratingValue, updated_at: new Date().toISOString() })
            .eq('id', existingRating.id);
          console.log(`Rating updated for post ${postId} by user ${userId} to ${ratingValue}`);
        } else {
          result = await supabase
            .from('ratings')
            .insert({ user_id: userId, post_id: postId, rating: ratingValue });
          console.log(`Rating inserted for post ${postId} by user ${userId} with ${ratingValue}`);
        }

        if (result.error) throw result.error;

        // Después de calificar, recargar los posts para que se actualice el promedio
        // y el rating del usuario en el feed.
        await postStore.fetchPosts(); 

        return { success: true, data: result.data };

      } catch (err) {
        this.error = err.message;
        console.error('Error submitting rating:', err.message);
        return { success: false, error: this.error };
      } finally {
        this.loading = false;
      }
    },
    // Estas funciones ya no son estrictamente necesarias aquí porque la función RPC las reemplaza
    // para la carga inicial y el submitRating recarga todos los posts.
    // Sin embargo, si quisieras una actualización más granular, podrías usarlas.
    async fetchUserRatingForPost(postId, userId) {
      if (!userId) return 0;
      try {
        const { data, error } = await supabase
          .from('ratings')
          .select('rating')
          .eq('user_id', userId)
          .eq('post_id', postId)
          .single();

        if (error && error.code !== 'PGRST116') {
          throw error;
        }
        return data ? data.rating : 0;
      } catch (err) {
        console.error('Error fetching user rating:', err.message);
        return 0;
      }
    },
    async fetchAverageRatingForPost(postId) {
      try {
        const { data, error } = await supabase
          .from('ratings')
          .select('rating')
          .eq('post_id', postId);

        if (error) throw error;

        if (data && data.length > 0) {
          const sumRatings = data.reduce((sum, r) => sum + r.rating, 0);
          return parseFloat((sumRatings / data.length).toFixed(1));
        }
        return 0;
      } catch (err) {
        console.error('Error fetching average rating:', err.message);
        return 0;
      }
    }
  },
});