#!/bin/bash

# Navigate to backend directory
cd /workspace/e-borrow-repo/backend

# Initialize the database with sample data
echo "Initializing database..."
python init_db.py

# Run the Flask application
echo "Starting Flask application..."
python app.py