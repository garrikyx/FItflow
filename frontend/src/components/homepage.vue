<template>
  <div class="homepage">
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&family=Poppins:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    
    <header class="header">
      <Logo />
      <NavBar />
    </header>

    <!-- Full Screen Landing Section -->
    <section class="landing-section">
      <div class="landing-content">
        <h1 class="site-title">FitFlow</h1>
        <p class="site-subtitle">Your Personal Fitness Journey Starts Here</p>
        <button class="get-started-btn" @click="scrollToContent">Get Started</button>
      </div>
    </section>

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
              <div v-if="recommendation">
                <h3>Today's Recommendation</h3>
                <p>{{ recommendation }}</p>
              </div>
              <div v-else>
                <h3>Loading...</h3>
                <p>Getting your personalized recommendation...</p>
            </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Activity Logging Section -->
      <section class="activity-logging">
        <h2>Log Your Activity</h2>
        <div class="activity-form">
          <div class="form-group">
            <label>Activity Type</label>
            <select v-model="activityData.type" class="form-input">
              <option value="">Select an activity</option>
              <option value="running">Running</option>
              <option value="walking">Walking</option>
              <option value="cycling">Cycling</option>
              <option value="swimming">Swimming</option>
              <option value="hiking">Hiking</option>
              <option value="yoga">Yoga</option>
              <option value="weightlifting">Weight Lifting</option>
              <option value="dancing">Dancing</option>
              <option value="basketball">Basketball</option>
              <option value="soccer">Soccer</option>
              <option value="tennis">Tennis</option>
            </select>
          </div>

          <div class="form-group">
            <label>Duration (minutes)</label>
            <input 
              type="number" 
              v-model="activityData.duration" 
              class="form-input"
              min="1"
              placeholder="Enter duration in minutes"
            />
          </div>

          <div class="form-group">
            <label>Calories Burned</label>
            <input 
              type="number" 
              v-model="activityData.calories"
              min="1"
              class="form-input"
              placeholder="Enter calories burned"
            ></input>
          </div>

          <div class="form-group">
            <label>Intensity</label>
            <select v-model="activityData.intensity" class="form-input">
              <option value="">Select an Intensity</option>
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
            </select>
          </div>

          <div class="form-group">
            <label>Notes (optional)</label>
            <textarea 
              v-model="activityData.notes" 
              class="form-input"
              placeholder="Add any notes about your activity"
            ></textarea>
          </div>

          <button @click="logActivity" class="log-btn">Log Activity</button>
        </div>
      </section>

      <!-- Progress Section -->
      <section class="progress-section">
        <h2>Your Progress</h2>
        <div class="progress-cards">
          <div class="progress-card">
            <h3>Workouts Completed</h3>
            <div class="progress-number">{{ stats.workouts || 0 }}</div>
            <p>This Week</p>
          </div>
          <div class="progress-card">
            <h3>Calories Burned</h3>
            <div class="progress-number">{{ stats.calories || 0 }}</div>
            <p>This Week</p>
          </div>
          <div class="progress-card">
            <h3>Active Minutes</h3>
            <div class="progress-number">{{ stats.minutes || 0 }}</div>
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
      activityData: {
        type: '',
        duration: null,
        notes: ''
      },
      stats: {
        workouts: 0,
        calories: 0,
        minutes: 0
      }
    }
  }, 

  setup() {  
    const recommendation = ref(null)

    const getFitnessRecommendation = async () => {
      try {
        const user = JSON.parse(localStorage.getItem('user'));
        if (!user || !user.userId) {
          recommendation.value = 'Please log in to get personalized recommendations.';
          return;
        }
        const response = await axios.get(`http://localhost:8000/fitnessrecommendation/recommendation?userId=${user.userId}&location=Singapore`);
        recommendation.value = response.data.recommendation || 'No recommendation available';
      } catch (error) {
        console.error('Error:', error);
        if (error.response?.status === 404) {
          recommendation.value = 'Welcome! Start by recording some activities to get personalized recommendations.'
        } else {
          recommendation.value = 'Unable to load recommendation at this time. Please try again later.'
        }
      }
    }

    onMounted(() => {
      getFitnessRecommendation()
    })

    return {  
      recommendation
    }
  },

  methods: {
    scrollToContent() {
      const mainContent = document.querySelector('.main-content')
      mainContent.scrollIntoView({ behavior: 'smooth' })
    },

    async getStats() {
      try {
        const user = JSON.parse(localStorage.getItem('user'))
        if (!user || !user.userId) return

        const response = await axios.get(`http://localhost:8000/activitylog/activity/${user.userId}`)
        if (response.data) {
          // Calculate weekly stats
          const now = new Date()
          const weekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000)
          
          const weeklyActivities = response.data.filter(activity => {
            const activityDate = new Date(activity.timestamp)
            return activityDate >= weekAgo
          })

          this.stats = {
            workouts: weeklyActivities.length,
            calories: weeklyActivities.reduce((sum, activity) => sum + activity.caloriesBurned, 0),
            minutes: weeklyActivities.reduce((sum, activity) => sum + activity.duration, 0)
          }
        }
      } catch (error) {
        console.error('Error fetching stats:', error)
      }
    },

    async logActivity() {
      if (!this.activityData.type || !this.activityData.duration || !this.activityData.calories || !this.activityData.intensity) {
        alert('Please fill in all required fields')
        return
      }

      try {
        const user = JSON.parse(localStorage.getItem('user'))
        if (!user || !user.userId) {
          alert('Please log in to log activities')
          return
        }

        const response = await axios.post('http://localhost:8000/activitylog/activity', {
          userId: user.userId,
          exerciseType: this.activityData.type,
          duration: parseInt(this.activityData.duration),
          intensity: this.activityData.intensity,
          caloriesBurned: parseInt(this.activityData.calories)
        })

        if (response.data) {
          // Clear form
          this.activityData = {
            type: '',
            duration: null,
            calories: null,
            intensity: '',
            notes: ''
          }
          alert('Activity logged successfully!')
          // Refresh recommendations and stats
          this.getFitnessRecommendation()
        }
      } catch (error) {
        console.error('Error logging activity:', error)
        alert('Failed to log activity. Please try again.')
      }
    },

    calculateIntensity(type, duration) {
      const highIntensity = ['running', 'swimming', 'basketball', 'soccer', 'tennis']
      const mediumIntensity = ['cycling', 'hiking', 'dancing', 'weightlifting']
      const lowIntensity = ['walking', 'yoga']

      let baseIntensity
      if (highIntensity.includes(type)) baseIntensity = 'high'
      else if (mediumIntensity.includes(type)) baseIntensity = 'medium'
      else baseIntensity = 'low'

      // Adjust based on duration
      if (duration < 15) return 'low'
      if (duration > 45) return 'high'
      return baseIntensity
    },

  
  },

  mounted() {
    this.getStats()
  }
}
</script>

