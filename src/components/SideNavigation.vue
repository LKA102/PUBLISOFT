<template>
  <aside class="side-navigation">
    <div class="user-profile">
      <router-link to="/profile" class="profile-link">
        <img
          :src="authStore.user?.avatar_url || 'https://via.placeholder.com/40/CCCCCC/FFFFFF?text=AV'"
          alt="Avatar del usuario"
          class="profile-avatar"
        />
        <span class="profile-name">{{ authStore.user?.alias || 'Mi Perfil' }}</span>
      </router-link>
    </div>

    <nav class="nav-menu">
      <ul>
        <li v-for="item in filteredNavItems" :key="item.path" :class="{ 'active': isActive(item.path) }">
          <router-link :to="item.path" class="nav-item">
            <i :class="item.icon"></i>
            <span class="nav-text">{{ item.label }}</span>
          </router-link>
        </li>
      </ul>
    </nav>
  </aside>
</template>

<script setup>
import { useAuthStore } from '@/modules/auth/stores/auth';
import { useRoute } from 'vue-router';
import { computed } from 'vue';

const authStore = useAuthStore();
const route = useRoute();

const navItems = [
  { path: '/feed', label: 'Inicio', icon: 'fas fa-home' },
  { path: '/notifications', label: 'Notificaciones', icon: 'fas fa-bell' },
  { path: '/ranking', label: 'Ranking', icon: 'fas fa-trophy' },
  { path: '/resources', label: 'Recursos académicos', icon: 'fas fa-book' },
  { path: '/dashboard', label: 'Panel admin', icon: 'fas fa-tools', adminOnly: true }
];

const filteredNavItems = computed(() => {
  return navItems.filter(item => {
    // Mostrar todos los items excepto los adminOnly si no es admin
    // O mostrar todos si es admin
    return !item.adminOnly || (item.adminOnly && authStore.isAdmin);
  });
});

const isActive = (path) => {
  return route.path.startsWith(path);
};
</script>

<style scoped>
.side-navigation {
  position: fixed;
  top: 60px; /* Ajusta según la altura de tu navbar */
  left: 0;
  bottom: 0;
  width: 250px;
  background-color: #ffffff;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
  z-index: 900;
  display: flex;
  flex-direction: column;
  border-right: 1px solid #e0e0e0;
}

.user-profile {
  padding: 20px;
  border-bottom: 1px solid #e0e0e0;
}

.profile-link {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: #333;
  transition: all 0.2s ease;
}

.profile-link:hover {
  color: #1E3984;
}

.profile-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
  margin-right: 12px;
  border: 2px solid #f0f2f5;
}

.profile-name {
  font-weight: 600;
  font-size: 1.1em;
}

.nav-menu {
  flex-grow: 1;
  overflow-y: auto;
  padding: 10px 0;
}

.nav-menu ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.nav-menu li {
  margin: 5px 0;
}

.nav-item {
  display: flex;
  align-items: center;
  padding: 12px 20px;
  text-decoration: none;
  color: #555;
  transition: all 0.2s ease;
  position: relative;
}

.nav-item:hover {
  background-color: #f5f7fa;
  color: #1E3984;
}

.nav-item i {
  font-size: 1.2em;
  width: 24px;
  text-align: center;
  margin-right: 15px;
  color: #666;
}

.nav-item:hover i {
  color: #1E3984;
}

.nav-text {
  font-size: 0.95em;
  font-weight: 500;
}

.active .nav-item {
  background-color: #f0f5ff;
  color: #1E3984;
  border-left: 3px solid #1E3984;
}

.active .nav-item i {
  color: #1E3984;
}

/* Ajustes para pantallas pequeñas */
@media (max-width: 992px) {
  .side-navigation {
    width: 70px;
    overflow: hidden;
  }
  
  .profile-name,
  .nav-text {
    display: none;
  }
  
  .nav-item {
    justify-content: center;
    padding: 15px 0;
  }
  
  .nav-item i {
    margin-right: 0;
    font-size: 1.4em;
  }
  
  .user-profile {
    padding: 15px 0;
    display: flex;
    justify-content: center;
  }
  
  .profile-avatar {
    margin-right: 0;
  }
}

@media (max-width: 768px) {
  .side-navigation {
    display: none;
  }
}
</style>