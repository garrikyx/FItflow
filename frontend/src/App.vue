<script>
export default {
  name: 'App'
}
</script>

<template>
  <router-view></router-view>
</template>

<style>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&family=Poppins:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');

/* Global styles */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Inter', sans-serif;
}

body {
  margin: 0;
  padding: 0;
  background: #333;
  color: white;
}

h1, h2, h3, h4, h5, h6 {
  font-family: 'Montserrat', sans-serif;
}

button, .btn {
  font-family: 'Poppins', sans-serif;
}
</style>
