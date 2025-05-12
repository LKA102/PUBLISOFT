import { defineStore } from 'pinia'
import { authService } from '../services/authService'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,  
    token: null 
  }),

  actions: {
    async login(email, password) {
      try {
        const { user, token } = await authService.login(email, password)
        this.user = user
        this.token = token
        localStorage.setItem('user', JSON.stringify(user))
        localStorage.setItem('token', token)
        return true
      } catch (error) {
        console.error('Login failed:', error)
        return false
      }
    },

    // Añade este nuevo método
    initialize() {
      // Solo carga del localStorage cuando se llame explícitamente
      this.user = JSON.parse(localStorage.getItem('user'))
      this.token = localStorage.getItem('token')
    },

    logout() {
      this.user = null
      this.token = null
      localStorage.removeItem('user')
      localStorage.removeItem('token')
    }
  },

  getters: {
    isAuthenticated: (state) => !!state.token
  }
})