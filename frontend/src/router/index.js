import { createRouter, createWebHistory } from 'vue-router'
import Homepage from '../components/homepage.vue'
// import WeatherRecc from '../components/weatherrecc.vue'
// import MealRecc from '../components/mealrecc.vue'
import Leaderboard from '../components/leaderboard.vue'
import authentication from '../components/authentication.vue'

const routes = [
  {
    path: '/',
    name: 'authentication',
    component: authentication
  },
  {
    path: '/homepage',
    name: 'Homepage',
    component: Homepage,
    meta: { requiresAuth: true }
  },
  // {
  //   path: '/weather',
  //   name: 'Weather',
  //   component: WeatherRecc,
  //   meta: { requiresAuth: true }
  // },
  // {
  //   path: '/meals',
  //   name: 'Meals',
  //   component: MealRecc,
  //   meta: { requiresAuth: true }
  // },
  {
    path: '/leaderboard',
    name: 'Leaderboard',
    component: Leaderboard,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('user')
  
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/')
  } else if (to.path === '/' && isAuthenticated) {
    next('/homepage')
  } else {
    next()
  }
})

export default router
