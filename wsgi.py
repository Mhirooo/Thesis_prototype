#!/usr/bin/env python3
"""
WSGI entry point for Render deployment.
This file allows Render to find and run the Flask app correctly.
"""
import sys
import os

# Add the Hirely directory to Python path
hirely_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Hirely')
sys.path.insert(0, hirely_path)

# Change working directory to Hirely
os.chdir(hirely_path)

# Import the Flask app
from run import app

if __name__ == "__main__":
    app.run()