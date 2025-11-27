"""
Main routes for public pages
"""
from flask import Blueprint, render_template, request, jsonify
from services.data_service import get_dashboard_stats, get_trends_data, search_job_role
from services.skill_service import get_required_skills, analyze_skill_gap
from services.recommendation_service import get_job_recommendations
from services.blog_service import get_all_posts, get_post_by_id

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Homepage"""
    return render_template('index.html')

@main_bp.route('/dashboard')
def dashboard():
    """Dashboard page with analytics"""
    stats = get_dashboard_stats()
    return render_template('dashboard.html', stats=stats)

@main_bp.route('/predict')
def predict():
    """Dataset upload and prediction page"""
    return render_template('predict.html')

@main_bp.route('/skill-gap')
def skill_gap():
    """Skill gap analyzer page"""
    return render_template('skill_gap.html')

@main_bp.route('/recommendations')
def recommendations():
    """Job recommendation engine page"""
    return render_template('recommendations.html')

@main_bp.route('/ml-insights')
def ml_insights():
    """ML model insights page"""
    return render_template('ml_insights.html')

@main_bp.route('/trends')
def trends():
    """Trends explorer page"""
    return render_template('trends.html')

@main_bp.route('/blog')
def blog():
    """Blog/insights listing page"""
    posts = get_all_posts()
    return render_template('blog.html', posts=posts)

@main_bp.route('/blog/<post_id>')
def blog_post(post_id):
    """Individual blog post page"""
    post = get_post_by_id(post_id)
    if not post:
        return render_template('errors/404.html'), 404
    return render_template('blog_post.html', post=post)

