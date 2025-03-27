<template>
  <div class="leaderboard">
    <header class="header">
      <Logo />
      <NavBar />
    </header>
    <div class="main-content">
      <!-- Friends Leaderboard Section -->
      <section class="leaderboard-section">
        <div class="section-header">
          <h2>Friends Leaderboard</h2>
          <div class="filter-buttons">
            <button class="filter-btn active">Weekly</button>
            <button class="filter-btn">Monthly</button>
            <button class="filter-btn">All Time</button>
          </div>
        </div>
        
        <div class="leaderboard-container">
          <!-- Top 3 Podium -->
          <div class="podium">
            <div class="podium-item">
              <div class="avatar-wrapper">
                <div class="avatar">🏃‍♀️</div>
                <div class="rank-badge">2</div>
              </div>
              <div class="podium-info">
                <span class="name">Sarah Lee</span>
                <span class="points">2,850 pts</span>
              </div>
            </div>
            <div class="podium-item">
              <div class="avatar-wrapper">
                <div class="avatar">🏋️‍♂️</div>
                <div class="rank-badge">1</div>
              </div>
              <div class="podium-info">
                <span class="name">John Doe</span>
                <span class="points">3,120 pts</span>
              </div>
            </div>
            <div class="podium-item">
              <div class="avatar-wrapper">
                <div class="avatar">🚴‍♂️</div>
                <div class="rank-badge">3</div>
              </div>
              <div class="podium-info">
                <span class="name">Mike Chen</span>
                <span class="points">2,740 pts</span>
              </div>
            </div>
          </div>

          <!-- Rest of Leaderboard -->
          <div class="leaderboard-list">
            <div class="leaderboard-item">
              <span class="rank">4</span>
              <div class="avatar">🏊‍♂️</div>
              <span class="name">Emma Wilson</span>
              <div class="stats">
                <span class="points">2,590 pts</span>
                <span class="streak">🔥 5 days</span>
              </div>
            </div>
            <div class="leaderboard-item you">
              <span class="rank">5</span>
              <div class="avatar">🏃‍♂️</div>
              <span class="name">You</span>
              <div class="stats">
                <span class="points">2,480 pts</span>
                <span class="streak">🔥 3 days</span>
              </div>
            </div>
            <div class="leaderboard-item">
              <span class="rank">6</span>
              <div class="avatar">🤸‍♀️</div>
              <span class="name">Lisa Park</span>
              <div class="stats">
                <span class="points">2,350 pts</span>
                <span class="streak">🔥 2 days</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Activity Calendar Section -->
      <section class="calendar-section">
        <h2>Your Activity Calendar</h2>
        <div class="calendar-header">
          <button class="calendar-nav">◀</button>
          <h3>March 2024</h3>
          <button class="calendar-nav">▶</button>
        </div>
        <div class="calendar">
          <div class="calendar-days">
            <span>Sun</span>
            <span>Mon</span>
            <span>Tue</span>
            <span>Wed</span>
            <span>Thu</span>
            <span>Fri</span>
            <span>Sat</span>
          </div>
          <div class="calendar-dates">
            <div class="date past">25</div>
            <div class="date past active">26</div>
            <div class="date past">27</div>
            <div class="date past active">28</div>
            <div class="date past active">1</div>
            <div class="date past">2</div>
            <div class="date past active">3</div>
            <div class="date past">4</div>
            <div class="date past active">5</div>
            <div class="date past active">6</div>
            <div class="date past">7</div>
            <div class="date past active">8</div>
            <div class="date past active">9</div>
            <div class="date past">10</div>
            <div class="date today active">11</div>
            <div class="date future">12</div>
            <div class="date future">13</div>
            <div class="date future">14</div>
            <div class="date future">15</div>
            <div class="date future">16</div>
            <div class="date future">17</div>
            <!-- Add remaining dates -->
          </div>
        </div>
        <div class="calendar-legend">
          <div class="legend-item">
            <div class="legend-dot active"></div>
            <span>Workout Day</span>
          </div>
          <div class="legend-item">
            <div class="legend-dot"></div>
            <span>Rest Day</span>
          </div>
        </div>
      </section>

      <!-- Monthly Stats -->
      <section class="stats-section">
        <h2>Monthly Statistics</h2>
        <div class="stats-container">
          <div class="stat-card">
            <h3>Active Days</h3>
            <div class="stat-number">15</div>
            <p>This Month</p>
          </div>
          <div class="stat-card">
            <h3>Current Streak</h3>
            <div class="stat-number">3 🔥</div>
            <p>Days</p>
          </div>
          <div class="stat-card">
            <h3>Best Streak</h3>
            <div class="stat-number">7 🏆</div>
            <p>Days</p>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script>
