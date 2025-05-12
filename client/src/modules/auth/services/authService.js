
export const authService = {
  async login(email, password) {
    
    // Simulación de API - usando ambos parámetros para evitar warning
  console.log('Simulando login con:', email, password)
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        user: {
          id: '123',
          name: email.split('@')[0],
          email,
          avatar: null
        },
        token: 'fake-jwt-token'
      })
    }, 500)
  })
  },

  async register(userData) {
    // Simulación de registro
    return this.login(userData.email, userData.password)
  },

  logout() {
    return Promise.resolve()
  }
}