<template>
  <div class="auth-page">
    <div class="auth-card">
      <h1 class="auth-title">¡Hola 👋!</h1>

      <form @submit.prevent="handleLogin"> 
        <div class="form-group">
          <label for="login-email">Correo:</label>
          <input type="email" id="login-email" v-model="email" placeholder="tu@ejemplo.com" class="auth-input" required/>
        </div>

        <div class="form-group">
          <label for="login-password">Contraseña:</label>
          <input type="password" id="login-password" v-model="password" placeholder="••••••••" class="auth-input" required/>
        </div>

        <button type="submit" class="auth-button" :disabled="authStore.isAuthLoading"> 
          {{ authStore.isAuthLoading ? 'Entrando...' : 'Entrar' }} 
        </button>
      </form>

      <p v-if="authStore.error" class="error-message">{{ authStore.error }}</p> 

      <p class="auth-link">
        ¿Aún no eres usuario? <router-link to="/register">Regístrate</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter, useRoute } from 'vue-router'; // Importa useRoute también
import { useAuthStore } from '@/modules/auth/stores/auth'; // Asegúrate de que la ruta es correcta

const email = ref('');
const password = ref('');
const authStore = useAuthStore(); 
const router = useRouter(); 
const route = useRoute(); // Para leer los query params, como el 'redirect'

const handleLogin = async () => { 
  // Limpia cualquier error anterior del store
  authStore.error = null; 

  const { success, error } = await authStore.login(email.value, password.value);

  if (success) {
    console.log('Login.vue: Login exitoso. Redirigiendo...');
    // Redirige al usuario a la ruta original si estaba intentando acceder a una protegida
    const redirectPath = route.query.redirect || '/feed';
    router.push(redirectPath);
  } else {
    // El error ya debería estar en authStore.error
    console.error('Login.vue: Error en el login:', error);
    // Opcional: Puedes mostrar una alerta o dejar que el v-if del template lo maneje
    // alert(`Error al iniciar sesión: ${error}`); 
  }
};
</script>

<style scoped>
/* Tus estilos CSS del componente Login.vue */
.auth-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: var(--primary-bg-color, #f0f2f5); /* Fallback si no hay variables */
}

.auth-card {
  background-color: var(--secondary-bg-color, #ffffff);
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
  max-width: 400px;
  width: 90%;
}

.auth-title {
  color: var(--text-color-dark, #333);
  margin-bottom: 1.5rem;
  font-size: 2rem;
}

.form-group {
  margin-bottom: 1rem;
  text-align: left;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: var(--text-color-medium, #666);
}

.auth-input {
  width: calc(100% - 20px); 
  padding: 10px;
  border: 1px solid var(--border-color, #ddd);
  border-radius: 4px;
  font-size: 1rem;
  box-sizing: border-box; 
}

.auth-button {
  background-color: var(--accent-color, #4CAF50); 
  color: white;
  padding: 12px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1.1rem;
  margin-top: 1rem;
  width: 100%;
  transition: background-color 0.3s ease;
}

.auth-button:hover:not(:disabled) {
  background-color: var(--accent-color-hover, #45a049);
}

.auth-button:disabled {
  background-color: var(--disabled-color, #ccc);
  cursor: not-allowed;
}

.auth-link {
  margin-top: 1.5rem;
  color: var(--text-color-medium, #666);
  font-size: 0.95rem;
}

.auth-link a {
  color: var(--link-color, #007bff);
  text-decoration: none;
  font-weight: bold;
}

.auth-link a:hover {
  text-decoration: underline;
}

.error-message {
    color: var(--error-color, #e74c3c); 
    margin-top: 1rem;
    font-size: 0.9rem;
}

/* Considera definir estas variables en un archivo global.css o similar */
/*
:root {
  --primary-bg-color: #f0f2f5;
  --secondary-bg-color: #ffffff;
  --text-color-dark: #333;
  --text-color-medium: #666;
  --border-color: #ddd;
  --accent-color: #4CAF50; // Verde 
  --accent-color-hover: #45a049;
  --link-color: #007bff;
  --disabled-color: #ccc;
  --error-color: #e74c3c;
}
*/
</style>