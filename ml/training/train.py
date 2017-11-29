from pathlib import Path

import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression


def generate_dataset(size: int = 5000) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed=42)
    age = rng.integers(18, 75, size)
    monthly_income = rng.normal(7000, 2500, size).clip(1000, 25000)
    credit_score = rng.normal(680, 90, size).clip(300, 850)
    loan_amount = rng.normal(120000, 75000, size).clip(1000, 500000)
    loan_term = rng.integers(6, 360, size)

    logits = (
        (loan_amount / monthly_income) * 0.08
        - (credit_score - 650) * 0.01
        + (loan_term / 360) * 1.4
    )
    probability = 1 / (1 + np.exp(-logits))
    labels = rng.binomial(1, probability)

    features = np.stack([age, monthly_income, credit_score, loan_amount, loan_term], axis=1)
    return features, labels


def train() -> None:
    features, labels = generate_dataset()
    model = LogisticRegression(max_iter=500)
    model.fit(features, labels)

    output = Path("ml/training/artifacts")
    output.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, output / "model.joblib")


if __name__ == "__main__":
    train()
