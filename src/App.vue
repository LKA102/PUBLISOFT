<template>
  <div class="app-container">
    <TheHeader />
    <SideNavigation />
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import TheHeader from '@/components/TheHeader.vue';
import SideNavigation from '@/components/SideNavigation.vue';
</script>

<style>
/* Añade estos estilos globales */
body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  background-color: #f5f7fa;
  color: #333;
}

.app-container {
  display: flex;
  min-height: 100vh;
}

.main-content {
  flex-grow: 1;
  margin-left: 250px; /* Igual al ancho del side navigation */
  padding: 20px;
  padding-top: 80px; /* Altura del navbar + espacio */
}

@media (max-width: 992px) {
  .main-content {
    margin-left: 70px;
  }
}

@media (max-width: 768px) {
  .main-content {
    margin-left: 0;
  }
}
</style>