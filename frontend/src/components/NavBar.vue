<!-- frontend/src/components/NavBar.vue -->
<template>
    <nav class="nav-menu">
      <router-link to="/" class="nav-link">Home</router-link>
      <router-link to="/weather" class="nav-link">Weather</router-link>
      <router-link to="/meals" class="nav-link">Meals</router-link>
      <router-link to="/leaderboard" class="nav-link">Leaderboard</router-link>
    </nav>
  </template>
  
  <script>
  export default {
    name: 'NavBar'
  }
  </script>
  
  <style scoped>
  .nav-menu {
    display: flex;
    gap: 30px;
  }
  
  .nav-link {
    text-decoration: none;
    color: #333;
    font-weight: 500;
  }
  
  .nav-link:hover {
    color: #42b983;
  }
  
  .router-link-active {
    color: #42b983;
    border-bottom: 2px solid #42b983;
  }
  </style>