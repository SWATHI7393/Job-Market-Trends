"""
Admin routes for managing data
"""
from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from models.user import User
import json
import os

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Find user
        user = None
        for u in User.users.values():
            if u.username == username:
                user = u
                break
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('admin.dashboard'))
        else:
            return render_template('admin/login.html', error='Invalid credentials')
    
    return render_template('admin/login.html')

@admin_bp.route('/logout')
@login_required
def logout():
    """Logout admin user"""
    logout_user()
    return redirect(url_for('main.index'))

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    """Admin dashboard"""
    if not current_user.is_admin:
        return redirect(url_for('main.index'))
    return render_template('admin/dashboard.html')

@admin_bp.route('/skills', methods=['GET', 'POST'])
@login_required
def manage_skills():
    """Manage skills database"""
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    if request.method == 'POST':
        data = request.get_json()
        job_role = data.get('job_role')
        skills = data.get('skills', [])
        
        # Update skills database
        skills_file = 'data/skills_database.json'
        if os.path.exists(skills_file):
            with open(skills_file, 'r') as f:
                skills_db = json.load(f)
        else:
            skills_db = {}
        
        skills_db[job_role] = skills
        
        with open(skills_file, 'w') as f:
            json.dump(skills_db, f, indent=2)
        
        return jsonify({'success': True, 'message': 'Skills updated'})
    
    # GET: Return skills database
    skills_file = 'data/skills_database.json'
    if os.path.exists(skills_file):
        with open(skills_file, 'r') as f:
            skills_db = json.load(f)
    else:
        skills_db = {}
    
    return jsonify({'success': True, 'skills': skills_db})

@admin_bp.route('/upload-dataset', methods=['POST'])
@login_required
def upload_dataset():
    """Admin endpoint to upload new datasets"""
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file and file.filename.endswith('.csv'):
        filename = secure_filename(file.filename)
        filepath = os.path.join('data', filename)
        file.save(filepath)
        return jsonify({'success': True, 'message': 'Dataset uploaded'})
    
    return jsonify({'error': 'Invalid file'}), 400