<style scoped>
/* Base Font Settings */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Inter', sans-serif;
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
  position: fixed;
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 80px;
  background: rgba(51, 51, 51, 0.9);
  border-bottom: 1px solid #444;
  z-index: 1000;
}

.main-content {
  position: relative;
  width: 100%;
  padding: 100px 80px 40px 80px;
  background: #333;
  min-height: 110vh;
}

/* Landing Section Styles */
.landing-section {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #333 0%, #222 100%);
  text-align: center;
  padding: 20px;
}

.landing-content {
  max-width: 800px;
}

/* Landing Section Typography */
.site-title {
  font-family: 'Montserrat', sans-serif;
  font-size: 5rem;
  font-weight: 700;
  color: #42b983;
  margin-bottom: 20px;
  animation: fadeInUp 1s ease;
  letter-spacing: -1px;
  text-transform: uppercase;
}

.site-subtitle {
  font-family: 'Poppins', sans-serif;
  font-size: 1.8rem;
  font-weight: 300;
  color: white;
  margin-bottom: 30px;
  animation: fadeInUp 1s ease 0.3s;
  opacity: 0;
  animation-fill-mode: forwards;
  letter-spacing: 0.5px;
}

.get-started-btn {
  font-family: 'Montserrat', sans-serif;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
  padding: 15px 40px;
  font-size: 1.1rem;
  background: #42b983;
  color: white;
  border: none;
  border-radius: 30px;
  cursor: pointer;
  transition: all 0.3s ease;
  animation: fadeInUp 1s ease 0.6s;
  opacity: 0;
  animation-fill-mode: forwards;
}

