"""
Authentication service for managing users
"""
from werkzeug.security import generate_password_hash
from models.user import User

def init_auth_users():
    """Initialize default admin user"""
    if not User.users:
        # Create default admin user: admin / admin123
        admin_user = User.create(
            username='admin',
            password_hash=generate_password_hash('admin123'),
            is_admin=True
        )
        print(f"Created default admin user: admin / admin123")

