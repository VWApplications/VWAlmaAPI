from enum import Enum


class TypeSet(Enum):
    """
    Tipos de questão
    """

    V_OR_F = "V_OR_F"
    MULTIPLE_CHOICES = "MULTIPLE_CHOICES"


class CorrectAnswerSet(Enum):
    """
    Alternativas corretas:
    V ou F: (TRUE ou FALSE)
    Multipla escolha: (A, B, C, D) 
    """

    UNDEFINED = "UNDEFINED"
    TRUE = "TRUE"
    FALSE = "FALSE"
    A = "A"
    B = "B"
    C = "C"
    D = "D"