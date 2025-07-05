<template>
  <div class="auth-page">
    <div class="auth-card">
      <h1 class="auth-title">¡Regístrate! 👋</h1> <!-- Título con emoji -->

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

        <button type="submit" :disabled="authStore.loading" class="auth-button">
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
import { storeToRefs } from 'pinia';

const email = ref('');
const password = ref('');
const code = ref('');
const alias = ref('');

const authStore = useAuthStore();
const { loading, error } = storeToRefs(authStore);

const handleRegister = async () => {
  await authStore.register(email.value, code.value, alias.value, password.value);
};
</script>

<style scoped>
/* No necesitamos estilos aquí porque están en global.css */
</style>