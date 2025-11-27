"""
Setup script for Job Market Trends Analytics
Run this to initialize the project
"""
import os
import sys

def create_directories():
    """Create necessary directories"""
    directories = [
        'uploads',
        'models',
        'static/dist',
        'data'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created directory: {directory}")

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import flask
        import pandas
        import sklearn
        print("✓ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("  Run: pip install -r requirements.txt")
        return False

def main():
    """Main setup function"""
    print("Job Market Trends Analytics - Setup")
    print("=" * 50)
    
    print("\n1. Creating directories...")
    create_directories()
    
    print("\n2. Checking dependencies...")
    if not check_dependencies():
        sys.exit(1)
    
    print("\n3. Setup complete!")
    print("\nNext steps:")
    print("  - Set SECRET_KEY in .env file (optional)")
    print("  - Run: python app.py")
    print("  - Open: http://localhost:5000")
    print("\nDefault admin credentials: admin / admin123")

if __name__ == '__main__':
    main()

