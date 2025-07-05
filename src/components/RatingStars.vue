<template>
  <div class="rating-container">
    <div class="average-rating" v-if="averageRating !== null && averageRating > 0">
      <span class="average-value">{{ averageRating.toFixed(1) }}</span>
      <span class="star-icon material-symbols-fill">star</span>
    </div>

    <div class="user-rating-stars">
      <span
        v-for="star in 5"
        :key="star"
        @click="emitRating(star)"
        :class="{
          'star-icon': true,
          'filled': star <= (hoverRating || internalUserRating),
          'interactive': isAuthenticated
        }"
        @mouseover="isAuthenticated && (hoverRating = star)"
        @mouseleave="isAuthenticated && (hoverRating = 0)"
      >
        <template v-if="star <= (hoverRating || internalUserRating)">&#xe838;</template>
        <template v-else>&#xe838;</template>
      </span>
      <span v-if="!isAuthenticated" class="rating-login-prompt">
        Inicia sesión para calificar
      </span>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { useRatingStore } from '@/stores/rating';

const props = defineProps({
  postId: {
    type: String,
    required: true,
  },
  initialAverageRating: {
    type: Number,
    default: 0,
  },
  initialUserRating: {
    type: Number,
    default: 0,
  },
});

const authStore = useAuthStore();
const ratingStore = useRatingStore();

const averageRating = ref(props.initialAverageRating);
const internalUserRating = ref(props.initialUserRating);
const hoverRating = ref(0);
const isAuthenticated = ref(false);

const emitRating = async (rating) => {
  if (!isAuthenticated.value) return;

  const newRatingValue = internalUserRating.value === rating ? 0 : rating;
  
  // Optimistic UI update (se asume que tendrá éxito)
  const oldUserRating = internalUserRating.value;
  internalUserRating.value = newRatingValue;

  const { success } = await ratingStore.submitRating(props.postId, newRatingValue);

  if (!success) {
    // Si hubo un error, revertir la UI
    internalUserRating.value = oldUserRating;
    console.error('Error al calificar: La calificación no se pudo guardar.');
    // Podrías añadir un `alert` o un toast aquí
  }
  // No necesitamos actualizar `averageRating.value` aquí directamente
  // porque `ratingStore.submitRating` ya llama a `postStore.fetchPosts()`
  // lo que hará que el `Feed.vue` se actualice y pase los nuevos props a este componente.
};

const checkAuthAndSetInitialRatings = () => {
  isAuthenticated.value = !!authStore.user;
  // Estos valores se reciben del postStore, que ya los trae de la función RPC
  averageRating.value = props.initialAverageRating;
  internalUserRating.value = props.initialUserRating;
};

onMounted(checkAuthAndSetInitialRatings);
watch([() => authStore.user, () => props.initialAverageRating, () => props.initialUserRating], checkAuthAndSetInitialRatings);

</script>

<style scoped>
/* Asegúrate de que esta URL esté accesible o de incluir Material Symbols globalmente */
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');

.rating-container {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-top: 10px;
  margin-bottom: 5px;
  color: #555;
  font-size: 1.1em;
}

.average-rating {
  display: flex;
  align-items: center;
  font-weight: bold;
  color: #f8c100;
}

.average-value {
  margin-right: 5px;
  font-size: 1.2em;
}

.star-icon {
  font-family: 'Material Symbols Rounded', sans-serif;
  font-weight: normal;
  font-style: normal;
  font-size: 24px;
  line-height: 1;
  letter-spacing: normal;
  text-transform: none;
  display: inline-block;
  white-space: nowrap;
  word-wrap: normal;
  direction: ltr;
  -webkit-font-feature-settings: 'liga';
  -webkit-font-smoothing: antialiased;
  cursor: default;

  font-variation-settings:
    'FILL' 0,
    'wght' 400,
    'GRAD' 0,
    'opsz' 24;
  color: #ccc;
  transition: color 0.2s ease, font-variation-settings 0.2s ease;
}

.star-icon.filled {
  font-variation-settings:
    'FILL' 1,
    'wght' 500,
    'GRAD' 0,
    'opsz' 24;
  color: #ffc107;
}

.star-icon.interactive {
  cursor: pointer;
}

.star-icon.interactive:hover {
  transform: scale(1.1);
}

.user-rating-stars .star-icon.interactive:hover ~ .star-icon.interactive {
  font-variation-settings:
    'FILL' 0,
    'wght' 400;
  color: #ccc;
}

.user-rating-stars .star-icon.interactive:hover,
.user-rating-stars .star-icon.interactive:hover + .star-icon.interactive {
  font-variation-settings:
    'FILL' 1,
    'wght' 500;
  color: #ffc107;
}

.rating-login-prompt {
  font-size: 0.85em;
  color: #777;
  margin-left: 10px;
}
</style>