"""
Prediction service for processing datasets and running predictions
"""
import logging
import pandas as pd
from ml.model import JobMarketPredictor

LOGGER = logging.getLogger(__name__)

def process_dataset(filepath):
    """Process uploaded dataset"""
    try:
        df = pd.read_csv(filepath)
        return {
            'rows': len(df),
            'columns': list(df.columns),
            'sample': df.head(5).to_dict('records')
        }
    except Exception as e:
        raise Exception(f"Error processing dataset: {str(e)}")

def run_prediction(filepath):
    """Run prediction on dataset"""
    try:
        # Load predictor
        predictor = JobMarketPredictor()
        
        # Load and process data
        df = pd.read_csv(filepath)
        
        # Run predictions (LSTM + fallbacks)
        try:
            predictions = predictor.predict_demand(df)
        except Exception as model_error:
            LOGGER.error("LSTM prediction failed: %s. Falling back to heuristic model.", model_error)
            predictions = predictor.fallback_predictions(df)
        
        skill_gap_scores = predictor.analyze_skill_gaps(df)
        saturation_scores = predictor.predict_saturation(df)
        
        return {
            'predictions': predictions,
            'skill_gap_scores': skill_gap_scores,
            'saturation_scores': saturation_scores,
            'summary': {
                'total_predictions': len(predictions),
                'avg_demand': sum(p['demand'] for p in predictions) / len(predictions) if predictions else 0,
                'high_demand_roles': [p['role'] for p in predictions if p['demand'] > 1000][:5]
            }
        }
    except Exception as e:
        raise Exception(f"Error running prediction: {str(e)}")

