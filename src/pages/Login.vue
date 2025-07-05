<template>
  <div class="auth-page">
    <div class="auth-card">
      <h1 class="auth-title">Iniciar Sesión</h1>

      <form @submit.prevent="login">
        <div class="form-group">
          <label for="login-email">Correo:</label>
          <input type="email" id="login-email" v-model="email" placeholder="tu@ejemplo.com" class="auth-input" required/>
        </div>

        <div class="form-group">
          <label for="login-password">Contraseña:</label>
          <input type="password" id="login-password" v-model="password" placeholder="••••••••" class="auth-input" required/>
        </div>

        <button type="submit" class="auth-button">Entrar</button>
      </form>

      <p class="auth-link">
        ¿No tienes cuenta? <router-link to="/register">Regístrate aquí</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'

const email = ref('')
const password = ref('')
const store = useAuthStore()

const login = () => {
  store.login(email.value, password.value)
}
</script>

<style scoped>
/* Estilos replicados del modal de PostUpload y del feed */
.auth-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f0f2f5; /* Fondo similar al de Facebook */
  padding: 20px;
  box-sizing: border-box;
}

.auth-card {
  background-color: #ffffff;
  border-radius: 10px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  padding: 30px;
  width: 100%;
  max-width: 400px; /* Ancho máximo para el formulario */
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
  text-align: left; /* Alinea etiquetas a la izquierda */
}

label {
  display: block;
  margin-bottom: 6px;
  font-weight: bold;
  color: #555;
  font-size: 0.9em;
}

.auth-input {
  width: calc(100% - 22px); /* Ajuste para padding y border */
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
  background-color: #1877f2; /* Azul principal de Facebook */
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1.1em;
  font-weight: bold;
  transition: background-color 0.2s ease, opacity 0.2s ease;
  margin-top: 15px;
}

.auth-button:hover {
  background-color: #166fe5;
}

/* Si tu store tiene propiedades 'loading' y 'error',
   puedes descomentar las líneas comentadas en el template
   y usar estos estilos: */
/* .auth-button:disabled {
  background-color: #a0c3ec;
  cursor: not-allowed;
  opacity: 0.7;
}
.error-message {
  color: #e53e3e;
  margin-top: 15px;
  font-size: 0.9em;
  background-color: #ffebeb;
  border: 1px solid #e53e3e;
  padding: 8px;
  border-radius: 5px;
} */

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