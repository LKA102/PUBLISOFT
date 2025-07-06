<template>
  <div class="admin-dashboard">
    <h2>Panel de Administración</h2>

    <div class="analytics-cards-container">
      <AnalyticsCard 
        title="Total Usuarios" 
        :value="adminStore.totalUsers" 
        icon="fas fa-users" 
        class="users"
      />
      <AnalyticsCard 
        title="Total Estudiantes" 
        :value="adminStore.totalStudents" 
        icon="fas fa-graduation-cap" 
        class="students"
      />
      <AnalyticsCard 
        title="Total Publicaciones" 
        :value="adminStore.totalPosts" 
        icon="fas fa-file-alt" 
        class="posts"
      />
    </div>

    <div class="dashboard-tabs">
      <button 
        :class="{ active: currentTab === 'users' }" 
        @click="currentTab = 'users'">
        <i class="fas fa-users"></i> Gestión de Usuarios
      </button>
      <button 
        :class="{ active: currentTab === 'verifications' }" 
        @click="currentTab = 'verifications'">
        <i class="fas fa-clipboard-check"></i> Códigos de Verificación
      </button>
    </div>

    <div class="tab-content">
      <div v-if="adminStore.loading" class="loading-message">
        <i class="fas fa-spinner fa-spin"></i> Cargando datos...
      </div>
      <div v-else-if="adminStore.error" class="error-message">
        Error: {{ adminStore.error }}
      </div>
      <div v-else>
        <UserList v-if="currentTab === 'users'" />
        <VerificationCodeList v-if="currentTab === 'verifications'" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'; // <--- CORRECCIÓN AQUÍ: Agregado 'watch'
import { useAdminStore } from '@/modules/admi/stores/admin'; // Assuming you kept the 'admi' folder name
import UserList from '@/modules/admi/components/UserList.vue';
import VerificationCodeList from '@/modules/admi/components/VerificationCodeList.vue';
import AnalyticsCard from '@/modules/admi/components/AnalyticsCard.vue';

const adminStore = useAdminStore();
const currentTab = ref('users'); // Pestaña inicial

onMounted(() => {
  // Cargar todas las métricas al montar el dashboard
  adminStore.fetchAllMetrics();
  
  // Cargar los datos de la pestaña inicial
  // No es estrictamente necesario volver a llamar fetchAllUsers/fetchVerificationCodes here
  // if fetchAllMetrics already triggers them, but it doesn't hurt.
  if (currentTab.value === 'users') {
    adminStore.fetchAllUsers();
  } else if (currentTab.value === 'verifications') {
    adminStore.fetchVerificationCodes();
  }
});

// Watcher para cargar datos cuando la pestaña cambia
watch(currentTab, (newTab) => {
  if (newTab === 'users') {
    adminStore.fetchAllUsers();
  } else if (newTab === 'verifications') {
    adminStore.fetchVerificationCodes();
  }
});
</script>

<style scoped>
.admin-dashboard {
  max-width: 900px;
  margin: 20px auto;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

h2 {
  text-align: center;
  color: #343a40;
  margin-bottom: 30px;
  font-size: 2.2em;
}

.dashboard-tabs {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
  background-color: #e9ecef;
  border-radius: 8px;
  padding: 5px;
}

.dashboard-tabs button {
  flex: 1;
  padding: 12px 20px;
  border: none;
  background-color: transparent;
  color: #495057;
  font-size: 1.1em;
  cursor: pointer;
  border-radius: 6px;
  transition: background-color 0.3s ease, color 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.dashboard-tabs button:hover {
  background-color: #dee2e6;
}

.dashboard-tabs button.active {
  background-color: #007bff;
  color: white;
  box-shadow: 0 2px 5px rgba(0, 123, 255, 0.2);
}

.tab-content {
  background-color: #ffffff;
  padding: 25px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

/* Estilos para el contenedor de las tarjetas */
.analytics-cards-container {
  display: flex;
  flex-wrap: wrap; /* Permite que las tarjetas salten de línea en pantallas pequeñas */
  justify-content: space-around; /* Distribuye las tarjetas equitativamente */
  margin-bottom: 30px;
  gap: 20px; /* Espacio entre las tarjetas */
}

/* Media queries para responsividad de las tarjetas */
@media (max-width: 768px) {
  .analytics-cards-container {
    flex-direction: column; /* Apila las tarjetas en pantallas pequeñas */
    align-items: center;
  }
  .analytics-card {
    width: 90%; /* Ocupa casi todo el ancho */
    margin: 10px 0; /* Ajusta el margen */
  }
}

.loading-message, .error-message {
  text-align: center;
  padding: 20px;
  font-size: 1.1em;
  color: #6c757d;
}

.error-message {
  color: #dc3545;
  font-weight: bold;
}
</style>