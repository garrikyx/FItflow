const express = require('express');
const bodyParser = require('body-parser');
const admin = require('firebase-admin');
const serviceAccount = require('./firebase-service-account.json');
const swaggerJsdoc = require('swagger-jsdoc');
const swaggerUi = require('swagger-ui-express');

// Initialize Firebase
admin.initializeApp({
  credential: admin.credential.cert(serviceAccount)
});

const db = admin.firestore();
const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(bodyParser.json());

// Collection reference
const activitiesCollection = db.collection('activities');

// Swagger definition
const swaggerOptions = {
  definition: {
    openapi: '3.0.0',
    info: {
      title: 'Activity Log API',
      version: '1.0.0',
      description: 'API for tracking user activities and exercises'
    },
    servers: [
      {
        url: `http://localhost:${PORT}`,
        description: 'Development server'
      }
    ]
  },
  apis: ['./activitylog.js']
};

const swaggerDocs = swaggerJsdoc(swaggerOptions);
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerDocs));

// Routes
/**
 * @swagger
 * /activity/{userId}:
 *   get:
 *     summary: Get user activities
 *     parameters:
 *       - in: path
 *         name: userId
 *         required: true
 *         schema:
 *           type: string
 */

app.get('/activity/:userId', async (req, res) => {
  try {
    const { userId } = req.params;
    const snapshot = await activitiesCollection
      .where('userId', '==', userId)
      .orderBy('timestamp', 'desc')
      .get();
    
    if (snapshot.empty) {
      return res.status(200).json([]);
    }
    
    const activities = [];
    snapshot.forEach(doc => {
      activities.push({
        id: doc.id,
        ...doc.data()
      });
    });
    
    res.status(200).json(activities);
  } catch (error) {
    console.error('Error getting activities:', error);
    res.status(500).json({ error: error.message });
  }
});

app.post('/activity', async (req, res) => {
  try {
    const { userId, exerciseType, duration, intensity, caloriesBurned } = req.body;
    
    // Validate required fields
    if (!userId || !exerciseType || !duration || !intensity || !caloriesBurned) {
      return res.status(400).json({ error: 'Missing required fields' });
    }
    
    const activity = {
      userId,
      exerciseType,
      duration,
      intensity,
      caloriesBurned,
      timestamp: admin.firestore.FieldValue.serverTimestamp()
    };
    
    const docRef = await activitiesCollection.add(activity);
    
    res.status(201).json({
      id: docRef.id,
      ...activity
    });
  } catch (error) {
    console.error('Error creating activity:', error);
    res.status(400).json({ error: error.message });
  }
});

// Health check endpoint
app.get('/health', (req, res) => {
  res.status(200).json({ status: 'OK' });
});

// Start server
app.listen(PORT, () => {
  console.log(`Activity Log microservice running on port ${PORT}`);
});