<template>
  <div class="app-container">
    <TheHeader v-if="authStore.isAuthenticated" />
    <SideNavigation v-if="authStore.isAuthenticated" />
    <main class="main-content" :class="{ 'full-width': !authStore.isAuthenticated }">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/modules/auth/stores/auth'
import TheHeader from '@/components/TheHeader.vue'
import SideNavigation from '@/components/SideNavigation.vue'

const authStore = useAuthStore()
</script>

<style>
/* Tus estilos existentes */
.app-container {
  display: flex;
  min-height: 100vh;
}

.main-content {
  flex-grow: 1;
  margin-left: 250px;
  padding: 20px;
  padding-top: 80px;
}

.main-content.full-width {
  margin-left: 0;
  padding-top: 20px;
}

@media (max-width: 992px) {
  .main-content:not(.full-width) {
    margin-left: 70px;
  }
}

@media (max-width: 768px) {
  .main-content:not(.full-width) {
    margin-left: 0;
  }
}
</style>