/* jshint esversion: 8 */
const express = require('express');
const mongoose = require('mongoose');
const fs = require('fs');
const cors = require('cors');
const bodyParser = require('body-parser');

const app = express();
const port = 3030;

// Middleware
app.use(cors());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(express.json()); // JSON parsing အတွက်

// Import Models
const Reviews = require('./review');
const Dealerships = require('./dealership');

// Connect to MongoDB
mongoose.connect("mongodb://mongo_db:27017/", { dbName: 'dealershipsDB' })
  .then(() => console.log("Connected to MongoDB"))
  .catch(err => console.error("Could not connect to MongoDB", err));

// Initial Data Seeding
const seedData = async () => {
  try {
    const reviewsData = JSON.parse(fs.readFileSync("reviews.json", 'utf8'));
    const dealershipsData = JSON.parse(fs.readFileSync("dealerships.json", 'utf8'));

    await Reviews.deleteMany({});
    await Reviews.insertMany(reviewsData.reviews);

    await Dealerships.deleteMany({});
    await Dealerships.insertMany(dealershipsData.dealerships);

    console.log("Data seeded successfully");
  } catch (error) {
    console.error("Error seeding data:", error);
  }
};
seedData();

// --- Routes ---

app.get('/', (req, res) => {
  res.send("Welcome to the Mongoose API");
});

app.get('/fetchReviews', async (req, res) => {
  try {
    const documents = await Reviews.find();
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching reviews' });
  }
});

app.get('/fetchReviews/dealer/:id', async (req, res) => {
  try {
    const documents = await Reviews.find({ dealership: req.params.id });
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching dealer reviews' });
  }
});

app.get('/fetchDealers', async (req, res) => {
  try {
    const documents = await Dealerships.find();
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching dealers' });
  }
});

app.get('/fetchDealers/:state', async (req, res) => {
  try {
    const documents = await Dealerships.find({ state: req.params.state });
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching dealers by state' });
  }
});

app.get('/fetchDealer/:id', async (req, res) => {
  try {
    const document = await Dealerships.findOne({ id: req.params.id });
    if (!document) return res.status(404).json({ error: 'Dealer not found' });
    res.json(document);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching dealer details' });
  }
});

app.post('/insert_review', async (req, res) => {
  try {
    const data = req.body;
    const lastReview = await Reviews.findOne().sort({ id: -1 });
    let newId = lastReview ? lastReview.id + 1 : 1;

    const review = new Reviews({
      id: newId,
      name: data.name,
      dealership: data.dealership,
      review: data.review,
      purchase: data.purchase,
      purchase_date: data.purchase_date,
      car_make: data.car_make,
      car_model: data.car_model,
      car_year: data.car_year,
    });

    const savedReview = await review.save();
    res.status(201).json(savedReview);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Error inserting review' });
  }
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
