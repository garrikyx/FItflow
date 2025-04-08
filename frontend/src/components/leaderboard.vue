<template>
  <div class="leaderboard">
    <header class="header">
      <Logo />
      <NavBar />
    </header>
    <div class="main-content">
      <!-- Inline Styled Notification - Only shows when rank changes detected -->
      <div v-if="showNotificationPopup && latestNotification" style="position: fixed; top: 20px; right: 20px; width: 300px; background-color: #333; color: white; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.2); z-index: 1000; overflow: hidden; animation: slideIn 0.3s ease-out;">
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 12px 15px; background-color: #42b983;">
          <span style="font-weight: 600; color: white; font-size: 14px;">Rank Change Alert</span>
          <button @click="closeNotificationPopup" style="background: none; border: none; color: white; font-size: 18px; cursor: pointer; padding: 0; line-height: 1;">×</button>
        </div>
        <div style="padding: 15px; color: white;">
          <p style="margin: 0; font-size: 14px;">{{ latestNotification.message }}</p>
          <span style="display: block; margin-top: 10px; font-size: 12px; color: #aaa; text-align: right;">{{ formatTime(latestNotification.timestamp) }}</span>
        </div>
      </div>

      <!-- Leaderboard Section -->
      <section class="leaderboard-section">
        <div class="section-header">
          <h2>Leaderboard</h2>
        </div>
        
        <div class="leaderboard-container">
          <!-- Loading State -->
          <div v-if="loading" class="loading-state">
            Loading leaderboard data...
          </div>
          
          <!-- Error State -->
          <div v-else-if="error" class="error-state">
            {{ error }}
          </div>
          
          <!-- Leaderboard Data -->
          <div v-else>
            <div class="leaderboard-list">
              <!-- Headers -->
              <div class="leaderboard-header">
                <span class="rank-header">Rank</span>
                <span class="name-header">User</span>
                <span class="points-header">Calories Burned</span>
              </div>
              
              <div 
                v-for="(user, index) in displayData" 
                :key="user.user_id"
                class="leaderboard-item"
                :class="{'highlighted': user.user_id === currentUser?.userId}"
              >
                <span class="rank" :data-rank="index + 1">
                  #{{ index + 1 }}
                  <span v-if="index < 3" class="rank-emoji">
                    {{ index === 0 ? '🥇' : index === 1 ? '🥈' : '🥉' }}
                  </span>
                </span>
                <span class="name">{{ user.display_name || user.user_id }}</span>
                <span class="points">{{ user.calories_burned }}</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Monthly Stats -->
      <section class="stats-section">
        <h2>Monthly Statistics</h2>
        <div class="stats-container">
          <div class="stat-card">
            <h3>{{ monthlyStats.totalDuration }}</h3>
            <p>Active Minutes</p>
          </div>
          <div class="stat-card">
            <h3>{{ monthlyStats.totalCalories }}</h3>
            <p>Calories Burned</p>
          </div>
          <div class="stat-card">
            <h3>{{ monthlyStats.activities }}</h3>
            <p>Workouts Completed</p>
          </div>
          <div class="stat-card">
            <h3>{{ monthlyStats.rank }}</h3>
            <p>Your Rank</p>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script>
import NavBar from './NavBar.vue';
import Logo from './logo.vue';
import axios from 'axios';

