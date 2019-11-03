from enum import Enum


class AlmaPermissionSet(Enum):
    """
    Lista de permissões do usuário
    """

    ADMIN = "ADMIN"
    TEACHER = "TEACHER"
    STUDENT = "STUDENT"