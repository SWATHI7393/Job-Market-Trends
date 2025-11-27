# How It Works: Prediction Flow & Architecture

## Overview

This document explains how the prediction system works and where to plug in real models and datasets.

## System Architecture

```
User Upload → File Processing → ML Model → Results Display
     ↓              ↓              ↓            ↓
  CSV File    Feature Extract   Predictions   Charts/Tables
```

## Prediction Flow

### 1. File Upload (`/predict`)

**User Action**: Uploads a CSV file with job postings data

**Backend Process**:
- File is saved to `uploads/` directory
- File metadata is stored
- API returns success with filename

**Code Location**: `routes/api.py` → `upload_file()`

### 2. Prediction Execution (`/api/predict`)

**User Action**: Clicks "Run Prediction"

**Backend Process**:
1. Loads the uploaded CSV file
2. Calls `prediction_service.run_prediction()`
3. Instantiates `JobMarketPredictor` from `ml/model.py`
4. Runs three prediction methods:
   - `predict_demand()` - Forecasts job demand
   - `analyze_skill_gaps()` - Analyzes skill requirements
   - `predict_saturation()` - Calculates market saturation

**Code Location**: 
- `routes/api.py` → `predict()`
- `services/prediction_service.py` → `run_prediction()`
- `ml/model.py` → `JobMarketPredictor` class

### 3. Results Processing

**ML Model Output**:
```python
{
    'predictions': [
        {
            'role': 'Data Scientist',
            'current_demand': 150,
            'demand': 173,
            'growth_rate': 15.0,
            'confidence': 0.85
        },
        ...
    ],
    'skill_gap_scores': {
        'top_skills': {...},
        'skill_demand_score': 85,
        'gap_analysis': {...}
    },
    'saturation_scores': [
        {
            'role': 'Data Scientist',
            'saturation_score': 75.5,
            'status': 'saturated'
        },
        ...
    ]
}
```

**Frontend Display**:
- Results are rendered in tables and charts
- Charts use Chart.js with dummy data (can be replaced with real predictions)

**Code Location**: `templates/predict.html` → JavaScript `displayResults()`

## ML Model Architecture

### Current Implementation (Placeholder)

**Location**: `ml/model.py`

**Classes**:
1. `JobMarketPredictor` - Main predictor class
   - `predict_demand()` - Simple growth factor calculation
   - `analyze_skill_gaps()` - Skill frequency analysis
   - `predict_saturation()` - Count-based saturation
   - `recommend_jobs()` - Rule-based matching

**Current Logic**:
- Demand: `predicted = current * 1.15` (15% growth)
- Skills: Counts skill frequency in dataset
- Saturation: `(count / max_count) * 100`

### Where to Add Real Models

#### 1. Time-Series Demand Forecasting

**Replace**: `predict_demand()` method

**Options**:
- **ARIMA** (statsmodels):
  ```python
  from statsmodels.tsa.arima.model import ARIMA
  model = ARIMA(demand_series, order=(1,1,1))
  fitted = model.fit()
  forecast = fitted.forecast(steps=12)
  ```

- **Prophet** (Facebook):
  ```python
  from prophet import Prophet
  model = Prophet()
  model.fit(df)
  future = model.make_future_dataframe(periods=12)
  forecast = model.predict(future)
  ```

- **LSTM** (TensorFlow):
  ```python
  from tensorflow.keras.models import Sequential
  from tensorflow.keras.layers import LSTM, Dense
  # Build and train LSTM model
  ```

**Data Requirements**:
- Historical job posting counts by month
- Features: date, job_role, industry, location

#### 2. Skill Gap Analysis

**Replace**: `analyze_skill_gaps()` method

**Enhancements**:
- Use NLP to extract skills from job descriptions
- Semantic similarity matching (Word2Vec, BERT)
- Skill ontology mapping
- Experience level weighting

**Example**:
```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')
user_skills_emb = model.encode(user_skills)
required_skills_emb = model.encode(required_skills)
similarity = cosine_similarity(user_skills_emb, required_skills_emb)
```

#### 3. Job Recommendation

**Replace**: `recommend_jobs()` method

**Options**:
- **Content-Based Filtering**: Match skills to job requirements
- **Collaborative Filtering**: User-job interaction matrix
- **Hybrid Approach**: Combine both methods

**Example with scikit-learn**:
```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

vectorizer = TfidfVectorizer()
job_vectors = vectorizer.fit_transform(job_descriptions)
user_vector = vectorizer.transform([user_skills_str])
similarity = cosine_similarity(user_vector, job_vectors)
```

