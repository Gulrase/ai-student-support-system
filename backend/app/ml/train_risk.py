from __future__ import annotations

from typing import Tuple


def clamp(value: float, min_value: float = 0.0, max_value: float = 1.0) -> float:
    return max(min_value, min(max_value, value))


def score_features(attendance_rate: float, gpa: float, missed_assignments: int) -> float:
    """Compute a simple risk score between 0 and 1.

    Heuristic model for prototype purposes only:
    - Lower attendance increases risk
    - Lower GPA increases risk
    - More missed assignments increase risk
    """

    attendance_component = 1.0 - clamp(attendance_rate, 0.0, 1.0)
    gpa_component = 1.0 - clamp(gpa / 4.0, 0.0, 1.0)
    assignments_component = clamp(missed_assignments / 10.0, 0.0, 1.0)

    # Weighted average
    risk = 0.45 * attendance_component + 0.35 * gpa_component + 0.20 * assignments_component
    return clamp(risk, 0.0, 1.0)


def train_placeholder_model() -> Tuple[float, float, float]:
    """Return weights for documentation/demo.

    In a real system, you would train a proper model and persist artifacts.
    """
    return 0.45, 0.35, 0.20


def score_chat_text(message_text: str) -> float:
    """Return a wellbeing score in [0, 1] based on simple keyword heuristics.

    Lower score indicates potential distress; higher score indicates positive state.
    This is not clinical and should be replaced with a proper model if needed.
    """
    text = (message_text or "").lower()

    negative_keywords = {
        "stressed": 0.15,
        "stress": 0.15,
        "anxious": 0.15,
        "anxiety": 0.15,
        "depressed": 0.1,
        "depression": 0.1,
        "lonely": 0.2,
        "alone": 0.2,
        "overwhelmed": 0.2,
        "burnout": 0.15,
        "panic": 0.15,
        "hard": 0.2,
        "struggle": 0.2,
        "struggling": 0.2,
        "cry": 0.15,
        "sad": 0.15,
        "tired": 0.1,
        "exhausted": 0.15,
        "hopeless": 0.05,
        "fail": 0.15,
        "failure": 0.15,
    }

    positive_keywords = {
        "happy": 0.9,
        "excited": 0.85,
        "confident": 0.85,
        "good": 0.8,
        "great": 0.85,
        "calm": 0.8,
        "relaxed": 0.8,
        "motivated": 0.85,
        "proud": 0.85,
        "win": 0.8,
        "success": 0.85,
    }

    # Base neutral score
    wellbeing_score = 0.6

    # Penalize for negative keywords (take minimum hit)
    for word, score_floor in negative_keywords.items():
        if word in text:
            wellbeing_score = min(wellbeing_score, score_floor)

    # Boost for positive keywords (take maximum boost)
    for word, score_target in positive_keywords.items():
        if word in text:
            wellbeing_score = max(wellbeing_score, score_target)

    return clamp(wellbeing_score, 0.0, 1.0)


