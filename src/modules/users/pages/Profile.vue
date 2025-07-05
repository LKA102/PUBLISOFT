<template>
  <div class="profile-page">
    <header class="profile-header">
      <router-link to="/feed" class="back-to-feed">
        <i class="fas fa-arrow-left"></i> Volver al Feed
      </router-link>
      <h1>Mi Perfil</h1>
      <div class="notification-area">
        <button @click="toggleNotifications" class="notification-icon">
          <i class="fas fa-bell"></i>
          <span v-if="unreadNotificationsCount > 0" class="notification-badge">
            {{ unreadNotificationsCount }}
          </span>
        </button>
        <div v-if="showNotifications" class="notifications-dropdown">
          <p v-if="notificationStore.loading">Cargando notificaciones...</p>
          <p v-else-if="notificationStore.error" class="error-message">{{ notificationStore.error }}</p>
          <ul v-else-if="notificationStore.notifications.length > 0">
            <li v-for="notif in notificationStore.notifications" :key="notif.id" :class="{ 'unread': !notif.read }">
              {{ notif.message }}
              <br>
              <small>{{ new Date(notif.created_at).toLocaleString('es-ES') }}</small>
            </li>
          </ul>
          <p v-else class="status-message">No hay notificaciones.</p>
          <button v-if="notificationStore.notifications.length > 0 && unreadNotificationsCount > 0" @click="markAllAsRead" class="mark-read-button">
            Marcar todas como leídas
          </button>
        </div>
      </div>
    </header>

    <section class="profile-details">
      <h2>Información del Perfil</h2>
      <div class="avatar-section">
        <img
          :src="authStore.user?.avatar_url || 'https://via.placeholder.com/150/CCCCCC/FFFFFF?text=AV'"
          alt="Avatar del usuario"
          class="profile-main-avatar"
        />
        <button @click="openAvatarUpload" class="edit-avatar-button">
          <i class="fas fa-camera"></i>
        </button>
        <input type="file" ref="avatarFileInput" @change="handleAvatarChange" accept="image/*" style="display: none;">
      </div>

      <div class="profile-info-group">
        <p><strong>Email:</strong> {{ authStore.user?.email }}</p>
        <p><strong>Rol:</strong> {{ authStore.user?.role || 'Cargando...' }}</p>
        <p v-if="authStore.user?.student_code"><strong>Código de Alumno:</strong> {{ authStore.user.student_code }}</p>
      </div>

      <div class="edit-profile-section">
        <h3>Editar Perfil</h3>
        <form @submit.prevent="updateProfile">
          <div class="form-group">
            <label for="edit-alias">Alias:</label>
            <input type="text" id="edit-alias" v-model="editableAlias" class="profile-input" required />
          </div>
          <div class="form-group">
            <label for="edit-password">Nueva Contraseña:</label>
            <input type="password" id="edit-password" v-model="newPassword" placeholder="Dejar en blanco para no cambiar" class="profile-input" />
          </div>
          <button type="submit" :disabled="authStore.loading" class="save-profile-button">
            {{ authStore.loading ? 'Guardando...' : 'Guardar Cambios' }}
          </button>
          <p v-if="updateError" class="error-message">{{ updateError }}</p>
          <p v-if="updateSuccess" class="success-message">{{ updateSuccess }}</p>
        </form>
      </div>
    </section>

    <section class="my-posts-section">
  <h2>Mis Publicaciones</h2>
  <p v-if="postStore.loading" class="status-message">Cargando mis publicaciones...</p>
  <p v-else-if="postStore.error" class="error-message">Error al cargar mis publicaciones: {{ postStore.error }}</p>
  <p v-else-if="myPosts.length === 0" class="status-message">Aún no tienes publicaciones.</p>
  <div v-else class="post-list">
    <div v-for="post in myPosts" :key="post.id" class="post-item">
      <div class="post-header">
        <img :src="post.users?.avatar_url || 'https://via.placeholder.com/40/CCCCCC/FFFFFF?text=AV'" alt="Avatar" class="post-avatar">
        <div class="post-info">
          <span class="post-author">
            {{ post.users ? post.users.alias || post.users.email : 'Usuario Desconocido' }}
          </span>
          <span class="post-date">
            {{ new Date(post.created_at).toLocaleDateString('es-ES', { day: '2-digit', month: 'long', year: 'numeric' }) }}
          </span>
        </div>
        <div class="post-actions" v-if="authStore.user?.id === post.user_id">
          <button @click="editPost(post.id)" class="action-button edit-button" title="Editar Publicación"><i class="fas fa-edit"></i></button>
          <button @click="confirmDeletePost(post.id)" class="action-button delete-button" title="Eliminar Publicación"><i class="fas fa-trash"></i></button>
        </div>
      </div>
      <h4 class="post-title"><strong>{{ post.title }}</strong></h4>
      <p class="post-detail"><strong>Curso:</strong> {{ post.course }}</p>
      <p class="post-detail"><strong>Ciclo:</strong> {{ post.cycle }}</p>

      <div v-if="post.average_rating !== undefined" class="post-rating">
        <strong>Estrellas:</strong>
        <span class="rating-value">
          {{ post.average_rating ? post.average_rating.toFixed(1) : 'Sin calificación' }}
        </span>
        <span v-if="post.average_rating" class="star-icon">⭐</span>
      </div>

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

    </div>
  </div>
