<!-- src/components/NavBar.vue -->
<template>
  <header class="navbar">
    <h2 class="navbar-title">PUBLISOFT</h2>
    <div class="navbar-actions">
      <div v-if="authStore.user" class="dropdown-container" @click.stop="toggleDropdown">
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
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();
const dropdownOpen = ref(false);

const toggleDropdown = () => {
  dropdownOpen.value = !dropdownOpen.value;
};

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

onMounted(() => {
  document.addEventListener('click', handleClickOutside);
});

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
});
</script>

<style scoped>
/* Estilos del navbar */
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  background-color: white;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 1000;
}

.navbar-title {
  color: #1E3984; /* Color azul oscuro para consistencia */
  margin: 0;
  font-size: 1.8em;
  font-weight: bold;
}

.navbar-actions {
  position: relative;
  display: flex;
  gap: 15px;
  align-items: center;
}

/* Contenedor del desplegable */
.dropdown-container {
  position: relative;
  display: inline-block;
  cursor: pointer;
  z-index: 100;
}

/* Botón que activa el desplegable */
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
  background-color: #DBE2F6; /* Color azul claro para consistencia */
}

.profile-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
  margin-right: 8px;
  border: 1px solid #1E3984; /* Borde azul oscuro */
}

.profile-alias {
  font-weight: bold;
  font-size: 0.95em;
  white-space: nowrap;
  color: #1E3984; /* Color azul oscuro */
}

.dropdown-arrow {
  margin-left: 8px;
  transition: transform 0.2s ease;
  color: #1E3984; /* Color azul oscuro */
}

.dropdown-arrow.rotate-180 {
  transform: rotate(180deg);
}

/* Menú desplegable */
.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  min-width: 180px;
  padding: 8px 0;
  z-index: 100;
  margin-top: 8px;
}

.dropdown-item {
  display: flex;
  align-items: center;
  padding: 10px 15px;
  color: #1E3984; /* Color azul oscuro */
  text-decoration: none;
  font-size: 0.95em;
  transition: background-color 0.2s ease;
  width: 100%;
}

.dropdown-item:hover {
  background-color: #DBE2F6; /* Color azul claro */
}

.dropdown-icon {
  margin-right: 10px;
  font-size: 1.1em;
  color: #1E3984; /* Color azul oscuro */
}

/* Estilo específico para el botón de cerrar sesión */
.logout-button-in-menu {
  color: #e53e3e;
  border-top: 1px solid #eee;
  margin-top: 8px;
  padding-top: 10px;
}

.logout-button-in-menu:hover {
  background-color: #ffebeb;
}

.logout-button-in-menu .dropdown-icon {
  color: #e53e3e;
}
</style>