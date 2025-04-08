<!-- frontend/src/components/Logo.vue -->
<template>
    <div class="logo">
      <router-link to="/" class="logo-link">
        <div class="logo-container">
          <span class="logo-emoji">🏋️</span>
          <h1>FitFlow</h1>
        </div>
      </router-link>
    </div>
  </template>
  
  <script>
  export default {
    name: 'Logo'
  }
  </script>
  
  <style scoped>
  .logo h1 {
    color: #2c3e50; /* Standard color for the logo */
    font-size: 24px; /* Standard font size for the logo */
    margin: 0; /* Remove default margin */
  }
  .logo-link {
    text-decoration: none; /* Remove underline from link */
  }
  .logo-container {
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .logo-emoji {
    font-size: 24px;
  }
  </style>