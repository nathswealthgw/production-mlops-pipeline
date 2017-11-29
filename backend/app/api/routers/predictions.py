import json

from fastapi import APIRouter, Header, HTTPException

from app.core.config import settings
from app.core.security import SignatureValidator
from app.schemas.prediction import PredictionRequest, PredictionResponse
from app.services.event_service import event_service
from app.services.model_service import model_service

router = APIRouter(tags=["predictions"])
validator = SignatureValidator(settings.hmac_secret)


@router.post("/predictions", response_model=PredictionResponse)
def predict(
    payload: PredictionRequest,
    x_signature: str = Header(default="", alias="x-signature"),
) -> PredictionResponse:
    payload_bytes = payload.model_dump_json().encode("utf-8")
    if not validator.verify(payload_bytes, x_signature):
        raise HTTPException(status_code=401, detail="Invalid request signature")

    result = model_service.predict(payload)
    event_service.publish_prediction_event(payload.model_dump(), json.loads(result.model_dump_json()))
    return result
