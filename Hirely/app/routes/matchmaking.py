from flask import Blueprint, request, jsonify, session
from app.models import db, Application, Job
from rank_bm25 import BM25Okapi
import numpy as np
from app.utils.decorators import login_required

matchmaking_bp = Blueprint('matchmaking', __name__)

@matchmaking_bp.route('/', methods=['GET'])
@login_required
def get_job_matches():
    try:    
        user_id = session['user_id']
        
        # Get user's most recent application
        latest_application = Application.query.filter_by(
            user_id=user_id
        ).order_by(Application.submission_date.desc()).first()
        
        if not latest_application:
            return jsonify({'error': 'No applications found for this user'}), 404
            
        user_resume_text = latest_application.resume_text
        
        # Get all active jobs
        jobs = Job.query.filter_by(is_active=True).all()
        job_descriptions = [f"{job.role} {job.description}" for job in jobs]
        
        # Create BM25 index for jobs
        tokenized_corpus = [desc.split() for desc in job_descriptions]
        bm25 = BM25Okapi(tokenized_corpus)
        
        # Tokenize query (user's resume)
        tokenized_query = user_resume_text.split()
        
        # Get scores
        doc_scores = bm25.get_scores(tokenized_query)
        
        # Get top 3 job matches
        top_indices = np.argsort(doc_scores)[::-1][:3]
        top_jobs = [jobs[i] for i in top_indices]
        top_scores = [doc_scores[i] for i in top_indices]
        
        # Prepare response
        results = []
        for job, score in zip(top_jobs, top_scores):
            results.append({
                'job_id': job.id,
                'role': job.role,
                'score': float(score),
                'description_preview': job.description[:100] + '...' if len(job.description) > 100 else job.description
            })
        
        return jsonify(results), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@matchmaking_bp.route('/explain/<int:job_id>', methods=['GET'])
@login_required
def explain_matchmaking(job_id):
    try:   
        user_id = session['user_id']
        
        # Get user's most recent application
        latest_application = Application.query.filter_by(
            user_id=user_id
        ).order_by(Application.submission_date.desc()).first()
        
        if not latest_application:
            return jsonify({'error': 'No applications found for this user'}), 404
            
        user_resume_text = latest_application.resume_text
        
        # Get the job
        job = Job.query.get_or_404(job_id)
        job_description = f"{job.role} {job.description}"
        
        # Use BM25 to get matching terms
        tokenized_corpus = [job_description.split()]
        bm25 = BM25Okapi(tokenized_corpus)
        tokenized_query = user_resume_text.split()
        
        # Get matching terms
        matching_terms = []
        for term in tokenized_query:
            if term in bm25.doc_freqs and term in job_description.lower():
                matching_terms.append(term)
        
        # Limit to top 10 terms
        matching_terms = list(set(matching_terms))[:10]
        
        return jsonify({
            'job_id': job.id,
            'job_role': job.role,
            'matching_terms': matching_terms,
            'explanation': f"This job matches your profile because your resume contains relevant terms like {', '.join(matching_terms[:3])} that align with the job requirements."
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500