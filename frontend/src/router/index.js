import { createRouter, createWebHistory } from 'vue-router'
import Homepage from '../components/homepage.vue'
import WeatherRecc from '../components/weatherrecc.vue'
import MealRecc from '../components/mealrecc.vue'
import Leaderboard from '../components/leaderboard.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Homepage
  },

  {
    path: '/weather',
    name: 'Weather',
    component: WeatherRecc
  },
  {
    path: '/meals',
    name: 'Meals',
    component: MealRecc
  },
  {
    path: '/leaderboard',
    name: 'Leaderboard',
    component: Leaderboard
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
