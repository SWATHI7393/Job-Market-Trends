"""Unit tests for the LSTM demand forecasting pipeline."""

import os
import unittest

import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.models import Sequential

from ml.model import JobMarketPredictor, slugify_role
from ml.train_lstm import WINDOW_SIZE, create_sequences, prepare_role_series


class TestLSTMUtilities(unittest.TestCase):
    """Validate helper utilities used by the LSTM workflow."""

    def test_create_sequences_shape(self):
        values = np.arange(1, WINDOW_SIZE + 5).reshape(-1, 1)
        X, y = create_sequences(values, WINDOW_SIZE)
        self.assertEqual(X.shape[0], y.shape[0])
        self.assertEqual(X.shape[1], WINDOW_SIZE)
        self.assertEqual(X.shape[2], 1)

    def test_prepare_role_series(self):
        dates = pd.date_range("2023-01-01", periods=6, freq="M")
        df = pd.DataFrame(
            {
                "date": list(dates) + list(dates),
                "job_role": ["Data Scientist"] * 6 + ["ML Engineer"] * 6,
                "postings_count": np.arange(12),
            }
        )
        series = prepare_role_series(df, "Data Scientist")
        self.assertEqual(len(series), 6)
        self.assertEqual(series.index.freqstr, "M")


class TestLSTMIntegration(unittest.TestCase):
    """Integration tests covering model loading and fallbacks."""

    @classmethod
    def setUpClass(cls):
        os.makedirs("models", exist_ok=True)

    def setUp(self):
        self.predictor = JobMarketPredictor()
        self.role_name = "Test Role"
        self.role_slug = slugify_role(self.role_name)
        self.model_path = os.path.join("models", f"lstm_{self.role_slug}.keras")
        self.scaler_path = os.path.join("models", f"scaler_{self.role_slug}.pkl")
        self._cleanup_role_files()

    def tearDown(self):
        self._cleanup_role_files()

    def _cleanup_role_files(self):
        for path in [self.model_path, self.scaler_path]:
            if os.path.exists(path):
                os.remove(path)

    def _save_dummy_model(self, values: np.ndarray):
        scaler = MinMaxScaler()
        scaled = scaler.fit_transform(values.reshape(-1, 1))
        X, y = create_sequences(scaled, WINDOW_SIZE)
        model = Sequential(
            [
                LSTM(10, input_shape=(WINDOW_SIZE, 1), return_sequences=True),
                LSTM(10),
                Dense(1),
            ]
        )
        model.compile(optimizer="adam", loss="mse")
        model.fit(X, y, epochs=1, verbose=0)
        model.save(self.model_path)
        joblib.dump(scaler, self.scaler_path)

    def test_model_loading(self):
        values = np.arange(1, WINDOW_SIZE + 5)
        self._save_dummy_model(values)
        model, scaler = self.predictor._load_lstm_resources(self.role_name)
        self.assertIsNotNone(model)
        self.assertIsNotNone(scaler)

    def test_predict_demand_with_lstm(self):
        values = np.arange(1, WINDOW_SIZE + 5)
        self._save_dummy_model(values)
        dates = pd.date_range("2023-01-01", periods=len(values), freq="M")
        df = pd.DataFrame(
            {
                "date": dates,
                "job_title": [self.role_name] * len(values),
                "postings_count": values,
            }
        )
        predictions = self.predictor.predict_demand(df)
        self.assertEqual(len(predictions), 1)
        self.assertEqual(predictions[0]["role"], self.role_name)

    def test_fallback_when_model_missing(self):
        dates = pd.date_range("2023-01-01", periods=WINDOW_SIZE + 1, freq="M")
        df = pd.DataFrame(
            {
                "date": dates,
                "job_title": ["Missing Model"] * len(dates),
                "postings_count": np.random.randint(50, 150, size=len(dates)),
            }
        )
        predictions = self.predictor.predict_demand(df)
        self.assertEqual(predictions[0]["role"], "Missing Model")
        self.assertGreaterEqual(predictions[0]["demand"], 0)


if __name__ == "__main__":
    unittest.main()


