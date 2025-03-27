<template>
  <div class="weatherrecc">
    <header class="header">
      <Logo />
      <NavBar />
    </header>

    <main class="main-content">
      <!-- Current Weather Section -->
      <section class="weather-section">
        <div class="location-header">
          <h2>Weather in Singapore</h2>
          <button class="location-btn">📍 Update Location</button>
        </div>
        
        <div class="weather-details">
          <div class="current-weather">
            <div class="temperature-display">
              <span class="temperature">32°C</span>
              <span class="weather-icon">☀️</span>
            </div>
            <div class="weather-info">
              <p class="condition">Sunny</p>
              <p class="humidity">Humidity: 75%</p>
              <p class="wind">Wind: 12 km/h</p>
            </div>
          </div>

          <div class="hourly-forecast">
            <div class="forecast-item">
              <span class="time">Now</span>
              <span class="icon">☀️</span>
              <span class="temp">32°C</span>
            </div>
            <div class="forecast-item">
              <span class="time">2PM</span>
              <span class="icon">⛅</span>
              <span class="temp">33°C</span>
            </div>
            <div class="forecast-item">
              <span class="time">3PM</span>
              <span class="icon">🌥️</span>
              <span class="temp">31°C</span>
            </div>
            <div class="forecast-item">
              <span class="time">4PM</span>
              <span class="icon">⛅</span>
              <span class="temp">30°C</span>
            </div>
          </div>
        </div>
      </section>

      <!-- Weather Tips Section -->
      <section class="tips-section">
        <h2>Weather Tips</h2>
        <div class="tips-container">
          <div class="tip-card">
            <span class="tip-icon">🧴</span>
            <div class="tip-content">
              <h3>UV Index: High</h3>
              <p>Apply sunscreen SPF 50+ before outdoor activities</p>
            </div>
          </div>
          <div class="tip-card">
            <span class="tip-icon">⏰</span>
            <div class="tip-content">
              <h3>Best Time to Exercise</h3>
              <p>Recommended: Before 9AM or after 6PM</p>
            </div>
          </div>
          <div class="tip-card">
            <span class="tip-icon">💧</span>
            <div class="tip-content">
              <h3>Stay Hydrated</h3>
              <p>Drink water every 15-20 minutes during exercise</p>
            </div>
          </div>
        </div>
      </section>

      <!-- Goals Progress Section -->
      <section class="goals-section">
        <h2>Your Fitness Goals</h2>
        <div class="goals-container">
          <div class="goal-card">
            <div class="goal-header">
              <h3>Weekly Exercise Goal</h3>
              <span class="goal-percentage">75%</span>
            </div>
            <div class="progress-bar">
              <div class="progress" style="width: 75%"></div>
            </div>
            <p class="goal-stats">3 of 4 workouts completed</p>
          </div>

          <div class="goal-card">
            <div class="goal-header">
              <h3>Monthly Active Days</h3>
              <span class="goal-percentage">60%</span>
            </div>
            <div class="progress-bar">
              <div class="progress" style="width: 60%"></div>
            </div>
            <p class="goal-stats">18 of 30 days active</p>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script>
import NavBar from './NavBar.vue';
import Logo from './Logo.vue';

export default {
  name: 'WeatherRecc',
  components: {
    NavBar,
    Logo
  },
  data() {
    return {
      // Mock data will be replaced with real data later
    }
  }
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.weatherrecc {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  min-height: 100vh;
  background: #333;
}

.header {
  position: relative;
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 80px;
  background: #333;
  border-bottom: 1px solid #444;
}

.main-content {
  position: relative;
  width: 100%;
  padding: 40px 80px;
  background: #333;
}

/* Weather Section */
.weather-section {
  position: relative;
  width: 100%;
  background: linear-gradient(135deg, #00b4db, #0083b0);
  color: white;
  padding: 30px;
  border-radius: 20px;
  margin-bottom: 30px;
}

.location-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.weather-details {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 30px;
}

.current-weather {
  text-align: center;
}

.temperature-display {
  margin: 20px 0;
}

.temperature {
  font-size: 64px;
  font-weight: bold;
  color: white;
}

.weather-icon {
  font-size: 48px;
  margin-left: 10px;
}

.hourly-forecast {
  display: flex;
  justify-content: space-between;
  background: rgba(255, 255, 255, 0.1);
  padding: 20px;
  border-radius: 15px;
}

.forecast-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

/* Tips Section */
.tips-section {
  position: relative;
  width: 100%;
  margin-bottom: 30px;
}

.tips-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.tip-card {
  background: #444;
  padding: 20px;
  border-radius: 15px;
  display: flex;
  align-items: center;
  color: white;
}

.tip-icon {
  font-size: 32px;
  margin-right: 20px;
}

/* Goals Section */
.goals-section {
  position: relative;
  width: 100%;
}

.goals-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.goal-card {
  background: #444;
  padding: 20px;
  border-radius: 15px;
  color: white;
}

.goal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.goal-percentage {
  color: #42b983;
  font-weight: bold;
}

.progress-bar {
  background: #555;
  height: 8px;
  border-radius: 4px;
  overflow: hidden;
}

.progress {
  background: #42b983;
  height: 100%;
}

.goal-stats {
  color: #ccc;
}

/* Text Colors */
h2 {
  color: white;
  margin-bottom: 20px;
}

h3 {
  color: white;
  margin: 0;
}

p {
  color: white;
}

/* Buttons */
.location-btn {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  padding: 8px 16px;
  border-radius: 20px;
  color: white;
  cursor: pointer;
}

@media (max-width: 1024px) {
  .header,
  .main-content {
    padding: 20px 40px;
  }
}

@media (max-width: 768px) {
  .header,
  .main-content {
    padding: 20px;
  }

  .weather-details {
    grid-template-columns: 1fr;
  }

  .hourly-forecast {
    overflow-x: auto;
    padding: 15px;
  }

  .forecast-item {
    min-width: 80px;
  }
  
}

/* Add after the header styles */
:deep(.logo h1) {
    color: #42b983;  
    font-size: 24px;
}

:deep(.logo a) {
    color: #42b983;
    text-decoration: none;
}
</style> 