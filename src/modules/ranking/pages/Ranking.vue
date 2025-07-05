<template>
  <div class="ranking-page">
    <header class="feed-header">
      <h2 class="header-title">PUBLISOFT</h2>
      <div class="header-actions">
        <router-link to="/feed" class="header-button feed-button">
          <i class="fas fa-home header-icon"></i>
          <span>Inicio</span>
        </router-link>
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

    <p v-if="rankingStore.loading" class="status-message">Cargando ranking...</p>
    <p v-else-if="rankingStore.error" class="error-message">Error: {{ rankingStore.error }}</p>


    <div v-if="rankingStore.currentRanking.length > 0" class="current-ranking-section">
      <h2 class="section-title">Ranking Actual</h2>

      <div class="podium-container">
        <div v-if="rankingStore.currentRanking[1]" class="podium-item second-place">
          <img :src="rankingStore.currentRanking[1].avatar_url || 'https://via.placeholder.com/60/CCCCCC/FFFFFF?text=AV'" alt="2º Puesto" class="podium-avatar">
          <span class="place-number">2</span>
          <span class="podium-alias">{{ rankingStore.currentRanking[1].alias || 'Desconocido' }}</span>
          <span class="podium-score">{{ parseFloat(rankingStore.currentRanking[1].ranking_score).toFixed(2) }} pts</span>
        </div>

        <div v-if="rankingStore.currentRanking[0]" class="podium-item first-place">
          <div class="crown-icon">👑</div>
          <img :src="rankingStore.currentRanking[0].avatar_url || 'https://via.placeholder.com/80/CCCCCC/FFFFFF?text=AV'" alt="1º Puesto" class="podium-avatar">
          <span class="place-number">1</span>
          <span class="podium-title">ESTUDIANTE DEL MES</span>
          <span class="podium-alias">{{ rankingStore.currentRanking[0].alias || 'Desconocido' }}</span>
          <span class="podium-score">{{ parseFloat(rankingStore.currentRanking[0].ranking_score).toFixed(2) }} pts</span>
        </div>

        <div v-if="rankingStore.currentRanking[2]" class="podium-item third-place">
          <img :src="rankingStore.currentRanking[2].avatar_url || 'https://via.placeholder.com/60/CCCCCC/FFFFFF?text=AV'" alt="3º Puesto" class="podium-avatar">
          <span class="place-number">3</span>
          <span class="podium-alias">{{ rankingStore.currentRanking[2].alias || 'Desconocido' }}</span>
          <span class="podium-score">{{ parseFloat(rankingStore.currentRanking[2].ranking_score).toFixed(2) }} pts</span>
        </div>
      </div>

      <h3 class="section-subtitle">Ranking Completo</h3>
      <ul class="full-ranking-list">
        <li v-for="(student, index) in rankingStore.currentRanking" :key="student.user_id" v-if="index >= 3" class="ranking-list-item">
          <span class="rank-number">{{ index + 1 }}.</span>
          <img :src="student.avatar_url || 'https://via.placeholder.com/30/CCCCCC/FFFFFF?text=AV'" alt="Avatar" class="list-avatar">
          <span class="list-alias">{{ student.alias || 'Desconocido' }}</span>
          <span class="list-details">{{ student.total_posts }} pubs, {{ parseFloat(student.average_rating).toFixed(1) }} avg</span>
          <span class="list-score">{{ parseFloat(student.ranking_score).toFixed(2) }} pts</span>
        </li>
      </ul>
    </div>
    <p v-else class="status-message">No hay datos para el ranking actual.</p>

    <div class="history-section">
      <h2 class="section-title">Historial de Estudiantes del Mes</h2>
      <p v-if="rankingStore.loading" class="status-message">Cargando historial...</p>
      <p v-else-if="rankingStore.monthlyHistory.length === 0" class="status-message">No hay historial disponible.</p>
      <ul v-else class="history-list">
        <li v-for="entry in rankingStore.monthlyHistory" :key="entry.id" class="history-list-item">
          <span class="history-month">{{ entry.month_year }}</span>
          <img :src="entry.users?.avatar_url || 'https://via.placeholder.com/40/CCCCCC/FFFFFF?text=AV'" alt="Avatar" class="history-avatar">
          <span class="history-alias">{{ entry.users?.alias || 'Desconocido' }}</span>
          <span class="history-score">Puntaje: {{ parseFloat(entry.top_score).toFixed(2) }}</span>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, onUnmounted } from 'vue'; // Importa ref y onUnmounted
import { useRankingStore } from '@modules/ranking/stores/ranking';
import { useAuthStore } from '@modules/auth/stores/auth'; // Importa el store de autenticación
import { useRouter } from 'vue-router'; // Importa el router

const rankingStore = useRankingStore();
const authStore = useAuthStore(); // Instancia el store de autenticación
const router = useRouter(); // Instancia el router

const dropdownOpen = ref(false); // Estado para controlar la visibilidad del desplegable

const toggleDropdown = () => {
  dropdownOpen.value = !dropdownOpen.value;
};

// Cierra el desplegable si se hace clic fuera
const handleClickOutside = (event) => {
  const dropdown = document.querySelector('.dropdown-container');
  // Asegúrate de que el clic no sea dentro del contenedor del desplegable
  if (dropdown && !dropdown.contains(event.target)) {
    dropdownOpen.value = false;
  }
};

const handleLogout = async () => {
  await authStore.signOut();
  router.push('/login');
};