</section>

    <section v-if="authStore.user?.role === 'admin'" class="admin-section">
      <h2>Gestión de Estudiantes</h2>
      <p v-if="!allStudents || allStudents.length === 0" class="status-message">No hay estudiantes registrados.</p>
      <div v-else class="student-list">
        <ul>
          <li v-for="student in allStudents" :key="student.id" class="student-item">
            <span>
              {{ student.alias || student.email }}
              <span v-if="student.student_code">(Código: {{ student.student_code }})</span>
            </span>
            <button @click="confirmDeleteStudent(student.id)" class="delete-student-button">Eliminar</button>
          </li>
        </ul>
      </div>
      <p v-if="deleteStudentError" class="error-message">{{ deleteStudentError }}</p>
      <p v-if="deleteStudentSuccess" class="success-message">{{ deleteStudentSuccess }}</p>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useAuthStore } from '@modules/auth/stores/auth';
import { usePostStore } from '@modules/posts/stores/post';
import { supabase } from '@/services/supabase'; // Importa supabase para operaciones directas (avatar, updateUser, admin delete)

// --- Stores ---
const authStore = useAuthStore();
const postStore = usePostStore();

// --- Estados Locales para Edición de Perfil ---
const editableAlias = ref('');
const newPassword = ref('');
const updateError = ref(null);
const updateSuccess = ref(null);
const avatarFileInput = ref(null); // Ref para el input de archivo oculto

// --- Estados Locales para Notificaciones ---
const showNotifications = ref(false);
// Usaremos un store específico para notificaciones (a crear si no existe)
// Por ahora, lo simularé con un 'mock' si no lo tienes.
const notificationStore = {
  notifications: ref([]),
  loading: ref(false),
  error: ref(null),
  async fetchNotifications() {
    this.loading.value = true;
    this.error.value = null;
    try {
      // Asegúrate de que tu tabla 'notifications' exista en Supabase
      // y que tenga una columna 'user_id' y 'read'.
      const { data, error } = await supabase
        .from('notifications')
        .select('*')
        .eq('user_id', authStore.user.id)
        .order('created_at', { ascending: false });

      if (error) throw error;
      this.notifications.value = data;
    } catch (err) {
      this.error.value = err.message || 'Error al cargar notificaciones.';
      console.error('Error fetching notifications:', err.message);
    } finally {
      this.loading.value = false;
    }
  },
  async markAllAsRead() {
    try {
      const { error } = await supabase
        .from('notifications')
        .update({ read: true })
        .eq('user_id', authStore.user.id)
        .eq('read', false); // Solo actualiza las no leídas

      if (error) throw error;
      await this.fetchNotifications(); // Volver a cargar para actualizar UI
    } catch (err) {
      this.error.value = err.message || 'Error al marcar notificaciones como leídas.';
      console.error('Error marking notifications as read:', err.message);
    }
  }
};

const unreadNotificationsCount = computed(() => {
  return notificationStore.notifications.value.filter(n => !n.read).length;
});

// --- Estados Locales para Gestión de Estudiantes (Admin) ---
const allStudents = ref([]);
const deleteStudentError = ref(null);
const deleteStudentSuccess = ref(null);

// --- Propiedades Computadas ---
const myPosts = computed(() => {
  if (postStore.posts && authStore.user) {
    // Filtramos las publicaciones del store general por el ID del usuario actual
    return postStore.posts.filter(post => post.user_id === authStore.user.id);
  }
  return [];
});

