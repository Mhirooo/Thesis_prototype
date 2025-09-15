from flask import Blueprint, request, jsonify
from app.models import db, Application, Job, User
from rank_bm25 import BM25Okapi
import numpy as np
from app.utils.decorators import admin_required

shortlist_bp = Blueprint('shortlist', __name__)

@shortlist_bp.route('/<int:job_id>', methods=['GET'])
@admin_required
def get_shortlist(job_id):
    try:
        # Get the target job
        target_job = Job.query.get_or_404(job_id)
        
        # Get all applications in the same cluster
        applications = Application.query.filter_by(cluster_id=target_job.cluster_id).all()
        
        if not applications:
            return jsonify({'message': 'No applications found for this job cluster'}), 404
        
        # Prepare corpus for BM25
        corpus = [app.resume_text for app in applications]
        tokenized_corpus = [doc.split() for doc in corpus]
        
        # Create BM25 index
        bm25 = BM25Okapi(tokenized_corpus)
        
        # Tokenize query (job description)
        tokenized_query = target_job.description.split()
        
        # Get scores
        doc_scores = bm25.get_scores(tokenized_query)
        
        # Get top 5 applications
        top_indices = np.argsort(doc_scores)[::-1][:5]
        top_applications = [applications[i] for i in top_indices]
        top_scores = [doc_scores[i] for i in top_indices]
        
        # Prepare response
        results = []
        for app, score in zip(top_applications, top_scores):
            user = User.query.get(app.user_id)
            results.append({
                'application_id': app.id,
                'user_id': app.user_id,
                'username': user.username,
                'email': user.email,
                'score': float(score),
                'resume_preview': app.resume_text[:200] + '...' if len(app.resume_text) > 200 else app.resume_text
            })
        
        return jsonify(results), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@shortlist_bp.route('/explain/<int:application_id>', methods=['GET'])
@admin_required
def explain_shortlist(application_id):
    try:
        application = Application.query.get_or_404(application_id)
        job = Job.query.get_or_404(application.job_id)
        
        # Use BM25 to get term weights
        tokenized_corpus = [application.resume_text.split()]
        bm25 = BM25Okapi(tokenized_corpus)
        tokenized_query = job.description.split()
        
        # Get top matching terms
        top_terms = []
        for term in tokenized_query:
            if term in bm25.doc_freqs and term in application.resume_text.lower():
                top_terms.append(term)
        
        # Limit to top 10 terms
        top_terms = list(set(top_terms))[:10]
        
        return jsonify({
            'application_id': application_id,
            'job_id': job.id,
            'job_role': job.role,
            'matching_terms': top_terms,
            'explanation': f"This resume was selected because it contains relevant terms like {', '.join(top_terms[:3])} and more that match the job requirements."
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500