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
          <div class="weather-info" v-if="weather">
            <span class="temperature">{{ weather.temperature }}°C</span>
            <span class="weather-icon">
              {{ weather.condition === 'Clear' ? '☀️' : weather.condition === 'Rain' ? '🌧️' : '☁️' }}
            </span>
            <p>{{ weather.condition }}</p><p :style="{ fontSize: '32px',fontWeight: '600',
                    textShadow: '1px 1px 4px rgba(0,0,0,0.4)',
                    margin: '10px 0' }">Humidity: {{ weather.humidity }}%</p>
          </div>
          <div v-else>
            <p>Loading weather data...</p>
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

      <!-- Activity History Section -->
    <section class="activity-history-section">
      <div class="history-header">
        <h2>Your Activity History</h2>
        <select v-model="historyFilter" class="history-filter">
          <option value="week">This Week</option>
          <option value="all">All</option>
        </select>
      </div>

      <div v-if="filteredActivities && filteredActivities.length" class="activity-history-list">
        <div 
          v-for="activity in filteredActivities" 
          :key="activity.id" 
          class="activity-item"
        >
          <div class="activity-main">
            <strong>{{ activity.exerciseType }}</strong> – {{ activity.duration }} mins
          </div>
          <div class="activity-meta">
            📅 {{ formatDate(activity.timestamp) }} · 🔥 {{ activity.caloriesBurned }} kcal · 
            <span class="badge" :class="activity.intensity">
              {{ activity.intensity === 'high' ? '💪' : activity.intensity === 'medium' ? '🏃' : '🧘' }} {{ activity.intensity }}
            </span>
          </div>
        </div>
      </div>

      <div v-else class="no-history">
        No activities found for selected period.
      </div>
    </section>


    <!-- Add toast notification -->
    <div v-if="showToast" class="toast-notification" :class="{ 'show': showToast }">
      <div class="toast-content">
        <div class="toast-icon">✓</div>
        <div class="toast-message">
          <h4>Activity Logged Successfully!</h4>
          <div class="activity-details">
            <p><strong>Type:</strong> {{ toastData.type }}</p>
            <p><strong>Duration:</strong> {{ toastData.duration }} minutes</p>
            <p><strong>Calories Burned:</strong> {{ toastData.calories }}</p>
            <p><strong>Intensity:</strong> {{ toastData.intensity }}</p>
          </div>
        </div>
      </div>
      <button class="toast-close" @click="closeToast">&times;</button>
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
      },
      
      showToast: false,
      toastData: {
        type: '',
        duration: 0,
        calories: 0,
        intensity: ''
      },
      historyFilter: 'week',
      allActivities: [],
    }
  }, 

  setup() {  
    const recommendation = ref(null)
    const weather = ref(null)

    const getFitnessRecommendation = async () => {
      try {
        const user = JSON.parse(localStorage.getItem('user'));
        if (!user || !user.userId) {
          recommendation.value = 'Please log in to get personalized recommendations.';
          return;
        }
        const response = await axios.get(`http://localhost:8000/fitnessrecommendation/recommendation?userId=${user.userId}&location=Singapore`);
        const data = response.data // ✅ YOU NEED THIS LINE

        console.log('Received response from fitnessrecommendation:', data)

        recommendation.value = response.data.recommendation || 'No recommendation available';

        if (data.weather) {
          weather.value = {
            temperature: data.weather.temperature,
            condition: data.weather.condition,
            humidity: data.weather.humidity
          }
        }
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
      recommendation,
      weather
    }
  },

  computed: {
    filteredActivities() {
        if (!this.allActivities || this.allActivities.length === 0) return []

        const now = new Date()
        const oneWeekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000)

        return this.historyFilter === 'week'
          ? this.allActivities.filter(activity => new Date(activity.timestamp) >= oneWeekAgo)
          : this.allActivities
      }
    },

  methods: {
    scrollToContent() {
      const mainContent = document.querySelector('.main-content')
      mainContent.scrollIntoView({ behavior: 'smooth' })
    },

    formatDate(dateStr) {
      const date = new Date(dateStr)
      return date.toLocaleDateString(undefined, {
        weekday: 'short',
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      })
    },

    async getStats() {
      try {
        const user = JSON.parse(localStorage.getItem('user'))
        if (!user || !user.userId) return

        const response = await axios.get(`http://localhost:8000/activity/${user.userId}`)
        if (response.data) {
          // Calculate weekly stats
          const now = new Date()
          const weekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000)
          
          const weeklyActivities = response.data.filter(activity => {
            const activityDate = new Date(activity.timestamp)
            return activityDate >= weekAgo
          })
          
          this.allActivities = response.data;

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

    showActivityToast(activityData) {
      this.toastData = {
        type: activityData.exerciseType,
        duration: activityData.duration,
        calories: activityData.caloriesBurned,
        intensity: activityData.intensity
      }
      this.showToast = true
      setTimeout(() => {
        this.closeToast()
      }, 5000) // Auto close after 5 seconds
    },

    closeToast() {
      this.showToast = false
    },

    async logActivity() {
      if (!this.activityData.type || !this.activityData.duration) {
        alert('Please fill in all required fields')
        return
      }

      try {
        const user = JSON.parse(localStorage.getItem('user'))
        if (!user || !user.userId) {
          alert('Please log in to log activities')
          return
        }

        console.log('Starting activity logging process...')
        console.log('User:', user.userId)
        console.log('Activity Data:', {
          type: this.activityData.type,
          duration: this.activityData.duration,
          notes: this.activityData.notes
        })

        // First, log the activity through ActivityCoordination service
        console.log('Sending request to ActivityCoordination service...')
        const coordinationResponse = await axios.post('http://localhost:8000/activitycoordination/activity', {
          userId: user.userId,
          activityType: this.activityData.type,
          duration: parseInt(this.activityData.duration)
        })

        console.log('ActivityCoordination response:', coordinationResponse.data)

        if (coordinationResponse.data && coordinationResponse.data.code === 200) {
          const activityData = coordinationResponse.data.data
          console.log('Activity processed successfully:', activityData)

          // Now verify the activity was logged in the activity log service
          try {
            console.log('Verifying activity log in database...')
            const logResponse = await axios.get(`http://localhost:8000/activity/${user.userId}`)
            console.log('Activity log verification response:', logResponse.data)

            // The response is an array of activities
            const activities = logResponse.data
            if (Array.isArray(activities) && activities.length > 0) {
              // Find the activity we just logged
              const matchingActivity = activities.find(activity => 
                activity.exerciseType === this.activityData.type &&
                activity.duration === parseInt(this.activityData.duration)
              )

              if (matchingActivity) {
                console.log('Activity successfully verified in database:', matchingActivity)
              } else {
                console.warn('Activity not found in database. Latest activities:', activities.slice(-3))
              }
            } else {
              console.warn('No activities found in database')
            }
          } catch (logError) {
            console.error('Error verifying activity log:', logError)
            if (logError.response) {
              console.error('Error response:', {
                status: logError.response.status,
                data: logError.response.data,
                headers: logError.response.headers
              })
            }
          }
          
          // Clear form
          this.activityData = {
            type: '',
            duration: null,
            notes: ''
          }
          
          // Show success toast
          this.showActivityToast(activityData.activity)
          
          // Refresh data
          console.log('Refreshing recommendations and stats...')
          //await this.getFitnessRecommendation()
          await this.getStats()
          console.log('Stats and recommendations refreshed')
        } else {
          throw new Error(coordinationResponse.data?.message || 'Failed to log activity')
        }
      } catch (error) {
        console.error('Error in activity logging process:', error)
        if (error.response) {
          console.error('Error response:', {
            status: error.response.status,
            data: error.response.data,
            headers: error.response.headers
          })
        }
        alert(error.message || 'Failed to log activity. Please try again.')
      }
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

.weather-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  margin-top: 10px;
}

.weather-icon {
  font-size: 2rem;
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

/* toast notif*/
.toast-notification {
  position: fixed;
  bottom: 30px;
  right: 30px;
  background-color: #333;
  color: white;
  padding: 16px 24px;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  z-index: 9999;
  display: flex;
  align-items: center;
  gap: 12px;
  max-width: 300px;
  animation: slideUp 0.4s ease-out;
}

.toast-icon {
  font-size: 24px;
  color: #42b983;
}

.toast-message h4 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
}

.toast-message p {
  font-size: 14px;
  margin: 4px 0 0;
}

.toast-close {
  background: none;
  border: none;
  color: white;
  font-size: 20px;
  margin-left: auto;
  cursor: pointer;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* history*/
.activity-history-section {
  margin-top: 50px;
  background: #444;
  padding: 30px;
  border-radius: 15px;
}

.history-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.history-filter {
  padding: 8px 12px;
  border-radius: 6px;
  background-color: #333;
  color: white;
  border: 1px solid #555;
}

.activity-history-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.activity-item {
  background: #333;
  padding: 12px 16px;
  border-radius: 8px;
  color: white;
  border: 1px solid #555;
  font-size: 0.95rem;
}

.no-history {
  color: #aaa;
  text-align: center;
  margin-top: 20px;
  font-style: italic;
}

.badge {
  background: #42b983;
  color: white;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 0.75rem;
  text-transform: capitalize;
}


</style>
