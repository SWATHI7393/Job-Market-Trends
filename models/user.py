"""
User model for authentication
"""
class User:
    """Simple user model for Flask-Login"""
    users = {}  # In-memory storage (replace with DB in production)
    
    def __init__(self, id, username, password_hash, is_admin=False):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.is_admin = is_admin
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False
    
    def get_id(self):
        """Return user ID"""
        return str(self.id)
    
    @classmethod
    def get(cls, user_id):
        """Get user by ID"""
        return cls.users.get(str(user_id))
    
    @classmethod
    def create(cls, username, password_hash, is_admin=False):
        """Create a new user"""
        user_id = str(len(cls.users) + 1)
        user = cls(user_id, username, password_hash, is_admin)
        cls.users[user_id] = user
        return user
    
    def check_password(self, password):
        """Check if password matches"""
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, password)

