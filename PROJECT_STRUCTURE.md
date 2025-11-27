# Project Structure Overview

Complete file tree and description of the Job Market Trends Analytics project.

```
job-trend/
│
├── app.py                          # Main Flask application entry point
├── requirements.txt                # Python dependencies
├── Procfile                        # Deployment configuration for Heroku/Render
├── runtime.txt                     # Python version specification
├── tailwind.config.js              # TailwindCSS configuration
├── postcss.config.js               # PostCSS configuration
├── setup.py                        # Setup script for project initialization
├── .gitignore                      # Git ignore rules
├── README.md                       # Main project documentation
├── HOW_IT_WORKS.md                 # Detailed explanation of prediction flow
├── PROJECT_STRUCTURE.md            # This file
│
├── models/                         # ML Models directory
│   └── model.py                    # ML prediction models (JobMarketPredictor)
│
├── routes/                         # Flask Blueprints (Route handlers)
│   ├── main.py                     # Public routes (homepage, dashboard, etc.)
│   ├── api.py                      # API endpoints (/api/*)
│   └── admin.py                    # Admin routes (/admin/*)
│
├── services/                       # Business Logic Services
│   ├── auth_service.py             # Authentication service
│   ├── data_service.py             # Data fetching service
│   ├── skill_service.py            # Skill gap analysis service
│   ├── recommendation_service.py  # Job recommendation service
│   ├── prediction_service.py       # Prediction execution service
│   └── blog_service.py             # Blog posts service
│
├── templates/                      # HTML Templates (Jinja2)
│   ├── base.html                   # Base template with layout
│   ├── index.html                  # Homepage/landing page
│   ├── dashboard.html              # Dashboard with analytics
│   ├── predict.html                # Dataset upload & prediction page
│   ├── skill_gap.html             # Skill gap analyzer page
│   ├── recommendations.html        # Job recommendations page
│   ├── trends.html                 # Trends explorer page
│   ├── ml_insights.html            # ML model insights page
│   ├── blog.html                   # Blog listing page
│   ├── blog_post.html              # Individual blog post page
│   │
│   ├── components/                 # Reusable UI components
│   │   ├── sidebar.html            # Sidebar navigation component
│   │   └── navbar.html             # Top navbar component
│   │
│   ├── admin/                      # Admin templates
│   │   └── dashboard.html          # Admin dashboard
│   │
│   ├── errors/                     # Error pages
│   │   ├── 404.html                # 404 Not Found page
│   │   └── 500.html                # 500 Server Error page
│   │
│   └── admin/                      # Admin login (root level)
│       └── login.html              # Admin login page
│
├── static/                         # Static files (CSS, JS, images)
│   └── css/
│       └── custom.css              # Custom CSS styles
│
├── data/                           # Data files (CSV, JSON)
│   ├── job_postings_sample.csv    # Sample job postings dataset
│   ├── skills_database.json       # Skills database per job role
│   ├── job_roles.json              # List of job roles
│   ├── all_skills.json             # Complete list of skills
│   └── blog_posts.json             # Blog posts data
│
├── tests/                          # Test files
│   ├── __init__.py                 # Tests package init
│   └── test_api.py                 # API endpoint tests
│
├── uploads/                        # User uploaded files (created at runtime)
└── models/                         # Trained ML models (created at runtime)
```

## Key Files Description

### Core Application Files

- **app.py**: Main Flask application. Initializes Flask, registers blueprints, sets up error handlers.

### Routes

- **routes/main.py**: Public-facing routes (homepage, dashboard, features)
- **routes/api.py**: REST API endpoints for predictions, skill gap, recommendations
- **routes/admin.py**: Admin-only routes for managing data

### Services

- **services/prediction_service.py**: Orchestrates prediction execution
- **services/skill_service.py**: Handles skill gap analysis logic
- **services/recommendation_service.py**: Job recommendation algorithm
- **services/data_service.py**: Fetches dashboard statistics and trends

### ML Models

- **ml/model.py**: Contains `JobMarketPredictor` class with:
  - Demand forecasting (placeholder)
  - Skill gap analysis
  - Market saturation prediction
  - Job recommendations

### Templates

All templates extend `base.html` and use TailwindCSS for styling. Components are reusable partials.

### Data Files

- **CSV files**: Sample datasets for testing
- **JSON files**: Configuration and reference data

## File Naming Conventions

- Python files: `snake_case.py`
- Templates: `kebab-case.html`
- Static files: `kebab-case.css/js`
- Data files: `snake_case.json/csv`

## Directory Purposes

- **models/**: Trained ML models (`.joblib`, `.pkl` files)
- **uploads/**: User-uploaded CSV files for prediction
- **static/**: CSS, JavaScript, images (served directly)
- **templates/**: Jinja2 HTML templates
- **data/**: Reference data and sample datasets
- **tests/**: Unit and integration tests

## Adding New Features

1. **New Page**: Add route in `routes/main.py`, create template in `templates/`
2. **New API**: Add endpoint in `routes/api.py`
3. **New Service**: Create file in `services/`
4. **New ML Model**: Add method to `ml/model.py` or create new file

## Deployment Files

- **Procfile**: Tells Heroku/Render how to run the app
- **runtime.txt**: Specifies Python version
- **requirements.txt**: Python package dependencies

