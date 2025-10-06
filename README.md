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
- **Multi-Admin System**: Independent admin accounts with isolated job management
- **Dual User Roles**: Separate interfaces for job seekers and employers/admins
- **Admin Isolation**: Each admin can only manage their own job postings
- **Resume Processing**: Automatic extraction and analysis of resume content
- **Real-time Matching**: Instant job recommendations based on resume content
- **Shortlisting**: Automated candidate shortlisting for employers
- **Match Explanations**: Transparent explanations of match scores
- **Secure Access Control**: Role-based permissions and ownership verification

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

5. **Database Migration** (if upgrading from older version):
   ```bash
   python migrate_add_created_by.py  # Adds admin ownership to existing jobs
   ```

6. **Create Admin Accounts**:
   - Navigate to `/admin_register` to create admin accounts
   - Each admin will have an isolated workspace for job management

## Database Architecture

The system uses two databases:

1. **SQLite Database** (`instance/resume_matcher.db`):
   - User accounts and profiles (job seekers and admins)
   - Job listings with admin ownership tracking
   - Applications and match data
   - System configurations

2. **ChromaDB** (`chroma_storage/`):
   - Vector embeddings for resumes
   - Vector embeddings for job descriptions
   - Optimized for semantic search

### Admin Isolation Features
- Each job posting is linked to its creator admin via `created_by` foreign key
- Admin dashboards show only jobs created by the current admin
- Edit/delete operations verify ownership before allowing access
- Resume viewing restricted to applicants of admin's own job postings

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
- `GET /api/jobs/`: List all active jobs (public view)
- `POST /api/jobs/`: Create new job posting (admin only, auto-assigns to creator)
- `DELETE /api/jobs/<id>`: Delete job posting (admin only, ownership verified)

### Admin Features
- `GET /admin_dashboard`: View admin's own job postings only
- `GET /edit_job/<id>`: Edit job (ownership verified)
- `POST /delete_job/<id>`: Delete job (ownership verified)
- `GET /view_resume/<user_id>`: View resumes (restricted to own job applicants)

### Applications
- `POST /api/applications/`: Submit job application
- `GET /api/applications/user`: Get user's applications

### Matchmaking
- `GET /api/matchmaking/`: Get job recommendations
- `GET /api/matchmaking/explain/<id>`: Get match explanation
- `GET /api/shortlist/<id>`: Get shortlisted candidates

## Security & Access Control

### Multi-Admin Architecture
- **Complete Isolation**: Each admin operates in their own workspace
- **Ownership Verification**: All job operations verify admin ownership
- **Secure Dashboards**: Admins see only their own job postings
- **Protected Routes**: Edit/delete operations require ownership validation
- **Resume Access Control**: Restricted to applicants of admin's own jobs

### User Roles
- **Job Seekers**: Can view all active jobs and apply to any position
- **Admins**: Can create, edit, and delete only their own job postings
- **System Admin**: Can manage multiple admin accounts (optional)

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

## Testing Multi-Admin Functionality

To verify the admin isolation system:

```bash
# Test admin isolation
python test_multi_admin.py

# Create test jobs for different admins
python create_test_jobs.py
```

Expected behavior:
- Each admin sees only their own job postings
- Cross-admin access to jobs is blocked
- Resume access limited to relevant applicants
- Edit/delete operations verify ownership

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is proprietary and confidential. All rights reserved.