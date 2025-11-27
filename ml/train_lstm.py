"""
LSTM training pipeline for job demand forecasting.

This script trains a separate LSTM model for each job role using historical
job posting counts. Models and scalers are saved under the `models/` directory.
"""
import argparse
import logging
import os
from typing import List, Tuple

import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.models import Sequential

LOGGER = logging.getLogger(__name__)
WINDOW_SIZE = 12


def slugify_role(role: str) -> str:
    """Create a filesystem-friendly slug for a job role."""
    return role.strip().lower().replace(" ", "_").replace("/", "-")


def create_sequences(values: np.ndarray, window_size: int) -> Tuple[np.ndarray, np.ndarray]:
    """
    Create sliding window sequences for LSTM training.

    Args:
        values: Array of scaled posting counts shaped (n, 1).
        window_size: Number of time steps to include in each sequence.

    Returns:
        Tuple of (X, y) where:
            X -> (samples, window_size, 1)
            y -> (samples, 1)
    """
    X, y = [], []
    for i in range(window_size, len(values)):
        X.append(values[i - window_size:i])
        y.append(values[i])
    return np.array(X), np.array(y)


def build_lstm_model(input_shape: Tuple[int, int]) -> Sequential:
    """Build the LSTM network."""
    model = Sequential(
        [
            LSTM(50, return_sequences=True, input_shape=input_shape),
            Dropout(0.2),
            LSTM(50),
            Dropout(0.2),
            Dense(1),
        ]
    )
    model.compile(optimizer="adam", loss="mse")
    return model


def prepare_role_series(df: pd.DataFrame, role: str) -> pd.Series:
    """Aggregate postings per month for a specific role."""
    role_df = df[df["job_role"] == role].copy()
    if role_df.empty:
        return pd.Series(dtype=float)

    role_df["date"] = pd.to_datetime(role_df["date"])
    role_df = role_df.set_index("date").sort_index()

    if "postings_count" in role_df.columns:
        monthly = role_df["postings_count"].resample("M").sum()
    else:
        monthly = role_df.resample("M").size()

    # Fill missing months with zeros to keep continuity
    monthly = monthly.asfreq("M", fill_value=0)
    return monthly


def train_role_model(role: str, series: pd.Series, models_dir: str) -> bool:
    """Train and persist an LSTM model for a given role."""
    if len(series) <= WINDOW_SIZE:
        LOGGER.warning("Skipping %s. Need > %s data points, got %s.", role, WINDOW_SIZE, len(series))
        return False

    values = series.values.reshape(-1, 1)
    scaler = MinMaxScaler()
    scaled_values = scaler.fit_transform(values)

    X, y = create_sequences(scaled_values, WINDOW_SIZE)
    if len(X) == 0:
        LOGGER.warning("Insufficient sequences for %s after scaling.", role)
        return False

    model = build_lstm_model((WINDOW_SIZE, 1))
    es = EarlyStopping(monitor="loss", patience=5, restore_best_weights=True)
    model.fit(X, y, epochs=50, batch_size=16, verbose=0, callbacks=[es])

    os.makedirs(models_dir, exist_ok=True)
    role_slug = slugify_role(role)
    model_path = os.path.join(models_dir, f"lstm_{role_slug}.keras")
    scaler_path = os.path.join(models_dir, f"scaler_{role_slug}.pkl")

    model.save(model_path)
    joblib.dump(scaler, scaler_path)
    LOGGER.info("Saved LSTM model and scaler for %s", role)
    return True


def train_lstm_models(data_path: str, models_dir: str = "models") -> List[str]:
    """Main training entry point."""
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Data file not found: {data_path}")

    df = pd.read_csv(data_path)
    required_cols = {"date", "job_role", "postings_count"}
    if not required_cols.issubset(df.columns):
        missing = required_cols - set(df.columns)
        raise ValueError(f"Missing required columns: {missing}")

    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    trained_roles = []
    for role in df["job_role"].unique():
        series = prepare_role_series(df, role)
        if train_role_model(role, series, models_dir):
            trained_roles.append(role)

    if not trained_roles:
        LOGGER.warning("No roles were trained. Check data availability.")
    return trained_roles


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(description="Train LSTM models for job roles.")
    parser.add_argument("--data", required=True, help="Path to CSV with columns date, job_role, postings_count.")
    parser.add_argument("--models-dir", default="models", help="Directory where models and scalers will be saved.")
    return parser.parse_args()


def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s - %(message)s")
    args = parse_args()
    trained = train_lstm_models(args.data, args.models_dir)
    LOGGER.info("Training complete. Models created for roles: %s", ", ".join(trained) if trained else "None")


if __name__ == "__main__":
    main()

