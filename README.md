# CoupleWays# Couple Ways - Trip Planning App

Welcome to Couple Ways, your go-to app for seamless trip planning and organization. Whether you're a solo traveler or planning with a partner, Couple Ways has got you covered. This README.md file provides you with all the information you need to set up and use the app.

## Table of Contents

- [Getting Started](#getting-started)
  - [Cloning the Repository](#cloning-the-repository)
  - [Setting up Flask Variables](#setting-up-flask-variables)
- [Project Overview](#project-overview)
  - [Trip Addition Feature](#trip-addition-feature)
  - [Trip Budget Simulation](#trip-budget-simulation)
  - [User Authentication](#user-authentication)

## Getting Started

### Cloning the Repository

To get started, you can either clone the official Couple Ways repository:

```bash
git clone https://github.com/Snapcaszz/CoupleWays


### Setting up Flask Variables

Before using the app, you need to set up the Flask variables. Create a .env file in the root of the application and configure the MongoDB URI:

# .env
MONGODB_URI=mongodb://mongodb_user:mongodb_password/127.0.0.1:27017/default_database

Make sure to replace placeholders in the MongoDB URI with your actual database user, password, server's hostname, and port number.

In the .flaskenv file, configure the following variables for development:

# .flaskenv
FLASK_APP=couple_ways
FLASK_ENV=development
FLASK_DEBUG=1

For production:

# .flaskenv
FLASK_APP=couple_ways
FLASK_ENV=production
FLASK_DEBUG=0

## Project Overview

### Trip Addition Feature
Allow users to add trips seamlessly, including form creation, data validation, storage in the database, and display in a user-friendly table.

Detailed trip page for editing and complementing trip information, including pricing details, photo banner, YouTube video for the trip, and savings plans calculation.

### Budget simulation for a specific hotel, including trip image edition and trip removal from the database.

### User Authentication features for registration, login, and personalized trip management.

## Feel free to explore and customize Couple Ways based on your travel planning needs. Safe travels! 🌍✈️
