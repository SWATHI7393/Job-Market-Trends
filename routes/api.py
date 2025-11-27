"""
API routes for data and predictions
"""
from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import json
from services.prediction_service import process_dataset, run_prediction
from services.skill_service import analyze_skill_gap, get_required_skills
from services.recommendation_service import get_job_recommendations
from services.data_service import get_trends_data, search_job_role
from ml.model import JobMarketPredictor

api_bp = Blueprint('api', __name__)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'csv', 'json'}

@api_bp.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload for prediction"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join('uploads', filename)
        file.save(filepath)
        
        return jsonify({
            'success': True,
            'filename': filename,
            'message': 'File uploaded successfully'
        })
    
    return jsonify({'error': 'Invalid file type'}), 400

@api_bp.route('/predict', methods=['POST'])
def predict():
    """Run prediction on uploaded dataset"""
    data = request.get_json()
    filename = data.get('filename')
    
    if not filename:
        return jsonify({'error': 'Filename required'}), 400
    
    filepath = os.path.join('uploads', filename)
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404
    
    try:
        results = run_prediction(filepath)
        return jsonify({
            'success': True,
            'results': results
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/skill-gap', methods=['POST'])
def api_skill_gap():
    """API endpoint for skill gap analysis"""
    data = request.get_json()
    job_role = data.get('job_role')
    experience_level = data.get('experience_level')
    user_skills = data.get('skills', [])
    
    if not job_role:
        return jsonify({'error': 'Job role required'}), 400
    
    try:
        result = analyze_skill_gap(job_role, experience_level, user_skills)
        return jsonify({
            'success': True,
            'result': result
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/recommendations', methods=['POST'])
def api_recommendations():
    """API endpoint for job recommendations"""
    data = request.get_json()
    skills = data.get('skills', [])
    
    try:
        recommendations = get_job_recommendations(skills)
        return jsonify({
            'success': True,
            'recommendations': recommendations
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/trends/<job_role>', methods=['GET'])
def api_trends(job_role):
    """Get trends data for a specific job role"""
    try:
        trends = get_trends_data(job_role)
        return jsonify({
            'success': True,
            'trends': trends
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/search', methods=['GET'])
def api_search():
    """Search for job roles"""
    query = request.args.get('q', '')
    if not query:
        return jsonify({'error': 'Query required'}), 400
    
    try:
        results = search_job_role(query)
        return jsonify({
            'success': True,
            'results': results
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/dashboard/stats', methods=['GET'])
def dashboard_stats():
    """Get dashboard statistics"""
    from services.data_service import get_dashboard_stats
    stats = get_dashboard_stats()
    return jsonify({
        'success': True,
        'stats': stats
    })

