"""
Job recommendation service
"""
import json
import os
from services.skill_service import get_required_skills

def get_job_recommendations(user_skills):
    """Get job recommendations based on user skills"""
    # Load all job roles
    roles_file = 'data/job_roles.json'
    if os.path.exists(roles_file):
        with open(roles_file, 'r') as f:
            all_roles = json.load(f)
    else:
        all_roles = [
            'Data Scientist', 'Machine Learning Engineer', 'Software Engineer',
            'DevOps Engineer', 'Cloud Architect', 'Data Analyst', 'Product Manager',
            'Full Stack Developer', 'Backend Developer', 'Frontend Developer'
        ]
    
    user_skills_lower = [s.lower() for s in user_skills]
    recommendations = []
    
    for role in all_roles:
        required = get_required_skills(role, 'mid')
        required_lower = [s.lower() for s in required]
        
        # Calculate match score
        matching = sum(1 for s in required_lower if s in user_skills_lower)
        match_percentage = (matching / len(required) * 100) if required else 0
        
        recommendations.append({
            'role': role,
            'match_percentage': round(match_percentage, 2),
            'required_skills': required[:5],  # Preview
            'matching_skills_count': matching,
            'total_required': len(required)
        })
    
    # Sort by match percentage
    recommendations.sort(key=lambda x: x['match_percentage'], reverse=True)
    
    return recommendations[:10]  # Top 10

