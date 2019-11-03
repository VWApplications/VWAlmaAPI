from django.contrib.auth import get_user_model
from django.db import models
from common.models import BaseModel
from .enum import AlmaPermissionSet

User = get_user_model()


class AlmaUser(BaseModel):
    """
    Cria usuários vinculados ao APP ALMA.
    """

    user = models.OneToOneField(
        User,
        on_delete=models.PROTECT,
        related_name='alma_user',
    )

    identifier = models.CharField(
        "Mátricula",
        help_text="Identificador dentro de sua universidade",
        max_length=50,
        blank=True
    )

    photo = models.ImageField(
        upload_to='accounts',
        help_text="Foto do usuário",
        blank=True,
        null=True
    )

    permission = models.CharField(
        "Permissão.",
        help_text="Verifica o tipo de permissão que o usuário tem.",
        max_length=50,
        default=AlmaPermissionSet.STUDENT.value
    )

    def __str__(self):
        """
        Retorno o objeto em formato de string.
        """

        return self.user.email

    class Meta:
        """
        Algumas informações adicionais.
        """

        db_table = "alma_user"
