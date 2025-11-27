"""
ML Model for Job Market Predictions
"""
import logging
import os
from typing import Optional, Tuple

import joblib
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model

LOGGER = logging.getLogger(__name__)


def slugify_role(role: str) -> str:
    """Create a filesystem-friendly slug for a job role."""
    return role.strip().lower().replace(" ", "_").replace("/", "-")


class JobMarketPredictor:
    """
    Main predictor class for job market analytics
    """
    
    def __init__(self):
        """Initialize the predictor with models"""
        self.models_dir = 'models'
        os.makedirs(self.models_dir, exist_ok=True)
        
        self.window_size = 12
        self.lstm_models = {}
        self.scalers = {}
        
    # ------------------------------------------------------------------
    # Demand Forecasting
    # ------------------------------------------------------------------
    def predict_demand(self, df):
        """
        Predict job demand for roles in the dataset using LSTM models
        with graceful fallbacks to traditional heuristics.
        """
        role_col = next((col for col in ['job_title', 'job_role', 'role'] if col in df.columns), None)
        if role_col is None:
            LOGGER.warning("Role column missing. Falling back to frequency-based predictions.")
            return self._fallback_predictions(df)
        
        if 'date' not in df.columns:
            LOGGER.warning("Date column missing. Falling back to frequency-based predictions.")
            return self._fallback_predictions(df)
        
        work_df = df.copy()
        work_df['date'] = pd.to_datetime(work_df['date'], errors='coerce')
        work_df = work_df.dropna(subset=['date'])
        if work_df.empty:
            LOGGER.warning("All date rows invalid. Falling back to frequency-based predictions.")
            return self._fallback_predictions(df)
        
        role_counts = work_df[role_col].value_counts().head(10)
        if role_counts.empty:
            LOGGER.warning("No roles available after filtering. Using default predictions.")
            return self._fallback_predictions(df)
        
        predictions = []
        for role in role_counts.index:
            role_df = work_df[work_df[role_col] == role]
            prediction = self._predict_role_with_lstm(role, role_df)
            predictions.append(prediction)
        return predictions
    
    def _predict_role_with_lstm(self, role: str, role_df: pd.DataFrame) -> dict:
        """Generate demand prediction for a single role."""
        series = self._build_monthly_series(role_df)
        current_demand = int(series.iloc[-1]) if not series.empty else 0
        
        predicted_value = None
        confidence = 0.65  # default fallback
        
        if len(series) >= self.window_size:
            model, scaler = self._load_lstm_resources(role)
            if model and scaler:
                predicted_value = self._predict_with_model(series, model, scaler)
                confidence = 0.92
            else:
                LOGGER.warning("Missing LSTM resources for %s. Using moving average.", role)
        
        if predicted_value is None:
            predicted_value = self._moving_average(series)
        
        predicted_value = max(0, float(predicted_value))
        growth_rate = (
            ((predicted_value - current_demand) / current_demand) * 100
            if current_demand > 0 else 0
        )
        
        return {
            'role': role,
            'current_demand': int(current_demand),
            'demand': int(round(predicted_value)),
            'growth_rate': round(growth_rate, 2),
            'confidence': round(confidence, 2)
        }
    
    def _build_monthly_series(self, role_df: pd.DataFrame) -> pd.Series:
        """Aggregate postings per month for a role."""
        role_df = role_df.sort_values('date').set_index('date')
        if 'postings_count' in role_df.columns:
            series = role_df['postings_count'].resample('M').sum()
        else:
            series = role_df.resample('M').size()
        series = series.asfreq('M', fill_value=0)
        return series
    
    def _load_lstm_resources(self, role: str) -> Tuple[Optional[object], Optional[object]]:
        """Load (and cache) LSTM model + scaler for a role."""
        slug = slugify_role(role)
        if slug in self.lstm_models and slug in self.scalers:
            return self.lstm_models[slug], self.scalers[slug]
        
        model_path = os.path.join(self.models_dir, f'lstm_{slug}.keras')
        scaler_path = os.path.join(self.models_dir, f'scaler_{slug}.pkl')
        
        if not os.path.exists(model_path) or not os.path.exists(scaler_path):
            LOGGER.warning("LSTM model or scaler missing for %s.", role)
            return None, None
        
        try:
            model = load_model(model_path)
            scaler = joblib.load(scaler_path)
            self.lstm_models[slug] = model
            self.scalers[slug] = scaler
            LOGGER.info("Loaded LSTM model for %s", role)
            return model, scaler
        except Exception as exc:
            LOGGER.error("Failed to load LSTM resources for %s: %s", role, exc)
            return None, None
    
    def _predict_with_model(self, series: pd.Series, model, scaler) -> float:
        """Invoke the LSTM model on the most recent window."""
        values = series.values.reshape(-1, 1)
        scaled = scaler.transform(values)
        input_seq = scaled[-self.window_size:]
        input_seq = np.expand_dims(input_seq, axis=0)
        prediction = model.predict(input_seq, verbose=0)
        return scaler.inverse_transform(prediction)[0][0]
    
    def _moving_average(self, series: pd.Series) -> float:
        """Simple moving average fallback."""
        if series.empty:
            return 0
        window = min(self.window_size, len(series))
        return float(series.tail(window).mean())
    
    def _fallback_predictions(self, df: pd.DataFrame):
        """Legacy heuristic predictions when LSTM cannot run."""
        if 'job_title' in df.columns:
            roles = df['job_title'].value_counts().head(10)
        elif 'role' in df.columns:
            roles = df['role'].value_counts().head(10)
        else:
            roles = pd.Series({'Data Scientist': 150, 'Software Engineer': 200})
        
        predictions = []
        for role, count in roles.items():
            growth_factor = 1.05
            predicted_demand = int(count * growth_factor)
            predictions.append({
                'role': role,
                'current_demand': int(count),
                'demand': predicted_demand,
                'growth_rate': round((growth_factor - 1) * 100, 2),
                'confidence': 0.5
            })
        return predictions
    
    def fallback_predictions(self, df: pd.DataFrame):
        """Public wrapper to expose fallback predictions."""
        return self._fallback_predictions(df)
    
    def analyze_skill_gaps(self, df):
        """
        Analyze skill gaps in the dataset
        
        Args:
            df: DataFrame with job postings and skills data
            
        Returns:
            Dictionary with skill gap scores
        """
        # Extract skills if available
        if 'skills' in df.columns or 'required_skills' in df.columns:
            skills_col = 'skills' if 'skills' in df.columns else 'required_skills'
            all_skills = []
            for skills_str in df[skills_col].dropna():
                if isinstance(skills_str, str):
                    skills = [s.strip() for s in skills_str.split(',')]
                    all_skills.extend(skills)
            
            skill_counts = pd.Series(all_skills).value_counts()
            
            return {
                'top_skills': skill_counts.head(10).to_dict(),
                'skill_demand_score': len(skill_counts),
                'gap_analysis': {
                    'high_demand_skills': skill_counts.head(5).index.tolist(),
                    'emerging_skills': skill_counts.tail(5).index.tolist()
                }
            }
        else:
            # Return default analysis
            return {
                'top_skills': {'Python': 150, 'SQL': 120, 'Machine Learning': 100},
                'skill_demand_score': 85,
                'gap_analysis': {
                    'high_demand_skills': ['Python', 'SQL', 'Machine Learning', 'Cloud', 'DevOps'],
                    'emerging_skills': ['LLM', 'MLOps', 'Kubernetes', 'Terraform', 'GraphQL']
                }
            }
    
    def predict_saturation(self, df):
        """
        Predict market saturation for job roles
        
        Args:
            df: DataFrame with job postings data
            
        Returns:
            List of saturation scores per role
        """
        if 'job_title' in df.columns:
            roles = df['job_title'].value_counts()
        elif 'role' in df.columns:
            roles = df['role'].value_counts()
        else:
            roles = pd.Series({'Data Scientist': 150, 'Software Engineer': 200})
        
        saturation_scores = []
        max_count = roles.max()
        
        for role, count in roles.head(10).items():
            # Saturation score: 0-100, higher = more saturated
            saturation = min(100, (count / max_count) * 100) if max_count > 0 else 0
            
            saturation_scores.append({
                'role': role,
                'saturation_score': round(saturation, 2),
                'job_count': int(count),
                'status': 'saturated' if saturation > 70 else 'moderate' if saturation > 40 else 'emerging'
            })
        
        return saturation_scores
    
    def recommend_jobs(self, user_skills, n_recommendations=5):
        """
        Recommend jobs based on user skills
        
        Args:
            user_skills: List of user skills
            n_recommendations: Number of recommendations to return
            
        Returns:
            List of recommended job roles with match scores
        """
        # This is a simplified rule-based approach
        # In production, you'd use a trained classifier
        
        # Load job role skills database
        skills_file = 'data/skills_database.json'
        if os.path.exists(skills_file):
            import json
            with open(skills_file, 'r') as f:
                role_skills = json.load(f)
        else:
            role_skills = {
                'Data Scientist': ['Python', 'SQL', 'Machine Learning', 'Statistics'],
                'Software Engineer': ['Programming', 'Algorithms', 'System Design'],
                'ML Engineer': ['Python', 'Machine Learning', 'MLOps', 'Cloud']
            }
        
        recommendations = []
        user_skills_lower = [s.lower() for s in user_skills]
        
        for role, required_skills in role_skills.items():
            required_lower = [s.lower() for s in required_skills]
            matches = sum(1 for s in required_lower if s in user_skills_lower)
            match_score = (matches / len(required_skills) * 100) if required_skills else 0
            
            recommendations.append({
                'role': role,
                'match_score': round(match_score, 2),
                'matching_skills': matches,
                'total_required': len(required_skills)
            })
        
        # Sort by match score
        recommendations.sort(key=lambda x: x['match_score'], reverse=True)
        return recommendations[:n_recommendations]

