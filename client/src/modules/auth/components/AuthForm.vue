<template>
  <form @submit.prevent="handleSubmit">
    <v-text-field
      v-model="form.email"
      label="Correo electrónico"
      type="email"
      outlined
      dense
      class="mb-3"
      :rules="[v => !!v || 'Email es requerido']"
    ></v-text-field>

    <v-text-field
      v-model="form.password"
      label="Contraseña"
      type="password"
      outlined
      dense
      class="mb-3"
      :rules="[v => !!v || 'Contraseña es requerida']"
    ></v-text-field>

    <v-btn
      color="primary"
      block
      type="submit"
      :loading="loading"
    >
      Iniciar Sesión
    </v-btn>

    <v-alert v-if="error" type="error" dense class="mt-3">
      {{ error }}
    </v-alert>
  </form>
</template>

<script setup>
import { ref, onMounted } from 'vue'

defineProps({
  isLogin: Boolean,
  initialEmail: {
    type: String,
    default: ''
  },
  initialPassword: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['submit'])

const form = ref({
  email: '',
  password: ''
})

const loading = ref(false)
const error = ref('')

// Inicializar con valores demo (opcional)
onMounted(() => {
  form.value = {
    email: 'demo@example.com',
    password: 'demo123'
  }
})

const handleSubmit = async () => {
  try {
    loading.value = true
    error.value = ''
    await emit('submit', form.value)
  } catch (err) {
  error.value = err.message || 'Credenciales incorrectas'
    } finally {
        loading.value = false
    }
}
</script>