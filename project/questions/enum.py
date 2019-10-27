from enum import Enum


class TypeSet(Enum):
    """
    Tipos de questão
    """

    V_OR_F = "V_OR_F"
    MULTIPLE_CHOICES = "MULTIPLE_CHOICES"
    SHOT = "SHOT"
    SCRATCH_CARD = "SCRATCH_CARD"
