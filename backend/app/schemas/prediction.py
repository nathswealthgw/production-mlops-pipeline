from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    age: int = Field(ge=18, le=100)
    monthly_income: float = Field(ge=0)
    credit_score: int = Field(ge=300, le=850)
    loan_amount: float = Field(ge=100)
    loan_term_months: int = Field(ge=6, le=480)


class PredictionResponse(BaseModel):
    model_version: str
    default_probability: float
    risk_band: str
    inference_ms: float