.get-started-btn:hover {
  background: #3aa876;
  transform: translateY(-2px);
}

/* Section Headers */
h2 {
  font-family: 'Montserrat', sans-serif;
  font-weight: 600;
  font-size: 2rem;
  color: white;
  margin-bottom: 1.5rem;
  letter-spacing: -0.5px;
}

h3 {
  font-family: 'Poppins', sans-serif;
  font-weight: 500;
  font-size: 1.2rem;
  color: white;
  margin-bottom: 0.5rem;
}

/* Form Labels and Inputs */
label {
  font-family: 'Inter', sans-serif;
  font-weight: 500;
  font-size: 0.9rem;
  color: white;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.form-input {
  font-family: 'Inter', sans-serif;
  font-size: 1rem;
  padding: 12px 16px;
  border: 1px solid #555;
  border-radius: 8px;
  background: #333;
  color: white;
}

/* Add styles for select element and its options */
select.form-input {
  appearance: none;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='white'%3e%3cpath d='M7 10l5 5 5-5z'/%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 1rem center;
  background-size: 1.5em 1.5em;
  padding-right: 2.5rem;
}

select.form-input option {
  background-color: #333;
  color: white;
  padding: 12px;
}

select.form-input:focus {
  outline: none;
  border-color: #42b983;
  box-shadow: 0 0 0 2px rgba(66, 185, 131, 0.2);
}

/* Weather and Activity Section */
.weather-activity {
  position: relative;
  width: 100%;
  display: flex;
  gap: 40px;
  margin-top: 40px;
}

.weather-card {
  width: 300px;
  background: linear-gradient(135deg, #00b4db, #0083b0);
  padding: 20px;
  border-radius: 15px;
  color: white;
}

.weather-card h2 {
  font-family: 'Poppins', sans-serif;
  font-size: 1.4rem;
  font-weight: 500;
}

.temperature {
  font-family: 'Montserrat', sans-serif;
  font-size: 3rem;
  font-weight: 700;
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

  .site-title {
    font-size: 4rem;
  }
  
  .site-subtitle {
    font-size: 1.5rem;
  }
  
  h2 {
    font-size: 1.8rem;
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

  .site-title {
    font-size: 3rem;
  }
  
  .site-subtitle {
    font-size: 1.2rem;
    }

  h2 {
    font-size: 1.6rem;
  }
  
  .progress-number {
    font-size: 2rem;
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

/* Activity Logging Styles */
.activity-logging {
  background: #444;
  padding: 30px;
  border-radius: 15px;
  margin: 40px 0;
}

.activity-form {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

/* Animation Keyframes */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.activity-form .log-btn {
  background: #42b983;
  border: none;
  cursor: pointer;
  font-size: 0.9rem;
  color: white;
  padding: 12px 32px;
  border-radius: 6px;
  transition: all 0.2s ease;
  margin: 25px auto 5px;
  display: block;
  text-transform: none;
  font-weight: 600;
  letter-spacing: 0.3px;
  white-space: nowrap;
  box-shadow: 0 1px 2px rgba(66, 185, 131, 0.15);
  width: 180px;
}

.activity-form .log-btn:hover {
  background: #3aa876;
  box-shadow: 0 2px 4px rgba(66, 185, 131, 0.2);
}

.activity-form .log-btn:active {
  background: #389d6e;
  transform: translateY(1px);
  box-shadow: none;
}
</style>
