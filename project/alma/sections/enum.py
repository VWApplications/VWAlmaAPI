from enum import Enum


class MethodologyTypeSet(Enum):
    """
    Tipos de metodologia aplicado a seção.
    """

    TRADITIONAL = "TRADITIONAL"
    TBL = "TBL"


class ConfigTitleSet(Enum):
    """
    Títulos de avaliações.
    """

    TRADITIONAL = "TRADITIONAL"
    EXERCISE = "EXERCISE"
    IRAT = "IRAT"
    GRAT = "GRAT"
    PRACTICAL = "PRACTICAL"
    PEER_REVIEW = "PEER_REVIEW"