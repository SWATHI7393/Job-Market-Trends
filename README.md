# Predictive Analytics for Job Market Trends

A comprehensive full-stack web application for analyzing and predicting job market trends using machine learning. This project provides insights into job demand forecasting, skill gap analysis, salary trends, and personalized job recommendations.

## 🚀 Features

- **Job Demand Forecasting**: Predict future job market demand using time-series models
- **Skill Gap Analyzer**: Identify missing skills and get personalized recommendations
- **Salary Trend Predictions**: Analyze and forecast salary trends across industries
- **Job Recommendation Engine**: AI-powered job recommendations based on skills
- **Trends Explorer**: Search and explore historical and forecasted trends for job roles
- **ML Model Insights**: Visualize model architecture, metrics, and performance
- **Admin Dashboard**: Manage skills database and upload datasets
- **Blog/Insights**: Educational content about job market trends

## 📋 Project Structure

```
job-trend/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Procfile              # Deployment configuration
├── tailwind.config.js    # TailwindCSS configuration
├── models/               # ML models directory
│   └── model.py         # ML prediction models
├── routes/               # Flask blueprints
│   ├── main.py          # Public routes
│   ├── api.py           # API endpoints
│   └── admin.py         # Admin routes
├── services/             # Business logic services
│   ├── auth_service.py
│   ├── data_service.py
│   ├── skill_service.py
│   ├── recommendation_service.py
│   ├── prediction_service.py
│   └── blog_service.py
├── templates/            # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── dashboard.html
│   ├── predict.html
│   ├── skill_gap.html
│   ├── recommendations.html
│   ├── trends.html
│   ├── ml_insights.html
│   ├── blog.html
│   ├── components/       # Reusable components
│   ├── admin/           # Admin templates
│   └── errors/          # Error pages
├── static/              # Static files (CSS, JS, images)
├── data/                # Data files
│   ├── job_postings_sample.csv
│   ├── skills_database.json
│   ├── job_roles.json
│   ├── all_skills.json
│   └── blog_posts.json
└── uploads/             # Uploaded files directory
```

## 🛠️ Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Local Development Setup

1. **Clone the repository** (or navigate to project directory)
   ```bash
   cd "job trend"
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Create necessary directories**
   ```bash
   mkdir uploads
   mkdir models
   ```

6. **Set environment variables** (optional)
   Create a `.env` file in the root directory:
   ```
   SECRET_KEY=your-secret-key-here
   FLASK_ENV=development
   ```

7. **Run the application**
   ```bash
   python app.py
   ```

8. **Access the application**
   - Open your browser and navigate to: `http://localhost:5000`
   - Default admin credentials: `admin` / `admin123`

## 🧪 Running ML Demo

To test the ML models with sample data:

```bash
python ml/model.py
```

This will:
- Load/create the demand forecasting model
- Process a dummy dataset
- Generate predictions, skill gap analysis, and saturation scores
- Display job recommendations

### LSTM Demand Forecaster

The demand forecasting engine now uses per-role LSTM models trained on monthly posting counts.

**Training script**

```bash
python ml/train_lstm.py --data data/job_postings_timeseries.csv
```

The CSV must contain:

```
date,job_role,postings_count
2023-01-01,Data Scientist,120
2023-02-01,Data Scientist,150
```

Running the script:
- Parses monthly demand for each job role
- Normalizes values (MinMaxScaler)
- Creates 12-month input windows
- Trains a 2-layer LSTM (50 units each + dropout)
- Saves models to `models/lstm_<role>.keras`
- Saves scalers to `models/scaler_<role>.pkl`

During API predictions, the system loads the latest 12 months for every role, applies the matching LSTM, and falls back to a moving average whenever data or models are missing.

## 🧠 ML Model Architecture

| Component | Description |
| --- | --- |
| **Demand Forecasting** | Per-role LSTM models trained on monthly posting counts (12-month window, 2 × 50-unit LSTM layers + dropout). Models live in `models/lstm_<role>.keras`, scalers in `models/scaler_<role>.pkl`. |
| **Skill Gap Analyzer** | Compares candidate skills with required skills stored in JSON, highlights matches, gaps, and recommendations. |
| **Job Recommendations** | Rule-based engine that scores each role by overlapping skills and experience level. |
| **Market Saturation** | Relative scoring based on frequency of postings per role within the provided dataset. |

**Prediction flow**
1. User uploads CSV containing `date`, `job_title`/`job_role`, and optionally `postings_count`.
2. Backend aggregates the latest 12 months of activity per role.
3. If an LSTM + scaler exists for the role, the sequence is scaled, fed through the model, and inverse-scaled to produce next-month demand.
4. If a model or sufficient history is missing, the system gracefully falls back to a moving-average projection.
5. Results are surfaced in the dashboard, API responses, and prediction summaries.

## 📊 API Endpoints

### Public Endpoints

