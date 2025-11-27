"""
Skill service for skill gap analysis
"""
import json
import os

def get_required_skills(job_role, experience_level='mid'):
    """Get required skills for a job role"""
    skills_file = 'data/skills_database.json'
    
    if os.path.exists(skills_file):
        with open(skills_file, 'r') as f:
            skills_db = json.load(f)
    else:
        # Default skills database
        skills_db = {
            'Data Scientist': {
                'entry': ['Python', 'SQL', 'Statistics', 'Data Analysis'],
                'mid': ['Python', 'SQL', 'Statistics', 'Machine Learning', 'Pandas', 'NumPy', 'Scikit-learn'],
                'senior': ['Python', 'SQL', 'Statistics', 'Machine Learning', 'Deep Learning', 'TensorFlow', 'PyTorch', 'MLOps', 'Cloud Computing']
            },
            'Software Engineer': {
                'entry': ['Programming', 'Data Structures', 'Algorithms', 'Git'],
                'mid': ['Programming', 'Data Structures', 'Algorithms', 'Git', 'System Design', 'Testing'],
                'senior': ['Programming', 'Data Structures', 'Algorithms', 'Git', 'System Design', 'Architecture', 'Microservices', 'Cloud']
            }
        }
    
    role_skills = skills_db.get(job_role, {})
    return role_skills.get(experience_level, role_skills.get('mid', []))

def analyze_skill_gap(job_role, experience_level, user_skills):
    """Analyze skill gap between user skills and required skills"""
    required = get_required_skills(job_role, experience_level)
    user_skills_lower = [s.lower() for s in user_skills]
    required_lower = [s.lower() for s in required]
    
    missing_skills = [s for s in required if s.lower() not in user_skills_lower]
    matching_skills = [s for s in required if s.lower() in user_skills_lower]
    
    match_percentage = (len(matching_skills) / len(required) * 100) if required else 0
    
    # Recommend additional skills
    all_skills_file = 'data/all_skills.json'
    recommended = []
    if os.path.exists(all_skills_file):
        with open(all_skills_file, 'r') as f:
            all_skills = json.load(f)
            recommended = [s for s in all_skills if s.lower() not in user_skills_lower][:5]
    
    return {
        'required_skills': required,
        'user_skills': user_skills,
        'matching_skills': matching_skills,
        'missing_skills': missing_skills,
        'match_percentage': round(match_percentage, 2),
        'recommended_skills': recommended
    }