def train_time_series_model(data_file='data/job_postings_sample.csv'):
    """
    Deprecated helper kept for compatibility. Use ml/train_lstm.py instead.
    """
    LOGGER.warning("train_time_series_model is deprecated. Run `python ml/train_lstm.py --data <file>` instead.")
    return None

if __name__ == '__main__':
    # Demo script
    print("Job Market Predictor - Demo")
    print("=" * 50)
    
    # Create predictor
    predictor = JobMarketPredictor()
    
    # Create dummy dataset
    dummy_data = pd.DataFrame({
        'job_title': ['Data Scientist'] * 50 + ['Software Engineer'] * 75 + ['ML Engineer'] * 30,
        'skills': ['Python, SQL, ML'] * 155,
        'date': pd.date_range('2024-01-01', periods=155, freq='D')
    })
    
    # Run predictions
    print("\n1. Demand Predictions:")
    predictions = predictor.predict_demand(dummy_data)
    for p in predictions[:3]:
        print(f"   {p['role']}: {p['demand']} jobs (growth: {p['growth_rate']}%)")
    
    print("\n2. Skill Gap Analysis:")
    skill_gaps = predictor.analyze_skill_gaps(dummy_data)
    print(f"   Top Skills: {list(skill_gaps['top_skills'].keys())[:5]}")
    
    print("\n3. Saturation Scores:")
    saturation = predictor.predict_saturation(dummy_data)
    for s in saturation[:3]:
        print(f"   {s['role']}: {s['saturation_score']}% ({s['status']})")
    
    print("\n4. Job Recommendations:")
    recommendations = predictor.recommend_jobs(['Python', 'SQL', 'Machine Learning'])
    for r in recommendations[:3]:
        print(f"   {r['role']}: {r['match_score']}% match")
    
    print("\nDemo completed!")

