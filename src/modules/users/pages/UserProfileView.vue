<template>
  <div class="profile-page">

    <section v-if="loadingProfile" class="status-message">
      Cargando perfil...
    </section>
    <section v-else-if="profileError" class="error-message">
      Error al cargar el perfil: {{ profileError }}
    </section>
    <section v-else-if="!userProfile" class="status-message">
      Usuario no encontrado.
    </section>
    <section v-else class="profile-details">
      <h2>Información de {{ userProfile.alias || userProfile.email }}</h2>
      <div class="avatar-section">
        <img
          :src="userProfile.avatar_url || 'https://via.placeholder.com/150/CCCCCC/FFFFFF?text=AV'"
          :alt="`Avatar de ${userProfile.alias || userProfile.email}`"
          class="profile-main-avatar"
        />
      </div>

      <div class="profile-info-group">
        <p><strong>Email:</strong> {{ userProfile.email }}</p>
        <p><strong>Rol:</strong> {{ userProfile.role || 'No especificado' }}</p>
      </div>

      <section class="user-posts-section">
        <h2>Publicaciones de {{ userProfile.alias || userProfile.email }}</h2>
        <p v-if="loadingPosts" class="status-message">Cargando publicaciones...</p>
        <p v-else-if="postsError" class="error-message">Error al cargar publicaciones: {{ postsError }}</p>
        <p v-else-if="userPosts.length === 0" class="status-message">Este usuario aún no tiene publicaciones.</p>
        <div v-else class="post-list">
          <div v-for="post in userPosts" :key="post.id" class="post-item">
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
            <div v-if="post.file_url" class="file-download-action">
  <a :href="post.file_url" target="_blank" rel="noopener noreferrer" class="download-button">
    <i class="fas fa-download"></i> Descargar Archivo Completo
  </a>
</div>
             <RatingStars
          :post-id="post.id"
          :initial-average-rating="post.average_rating"
          :initial-user-rating="post.user_rating"
        />

            </div>
        </div>
      </section>
    </section>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { supabase } from '@/services/supabase';
import TheHeader from '@/components/TheHeader.vue';
import RatingStars from '@modules/ranking/components/RatingStars.vue'
import { useAuthStore } from '@/modules/auth/stores/auth';

const route = useRoute();
const authStore = useAuthStore();

const userProfile = ref(null);
const loadingProfile = ref(true);
const profileError = ref(null);

const userPosts = ref([]);
const loadingPosts = ref(true);
const postsError = ref(null);

const currentUserId = ref(null);

const fetchUserProfile = async (userId) => {
  loadingProfile.value = true;
  profileError.value = null;
  userProfile.value = null;

  if (!userId) {
    profileError.value = 'ID de usuario no proporcionado.';
    loadingProfile.value = false;
    return;
  }

  try {
    const { data: profileData, error: profileFetchError } = await supabase
      .from('users')
      .select('id, email, alias, avatar_url, role')
      .eq('id', userId)
      .single();

    if (profileFetchError) throw profileFetchError;

    userProfile.value = profileData;

  } catch (err) {
    profileError.value = err.message || 'Error desconocido al cargar la información del perfil.';
    console.error('Error fetching user profile:', err);
  } finally {
    loadingProfile.value = false;
  }
};

const fetchUserPosts = async (userId) => {
  loadingPosts.value = true;
  postsError.value = null;
  userPosts.value = [];

  if (!userId) {
    postsError.value = 'ID de usuario no proporcionado para publicaciones.';
    loadingPosts.value = false;
    return;
  }

  try {
    const { data: postsData, error: postsFetchError } = await supabase
      .from('posts')
      .select(`
        *,
        users (alias, email, avatar_url, role),
        ratings (rating, user_id)
      `)
      .eq('user_id', userId)
      .order('created_at', { ascending: false });

    if (postsFetchError) throw postsFetchError;

    userPosts.value = postsData.map(post => {
      const totalRating = post.ratings ? post.ratings.reduce((sum, r) => sum + r.rating, 0) : 0;
      const averageRating = post.ratings && post.ratings.length > 0 ? totalRating / post.ratings.length : 0;
      
      const userRating = post.ratings ? post.ratings.find(r => r.user_id === currentUserId.value)?.rating : null;

      return {
        ...post,
        average_rating: averageRating,
        user_rating: userRating
      };
    });

  } catch (err) {
    postsError.value = err.message || 'Error desconocido al cargar las publicaciones.';
    console.error('Error fetching user posts:', err);
  } finally {
    loadingPosts.value = false;
  }
};

