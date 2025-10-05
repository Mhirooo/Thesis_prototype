# Hirely - AI-Powered Job Matching System

Hirely is an intelligent job matching system that uses natural language processing and machine learning to match job seekers with relevant job opportunities. The system analyzes resumes and job descriptions to provide accurate matches based on skills, experience, and requirements.

## Table of Contents
- [System Overview](#system-overview)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [Database Architecture](#database-architecture)
- [Machine Learning Components](#machine-learning-components)
- [API Documentation](#api-documentation)

## System Overview

Hirely uses a hybrid approach for job matching:
- Vector embeddings for semantic understanding of resumes and job descriptions
- K-means clustering for job category classification
- Hybrid scoring system combining cosine similarity (70%) and BM25 (30%) for accurate matching

## Key Features

- **Smart Job Matching**: AI-powered matching between resumes and job postings
- **Dual User Roles**: Separate interfaces for job seekers and employers
- **Resume Processing**: Automatic extraction and analysis of resume content
- **Real-time Matching**: Instant job recommendations based on resume content
- **Shortlisting**: Automated candidate shortlisting for employers
- **Match Explanations**: Transparent explanations of match scores

## Technology Stack

- **Backend**: Python Flask
- **Databases**:
  - SQLite (Main application data)
  - ChromaDB (Vector embeddings storage)
- **ML/NLP Components**:
  - SentenceTransformers (all-MiniLM-L6-v2)
  - scikit-learn (K-means clustering)
  - BM25 ranking algorithm
- **Frontend**: HTML, CSS, JavaScript

## Project Structure

```
Hirely/
├── app/                      # Main application package
│   ├── models.py            # Database models
│   ├── routes/              # API routes and views
│   ├── templates/           # HTML templates
│   ├── static/              # Static assets
│   └── utils/               # Utility functions
├── tools/                   # Management scripts
├── instance/                # Instance-specific config
├── k-means_model_training/  # Model training notebooks
├── chroma_storage/          # Vector database storage
└── uploads/                 # User uploaded files
```

## Setup Instructions

1. **Environment Setup**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Initialize Databases**:
   ```bash
   python tools/init_chroma.py  # Initialize ChromaDB
   ```

3. **Train K-means Model** (optional, pre-trained model included):
   ```bash
   jupyter notebook k-means_model_training/k-means_model_train.ipynb
   ```

4. **Run the Application**:
   ```bash
   python run.py
   ```

## Database Architecture

The system uses two databases:

1. **SQLite Database** (`instance/resume_matcher.db`):
   - User accounts and profiles
   - Job listings
   - Applications
   - System configurations

2. **ChromaDB** (`chroma_storage/`):
   - Vector embeddings for resumes
   - Vector embeddings for job descriptions
   - Optimized for semantic search

## Machine Learning Components

1. **Text Embeddings**:
   - Model: SentenceTransformer (all-MiniLM-L6-v2)
   - Used for converting text to vector representations
   - Located in `matching_service.py`

2. **Job Classification**:
   - K-means clustering model
   - Trained on job descriptions dataset
   - Model file: `data/kmeans_model.pkl`

3. **Matching Algorithm**:
   - Hybrid scoring system
   - 70% weight on cosine similarity
   - 30% weight on BM25 ranking
   - Implementation in `matching_service.py`

## API Documentation

### Authentication Endpoints
- `POST /auth/register`: Register new user
- `POST /auth/admin_register`: Register admin user
- `POST /auth/api/login`: User login
- `POST /auth/api/logout`: User logout

### Job Management
- `GET /api/jobs/`: List all jobs
- `POST /api/jobs/`: Create new job posting
- `DELETE /api/jobs/<id>`: Delete job posting

### Applications
- `POST /api/applications/`: Submit job application
- `GET /api/applications/user`: Get user's applications

### Matchmaking
- `GET /api/matchmaking/`: Get job recommendations
- `GET /api/matchmaking/explain/<id>`: Get match explanation
- `GET /api/shortlist/<id>`: Get shortlisted candidates

## Health Checks

The system includes built-in health checks for both databases:
```bash
# Run the application to see database status
python run.py
```

Expected output:
```
SQLAlchemy connection: OK
ChromaDB connection: OK
ChromaDB collections:
- Resumes: X documents
- Jobs: Y documents
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is proprietary and confidential. All rights reserved.