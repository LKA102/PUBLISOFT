
import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/modules/home/pages/Home.vue'
import Login from '@/modules/auth/pages/Login.vue'
import Register from '@/modules/auth/pages/Register.vue'
import Feed from '@/modules/users/pages/Feed.vue'
import MyPublications from '@/modules/posts/pages/MyPublications.vue'
import Profile from '@/modules/users/pages/Profile.vue'
import Notifications from '@/modules/users/pages/Notifications.vue'
import Ranking from '@modules/ranking/pages/Ranking.vue'

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
