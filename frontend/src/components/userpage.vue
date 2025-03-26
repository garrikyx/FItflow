<template>
    <div class="userpage">
      <header class="header">
        <div class="logo">
          <h1>EcoSmart Diet</h1>
        </div>
        <nav class="nav-menu">
          <a href="#" class="nav-link active">Home</a>
          <a href="#" class="nav-link">Weather</a>
          <a href="#" class="nav-link">Meals</a>
          <a href="#" class="nav-link">Leaderboard</a>
          <a href="#" class="nav-link">User</a>
        </nav>
      </header>
  
      <main class="main-content">
        <!-- <section class="hero-section">
          <h2>Make Sustainable Food Choices</h2>
          <p>Get personalized meal recommendations based on local weather conditions</p>
          <div class="cta-buttons">
            <button class="primary-btn">Get Started</button>
            <button class="secondary-btn">Learn More</button>
          </div>
        </section> -->
        <!-- <div class="report">This month's exercise report: <button class="just-right">📃📩</button></div>
        <div class="report">Month by month report: <button class="just-right">📃📩</button></div> -->
        <div class="monthly-stats">Monthly Stats:</div>
        <section class="stats-section">
          <div class="stat-card">
            <h3>{{ time }}</h3>
            <p>Minutes Exercised</p>
          </div>
          <div class="stat-card">
            <h3>{{ distance }}</h3>
            <p>KM Covered</p>
          </div>
          <div class="stat-card">
            <h3>{{ calories }}</h3>
            <p>Calories Burned</p>
          </div>
        </section>

        <div class="for-month">for the month of {{ date }}</div>
        <!-- <section class="features">
          <div class="feature-card">
            <div class="feature-icon">🌤️</div>
            <h3>Weather-Based</h3>
            <p>Recommendations based on real-time weather data</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">🥗</div>
            <h3>Healthy Choices</h3>
            <p>Nutritious and sustainable meal options</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">🌍</div>
            <h3>Eco Impact</h3>
            <p>Track your environmental impact</p>
          </div>
        </section> -->
  
        <!-- <section class="how-it-works">
          <h2>How It Works</h2>
          <div class="steps">
            <div class="step">
              <div class="step-number">1</div>
              <h3>Check Weather</h3>
              <p>We analyze local weather conditions</p>
            </div>
            <div class="step">
              <div class="step-number">2</div>
              <h3>Get Recommendations</h3>
              <p>Receive personalized meal suggestions</p>
            </div>
            <div class="step">
              <div class="step-number">3</div>
              <h3>Track Progress</h3>
              <p>Monitor your eco-friendly choices</p>
            </div>
          </div>
        </section> -->
      </main>
  
      <footer class="footer">
        <p>© 2024 EcoSmart Diet. All rights reserved.</p>
      </footer>
    </div>
  </template>
  
  <script>
  export default {
    name: 'userpage',
    data() {
      return {
        // Add reactive data here if needed
        'time': "342",
        'distance': "123",
        'calories': '23,457',
        'date': new Date().toLocaleDateString('default', { month: 'long' })
      }
    }
  }
  </script>
  
  <style scoped>
  .userpage {
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
  
  .nav-link.active {
    color: #42b983;
    border-bottom: 2px solid #42b983;
  }
  
  .nav-link:hover {
    color: #42b983;
  }
  
  .hero-section {
    text-align: center;
    padding: 80px 0;
    background-color: #f8f9fa;
    border-radius: 12px;
    margin: 40px 0;
  }
  
  .cta-buttons {
    margin-top: 30px;
    display: flex;
    gap: 20px;
    justify-content: center;
  }
  
  .primary-btn, .secondary-btn {
    padding: 12px 24px;
    border-radius: 6px;
    font-size: 16px;
    cursor: pointer;
    transition: all 0.3s ease;
  }
  
  .primary-btn {
    background-color: #42b983;
    color: white;
    border: none;
  }

  .secondary-btn {
    background-color: white;
    color: #42b983;
    border: 2px solid #42b983;
  }

  .report {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .just-right {
    margin-left: auto;
    background-color: #333;
    
  }

  
  .monthly-stats {
    color: rgba(255, 255, 255, 0.7);
    display: flex;
    justify-content: center;
    font-size: 40px;
    align-items: flex-end;
    margin-top: 10px;
  }
  
  .stats-section {
    display: flex;
    justify-content: space-around;
    margin: 20px 0;
  }
  
  .stat-card {
    text-align: center;
  }
  
  .stat-card h3 {
    color: #42b983;
    font-size: 36px;
    margin-bottom: 10px;
  }

  .for-month {
    display: flex;
    justify-content: flex-end;
    font-size: small;
  }

  
  .features {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 30px;
    margin: 60px 0;
  }
  
  .feature-card {
    padding: 30px;
    background-color: white;
    border-radius: 12px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    text-align: center;
    transition: transform 0.3s ease;
  }
  
  .feature-card:hover {
    transform: translateY(-5px);
  }
  
  .feature-icon {
    font-size: 40px;
    margin-bottom: 20px;
  }
  
  .how-it-works {
    text-align: center;
    margin: 60px 0;
  }
  
  .steps {
    display: flex;
    justify-content: space-around;
    margin-top: 40px;
  }
  
  .step {
    flex: 1;
    max-width: 250px;
  }
  
  .step-number {
    width: 40px;
    height: 40px;
    background-color: #42b983;
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 20px;
    font-size: 20px;
  }
  
  .footer {
    text-align: center;
    padding: 20px 0;
    margin-top: 60px;
    border-top: 1px solid #eee;
    color: #666;
  }
  
  h2 {
    color: #2c3e50;
    margin-bottom: 20px;
    font-size: 32px;
  }
  
  h3 {
    color: #2c3e50;
    margin-bottom: 15px;
  }
  
  p {
    color: rgba(255, 255, 255, 0.7);
    line-height: 1.6;
  }
  
  @media (max-width: 768px) {
    .steps {
      flex-direction: column;
      align-items: center;
      gap: 30px;
    }
    
    .stats-section {
      flex-direction: column;
      gap: 30px;
    }
  }
  </style>
  