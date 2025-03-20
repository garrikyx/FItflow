// activity-log-service.js
const express = require('express');
const mongoose = require('mongoose');
const activityRouter = express.Router();

// Activity Log Schema
const activitySchema = new mongoose.Schema({
  userId: { type: String, required: true, index: true },
  exerciseType: { type: String, required: true },
  duration: { type: Number, required: true }, // in minutes
  intensity: { type: String, enum: ['low', 'moderate', 'high'], required: true },
  date: { type: Date, default: Date.now },
  caloriesBurned: { type: Number },
  location: { type: String },
  notes: { type: String }
});

const Activity = mongoose.model('Activity', activitySchema);

// Get activity log for a user
activityRouter.get('/api/activities/:userId', async (req, res) => {
  try {
    const activities = await Activity.find({ userId: req.params.userId })
      .sort({ date: -1 }) // Most recent first
      .limit(20); // Last 20 activities
      
    res.status(200).json(activities);
  } catch (error) {
    console.error('Error fetching activity log:', error);
    res.status(500).json({ error: 'Failed to fetch activity log' });
  }
});

// Add a new activity
activityRouter.post('/api/activities', async (req, res) => {
  try {
    const { userId, exerciseType, duration, intensity, caloriesBurned, location, notes } = req.body;
    
    // Validate required fields
    if (!userId || !exerciseType || !duration || !intensity) {
      return res.status(400).json({ error: 'Missing required fields' });
    }
    
    const newActivity = new Activity({
      userId,
      exerciseType,
      duration,
      intensity,
      caloriesBurned,
      location,
      notes
    });
    
    await newActivity.save();
    
    res.status(201).json(newActivity);
  } catch (error) {
    console.error('Error creating activity:', error);
    res.status(500).json({ error: 'Failed to create activity' });
  }
});

module.exports = activityRouter;

// -----------------------------------------
// user-service.js
const express = require('express');
const mongoose = require('mongoose');
const userRouter = express.Router();

// User Schema
const userSchema = new mongoose.Schema({
  userId: { type: String, required: true, unique: true },
  fitnessGoal: { type: String, enum: ['weight loss', 'muscle gain', 'endurance', 'cardio', 'general fitness'] },
  healthConditions: [String],
  preferences: {
    preferredActivities: [String],
    preferredIntensity: { type: String, enum: ['low', 'moderate', 'high'] },
    preferredTime: { type: String },
    outdoorPreference: { type: Boolean, default: true }
  },
  height: Number, // in cm
  weight: Number, // in kg
  age: Number,
  gender: String,
  activityLevel: { type: String, enum: ['sedentary', 'lightly active', 'moderately active', 'very active'] }
});

const User = mongoose.model('User', userSchema);

// Get user data
userRouter.get('/api/users/:userId', async (req, res) => {
  try {
    const user = await User.findOne({ userId: req.params.userId });
    
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }
    
    res.status(200).json(user);
  } catch (error) {
    console.error('Error fetching user data:', error);
    res.status(500).json({ error: 'Failed to fetch user data' });
  }
});

// Create or update user
userRouter.post('/api/users', async (req, res) => {
  try {
    const { userId, fitnessGoal, healthConditions, preferences, height, weight, age, gender, activityLevel } = req.body;
    
    if (!userId) {
      return res.status(400).json({ error: 'User ID is required' });
    }
    
    const userData = {
      fitnessGoal,
      healthConditions,
      preferences,
      height,
      weight,
      age,
      gender,
      activityLevel
    };
    
    // Find and update or create new
    const user = await User.findOneAndUpdate(
      { userId }, 
      userData, 
      { new: true, upsert: true }
    );
    
    res.status(200).json(user);
  } catch (error) {
    console.error('Error updating user data:', error);
    res.status(500).json({ error: 'Failed to update user data' });
  }
});

module.exports = userRouter;

// -----------------------------------------
// notification-service.js
const express = require('express');
const notificationRouter = express.Router();

// Simulated push notification service
// In a real implementation, this would use Firebase Cloud Messaging, 
// Apple Push Notification Service, or another push notification provider

notificationRouter.post('/api/notify', async (req, res) => {
  try {
    const { userId, title, body, data } = req.body;
    
    if (!userId || !title || !body) {
      return res.status(400).json({ error: 'Missing required fields' });
    }
    
    // Log the notification (in a real service, this would send to FCM/APNS)
    console.log(`Sending notification to user ${userId}:`);
    console.log(`Title: ${title}`);
    console.log(`Body: ${body}`);
    console.log('Data:', data);
    
    // Simulate push notification sending
    // In reality, you would use a provider's SDK or API here
    const successRate = 0.95; // 95% success rate simulation
    
    if (Math.random() < successRate) {
      res.status(200).json({ success: true, message: 'Notification sent successfully' });
    } else {
      throw new Error('Simulated notification failure');
    }
  } catch (error) {
    console.error('Error sending notification:', error);
    res.status(500).json({ error: 'Failed to send notification' });
  }
});

module.exports = notificationRouter;