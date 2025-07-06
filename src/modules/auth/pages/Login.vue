<template>
  <div class="auth-page">
    <div class="auth-card">
      <h1 class="auth-title">¡Hola 👋!</h1> <!-- Cambiado el título con emoji -->

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
        ¿Aún no eres usuario? <router-link to="/register">Regístrate</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@modules/auth/stores/auth';

const email = ref('')
const password = ref('')
const store = useAuthStore()

const login = () => {
  store.login(email.value, password.value)
}
</script>