<template>
  <div class="homepage">
    <header class="header">
      <Logo />
      <NavBar />
    </header>

    <div class="main-content">
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
              <!-- <span class="activity-icon">🏊‍♂️</span>
              <h3>Swimming</h3>
              <p>Perfect for hot weather!</p>
              <button class="start-btn">Start Activity</button>
              {{ recommendation }}
            </div>
            <div class="activity-card">
              <span class="activity-icon">🏃‍♂️</span>
              <h3>Indoor Running</h3>
              <p>Beat the heat at the gym</p>
              <button class="start-btn">Start Activity</button>
              {{ recommendation }} -->
              <div v-if="recommendation">{{ recommendation }}</div>
              <div v-else>Loading recommendation...</div>
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
    </div>

    <footer class="footer">
      <p>© 2024 EcoSmart Diet. All rights reserved.</p>
    </footer>
  </div>
</template>

<script>
import NavBar from './NavBar.vue';
import Logo from './logo.vue';
import { ref, onMounted } from 'vue';
import axios from 'axios';

export default {
  name: 'Homepage',
  components: {
    NavBar,
    Logo
  },
  data() {
    return {
      // Mock data can be moved here later
    }
  }, 

  setup() {  
    const recommendation = ref(null)

    const getFitnessRecommendation = async () => {
      try {
        const response = await axios.get('http://localhost:5050/recommendation') 
        recommendation.value = response.data.recommendation
      } catch (error) {
        recommendation.value = 'Failed to fetch recommendation'
      }
    }

    onMounted(() => {
      getFitnessRecommendation()
    })

    return {  
      recommendation
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

.homepage,
.weatherrecc,
.userpage,
.leaderboard,
.authentication,
.mealrecc {
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

/* Weather and Activity Section */
.weather-activity {
  position: relative;
  width: 100%;
  display: flex;
  gap: 40px;
}

.weather-card {
  width: 300px;
  background: linear-gradient(135deg, #00b4db, #0083b0);
  padding: 20px;
  border-radius: 15px;
  color: white;
}

.activity-recommendations {
  flex: 1;
}

.activity-cards {
  display: flex;
  gap: 30px;
}

.activity-card {
  flex: 1;
  background: #444;
  padding: 20px;
  border-radius: 15px;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
  color: white;
}

/* Progress Section */
.progress-cards {
  display: flex;
  gap: 30px;
}

.progress-card {
  flex: 1;
  background: #444;
  padding: 20px;
  border-radius: 15px;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
  color: white;
}

.footer {
  width: 100%;
  padding: 20px 80px;
  border-top: 1px solid #444;
  text-align: center;
  color: white;
  background-color: #333;
}

h1, h2, h3, p {
  color: white;
}

@media (max-width: 1024px) {
  .header,
  .main-content,
  .footer {
    padding-left: 40px;
    padding-right: 40px;
  }
}

@media (max-width: 768px) {
  .header,
  .main-content,
  .footer {
    padding-left: 20px;
    padding-right: 20px;
  }

  .weather-activity,
  .activity-cards,
  .progress-cards {
    flex-direction: column;
  }

  .weather-card {
    width: 100%;
  }
  :deep(.logo h1) {
        color: #42b983;  
        font-size: 24px;
    }

    :deep(.logo a) {
        color: #42b983;
        text-decoration: none;
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