export default {
  name: 'Leaderboard',
  components: {
    NavBar,
    Logo
  },
  data() {
    return {
      leaderboardData: [],
      friendsLeaderboardData: [],
      loading: true,
      error: null,
      currentUser: null,
      activeTab: 'weekly',
      notifications: [],
      showNotificationPopup: false,
      latestNotification: null,
      userPreviousRank: null,
      eventSource: null
    }
  },
  computed: {
    currentUserId() {
      return this.currentUser?.userId;
    },
    displayData() {
      // Both tabs show the same filtered data now
      return this.leaderboardData;
    },
    monthlyStats() {
      // Find user in leaderboard
      const userRank = this.findUserRank();
      
      // Calculate total calories
      let totalCalories = 0;
      if (this.displayData.length > 0) {
        const userEntry = this.displayData.find(entry => entry.user_id === this.currentUserId);
        if (userEntry) {
          totalCalories = userEntry.calories_burned;
        }
      }
      
      return {
        totalDuration: this.calculateTotalDuration(),
        totalCalories: totalCalories,
        activities: this.calculateTotalActivities(),
        rank: userRank ? userRank : '-'
      };
    }
  },
  methods: {
    async fetchFriendIds() {
      try {
        if (!this.currentUser || !this.currentUser.userId) {
          console.log('No user ID available to fetch friends');
          return [];
        }
        
        // Call the external friendship API
        const response = await axios.get(`https://personal-ywco1luc.outsystemscloud.com/SocialsService/rest/FriendAPI/Friends/${this.currentUser.userId}`);
        
        console.log('Friends response:', response.data);
        
        // Extract friend IDs from the response
        // Adapt this based on the actual response structure
        const friendIds = response.data.map(friend => friend.FriendId.toString());
        
        console.log('Friend IDs:', friendIds);
        return friendIds;
      } catch (error) {
        console.error('Error fetching friends:', error);
        return [];
      }
    },
    
    async fetchLeaderboardData() {
      try {
        this.loading = true;
        this.currentUser = JSON.parse(localStorage.getItem('user'));
        console.log('Current user:', this.currentUser);
        
        if (!this.currentUser || !this.currentUser.userId) {
          this.error = 'Please log in to view the leaderboard';
          console.log('No user found in localStorage');
          return;
        }

        // Get friend IDs first
        const friendIds = await this.fetchFriendIds();
        console.log('Friend IDs for filtering:', friendIds);
        
        // Add the current user's ID to the allowed IDs
        const allowedUserIds = [...friendIds, this.currentUser.userId];

        // Get weekly leaderboard data
        const weeklyResponse = await axios.get(`http://localhost:8000/leaderboard/weekly`);
        console.log('Weekly leaderboard response:', weeklyResponse.data);
        
        if (weeklyResponse.data?.code === 200) {
          const entries = weeklyResponse.data.data.entries;
          
          // Filter to only include friends and the current user
          const filteredEntries = entries.filter(entry => 
            allowedUserIds.includes(entry.user_id)
          );
          
          // Fetch user names for each entry
          for (let entry of filteredEntries) {
            try {
              const userResponse = await axios.get(`http://localhost:8000/user/${entry.user_id}`);
              if (userResponse.data?.data?.name) {
                entry.display_name = userResponse.data.data.name;
              }
            } catch (error) {
              console.warn(`Could not fetch name for user ${entry.user_id}:`, error);
              entry.display_name = entry.user_id;
            }
          }
          
          // Store previous rank before updating data
          this.storePreviousRank();
          
          this.leaderboardData = filteredEntries;
          
          // Check for rank changes after updating data
          this.checkRankChanges();
        }

        // No need to fetch separate friends leaderboard since we're already filtering
        // Just use the same data for both tabs
        this.friendsLeaderboardData = [...this.leaderboardData];
      } catch (error) {
        console.error('Error fetching leaderboard data:', error);
        this.error = 'Failed to load leaderboard data. Please try again later.';
      } finally {
        this.loading = false;
      }
    },
    
    storePreviousRank() {
      if (this.currentUser && this.leaderboardData.length > 0) {
        const currentUserIndex = this.leaderboardData.findIndex(
          entry => entry.user_id === this.currentUser.userId
        );
        if (currentUserIndex !== -1) {
          this.userPreviousRank = currentUserIndex + 1;
        }
      }
    },
    
    async checkRankChanges() {
      if (!this.userPreviousRank || !this.currentUser) return;
      
      const currentUserIndex = this.leaderboardData.findIndex(
        entry => entry.user_id === this.currentUser.userId
      );
      
      if (currentUserIndex !== -1) {
        const currentRank = currentUserIndex + 1;
        
        if (currentRank > this.userPreviousRank) {
          // User has been surpassed
          const potentiallySurpassingUsers = this.leaderboardData
            .filter((entry, index) => 
              index + 1 < currentRank && 
              index + 1 >= this.userPreviousRank && 
              entry.user_id !== this.currentUser.userId
            );
          
          if (potentiallySurpassingUsers.length > 0) {
            // Fetch friend IDs to filter only friends
            const friendIds = await this.fetchFriendIds();
            
            // Filter surpassing users to only include friends
            const surpassingFriends = potentiallySurpassingUsers
              .filter(user => friendIds.includes(user.user_id))
              .map(user => user.display_name || user.user_id);
            
            // Only show notification if friends surpassed the user
            if (surpassingFriends.length > 0) {
              this.showRankChangeNotification(surpassingFriends, currentRank);
              this.sendNotificationToService(surpassingFriends, currentRank);
            }
          }
        }
      }
    },
    
    showRankChangeNotification(users, newRank) {
      const userNames = users.join(', ');
      const message = users.length === 1 
        ? `${userNames} has surpassed you! You're now ranked #${newRank}.` 
        : `${userNames} have surpassed you! You're now ranked #${newRank}.`;
      
      const notification = {
        id: Date.now(),
        message: message,
        timestamp: new Date().toISOString()
      };
      
      this.latestNotification = notification;
      this.notifications.unshift(notification);
      this.showNotificationPopup = true;
      
      // Auto-hide after 8 seconds
      setTimeout(() => {
        this.showNotificationPopup = false;
      }, 8000);
    },
    
    async sendNotificationToService(surpassingFriends, newRank) {
      if (!this.currentUser) return;
      
      try {
        const userNames = surpassingFriends.join(', ');
        const message = surpassingFriends.length === 1 
          ? `${userNames} has surpassed you! You're now ranked #${newRank}.` 
          : `${userNames} have surpassed you! You're now ranked #${newRank}.`;
        
        // Get friend IDs
        const friendIds = await this.fetchFriendIds();
        
        // Send to notification service
        await axios.post('http://localhost:8000/notification/notify_leaderboard', {
          friends_user_ids: [this.currentUser.userId], // Only notify current user
          userId: surpassingFriends[0], // ID of user who surpassed
          name: surpassingFriends[0], // Name of user who surpassed
          message: message,
          timestamp: new Date().toISOString()
        });
        
        console.log('Leaderboard notification sent to service');
      } catch (error) {
        console.error('Failed to send notification to service:', error);
      }
    },
    
    setupNotifications() {
      this.currentUser = JSON.parse(localStorage.getItem('user'));
      if (!this.currentUser || !this.currentUser.userId) {
        console.log('No user found in localStorage');
        return;
      }

      try {
        console.log('Setting up notification system');
        
        // Connect to the notification stream
        this.connectToNotificationStream();
      } catch (error) {
        console.error('Error setting up notifications:', error);
      }
    },
    
    connectToNotificationStream() {
      // Use the correct notification service endpoint
      this.eventSource = new EventSource('http://localhost:8000/notification/events');
      
      this.eventSource.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          console.log('Received notification:', data);
          
          // Check if this notification is relevant to the current user
          if (data.type === 'leaderboard_pass' && data.friends_user_ids.includes(this.currentUser.userId)) {
            // Display the notification
            const notification = {
              id: Date.now(),
              message: data.message,
              timestamp: data.timestamp
            };
            
            this.latestNotification = notification;
            this.notifications.unshift(notification);
            this.showNotificationPopup = true;
            
            // Auto-hide after 8 seconds
            setTimeout(() => {
              this.showNotificationPopup = false;
            }, 8000);
          }
        } catch (error) {
          console.error('Error processing notification:', error);
        }
      };
      
      this.eventSource.onerror = (error) => {
        console.error('SSE Error:', error);
        this.eventSource.close();
        
        // Attempt to reconnect after 5 seconds
        setTimeout(() => {
          this.connectToNotificationStream();
        }, 5000);
      };
    },
    
    switchTab(tab) {
      this.activeTab = tab;
    },
    
    closeNotificationPopup() {
      this.showNotificationPopup = false;
    },
    
    formatTime(timestamp) {
      const date = new Date(timestamp);
      return date.toLocaleTimeString();
    },
    
    findUserRank() {
      if (!this.currentUser || this.displayData.length === 0) return '-';
      
      const userIndex = this.displayData.findIndex(
        entry => entry.user_id === this.currentUser.userId
      );
      
      return userIndex !== -1 ? userIndex + 1 : '-';
    },
    
    calculateTotalDuration() {
      return 120; // minutes
    },
    
    calculateTotalActivities() {
      return 8; // activities
    }
  },
  mounted() {
    this.fetchLeaderboardData();
    this.setupNotifications();
    
    // Set up periodic refresh (every 30 seconds)
    this.refreshInterval = setInterval(() => {
      this.fetchLeaderboardData();
    }, 30000);
  },
  beforeDestroy() {
    // Clear intervals and close connections
    if (this.refreshInterval) {
      clearInterval(this.refreshInterval);
    }
    
    if (this.eventSource) {
      this.eventSource.close();
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

@keyframes slideIn {
  0% {
    transform: translateX(100%);
    opacity: 0;
  }
  100% {
    transform: translateX(0);
    opacity: 1;
  }
}

.leaderboard {
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

.leaderboard-table {
  background: #444;
  border-radius: 15px;
  color: white;
}

h1, h2, h3, p {
  color: white;
}

/* For any card layouts */
.card-container {
  position: relative;
  width: 100%;
  display: flex;
  gap: 40px;
}

.card {
  background: white;
  padding: 20px;
  border-radius: 15px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

/* For grid layouts */
.grid-container {
  position: relative;
  width: 100%;
  display: grid;
  gap: 40px;
}

/* Responsive design */
@media (max-width: 1024px) {
  .header,
  .main-content {
    padding-left: 40px;
    padding-right: 40px;
  }
}

@media (max-width: 768px) {
  .header,
  .main-content {
    padding: 20px;
  }
  
  .card-container {
    flex-direction: column;
  }
}

.logo h1 {
  color: #42b983;
  font-size: 24px;
}

.logo-link {
  text-decoration: none;
}

.router-link-active {
  color: #42b983;
  border-bottom: 2px solid #42b983;
}

/* Leaderboard Section */
.leaderboard-container {
  background: white;
  border-radius: 20px;
  padding: 10px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  width: 100%;
  max-width: 900px;
  margin: 0 auto;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

/* Leaderboard List & Items */
.leaderboard-list {
  width: 100%;
  background: none;
  border-radius: 0;
}

.leaderboard-header {
  display: grid;
  grid-template-columns: 100px 1fr 200px;
  gap: 20px;
  padding: 15px 20px;
  background: #f5f5f5;
  color: #333;
  font-weight: bold;
  margin-bottom: 15px;
  border-radius: 8px;
}

.leaderboard-item {
  display: grid;
  grid-template-columns: 100px 1fr 200px;
  gap: 20px;
  align-items: center;
  padding: 15px 20px;
  border-bottom: 1px solid #eee;
  transition: background-color 0.2s;
}

.leaderboard-item:hover {
  background-color: #f8f9fa;
}

.leaderboard-item.highlighted {
  background-color: rgba(66, 185, 131, 0.1);
  border-left: 4px solid #42b983;
}

/* Column Styles */
.rank, .rank-header {
  text-align: left;
}

.rank {
  font-weight: bold;
  color: #42b983;
  font-size: 1.2em;
}

.name, .name-header {
  text-align: left;
  color: #333;
  font-size: 1.1em;
}

.points, .points-header {
  text-align: right;
  color: #666;
  font-weight: 500;
}

/* Stats Section */
.stats-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.stat-card {
  background: white;
  padding: 20px;
  border-radius: 15px;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.stat-card h3 {
  font-size: 28px;
  color: #42b983;
  margin: 10px 0;
}

.stat-card p {
  color: #666;
}

.loading-state,
.error-state {
  text-align: center;
  padding: 40px;
  color: #333;
  font-size: 1.2em;
}

.error-state {
  color: #ff6b6b;
}

:deep(.logo h1) {
    color: #42b983;  
    font-size: 24px;
}

:deep(.logo a) {
    color: #42b983;
    text-decoration: none;
}
</style> 