// --- Watchers ---
// Inicializar editableAlias cuando el usuario esté disponible
watch(() => authStore.user, (newUser) => {
  if (newUser?.alias) {
    editableAlias.value = newUser.alias;
  }
}, { immediate: true }); // 'immediate: true' para que se ejecute en la carga inicial

// --- Ciclo de Vida ---
onMounted(async () => {
  // Asegurarse de que el perfil del usuario esté completamente cargado
  // Esto es crucial para que 'alias', 'avatar_url', 'role' estén disponibles
  try {
    const { data: { user: currentUser } } = await supabase.auth.getUser();
    if (currentUser) {
      await authStore.fetchUserProfile(currentUser.id);
    }
  } catch (err) {
    console.error('Error al obtener usuario actual o perfil en Mount:', err.message);
    // Podrías redirigir a login si es un error crítico
  }

  // Cargar publicaciones (todas, luego las filtramos con 'myPosts')
  // Si tienes muchas publicaciones, considera una acción en postStore para 'fetchUserPosts'
  postStore.fetchPosts();

  // Cargar notificaciones
  if (authStore.user) { // Asegurarse de que hay un usuario logueado
    await notificationStore.fetchNotifications();
  }

  // Cargar todos los estudiantes si el usuario es administrador
  if (authStore.user?.role === 'admin') {
    await fetchAllStudents();
  }
});

// --- Funciones de Edición de Perfil ---
const updateProfile = async () => {
  updateError.value = null;
  updateSuccess.value = null;
  authStore.loading = true; // Usa el estado de carga del store de autenticación

  try {
    let profileUpdated = false;
    let authUserUpdated = false;

    // 1. Actualizar Alias en la tabla 'users'
    if (editableAlias.value !== authStore.user?.alias) {
      const { error: profileError } = await supabase
        .from('users')
        .update({ alias: editableAlias.value })
        .eq('id', authStore.user.id);

      if (profileError) throw new Error(`Error al actualizar alias: ${profileError.message}`);
      profileUpdated = true;
    }

    // 2. Actualizar Contraseña en Supabase Auth
    if (newPassword.value) {
      const { error: authError } = await supabase.auth.updateUser({
        password: newPassword.value,
      });
      if (authError) throw new Error(`Error al actualizar contraseña: ${authError.message}`);
      authUserUpdated = true;
    }

    if (profileUpdated || authUserUpdated) {
      // Si algo se actualizó, refrescar los datos del usuario en el store
      await authStore.fetchUserProfile(authStore.user.id);
      updateSuccess.value = 'Perfil actualizado exitosamente.';
      newPassword.value = ''; // Limpiar el campo de contraseña
    } else {
      updateSuccess.value = 'No se realizaron cambios en el perfil.';
    }

  } catch (err) {
    updateError.value = err.message || 'Error desconocido al actualizar perfil.';
    console.error('Error updating profile:', err);
  } finally {
    authStore.loading = false;
  }
};

const openAvatarUpload = () => {
  avatarFileInput.value.click(); // Simula un clic en el input de tipo file oculto
};

const handleAvatarChange = async (event) => {
  const file = event.target.files[0];
  if (!file) return;

  updateError.value = null;
  updateSuccess.value = null;
  authStore.loading = true;

  try {
    const fileExt = file.name.split('.').pop();
    // Path único para el avatar en el storage (ej. 'user_id/timestamp.ext')
    const filePath = `${authStore.user.id}/${Date.now()}.${fileExt}`;

    // Subir el archivo al bucket 'avatars'
    const { error: uploadError } = await supabase.storage
      .from('avatars') // Asegúrate de que este sea el nombre de tu bucket
      .upload(filePath, file, {
        cacheControl: '3600', // Caching por una hora
        upsert: true, // Sobrescribe si el archivo ya existe
      });

    if (uploadError) throw new Error(`Error al subir avatar: ${uploadError.message}`);

    // Obtener la URL pública del avatar subido
    const { data: publicUrlData } = supabase.storage
      .from('avatars')
      .getPublicUrl(filePath);

    const newAvatarUrl = publicUrlData.publicUrl;

    // Actualizar la columna 'avatar_url' en la tabla 'users'
    const { error: updateErrorDb } = await supabase
      .from('users')
      .update({ avatar_url: newAvatarUrl })
      .eq('id', authStore.user.id);

    if (updateErrorDb) throw new Error(`Error al actualizar URL del avatar en DB: ${updateErrorDb.message}`);

    // Refrescar los datos del usuario en el store para que la UI se actualice
    await authStore.fetchUserProfile(authStore.user.id);
    updateSuccess.value = 'Avatar actualizado exitosamente.';

  } catch (err) {
    updateError.value = err.message || 'Error desconocido al subir avatar.';
    console.error('Error uploading avatar:', err);
  } finally {
    authStore.loading = false;
  }
};

