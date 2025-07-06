<template>
  <div class="user-list-container">
    <h3>Lista de Usuarios</h3>
    <p v-if="adminStore.users.length === 0 && !adminStore.loading && !adminStore.error" class="no-data-message">
      No hay usuarios registrados.
    </p>
    <div v-else class="table-responsive">
      <table class="user-table">
        <thead>
          <tr>
            <th>Alias</th>
            <th>Email</th>
            <th>Rol</th>
            <th>Fecha de Creación</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in adminStore.users" :key="user.id">
            <td>{{ user.alias }}</td>
            <td>{{ user.email }}</td>
            <td>{{ user.role }}</td>
            <td>{{ new Date(user.created_at).toLocaleDateString() }}</td>
            <td>
              <button 
                @click="confirmDeleteUser(user.id, user.alias)" 
                class="delete-button"
                :disabled="user.role === 'admin' || adminStore.loading"> 
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
import { useAdminStore } from '@/modules/admi/stores/admin';
import { useAuthStore } from '@/modules/auth/stores/auth'; // Para el ID del admin actual

const adminStore = useAdminStore();
const authStore = useAuthStore();

const confirmDeleteUser = async (userId, userAlias) => {
  if (authStore.user?.id === userId) {
    alert('No puedes eliminar tu propia cuenta de administrador.');
    return;
  }
  if (confirm(`¿Estás seguro de que quieres eliminar al usuario ${userAlias}? Esta acción es irreversible.`)) {
    await adminStore.deleteUser(userId);
  }
};
</script>

<style scoped>
.user-list-container {
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
  overflow-x: auto; /* Permite scroll horizontal en pantallas pequeñas */
}

.user-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 15px;
  background-color: #fff;
  border-radius: 8px;
  overflow: hidden; /* Para que los border-radius se apliquen a la tabla */
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.user-table th, .user-table td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #dee2e6;
}

.user-table th {
  background-color: #f2f2f2;
  color: #495057;
  font-weight: bold;
  text-transform: uppercase;
  font-size: 0.9em;
}

.user-table tbody tr:nth-child(even) {
  background-color: #f9f9f9;
}

.user-table tbody tr:hover {
  background-color: #e9ecef;
}

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
  .user-table thead {
    display: none; /* Oculta el encabezado en móviles */
  }

  .user-table, .user-table tbody, .user-table tr, .user-table td {
    display: block;
    width: 100%;
  }

  .user-table tr {
    margin-bottom: 15px;
    border: 1px solid #dee2e6;
    border-radius: 8px;
    overflow: hidden;
  }

  .user-table td {
    text-align: right;
    padding-left: 50%;
    position: relative;
  }

  .user-table td::before {
    content: attr(data-label); /* Usa el atributo data-label para mostrar el nombre de la columna */
    position: absolute;
    left: 15px;
    width: calc(50% - 30px);
    padding-right: 10px;
    white-space: nowrap;
    text-align: left;
    font-weight: bold;
    color: #495057;
  }

  /* Aplica data-label a las celdas en el template Vue */
  .user-table td:nth-of-type(1)::before { content: "Alias"; }
  .user-table td:nth-of-type(2)::before { content: "Email"; }
  .user-table td:nth-of-type(3)::before { content: "Rol"; }
  .user-table td:nth-of-type(4)::before { content: "Fecha de Creación"; }
  .user-table td:nth-of-type(5)::before { content: "Acciones"; }

  .delete-button {
    width: 100%;
    justify-content: center;
  }
}
</style>