// --- NUEVA FUNCIÓN PARA MANEJAR LA ACTUALIZACIÓN DE CALIFICACIÓN ---
const handleRatingUpdated = async (postId) => {
  // Cuando una calificación se actualiza en RatingStars, volvemos a cargar las publicaciones
  // para reflejar los cambios en el promedio y la calificación del usuario.
  console.log(`Rating updated for post ID: ${postId}. Re-fetching user posts...`);
  await fetchUserPosts(route.params.userId);
};


watch(() => route.params.userId, async (newUserId) => {
  if (newUserId) {
    if (!currentUserId.value) {
      currentUserId.value = authStore.user?.id;
    }
    await Promise.all([
      fetchUserProfile(newUserId),
      fetchUserPosts(newUserId)
    ]);
  }
}, { immediate: true });

const isImage = (fileType) => {
  if (!fileType) return false;
  const lowerCaseType = fileType.toLowerCase();
  return ['image/jpeg', 'image/png', 'image/gif', 'image/bmp', 'image/webp', 'jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'].includes(lowerCaseType);
};

const isPdf = (fileType) => {
  if (!fileType) return false;
  return fileType.toLowerCase() === 'application/pdf' || fileType.toLowerCase() === 'pdf';
};

onMounted(async () => {
  if (authStore.user) {
    currentUserId.value = authStore.user.id;
  } else {
    console.warn('No user logged in. Rating functionality might be limited.');
  }
});
</script>

<style scoped>
/* Tu CSS actual está bien para el average_rating y los estilos. */
/* Asegúrate de que RatingStars también tenga un width/height adecuado para mostrarse */
/* Si el div .post-rating debajo de RatingStars está duplicando la visualización,
   puedes comentarlo o eliminarlo como se muestra en el template. */
/* ... (Mantén todos tus estilos existentes sin cambios aquí) ... */

/* Estilos generales de la página de perfil de usuario */
.profile-page {
  max-width: 900px;
  margin: 20px auto;
  padding: 20px;
  background-color: #f0f2f5;
  min-height: calc(100vh - 40px); /* Ajusta para el padding */
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0,0,0,0.05);
}

.profile-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #fff;
  padding: 10px 20px;
  border-radius: 8-x;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.profile-header h1 {
  color: #1877f2;
  margin: 0;
  font-size: 1.8em;
}

.back-to-feed {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #1877f2;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.2s ease;
}

.back-to-feed:hover {
  color: #155bb5;
}

.back-to-feed i {
  font-size: 1.2em;
}

.profile-details {
  background-color: #fff;
  padding: 25px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
  text-align: center; /* Centra el avatar y la info */
}

/* Sección de acción de descarga */
.file-download-action {
  text-align: center;
  margin-top: 20px; /* Espacio superior para separarlo de la previsualización */
  padding-top: 15px; /* Padding superior para el botón */
  border-top: 1px solid #eee; /* Línea divisoria */
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
.profile-details h2 {
  color: #333;
  margin-top: 0;
  margin-bottom: 25px;
  font-size: 1.6em;
}

.avatar-section {
  position: relative;
  width: 150px;
  height: 150px;
  margin: 0 auto 20px auto; /* Centra el avatar */
}

.profile-main-avatar {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
  border: 4px solid #1877f2;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.profile-info-group {
    margin-bottom: 20px;
}

.profile-info-group p {
  font-size: 1.1em;
  color: #444;
  margin-bottom: 10px;
}

.profile-info-group strong {
  color: #222;
}

.status-message {
  text-align: center;
  padding: 20px;
  color: #777;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.error-message {
  color: #dc3545;
  text-align: center;
  padding: 20px;
  background-color: #fff0f0;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* Estilos para la sección de publicaciones del usuario (adaptados del feed/profile) */
.user-posts-section {
  background-color: #fff;
  padding: 25px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-top: 20px; /* Separación de la info del perfil */
}

.user-posts-section h2 {
  color: #333;
  margin-bottom: 20px;
  font-size: 1.6em;
  text-align: center;
}

.post-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
/* Estilos para un post individual dentro de la lista (copia de FeedPage) */
.post-item {
  background-color: #ffffff;
  border-radius: 10px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  padding: 20px;
  border: 1px solid #eee;
}

.post-header {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

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

.post-file-preview-container {
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid #eee;
  text-align: center;
}

.file-preview-image {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  margin-bottom: 10px;
}

.file-preview-pdf {
  border: 1px solid #ddd;
  border-radius: 8px;
  width: 100%;
  min-height: 300px;
  max-height: 600px;
}

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

.post-rating {
  margin-top: 15px;
  font-size: 0.95em;
  color: #555;
  display: flex;
  align-items: center;
  gap: 5px;
}

.rating-value {
  font-weight: bold;
  color: #222;
}

.star-icon {
  font-size: 1.2em;
}
</style>