// --- Funciones de Notificaciones ---
const toggleNotifications = () => {
  showNotifications.value = !showNotifications.value;
  if (showNotifications.value) {
    // Si abrimos las notificaciones, las cargamos
    notificationStore.fetchNotifications();
  }
};

const markAllAsRead = async () => {
  await notificationStore.markAllAsRead();
};

// --- Funciones de Utilidad de Posts (copiadas de Feed.vue) ---
const isImage = (fileType) => {
  if (!fileType) return false;
  const lowerCaseType = fileType.toLowerCase();
  return ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'].includes(lowerCaseType);
};

const isPdf = (fileType) => {
  if (!fileType) return false;
  return fileType.toLowerCase() === 'pdf';
};

// --- Acciones de Posts (Editar/Eliminar propias publicaciones) ---
const editPost = (postId) => {
  alert(`Funcionalidad de editar publicación ${postId} pendiente.`);
  // Aquí puedes redirigir a una página de edición o abrir un modal
};

const confirmDeletePost = async (postId) => {
  if (confirm('¿Estás seguro de que quieres eliminar esta publicación? Esta acción no se puede deshacer.')) {
    try {
      // Necesitarás implementar una acción 'deletePost' en tu postStore.js
      // que haga supabase.from('posts').delete().eq('id', postId);
      const { error: deleteError } = await supabase
        .from('posts')
        .delete()
        .eq('id', postId);

      if (deleteError) throw deleteError;

      alert('Publicación eliminada exitosamente.');
      // Después de eliminar, recargar las publicaciones para actualizar la lista
      postStore.fetchPosts();
    } catch (error) {
      alert('Error al eliminar publicación: ' + error.message);
      console.error('Error deleting post:', error);
    }
  }
};


// --- Funciones de Administración (Eliminar Estudiantes) ---
const fetchAllStudents = async () => {
  deleteStudentError.value = null;
  try {
    // Busca usuarios con rol 'student'.
    // Asumo que 'student_code' está directamente en la tabla 'users' o que la relación es simple.
    // Si 'student_code' está en una tabla 'students' separada y no la obtienes automáticamente
    // a través de la relación de Supabase, necesitarás un JOIN o una lógica adicional.
    const { data, error } = await supabase
      .from('users')
      .select('id, email, alias, role, students(code)') // Selecciona 'students(code)' para obtener el código si existe
      .eq('role', 'student');

    if (error) throw error;

    // Mapea los datos para incluir el código de estudiante directamente
    allStudents.value = data.map(user => ({
      ...user,
      student_code: user.students?.[0]?.code || 'N/A' // Extrae el código si existe
    }));

  } catch (err) {
    deleteStudentError.value = `Error al cargar estudiantes: ${err.message}`;
    console.error('Error fetching all students:', err);
  }
};

const confirmDeleteStudent = async (studentIdToDelete) => {
  if (confirm('¡ADVERTENCIA! ¿Estás seguro de que deseas ELIMINAR PERMANENTEMENTE a este estudiante y todos sus datos?')) {
    await deleteStudent(studentIdToDelete);
  }
};

