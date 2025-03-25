<template>
  <div class="homepage">
    <header class="header">
      <div class="logo">
        <h1>FitFlow</h1>
      </div>
      <nav class="nav-menu">
        <router-link to="/" class="nav-link">Home</router-link>
        <router-link to="/weather" class="nav-link">Weather</router-link>
        <router-link to="/meals" class="nav-link">Meals</router-link>
        <router-link to="/leaderboard" class="nav-link">Leaderboard</router-link>
      </nav>
    </header>

    <main class="main-content">
      <!-- Weather and Activity Section -->
      <section class="weather-activity">
        <div class="weather-card">
          <h2>Current Weather in Singapore</h2>
          <div class="weather-info">
            <span class="temperature">32°C</span>
            <span class="weather-icon">☀️</span>
            <p>Sunny, Humidity: 75%</p>
          </div>
        </div>
        
        <div class="activity-recommendations">
          <h2>Recommended Activities</h2>
          <div class="activity-cards">
            <div class="activity-card">
              <span class="activity-icon">🏊‍♂️</span>
              <h3>Swimming</h3>
              <p>Perfect for hot weather!</p>
              <button class="start-btn">Start Activity</button>
            </div>
            <div class="activity-card">
              <span class="activity-icon">🏃‍♂️</span>
              <h3>Indoor Running</h3>
              <p>Beat the heat at the gym</p>
              <button class="start-btn">Start Activity</button>
            </div>
          </div>
        </div>
      </section>

      <!-- Progress Section -->
      <section class="progress-section">
        <h2>Your Progress</h2>
        <div class="progress-cards">
          <div class="progress-card">
            <h3>Workouts Completed</h3>
            <div class="progress-number">12</div>
            <p>This Week</p>
          </div>
          <div class="progress-card">
            <h3>Calories Burned</h3>
            <div class="progress-number">2,450</div>
            <p>This Week</p>
          </div>
          <div class="progress-card">
            <h3>Active Minutes</h3>
            <div class="progress-number">320</div>
            <p>This Week</p>
          </div>
        </div>
      </section>

      <!-- Meal Recommendations -->
      <section class="meal-section">
        <h2>Today's Meal Plan</h2>
        <div class="meal-cards">
          <div class="meal-card">
            <img src="https://placehold.co/200x150" alt="Breakfast" class="meal-image">
            <h3>Breakfast</h3>
            <p>Oatmeal with Berries</p>
            <span class="calories">320 cal</span>
          </div>
          <div class="meal-card">
            <img src="https://placehold.co/200x150" alt="Lunch" class="meal-image">
            <h3>Lunch</h3>
            <p>Grilled Chicken Salad</p>
            <span class="calories">450 cal</span>
          </div>
          <div class="meal-card">
            <img src="https://placehold.co/200x150" alt="Dinner" class="meal-image">
            <h3>Dinner</h3>
            <p>Salmon with Quinoa</p>
            <span class="calories">580 cal</span>
          </div>
        </div>
      </section>
    </main>

    <footer class="footer">
      <p>© 2024 EcoSmart Diet. All rights reserved.</p>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'Homepage',
  data() {
    return {
      // Mock data can be moved here later
    }
  }
}
</script>

<style scoped>
.homepage {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 0;
  border-bottom: 1px solid #eee;
}

.logo h1 {
  color: #2c3e50;
  font-size: 24px;
}

.nav-menu {
  display: flex;
  gap: 30px;
}

.nav-link {
  text-decoration: none;
  color: #333;
  font-weight: 500;
  padding: 5px 10px;
}

.router-link-active {
  color: #42b983;
  border-bottom: 2px solid #42b983;
}

/* Weather and Activity Section */
.weather-activity {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 20px;
  margin: 30px 0;
}

.weather-card {
  background: linear-gradient(135deg, #00b4db, #0083b0);
  color: white;
  padding: 20px;
  border-radius: 15px;
  text-align: center;
}

.weather-info {
  margin-top: 20px;
}

.temperature {
  font-size: 48px;
  font-weight: bold;
}

.weather-icon {
  font-size: 40px;
  margin-left: 10px;
}

.activity-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.activity-card {
  background: white;
  padding: 20px;
  border-radius: 15px;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.activity-icon {
  font-size: 32px;
}

.start-btn {
  background: #42b983;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 10px;
}

/* Progress Section */
.progress-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin: 20px 0;
}

.progress-card {
  background: white;
  padding: 20px;
  border-radius: 15px;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.progress-number {
  font-size: 36px;
  font-weight: bold;
  color: #42b983;
  margin: 10px 0;
}

/* Meal Section */
.meal-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin: 20px 0;
}

.meal-card {
  background: white;
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.meal-image {
  width: 100%;
  height: 150px;
  object-fit: cover;
}

.meal-card h3,
.meal-card p,
.meal-card .calories {
  padding: 5px 15px;
}

.calories {
  color: #666;
  font-size: 14px;
  display: block;
  padding-bottom: 15px;
}

h2 {
  color: #2c3e50;
  margin: 30px 0 20px;
}

@media (max-width: 768px) {
  .weather-activity {
    grid-template-columns: 1fr;
  }
  
  .progress-cards,
  .meal-cards {
    grid-template-columns: 1fr;
  }
}

.footer {
  text-align: center;
  padding: 20px 0;
  margin-top: 60px;
  border-top: 1px solid #eee;
  color: #666;
}
</style>
