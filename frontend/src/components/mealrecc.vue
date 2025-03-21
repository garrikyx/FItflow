<template>
  <div class="meal-page">
    <header class="header">
      <h1>Meal Recommendations</h1>
      <nav class="nav-menu">
        <a href="#" class="nav-link">Home</a>
        <a href="#" class="nav-link">Weather</a>
        <a href="#" class="nav-link">Meals</a>
        <a href="#" class="nav-link">Leaderboard</a>
      </nav>
    </header>

    <main class="main-content">
      <!-- Content will be added later -->
    </main>
  </div>
</template>

<script>
export default {
  name: 'MealRecc',
  data() {
    return {
      // Add data properties here
    }
  }
}
</script>

<style scoped>
.meal-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 0;
}

.nav-menu {
  display: flex;
  gap: 20px;
}

.nav-link {
  text-decoration: none;
  color: #333;
  font-weight: 500;
}

.nav-link:hover {
  color: #007bff;
}
</style> 