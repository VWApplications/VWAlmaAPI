from enum import Enum


class ExamSet(Enum):
    """
    Tipos de avaliações.
    """

    EXERCISE = "EXERCISE"
    GAMIFICATION = "GAMIFICATION"
    TRADITIONAL = "TRADITIONAL"
    IRAT = "IRAT"
    GRAT = "GRAT"
    PEER_REVIEW = "PEER_REVIEW"