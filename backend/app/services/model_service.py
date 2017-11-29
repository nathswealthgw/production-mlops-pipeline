import time
from pathlib import Path

import joblib
import numpy as np

from app.core.config import settings
from app.schemas.prediction import PredictionRequest, PredictionResponse


class ModelService:
    def __init__(self) -> None:
        self._model = None
        self.model_version = settings.model_version
        self._load_model()

    def _load_model(self) -> None:
        artifact = Path(settings.model_artifact_path)
        if artifact.exists():
            self._model = joblib.load(artifact)
        else:
            self._model = None

    def _to_vector(self, payload: PredictionRequest) -> np.ndarray:
        return np.array(
            [[
                payload.age,
                payload.monthly_income,
                payload.credit_score,
                payload.loan_amount,
                payload.loan_term_months,
            ]],
            dtype=float,
        )

    def predict(self, payload: PredictionRequest) -> PredictionResponse:
        start = time.perf_counter()
        if self._model is None:
            probability = min(0.95, max(0.05, payload.loan_amount / (payload.monthly_income * 20)))
        else:
            probability = float(self._model.predict_proba(self._to_vector(payload))[0][1])

        if probability < 0.2:
            band = "low"
        elif probability < 0.5:
            band = "medium"
        else:
            band = "high"

        inference_ms = (time.perf_counter() - start) * 1000
        return PredictionResponse(
            model_version=self.model_version,
            default_probability=round(probability, 4),
            risk_band=band,
            inference_ms=round(inference_ms, 2),
        )


model_service = ModelService()