const deleteStudent = async (studentIdToDelete) => {
    deleteStudentError.value = null;
    deleteStudentSuccess.value = null;
    try {
        // --- ADVERTENCIA DE SEGURIDAD CRÍTICA ---
        // Eliminar usuarios y sus datos asociados directamente desde el cliente NO es lo más seguro ni robusto.
        // Lo *altamente* recomendado es:
        // 1. Crear una función de PostgreSQL en Supabase que reciba el user_id y realice la eliminación en cascada (students, posts, users, auth.users).
        // 2. Crear una Supabase Edge Function que llame a esa función de PostgreSQL.
        // 3. Llamar a la Edge Function desde el cliente.
        // Esto asegura que la eliminación sea atómica, segura (usando Service Role Key en el backend) y consistente.
        // La implementación a continuación es solo para fines de demostración/prueba y podría tener problemas de permisos o consistencia con RLS estrictas.

        // 1. Eliminar publicaciones del estudiante
        console.log(`Eliminando publicaciones del usuario ${studentIdToDelete}...`);
        const { error: postsDeleteError } = await supabase
            .from('posts')
            .delete()
            .eq('user_id', studentIdToDelete);
        if (postsDeleteError) {
            console.warn(`Advertencia: No se pudieron eliminar todas las publicaciones del estudiante: ${postsDeleteError.message}`);
            // No lanzamos error para permitir que continúe con la eliminación del usuario,
            // pero es importante registrar esto.
        }

        // 2. Eliminar de la tabla 'students' (si aplica)
        console.log(`Eliminando de la tabla students al usuario ${studentIdToDelete}...`);
        const { error: studentDeleteError } = await supabase
            .from('students')
            .delete()
            .eq('user_id', studentIdToDelete);

        if (studentDeleteError) {
            console.error('Error deleting from students:', studentDeleteError.message);
            throw new Error(`Error al eliminar datos de estudiante: ${studentDeleteError.message}`);
        }

        // 3. Eliminar de la tabla 'users' (perfil)
        console.log(`Eliminando de la tabla users al usuario ${studentIdToDelete}...`);
        const { error: userProfileDeleteError } = await supabase
            .from('users')
            .delete()
            .eq('id', studentIdToDelete);

        if (userProfileDeleteError) {
            console.error('Error deleting from users:', userProfileDeleteError.message);
            throw new Error(`Error al eliminar perfil de usuario: ${userProfileDeleteError.message}`);
        }

        // 4. Eliminar de Supabase Auth (auth.users)
        // ESTO REQUIERE PERMISOS DE ADMINISTRADOR EN SUPABASE.
        // Si usas RLS en auth.users, esta operación desde el cliente fallará
        // a menos que el usuario logueado tenga permisos muy elevados
        // o si usas la clave de servicio (que NO debe estar en el cliente).
        console.log(`Eliminando de auth.users al usuario ${studentIdToDelete}...`);
        const { error: authDeleteError } = await supabase.auth.admin.deleteUser(studentIdToDelete);

        if (authDeleteError) {
            console.error('Error deleting from auth.users:', authDeleteError.message);
            throw new Error(`Error al eliminar usuario de autenticación: ${authDeleteError.message}. Necesitas usar una función de servidor con la clave de servicio.`);
        }

        deleteStudentSuccess.value = 'Estudiante y todos sus datos eliminados exitosamente.';
        alert(deleteStudentSuccess.value);
        await fetchAllStudents(); // Refrescar la lista de estudiantes
    } catch (err) {
        deleteStudentError.value = err.message || 'Error desconocido al eliminar estudiante.';
        console.error('Error deleting student:', err);
    }
};

</script>

<style scoped>
/* Estilos generales de la página de perfil */
.profile-page {
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
  background-color: #f0f2f5; /* Fondo claro */
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0,0,0,0.05);
}

.profile-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 15px;
  border-bottom: 1px solid #e0e0e0;
}

.profile-header h1 {
  margin: 0;
  color: #333;
  font-size: 2em;
  flex-grow: 1;
  text-align: center;
}

.back-to-feed {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: #1877f2;
  font-weight: bold;
  padding: 5px 10px;
  border-radius: 5px;
  transition: background-color 0.2s ease;
}

.back-to-feed:hover {
  background-color: #e4e6eb;
}

.back-to-feed i {
  margin-right: 5px;
}

/* Notificaciones */
.notification-area {
  position: relative;
}

.notification-icon {
  background: none;
  border: none;
  font-size: 1.5em;
  color: #555;
  cursor: pointer;
  padding: 5px;
  border-radius: 50%;
  transition: background-color 0.2s ease;
  position: relative;
}

.notification-icon:hover {
  background-color: #e4e6eb;
}

.notification-badge {
  position: absolute;
  top: 0px;
  right: 0px;
  background-color: #ff0000;
  color: white;
  border-radius: 50%;
  padding: 2px 6px;
  font-size: 0.7em;
  font-weight: bold;
  pointer-events: none; /* Asegura que los clics pasen al botón */
}

.notifications-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  background-color: white;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  width: 300px;
  max-height: 400px;
  overflow-y: auto;
  z-index: 1000;
  padding: 15px;
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
  font-size: 0.9em;
  color: #555;
}

.notifications-dropdown li:last-child {
  border-bottom: none;
}

.notifications-dropdown li.unread {
  font-weight: bold;
  background-color: #f9f9f9;
}

.mark-read-button {
  width: 100%;
  padding: 8px;
  background-color: #1877f2;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 10px;
  font-size: 0.9em;
  transition: background-color 0.2s ease;
}

.mark-read-button:hover {
  background-color: #166fe5;
}