onMounted(async () => {
  // Asegúrate de que la sesión del usuario esté cargada para el desplegable
  await authStore.fetchUserProfile(authStore.user?.id); 
  
  // Siempre cargar el ranking actual
  await rankingStore.fetchCurrentRanking();

  // Siempre cargar el historial
  await rankingStore.fetchMonthlyHistory();

  // Intentar guardar/actualizar el Estudiante del Mes cada vez que se carga la página
  console.log('Iniciando actualización diaria del Estudiante del Mes...');
  await rankingStore.saveMonthlyTopStudent();

  // Agrega el event listener al montar el componente
  document.addEventListener('click', handleClickOutside);
});

// Limpia el event listener al desmontar el componente
onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
});
</script>

<style scoped>
/* Tus estilos Tailwind CSS existentes */
/* ... (todo el CSS que ya tienes aquí) ... */

/* ============== ESTILOS DEL HEADER Y DESPLEGABLE (COPIADOS DE FEED.VUE) ============== */

/* Estilos generales del contenedor principal */
.ranking-page {
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
  background-color: #f0f2f5;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0,0,0,0.05);
}

/* Estilos del encabezado */
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
  /* Alinea el título a la izquierda si el espacio lo permite */
  text-align: left; 
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

/* Para el elemento del menú que corresponde a la página actual */
.dropdown-item.current-page {
  font-weight: bold;
  color: #1877f2; /* Color distintivo para la página actual */
  background-color: #e6f2ff; /* Un fondo sutil para la página actual */
  cursor: default; /* No permitir clic si ya estás en esa página */
}
.dropdown-item.current-page .dropdown-icon {
  color: #1877f2;
}
.dropdown-item.current-page:hover {
  background-color: #e6f2ff; /* Mantener el mismo fondo al pasar el ratón */
  color: #1877f2;
}


/* ============== FIN ESTILOS DEL HEADER Y DESPLEGABLE ============== */

/* Tus estilos específicos del ranking (ajustados para no duplicar títulos) */
.page-title { /* Este se puede quitar si el h2.header-title es suficiente */
  display: none; /* O puedes comentarlo si prefieres mantenerlo pero oculto */
}

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
.manual-ranking-actions {
  @apply flex flex-col items-center justify-center; /* Centra el botón */
}

.generate-ranking-btn {
  @apply bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-lg shadow-md transition-colors duration-200;
}

.generate-ranking-btn:disabled {
  @apply bg-gray-400 cursor-not-allowed;
}

/* Resto de estilos del ranking */
.ranking-page {
  @apply container mx-auto px-4 py-8;
}

.page-title {
  @apply text-3xl font-bold text-center mb-8 text-gray-800;
}

.status-message {
  @apply text-center text-gray-600 italic mt-4;
}

.error-message {
  @apply text-center text-red-600 font-bold mt-4;
}

.current-ranking-section, .history-section {
  @apply bg-white shadow-lg rounded-lg p-6 mb-8;
}

.section-title {
  @apply text-2xl font-semibold text-center mb-6 text-blue-700;
}

.podium-container {
  @apply flex justify-center items-end gap-6 mb-8;
}

.podium-item {
  @apply flex flex-col items-center text-center p-4 rounded-lg shadow-md;
  @apply bg-gray-100; /* Fondo base para todos los podios */
  min-width: 150px;
}

.first-place {
  @apply bg-yellow-100 border-4 border-yellow-400 relative;
  @apply pb-8; /* Espacio extra para la corona */
  min-width: 180px;
  transform: translateY(-20px); /* Ligeramente más alto */
  z-index: 10;
}

.second-place {
  @apply bg-gray-200 border-4 border-gray-300;
  min-width: 150px;
  transform: translateY(-10px); /* Ligeramente más alto que el tercero */
}

.third-place {
  @apply bg-orange-100 border-4 border-orange-300;
  min-width: 150px;
}

.crown-icon {
  @apply absolute -top-5 text-4xl;
}

.podium-avatar {
  @apply rounded-full object-cover mb-2;
  width: 80px;
  height: 80px;
  border: 3px solid;
}

.first-place .podium-avatar { @apply border-yellow-500; width: 100px; height: 100px; }
.second-place .podium-avatar { @apply border-gray-400; }
.third-place .podium-avatar { @apply border-orange-400; }

.place-number {
  @apply font-black text-4xl mb-1;
}
.first-place .place-number { @apply text-yellow-600; }
.second-place .place-number { @apply text-gray-600; }
.third-place .place-number { @apply text-orange-600; }

.podium-title {
  @apply text-lg font-bold text-green-700 mb-1;
}

.podium-alias {
  @apply text-xl font-semibold text-gray-800;
}

.podium-score {
  @apply text-base text-gray-600 mt-1;
}

.section-subtitle {
  @apply text-xl font-semibold text-center mb-4 text-gray-700;
}

.full-ranking-list {
  @apply list-none p-0;
}

.ranking-list-item {
  @apply flex items-center justify-between bg-white border border-gray-200 rounded-md p-3 mb-2;
  @apply shadow-sm;
}

.rank-number {
  @apply font-bold text-lg text-gray-700 mr-3;
}

.list-avatar {
  @apply rounded-full object-cover mr-3;
  width: 30px;
  height: 30px;
}

.list-alias {
  @apply font-medium text-gray-800 flex-grow;
}

.list-score {
  @apply font-semibold text-blue-600 ml-auto;
}

.list-details {
  @apply text-sm text-gray-500 ml-4;
}

.history-list {
  @apply list-none p-0;
}

.history-list-item {
  @apply flex items-center bg-gray-50 border border-gray-200 rounded-md p-3 mb-2;
}

.history-month {
  @apply font-bold text-gray-700 mr-4;
  min-width: 80px;
}

.history-avatar {
  @apply rounded-full object-cover mr-3;
  width: 40px;
  height: 40px;
}

.history-alias {
  @apply font-medium text-gray-800 flex-grow;
}

.history-score {
  @apply text-sm text-gray-600 ml-auto;
}


</style>