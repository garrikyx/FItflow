<template>
  <div class="meal-page">
    <header class="header">
      <div class="logo">
        <router-link to="/" class="logo-link">
          <h1>FitFlow</h1>
        </router-link>
      </div>
      <nav class="nav-menu">
        <router-link to="/" class="nav-link">Home</router-link>
        <router-link to="/weather" class="nav-link">Weather</router-link>
        <router-link to="/meals" class="nav-link">Meals</router-link>
        <router-link to="/leaderboard" class="nav-link">Leaderboard</router-link>
      </nav>
    </header>

    <main class="main-content">
      <!-- Today's Activity Summary -->
      <section class="activity-summary">
        <h2>Today's Activity</h2>
        <div class="activity-card">
          <div class="activity-icon">🏃‍♂️</div>
          <div class="activity-details">
            <h3>Morning Run</h3>
            <p>Duration: 45 minutes</p>
            <p>Intensity: High</p>
            <p>Calories Burned: 450</p>
          </div>
        </div>
      </section>

      <!-- Meal Recommendations -->
      <section class="meals-section">
        <h2>Recommended Meals</h2>
        <div class="meal-cards">
          <!-- Breakfast -->
          <div class="meal-card">
            <div class="meal-header">
              <h3>Breakfast</h3>
              <span class="time">7:00 AM</span>
            </div>
            <img src="https://placehold.co/300x200" alt="Breakfast" class="meal-image">
            <div class="meal-content">
              <h4>Protein Oatmeal Bowl</h4>
              <p class="description">Oatmeal with banana, protein powder, and mixed berries</p>
              <div class="macros">
                <div class="macro">
                  <span class="macro-label">Protein</span>
                  <span class="macro-value">25g</span>
                </div>
                <div class="macro">
                  <span class="macro-label">Carbs</span>
                  <span class="macro-value">45g</span>
                </div>
                <div class="macro">
                  <span class="macro-label">Fats</span>
                  <span class="macro-value">12g</span>
                </div>
              </div>
              <div class="calories">420 calories</div>
            </div>
          </div>

          <!-- Lunch -->
          <div class="meal-card">
            <div class="meal-header">
              <h3>Lunch</h3>
              <span class="time">12:30 PM</span>
            </div>
            <img src="https://placehold.co/300x200" alt="Lunch" class="meal-image">
            <div class="meal-content">
              <h4>Grilled Chicken Quinoa Bowl</h4>
              <p class="description">Grilled chicken breast with quinoa, roasted vegetables</p>
              <div class="macros">
                <div class="macro">
                  <span class="macro-label">Protein</span>
                  <span class="macro-value">35g</span>
                </div>
                <div class="macro">
                  <span class="macro-label">Carbs</span>
                  <span class="macro-value">55g</span>
                </div>
                <div class="macro">
                  <span class="macro-label">Fats</span>
                  <span class="macro-value">15g</span>
                </div>
              </div>
              <div class="calories">520 calories</div>
            </div>
          </div>

          <!-- Dinner -->
          <div class="meal-card">
            <div class="meal-header">
              <h3>Dinner</h3>
              <span class="time">7:00 PM</span>
            </div>
            <img src="https://placehold.co/300x200" alt="Dinner" class="meal-image">
            <div class="meal-content">
              <h4>Salmon with Sweet Potato</h4>
              <p class="description">Baked salmon fillet with sweet potato mash and greens</p>
              <div class="macros">
                <div class="macro">
                  <span class="macro-label">Protein</span>
                  <span class="macro-value">30g</span>
                </div>
                <div class="macro">
                  <span class="macro-label">Carbs</span>
                  <span class="macro-value">40g</span>
                </div>
                <div class="macro">
                  <span class="macro-label">Fats</span>
                  <span class="macro-value">18g</span>
                </div>
              </div>
              <div class="calories">480 calories</div>
            </div>
          </div>
        </div>
      </section>

      <!-- Daily Nutrition Summary -->
      <section class="nutrition-summary">
        <h2>Daily Nutrition Goals</h2>
        <div class="nutrition-cards">
          <div class="nutrition-card">
            <h3>Total Calories</h3>
            <div class="progress-circle">
              <span class="progress-text">1,420</span>
              <span class="progress-subtext">of 2,000</span>
            </div>
          </div>
          <div class="nutrition-card">
            <h3>Protein</h3>
            <div class="progress-bar">
              <div class="progress" style="width: 75%"></div>
            </div>
            <span class="progress-text">90g of 120g</span>
          </div>
          <div class="nutrition-card">
            <h3>Carbs</h3>
            <div class="progress-bar">
              <div class="progress" style="width: 65%"></div>
            </div>
            <span class="progress-text">140g of 220g</span>
          </div>
          <div class="nutrition-card">
            <h3>Fats</h3>
            <div class="progress-bar">
              <div class="progress" style="width: 80%"></div>
            </div>
            <span class="progress-text">45g of 55g</span>
          </div>
        </div>
      </section>
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

.logo-link {
  text-decoration: none;
}

.router-link-active {
  color: #42b983;
  border-bottom: 2px solid #42b983;
}

.nav-link:hover {
  color: #42b983;
}

/* Activity Summary */
.activity-card {
  display: flex;
  align-items: center;
  background: white;
  padding: 20px;
  border-radius: 15px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  margin: 20px 0;
}

.activity-icon {
  font-size: 48px;
  margin-right: 20px;
}

/* Meal Cards */
.meal-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
  margin: 20px 0;
}

.meal-card {
  background: white;
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.meal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  background: #f8f9fa;
}

.meal-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.meal-content {
  padding: 20px;
}

.macros {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
  margin: 15px 0;
  padding: 15px 0;
  border-top: 1px solid #eee;
  border-bottom: 1px solid #eee;
}

.macro {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.macro-label {
  font-size: 14px;
  color: #666;
}

.macro-value {
  font-weight: bold;
  color: #42b983;
}

.calories {
  text-align: right;
  font-weight: bold;
  color: #2c3e50;
}

/* Nutrition Summary */
.nutrition-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin: 20px 0;
}

.nutrition-card {
  background: white;
  padding: 20px;
  border-radius: 15px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  text-align: center;
}

.progress-circle {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: #f8f9fa;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin: 15px auto;
  border: 8px solid #42b983;
}

.progress-text {
  font-size: 24px;
  font-weight: bold;
  color: #2c3e50;
}

.progress-subtext {
  font-size: 14px;
  color: #666;
}

.progress-bar {
  background: #eee;
  height: 8px;
  border-radius: 4px;
  overflow: hidden;
  margin: 15px 0;
}

.progress {
  background: #42b983;
  height: 100%;
  border-radius: 4px;
}

@media (max-width: 768px) {
  .meal-cards {
    grid-template-columns: 1fr;
  }
  
  .nutrition-cards {
    grid-template-columns: 1fr;
  }
}
</style> 