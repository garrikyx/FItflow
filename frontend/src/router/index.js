import { createRouter, createWebHistory } from 'vue-router'
import Homepage from '../components/userpage.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Homepage
  },

]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
