// fitness-recommendation-service.js
const express = require('express');
const axios = require('axios');
const router = express.Router();

// Fitness Recommendation Service
// This is the main composite service that orchestrates the workflow

// 1. Request advice endpoint (from Fitness UI)
router.post('/api/fitness/recommendations', async (req, res) => {
  try {
    const { userId, location, time } = req.body;
    
    if (!userId || !location || !time) {
      return res.status(400).json({ error: 'Missing required parameters' });
    }

    // 2-3. Fetch weather data
    const weatherData = await fetchWeatherData(location);
    
    // 4-5. Get activity log
    const activityLog = await fetchActivityLog(userId);
    
    // 6-7. Get user profile
    const userData = await fetchUserData(userId);
    
    // Process all data to generate recommendation
    const recommendation = generateRecommendation(
      userData,
      weatherData,
      activityLog,
      time
    );
    
    // 8. Return advice
    res.status(200).json(recommendation);
    
    // 9. Push notification (async)
    sendNotification(userId, recommendation);
    
  } catch (error) {
    console.error('Error generating fitness recommendation:', error);
    res.status(500).json({ error: 'Failed to generate recommendation' });
  }
});

// Helper function to fetch weather data
async function fetchWeatherData(location) {
  try {
    // 2. Fetch weather from external API
    const response = await axios.get('https://weather-api.example.com/forecast', {
      params: {
        location,
        apiKey: process.env.WEATHER_API_KEY
      }
    });
    
    // 3. Return processed weather data
    const { temp, uv, humidity, forecast } = response.data;
    return { temp, uv, humidity, forecast };
  } catch (error) {
    console.error('Error fetching weather data:', error);
    throw new Error('Weather service unavailable');
  }
}

// Helper function to fetch activity log
async function fetchActivityLog(userId) {
  try {
    // 4. Get activity log
    const response = await axios.get(`http://activity-log-service/api/activities/${userId}`);
    
    // 5. Return activity data
    return response.data;
  } catch (error) {
    console.error('Error fetching activity log:', error);
    throw new Error('Activity log service unavailable');
  }
}

// Helper function to fetch user data
async function fetchUserData(userId) {
  try {
    // 6. Get user profile
    const response = await axios.get(`http://user-service/api/users/${userId}`);
    
    // 7. Return user data
    return response.data;
  } catch (error) {
    console.error('Error fetching user data:', error);
    throw new Error('User service unavailable');
  }
}

// Function to generate recommendation based on all data
function generateRecommendation(userData, weatherData, activityLog, time) {
  // Logic to determine best exercise recommendations based on:
  // - User preferences and fitness goals
  // - Weather conditions (temperature, UV index, humidity)
  // - Recent activity history
  // - Time of day
  
  const { fitnessGoal, healthConditions, preferences } = userData;
  const { temp, uv, humidity, forecast } = weatherData;
  const recentActivities = activityLog.slice(0, 5); // Last 5 activities
  
  let exerciseRecommendation;
  let sunscreenRecommendation = '';
  let intensityRecommendation = '';
  
  // Example logic for exercise recommendation
  if (forecast.includes('rain') || forecast.includes('storm')) {
    exerciseRecommendation = 'indoor';
  } else {
    exerciseRecommendation = 'outdoor';
  }
  
  // Determine exercise type based on user preferences and goals
  if (exerciseRecommendation === 'outdoor') {
    if (fitnessGoal === 'cardio') {
      exerciseRecommendation = 'running';
    } else if (fitnessGoal === 'strength') {
      exerciseRecommendation = 'outdoor bodyweight workout';
    }
  } else {
    if (fitnessGoal === 'cardio') {
      exerciseRecommendation = 'treadmill or stationary bike';
    } else if (fitnessGoal === 'strength') {
      exerciseRecommendation = 'weight training';
    }
  }
  
  // UV index recommendations
  if (uv > 7) {
    sunscreenRecommendation = 'high SPF 50+';
  } else if (uv > 3) {
    sunscreenRecommendation = 'moderate SPF 30';
  } else {
    sunscreenRecommendation = 'low SPF 15';
  }
  
  // Intensity recommendations based on temperature and user history
  if (temp > 30) { // hot weather
    intensityRecommendation = 'low to moderate';
  } else if (temp < 5) { // cold weather
    intensityRecommendation = 'moderate with proper warm-up';
  } else {
    intensityRecommendation = 'moderate to high';
  }
  
  // Adjust based on recent activity (prevent overtraining)
  const recentIntenseWorkouts = recentActivities.filter(a => a.intensity === 'high').length;
  if (recentIntenseWorkouts >= 3) {
    intensityRecommendation = 'low (recovery recommended)';
  }
  
  return {
    exerciseRecommendation,
    sunscreenRecommendation,
    intensityRecommendation,
    weatherAlert: temp > 35 ? 'Extreme heat warning' : 
                  uv > 10 ? 'Extreme UV warning' : '',
    hydrationTip: temp > 25 ? 'Drink extra water' : 'Stay hydrated'
  };
}

// Function to send notification (async)
async function sendNotification(userId, recommendation) {
  try {
    await axios.post('http://notification-service/api/notify', {
      userId,
      title: 'Your Fitness Recommendation',
      body: `Today's recommendation: ${recommendation.exerciseRecommendation} at ${recommendation.intensityRecommendation} intensity`,
      data: recommendation
    });
    console.log(`Notification sent to user ${userId}`);
  } catch (error) {
    console.error('Error sending notification:', error);
    // Non-critical failure, don't throw
  }
}

module.exports = router;