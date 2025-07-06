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
        <template v-if="star <= (hoverRating || internalUserRating)">&#xe838;</template> <template v-else>&#xe83a;</template> </span>
      <span v-if="!isAuthenticated" class="rating-login-prompt">
        Inicia sesión para calificar
      </span>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useAuthStore } from '@modules/auth/stores/auth';
import { useRatingStore } from '@modules/ranking/stores/rating';

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
  
  // Optimistic UI update
  const oldUserRating = internalUserRating.value;
  internalUserRating.value = newRatingValue;

  const { success } = await ratingStore.submitRating(props.postId, newRatingValue);

  if (!success) {
    // If there was an error, revert the UI
    internalUserRating.value = oldUserRating;
    console.error('Error al calificar: La calificación no se pudo guardar.');
    // You could add an `alert` or a toast here
  }
  // The `postStore.fetchPosts()` call in `submitRating` will cause the parent
  // `Feed.vue` to re-render, passing down the new `initialUserRating` and `initialAverageRating`
  // props, which will be picked up by the `watch` below.
};

const checkAuthAndSetInitialRatings = () => {
  isAuthenticated.value = !!authStore.user;
  // These values are received from the postStore, which already fetches them
  // from the RPC function.
  averageRating.value = props.initialAverageRating;
  internalUserRating.value = props.initialUserRating;
};

onMounted(checkAuthAndSetInitialRatings);

// Watch for changes in authStore.user, initialAverageRating, and initialUserRating props
// This ensures the component reacts to updates from the parent after `fetchPosts` runs.
watch(
  [() => authStore.user, () => props.initialAverageRating, () => props.initialUserRating],
  ([newUser, newAverageRating, newUserRating]) => {
    isAuthenticated.value = !!newUser;
    averageRating.value = newAverageRating;
    internalUserRating.value = newUserRating;
  },
  { immediate: true } // Run the watcher immediately on component mount
);
</script>

<style scoped>
/* Make sure this URL is accessible or include Material Symbols globally */
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
    'FILL' 0, /* Default for unfilled stars */
    'wght' 400,
    'GRAD' 0,
    'opsz' 24;
  color: #ccc; /* Default color for unfilled stars */
  transition: color 0.2s ease, font-variation-settings 0.2s ease;
}

.star-icon.filled {
  font-variation-settings:
    'FILL' 1, /* Filled state */
    'wght' 500,
    'GRAD' 0,
    'opsz' 24;
  color: #ffc107; /* Color for filled stars */
}

.star-icon.interactive {
  cursor: pointer;
}

.star-icon.interactive:hover {
  transform: scale(1.1);
}

/* Hover effect for interactive stars */
.user-rating-stars .star-icon.interactive:hover,
.user-rating-stars .star-icon.interactive:hover ~ .star-icon.interactive {
  font-variation-settings:
    'FILL' 1,
    'wght' 500;
  color: #ffc107;
}

/* Reset hover effect for stars *after* the one being hovered */
.user-rating-stars .star-icon.interactive:hover ~ .star-icon.interactive {
  font-variation-settings:
    'FILL' 0,
    'wght' 400;
  color: #ccc;
}


.rating-login-prompt {
  font-size: 0.85em;
  color: #777;
  margin-left: 10px;
}
</style>