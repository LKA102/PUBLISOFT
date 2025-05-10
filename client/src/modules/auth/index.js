import LoginView from './views/LoginView.vue'

export default [
  {
    path: '/login',
    name: 'Login',
    component: LoginView,
    meta: { requiresGuest: true }
  }
]