<template>
  <div class="auth-page">
    <div class="auth-card">
      <h1 class="auth-title">Registro</h1>

      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label for="register-email">Correo Institucional:</label>
          <input type="email" id="register-email" v-model="email" placeholder="tu@institucion.edu" class="auth-input" required />
        </div>

        <div class="form-group">
          <label for="register-code">Código de Alumno:</label>
          <input type="text" id="register-code" v-model="code" placeholder="Ej: 20201234" class="auth-input" required />
        </div>

        <div class="form-group">
          <label for="register-alias">Alias (Nombre de Usuario):</label>
          <input type="text" id="register-alias" v-model="alias" placeholder="Tu nombre de autor" class="auth-input" required />
        </div>

        <div class="form-group">
          <label for="register-password">Contraseña:</label>
          <input type="password" id="register-password" v-model="password" placeholder="••••••••" class="auth-input" required />
        </div>

        <p v-if="authStore.error" class="error-message">{{ authStore.error }}</p>

        <button type="submit" :disabled="authStore.loading" class="auth-button register-button">
          <span v-if="authStore.loading">Registrando...</span>
          <span v-else>Registrarse</span>
        </button>
      </form>

      <p class="auth-link">
        ¿Ya tienes cuenta? <router-link to="/login">Inicia sesión aquí</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { storeToRefs } from 'pinia'; // Importa storeToRefs para acceder a propiedades reactivas del store

const email = ref('');
const password = ref('');
const code = ref('');       // Para el código de alumno
const alias = ref('');      // NUEVO: ref para el alias/nombre de usuario

const authStore = useAuthStore();
const { loading, error } = storeToRefs(authStore); // Accede a loading y error del store

const handleRegister = async () => {
  // Asegúrate de que los parámetros coincidan con la acción 'register' en tu store
  // Enviamos email, code, password, y AHORA también alias
  await authStore.register(email.value, code.value, password.value, alias.value);
};
</script>

<style scoped>
/* RECUERDA: Estos estilos son los mismos que te di anteriormente,
   manteniendo la consistencia visual. */

.auth-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f0f2f5;
  padding: 20px;
  box-sizing: border-box;
}

.auth-card {
  background-color: #ffffff;
  border-radius: 10px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  padding: 30px;
  width: 100%;
  max-width: 400px;
  text-align: center;
}

.auth-title {
  font-size: 2em;
  color: #333;
  margin-bottom: 25px;
  font-weight: bold;
}

.form-group {
  margin-bottom: 18px;
  text-align: left;
}

label {
  display: block;
  margin-bottom: 6px;
  font-weight: bold;
  color: #555;
  font-size: 0.9em;
}

.auth-input {
  width: calc(100% - 22px);
  padding: 12px 10px;
  border: 1px solid #ddd;
  border-radius: 6px;
  box-sizing: border-box;
  font-size: 1em;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.auth-input:focus {
  outline: none;
  border-color: #1877f2;
  box-shadow: 0 0 0 2px rgba(24, 119, 242, 0.2);
}

.auth-button {
  width: 100%;
  padding: 12px 20px;
  background-color: #1877f2;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1.1em;
  font-weight: bold;
  transition: background-color 0.2s ease, opacity 0.2s ease;
  margin-top: 15px;
}

.auth-button:hover:not(:disabled) {
  background-color: #166fe5;
}

.auth-button:disabled {
  background-color: #a0c3ec;
  cursor: not-allowed;
  opacity: 0.7;
}

.register-button {
  background-color: #42b72a;
}

.register-button:hover:not(:disabled) {
  background-color: #36a420;
}

.error-message {
  color: #e53e3e;
  margin-top: 15px;
  font-size: 0.9em;
  background-color: #ffebeb;
  border: 1px solid #e53e3e;
  padding: 8px;
  border-radius: 5px;
}

.auth-link {
  margin-top: 20px;
  color: #65676b;
  font-size: 0.95em;
}

.auth-link a {
  color: #1877f2;
  text-decoration: none;
  font-weight: bold;
}

.auth-link a:hover {
  text-decoration: underline;
}
</style>