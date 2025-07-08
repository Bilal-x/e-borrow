#!/bin/bash

# Navigate to project directory
cd /workspace/e-borrow-repo

# Initialize the database with sample data
echo "Initializing database..."
python -m backend.init_db

# Run the Flask application
echo "Starting Flask application..."
python -m backend.app