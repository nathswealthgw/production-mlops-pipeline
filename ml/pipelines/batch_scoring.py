from dataclasses import dataclass

import numpy as np


@dataclass
class BatchMetrics:
    row_count: int
    mean_default_probability: float


def score_batch(rows: np.ndarray) -> BatchMetrics:
    scores = np.clip(rows[:, 3] / (rows[:, 1] * 20), 0.01, 0.99)
    return BatchMetrics(row_count=int(rows.shape[0]), mean_default_probability=float(scores.mean()))
