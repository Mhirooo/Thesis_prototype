from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sentence_transformers import SentenceTransformer
import joblib
import chromadb
import os

db = SQLAlchemy()
model = None
kmeans_model = None
chroma_client = None
jobs_collection = None

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_pyfile('config.py', silent=False)
    
    # Initialize extensions
    db.init_app(app)
    
    # Load ML models (with error handling)
    global model, kmeans_model, chroma_client, jobs_collection
    try:
        model = SentenceTransformer('all-MiniLM-L6-v2')
        kmeans_model = joblib.load('../data/kmeans_model.pkl')
        chroma_client = chromadb.PersistentClient(path="../chroma_storage")
        jobs_collection = chroma_client.get_or_create_collection(name="jobs")
        print("ML models and ChromaDB initialized successfully")
    except Exception as e:
        print(f"Error loading models: {e}")
        # Set to None but allow app to run for testing
        model = None
        kmeans_model = None
        chroma_client = None
        jobs_collection = None
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.jobs import jobs_bp
    from app.routes.applications import applications_bp
    from app.routes.shortlist import shortlist_bp
    from app.routes.matchmaking import matchmaking_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(jobs_bp, url_prefix='/api/jobs')
    app.register_blueprint(applications_bp, url_prefix='/api/applications')
    app.register_blueprint(shortlist_bp, url_prefix='/api/shortlist')
    app.register_blueprint(matchmaking_bp, url_prefix='/api/matchmaking')
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app