<template>
  <div class="verification-codes-container">
    <h3>Códigos de Verificación</h3>
    <p v-if="adminStore.verificationCodes.length === 0 && !adminStore.loading && !adminStore.error" class="no-data-message">
      No hay códigos de verificación registrados.
    </p>
    <div v-else class="table-responsive">
      <table class="codes-table">
        <thead>
          <tr>
            <th>Código</th>
            <th>Email</th>
            <th>Acciones</th> </tr>
        </thead>
        <tbody>
          <tr v-for="codeEntry in adminStore.verificationCodes" :key="codeEntry.code"> 
            <td>{{ codeEntry.code }}</td>
            <td>{{ codeEntry.email }}</td>
            <td>
              <button 
                @click="confirmDeleteCode(codeEntry.code)" class="delete-button"
                :disabled="adminStore.loading">
                <i class="fas fa-trash-alt"></i> Eliminar
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { useAdminStore } from '@/modules/admi/stores/admin'; // Asegúrate de la ruta correcta

const adminStore = useAdminStore();

// La función ahora recibe el valor del código, no un ID
const confirmDeleteCode = async (codeValue) => {
  if (confirm(`¿Estás seguro de que quieres eliminar el código ${codeValue}?`)) {
    await adminStore.deleteVerificationCode(codeValue);
  }
};
</script>

<style scoped>
/* Tus estilos existentes para VerificationCodeList.vue */
.verification-codes-container {
  margin-top: 20px;
}

h3 {
  color: #343a40;
  margin-bottom: 15px;
  font-size: 1.5em;
  text-align: center;
}

.no-data-message {
  text-align: center;
  color: #6c757d;
  font-style: italic;
  padding: 20px;
}

.table-responsive {
  overflow-x: auto;
}

.codes-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 15px;
  background-color: #fff;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.codes-table th, .codes-table td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #dee2e6;
}

.codes-table th {
  background-color: #f2f2f2;
  color: #495057;
  font-weight: bold;
  text-transform: uppercase;
  font-size: 0.9em;
}

.codes-table tbody tr:nth-child(even) {
  background-color: #f9f9f9;
}

.codes-table tbody tr:hover {
  background-color: #e9ecef;
}

/* Icons for 'is_used' are removed as the column is gone */

.delete-button {
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 0.9em;
  display: flex;
  align-items: center;
  gap: 5px;
  transition: background-color 0.2s ease;
}

.delete-button:hover:not(:disabled) {
  background-color: #c82333;
}

.delete-button:disabled {
  background-color: #a0a0a0;
  cursor: not-allowed;
}

/* Responsividad para la tabla */
@media (max-width: 768px) {
  .codes-table thead {
    display: none;
  }

  .codes-table, .codes-table tbody, .codes-table tr, .codes-table td {
    display: block;
    width: 100%;
  }

  .codes-table tr {
    margin-bottom: 15px;
    border: 1px solid #dee2e6;
    border-radius: 8px;
    overflow: hidden;
  }

  .codes-table td {
    text-align: right;
    padding-left: 50%;
    position: relative;
  }

  .codes-table td::before {
    content: attr(data-label);
    position: absolute;
    left: 15px;
    width: calc(50% - 30px);
    padding-right: 10px;
    white-space: nowrap;
    text-align: left;
    font-weight: bold;
    color: #495057;
  }

  /* Actualiza los data-label para reflejar solo 'Código', 'Email', 'Acciones' */
  .codes-table td:nth-of-type(1)::before { content: "Código"; }
  .codes-table td:nth-of-type(2)::before { content: "Email"; }
  .codes-table td:nth-of-type(3)::before { content: "Acciones"; }

  .delete-button {
    width: 100%;
    justify-content: center;
  }
}
</style>