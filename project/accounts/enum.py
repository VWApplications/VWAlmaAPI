from enum import Enum


class PermissionSet(Enum):
    """
    Lista de permissões do usuário
    """

    ADMIN = "ADMIN"
    TEACHER = "TEACHER"
    STUDENT = "STUDENT"
    MONITOR = "MONITOR"