- `GET /` - Homepage
- `GET /dashboard` - Dashboard with analytics
- `GET /predict` - Prediction page
- `GET /skill-gap` - Skill gap analyzer
- `GET /recommendations` - Job recommendations
- `GET /trends` - Trends explorer
- `GET /ml-insights` - ML model insights
- `GET /blog` - Blog listing
- `GET /blog/<post_id>` - Individual blog post

### API Endpoints

- `POST /api/upload` - Upload CSV file for prediction
- `POST /api/predict` - Run prediction on uploaded file
- `POST /api/skill-gap` - Analyze skill gap
- `POST /api/recommendations` - Get job recommendations
- `GET /api/trends/<job_role>` - Get trends for a job role
- `GET /api/search?q=<query>` - Search job roles
- `GET /api/dashboard/stats` - Get dashboard statistics

### Admin Endpoints

- `GET /admin/login` - Admin login page
- `POST /admin/login` - Admin login
- `GET /admin/dashboard` - Admin dashboard (requires login)
- `POST /admin/skills` - Update skills database
- `POST /admin/upload-dataset` - Upload new dataset

## 🚀 Deployment

### Deploying to Render

1. **Create a Render account** at [render.com](https://render.com)

2. **Create a new Web Service**
   - Connect your GitHub repository
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `gunicorn app:app`
   - Set environment variables:
     - `SECRET_KEY`: Generate a secure random key

3. **Deploy**
   - Render will automatically deploy on push to main branch

### Deploying to Heroku

1. **Install Heroku CLI** and login
   ```bash
   heroku login
   ```

2. **Create a Heroku app**
   ```bash
   heroku create your-app-name
   ```

3. **Set environment variables**
   ```bash
   heroku config:set SECRET_KEY=your-secret-key
   ```

4. **Deploy**
   ```bash
   git push heroku main
   ```

### Deploying with Gunicorn (Production)

1. **Install Gunicorn** (already in requirements.txt)

2. **Run with Gunicorn**
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

3. **Using systemd (Linux)**
   Create `/etc/systemd/system/jobtrends.service`:
   ```ini
   [Unit]
   Description=Job Trends Analytics App
   After=network.target

   [Service]
   User=www-data
   WorkingDirectory=/path/to/job-trend
   Environment="PATH=/path/to/venv/bin"
   ExecStart=/path/to/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app

   [Install]
   WantedBy=multi-user.target
   ```

   Enable and start:
   ```bash
   sudo systemctl enable jobtrends
   sudo systemctl start jobtrends
   ```

## 🔧 Configuration

### TailwindCSS

The project uses TailwindCSS via CDN for quick setup. For production, you can:

1. Install TailwindCSS CLI:
   ```bash
   npm install -D tailwindcss
   npx tailwindcss init
   ```

2. Build CSS:
   ```bash
   npx tailwindcss -i ./static/src/input.css -o ./static/dist/output.css --watch
   ```

### Environment Variables

- `SECRET_KEY`: Flask secret key for sessions (required in production)
- `FLASK_ENV`: Set to `development` or `production`

## 📝 Extending the ML Stack

The platform now ships with production-ready LSTM demand forecasting. Future enhancements could include:

- **Job Recommendations**: Swap the rule-based matcher with a trained classifier or hybrid recommender.
- **Skill Gap Analysis**: Use NLP to extract skills from job descriptions and map them to ontologies for richer insights.
- **Additional Forecasting Models**: Experiment with Prophet/ARIMA or ensemble methods for benchmarking alongside the LSTM.

## 🧪 Testing

Run basic tests:
```bash
python -m pytest tests/  # If tests are added
```

## 📚 Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML, TailwindCSS, JavaScript
- **Charts**: Chart.js
- **ML Libraries**: TensorFlow/Keras, scikit-learn, pandas, numpy, statsmodels
- **Authentication**: Flask-Login
- **Deployment**: Gunicorn

## 🔄 Converting to Django

To convert this project to Django:

1. **Create Django project**:
   ```bash
   django-admin startproject jobtrends
   cd jobtrends
   python manage.py startapp main
   python manage.py startapp api
   python manage.py startapp admin_panel
   ```

2. **Map routes**:
   - Flask `@app.route('/')` → Django `urls.py` and `views.py`
   - Flask blueprints → Django apps
   - Flask templates → Django templates (similar structure)

3. **Update models**:
   - Convert Flask-Login User model to Django User model
   - Use Django ORM instead of JSON files

4. **Update services**:
   - Keep ML services mostly the same
   - Use Django's file handling instead of Flask's

5. **Update templates**:
   - Change `url_for()` to Django's `{% url %}` tag
   - Update template inheritance syntax if needed

## 🤝 Contributing

This is a final year project. For improvements:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is created for educational purposes as a final year project.

## 👥 Credits

- **Developer**: Swathi C
- **Project**: Predictive Analytics for Job Market Trends
- **Year**: 2025
- **Framework**: Flask (Python)
- **UI/UX**: TailwindCSS, Chart.js

## 📞 Support

For questions or issues, please refer to the project documentation or contact the development team.

---

**Note**: This is a demonstration project with sample data and placeholder ML models. For production use, integrate real datasets and trained models.

