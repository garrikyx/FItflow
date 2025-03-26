<!-- frontend/src/components/Logo.vue -->
<template>
    <div class="logo">
      <router-link to="/" class="logo-link">
        <h1>FitFlow</h1>
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
  </style>