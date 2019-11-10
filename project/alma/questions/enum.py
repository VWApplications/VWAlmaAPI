from enum import Enum


class TypeSet(Enum):
    """
    Tipos de questão
    """

    V_OR_F = "V_OR_F"
    MULTIPLE_CHOICES = "MULTIPLE_CHOICES"
    SHOT = "SHOT"


class ExamTypeSet(Enum):
    """
    Tipos de prova a ser aplicada a questão
    """

    EXERCISE = "EXERCISE"
    TRADITIONAL = "TRADITIONAL"
    TBL = "TBL"