import NavBar from './NavBar.vue';
import Logo from './Logo.vue';

export default {
  name: 'Leaderboard',
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

.leaderboard-item {
  border-bottom: 1px solid #555;
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
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.filter-buttons {
  display: flex;
  gap: 10px;
}

.filter-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 20px;
  background: #f1f5f9;
  color: #666;
  cursor: pointer;
  transition: all 0.3s ease;
}

.filter-btn.active {
  background: #42b983;
  color: white;
}

.podium {
  display: flex;
  justify-content: center;
  align-items: flex-end;
  gap: 20px;
  padding: 20px;
}

.podium-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px;
  min-width: 120px;
}

.avatar-wrapper {
  position: relative;
  margin-bottom: 15px;
}

.avatar {
  font-size: 40px;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  padding: 10px;
  margin-bottom: 5px;
}

.rank-badge {
  position: absolute;
  bottom: -5px;
  right: -5px;
  background: white;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 14px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.podium-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.name {
  font-weight: 500;
  font-size: 14px;
  color: #333;
}

.points {
  font-size: 12px;
  color: #666;
}

.leaderboard-list {
  background: none;
  border-radius: 0;
}

.leaderboard-item {
  display: grid;
  grid-template-columns: 40px 50px auto 120px;
  align-items: center;
  padding: 10px;
  border-bottom: 1px solid #ddd;
}

.leaderboard-item:hover {
  background-color: transparent;
}

.leaderboard-item.you {
  background: none;
  border-left: none;
}

.leaderboard-item .avatar {
  font-size: 24px;
  margin: 0 15px;
}

.stats {
  margin-left: auto;
  text-align: right;
}

.streak {
  font-size: 14px;
  color: #666;
  margin-left: 10px;
}

/* Calendar Section */
.calendar-section {
  margin-top: 40px;
}

.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.calendar-nav {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  padding: 5px 10px;
}

.calendar {
  background: white;
  border-radius: 15px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.calendar-days {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  text-align: center;
  font-weight: bold;
  margin-bottom: 10px;
}

.calendar-dates {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 5px;
}

.date {
  aspect-ratio: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  cursor: pointer;
}

.date.active {
  background: #42b983;
  color: white;
}

.date.today {
  border: 2px solid #42b983;
}

.date.past {
  color: #666;
}

.date.future {
  color: #ccc;
}

.calendar-legend {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 20px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.legend-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #eee;
}

.legend-dot.active {
  background: #42b983;
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

.stat-number {
  font-size: 36px;
  font-weight: bold;
  color: #42b983;
  margin: 10px 0;
}

@media (max-width: 768px) {
  .section-header {
    flex-direction: column;
    gap: 15px;
  }

  .podium {
    min-height: 220px;
  }

  .gold {
    height: 180px;
  }

  .silver {
    height: 150px;
    margin-bottom: 20px;
  }

  .bronze {
    height: 120px;
    margin-bottom: 40px;
  }

  .podium-item {
    min-width: 100px;
    padding: 15px 10px;
  }

  .avatar {
    font-size: 30px;
  }

  .name {
    font-size: 14px;
    max-width: 90px;
  }

  .points {
    font-size: 12px;
  }

  .leaderboard-item {
    grid-template-columns: 30px 40px auto 100px;
    padding: 12px 15px;
  }

  .calendar-dates {
    gap: 2px;
  }

  .date {
    font-size: 14px;
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