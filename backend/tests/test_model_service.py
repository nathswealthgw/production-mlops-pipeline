from app.schemas.prediction import PredictionRequest
from app.services.model_service import ModelService


def test_predict_returns_valid_probability() -> None:
    service = ModelService()
    response = service.predict(
        PredictionRequest(
            age=35,
            monthly_income=8000,
            credit_score=700,
            loan_amount=120000,
            loan_term_months=240,
        )
    )

    assert 0 <= response.default_probability <= 1
    assert response.risk_band in {"low", "medium", "high"}
