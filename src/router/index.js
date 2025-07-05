
import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/pages/Home.vue'
import Login from '@/pages/Login.vue'
import Register from '@/pages/Register.vue'
import Feed from '@/pages/Feed.vue'
import MyPublications from '@/pages/MyPublications.vue'
import Profile from '@/pages/Profile.vue'
import Notifications from '@/pages/Notifications.vue'
import Ranking from '@/pages/Ranking.vue'

const routes = [
  { path: '/', name: 'Home', component: Login },
  { path: '/login', name: 'Login', component: Login },
  { path: '/register', name: 'Register', component: Register },
  { path: '/feed', name: 'Feed', component: Feed },
  { path: '/myposts', name: 'MyPublications', component: MyPublications },
  { path: '/profile', name: 'Profile', component: Profile },
  { path: '/notifications', name: 'Notifications', component: Notifications },
  { path: '/ranking', name: 'Ranking', component: Ranking }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