## Data Flow

### Input Data Format

**CSV Structure** (expected):
```csv
job_title,company,location,skills,date,salary_min,salary_max
Data Scientist,TechCorp,Remote,"Python, SQL, ML",2024-01-15,90000,120000
```

**Required Columns**:
- `job_title` or `role`: Job role name
- `skills` or `required_skills`: Comma-separated skills
- `date`: Posting date (for time-series)

**Optional Columns**:
- `company`, `location`, `salary_min`, `salary_max`

### Data Storage

**Current**:
- Skills database: `data/skills_database.json`
- Job roles: `data/job_roles.json`
- Sample data: `data/job_postings_sample.csv`

**For Production**:
- Replace JSON files with SQLite/PostgreSQL database
- Use proper data models (SQLAlchemy)
- Implement data validation and cleaning

## Integration Points

### 1. Replace Dummy Data

**Location**: `services/data_service.py`

**Current**: Hardcoded statistics
```python
return {
    'total_jobs': 125000,
    'growth_rate': 12.5,
    ...
}
```

**Replace with**: Database queries
```python
from models import JobPosting
total_jobs = JobPosting.query.count()
growth_rate = calculate_growth_rate()
```

### 2. Add Real Charts

**Location**: Template JavaScript (e.g., `templates/dashboard.html`)

**Current**: Static dummy data
```javascript
data: [1200, 1350, 1500, ...]
```

**Replace with**: API calls
```javascript
fetch('/api/dashboard/stats')
  .then(res => res.json())
  .then(data => {
    chart.data.datasets[0].data = data.demand_series;
    chart.update();
  });
```

### 3. Model Training Pipeline

**Create**: `ml/train.py`

**Structure**:
```python
def train_demand_model():
    # Load historical data
    df = load_historical_data()
    
    # Feature engineering
    features = engineer_features(df)
    
    # Train model
    model = train_arima(features)
    
    # Save model
    joblib.dump(model, 'models/demand_model.joblib')

if __name__ == '__main__':
    train_demand_model()
```

**Run periodically**: Use cron jobs or scheduled tasks

## API Integration

### External Data Sources

**Job Postings APIs**:
- Indeed API
- LinkedIn API
- Glassdoor API
- Adzuna API

**Example Integration**:
```python
import requests

def fetch_job_postings(role, location):
    api_key = os.getenv('JOB_API_KEY')
    url = f'https://api.example.com/jobs?role={role}&location={location}'
    response = requests.get(url, headers={'Authorization': f'Bearer {api_key}'})
    return response.json()
```

## Performance Optimization

### Current Limitations

1. **In-memory user storage**: Replace with database
2. **No caching**: Add Redis for API responses
3. **Synchronous processing**: Use Celery for async predictions
4. **No model versioning**: Implement MLflow or similar

### Recommended Improvements

1. **Database**: SQLite (dev) → PostgreSQL (production)
2. **Caching**: Redis for frequently accessed data
3. **Async Tasks**: Celery for long-running predictions
4. **Model Registry**: MLflow for model versioning
5. **API Rate Limiting**: Flask-Limiter

## Testing ML Models

### Unit Tests

**Create**: `tests/test_ml_models.py`

```python
import unittest
from ml.model import JobMarketPredictor

class TestPredictor(unittest.TestCase):
    def test_predict_demand(self):
        predictor = JobMarketPredictor()
        # Test with sample data
        results = predictor.predict_demand(sample_df)
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
```

### Integration Tests

Test the full prediction pipeline:
```python
def test_prediction_flow():
    # Upload file
    # Run prediction
    # Verify results format
    # Check database updates
```

## Deployment Considerations

### Model Files

- Store trained models in `models/` directory
- Version control model files (Git LFS for large files)
- Include model metadata (version, training date, metrics)

### Environment Variables

```bash
SECRET_KEY=...
MODEL_PATH=models/
DATA_PATH=data/
API_KEYS=...
```

### Scaling

- Use load balancer for multiple app instances
- Separate ML service (microservice architecture)
- Use message queue for prediction jobs

## Next Steps

1. **Collect Real Data**: Scrape or use APIs for job postings
2. **Train Models**: Implement and train time-series models
3. **Improve UI**: Add real-time updates, better visualizations
4. **Add Authentication**: User accounts, saved predictions
5. **Deploy**: Set up production environment with proper monitoring

---

For questions or clarifications, refer to the main README.md or the code comments in `ml/model.py`.

