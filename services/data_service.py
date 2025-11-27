"""
Data service for fetching dashboard stats and trends
"""
import json
import os
import pandas as pd
from datetime import datetime, timedelta

def get_dashboard_stats():
    """Get dashboard statistics"""
    return {
        'total_jobs': 125000,
        'growth_rate': 12.5,
        'top_roles': [
            {'role': 'Data Scientist', 'growth': 25.3},
            {'role': 'ML Engineer', 'growth': 22.1},
            {'role': 'DevOps Engineer', 'growth': 18.7},
            {'role': 'Cloud Architect', 'growth': 16.4},
        ],
        'avg_salary': 95000,
        'active_industries': 15
    }

def get_trends_data(job_role=None):
    """Get trends data for job roles"""
    # Generate sample time series data
    dates = pd.date_range(start='2020-01-01', end='2024-12-01', freq='M')
    
    if job_role:
        # Simulate role-specific trends
        base_demand = 1000
        trend = [base_demand + i * 10 + (i % 12) * 50 for i in range(len(dates))]
    else:
        trend = [5000 + i * 50 + (i % 12) * 200 for i in range(len(dates))]
    
    return {
        'dates': [d.strftime('%Y-%m') for d in dates],
        'demand': trend,
        'forecast': trend[-12:] + [t * 1.15 for t in trend[-12:]]
    }

def search_job_role(query):
    """Search for job roles matching query"""
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
    
    query_lower = query.lower()
    matches = [role for role in all_roles if query_lower in role.lower()]
    return matches[:10]

