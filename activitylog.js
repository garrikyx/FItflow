const express = require('express');
const bodyParser = require('body-parser');
const { MongoClient, ObjectId } = require('mongodb');
const swaggerJsdoc = require('swagger-jsdoc');
const swaggerUi = require('swagger-ui-express');

// MongoDB connection
const uri = 'mongodb://localhost:27017';
const client = new MongoClient(uri);
let db;
let activitiesCollection;

async function connectToDatabase() {
  await client.connect();
  db = client.db('activitylogger');
  activitiesCollection = db.collection('activities');
  console.log('Connected to MongoDB');
}

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(bodyParser.json());

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
app.get('/activity/:userId', async (req, res) => {
  try {
    const { userId } = req.params;
    
    const activities = await activitiesCollection
      .find({ userId })
      .sort({ timestamp: -1 })
      .toArray();
    
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
      timestamp: new Date()
    };
    
    const result = await activitiesCollection.insertOne(activity);
    
    res.status(201).json({
      id: result.insertedId,
      ...activity
    });
  } catch (error) {
    console.error('Error creating activity:', error);
    res.status(400).json({ error: error.message });
  }
});

app.get('/health', (req, res) => {
  res.status(200).json({ status: 'OK' });
});


(async () => {
  await connectToDatabase();
  app.listen(PORT, () => {
    console.log(`Activity Log microservice running on port ${PORT}`);
  });
})().catch(console.error);