/* Detalles del perfil */
.profile-details {
  background-color: #ffffff;
  border-radius: 10px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  padding: 25px;
  margin-bottom: 30px;
  text-align: center;
}

.profile-details h2, .edit-profile-section h3, .my-posts-section h2, .admin-section h2 {
  color: #333;
  margin-top: 0;
  margin-bottom: 20px;
  text-align: center;
}

.avatar-section {
  position: relative;
  display: inline-block;
  margin-bottom: 20px;
}

.profile-main-avatar {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  object-fit: cover;
  border: 4px solid #1877f2;
  box-shadow: 0 0 10px rgba(0,0,0,0.1);
}

.edit-avatar-button {
  position: absolute;
  bottom: 5px;
  right: 5px;
  background-color: #1877f2;
  color: white;
  border: none;
  border-radius: 50%;
  width: 35px;
  height: 35px;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  font-size: 1.1em;
  box-shadow: 0 2px 5px rgba(0,0,0,0.2);
  transition: background-color 0.2s ease;
}

.edit-avatar-button:hover {
  background-color: #166fe5;
}

.profile-info-group {
  text-align: left;
  margin-top: 20px;
  font-size: 1.1em;
  color: #555;
}

.profile-info-group p {
  margin-bottom: 8px;
}

.edit-profile-section {
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.profile-input {
  width: calc(100% - 22px);
  padding: 12px 10px;
  border: 1px solid #ddd;
  border-radius: 6px;
  box-sizing: border-box;
  font-size: 1em;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.profile-input:focus {
  outline: none;
  border-color: #1877f2;
  box-shadow: 0 0 0 2px rgba(24, 119, 242, 0.2);
}

.save-profile-button {
  width: 100%;
  padding: 12px 20px;
  background-color: #42b72a;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1.1em;
  font-weight: bold;
  transition: background-color 0.2s ease, opacity 0.2s ease;
  margin-top: 15px;
}

.save-profile-button:hover:not(:disabled) {
  background-color: #36a420;
}

.save-profile-button:disabled {
  background-color: #a0ec94;
  cursor: not-allowed;
  opacity: 0.7;
}

/* Sección Mis Publicaciones */
.my-posts-section {
  background-color: #ffffff;
  border-radius: 10px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  padding: 25px;
  margin-bottom: 30px;
}

.post-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

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
  position: relative; /* Para posicionar los botones de acción */
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
  flex-grow: 1; /* Permite que la info ocupe el espacio restante */
}

.post-author {
  font-weight: bold;
  color: #333;
}

.post-date {
  font-size: 0.85em;
  color: #777;
}

.post-actions {
  position: absolute;
  top: 0;
  right: 0;
  display: flex;
  gap: 8px;
}

.action-button {
  background: none;
  border: none;
  font-size: 1.1em;
  cursor: pointer;
  color: #555;
  padding: 5px;
  border-radius: 50%;
  transition: background-color 0.2s ease;
}

.action-button:hover {
  background-color: #eee;
}

.action-button.edit-button { color: #1877f2; }
.action-button.delete-button { color: #dc3545; }


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

/* Sección de Administración */
.admin-section {
  background-color: #fff3cd; /* Fondo amarillo claro para indicar sección admin */
  border-radius: 10px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  padding: 25px;
  border: 1px solid #ffeeba;
}

.admin-section h2 {
  color: #856404; /* Color de texto más oscuro */
}

.student-list ul {
  list-style: none;
  padding: 0;
}

.student-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid #eee;
  font-size: 1em;
  color: #333;
}

.student-item:last-child {
  border-bottom: none;
}

.delete-student-button {
  background-color: #dc3545;
  color: white;
  padding: 6px 12px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 0.9em;
  transition: background-color 0.2s ease;
}

.delete-student-button:hover {
  background-color: #c82333;
}


/* Mensajes de estado y error/éxito */
.status-message {
  text-align: center;
  color: #666;
  font-style: italic;
  margin-top: 20px;
}

.error-message {
  color: #e53e3e;
  margin-top: 15px;
  font-size: 0.9em;
  background-color: #ffebeb;
  border: 1px solid #e53e3e;
  padding: 8px;
  border-radius: 5px;
  text-align: center;
}

.success-message {
  color: #28a745;
  margin-top: 15px;
  font-size: 0.9em;
  background-color: #d4edda;
  border: 1px solid #28a745;
  padding: 8px;
  border-radius: 5px;
  text-align: center;
}
</style>
