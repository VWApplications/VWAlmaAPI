from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)


class UserProfileManager(BaseUserManager):
    """
    O gerenciador de objetos é outra classe que podemos usar para ajudar a gerenciar
    os perfis de usuário que nos fornecerão algumas funcionalidades extras, como a
    criação de um usuário administrador ou a criação de um usuário comum.
    """

    def create_user(self, email, name, password=None):
        """
        Cria um usuário comum.
        """

        if not email:
            raise ValueError(_("Users must have an email address."))

        # Transforma o email e caixa baixa e será padronizado
        email = self.normalize_email(email)

        user = self.model(
            email=email,
            name=name
        )

        # Criptografa a senha.
        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """
        Cria um super usuário.
        """

        user = self.create_user(email, name, password)

        # Insere previlégios de superuser
        user.is_superuser = True
        user.is_staff = True
        user.is_teacher = True

        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Crie a base do perfil de usuário padrão do django e nos permita
    adicionar permissão ao nosso modelo de usuário.
    """

    email = models.EmailField(
        'email',
        help_text="E-mail que será usado como nome de usuário.",
        unique=True
    )

    identifier = models.CharField(
        "Mátricula",
        help_text="Identificador dentro de sua universidade",
        max_length=50,
        blank=True
    )

    name = models.CharField(
        'Nome',
        help_text="Nome completo do usuário.",
        max_length=150
    )

    photo = models.ImageField(
        upload_to='accounts',
        help_text="Foto do usuário",
        blank=True,
        null=True
    )

    is_teacher = models.BooleanField(
        'É professor?',
        help_text="Verifique se o usuário é professor ou aluno.",
        default=False
    )

    # Ao inves de deletar usuários, você pode desativa-los.
    is_active = models.BooleanField(
        'Está ativo?',
        help_text="Verifique se o usuário está ativo no sistema.",
        default=True
    )

    is_staff = models.BooleanField(
        'É administrador?',
        help_text="Transforma o usuário em um superuser.",
        default=False
    )

    created_at = models.DateTimeField(
        'Criado em',
        help_text="Data em que o usuário é criado.",
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        'Atualizado em',
        help_text="Data em que o usuário foi atualizado.",
        auto_now=True
    )

    # Gerenciador de querysets
    objects = UserProfileManager()

    # O campo que será usado para autenticação
    USERNAME_FIELD = 'email'

    # É uma lista de campos necessários para todos os usuários,
    # o USERNAME_FIELD não precisa ser passado.
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        """
        Retorno o objeto em formato de string.
        """

        return self.email

    @property
    def updated_at_formated(self):
        """
        Data de atualização
        """

        local_datetime = timezone.localtime(self.updated_at)

        return local_datetime.strftime("Atualizado %A, %d de %B de %Y às %H:%M")

    @property
    def full_name(self):
        """
        Pega o nome completo do usuário.
        """

        return self.name

    @property
    def short_name(self):
        """
        Pega o primeiro e último nome do usuário.
        """

        LAST_NAME = -1
        FIRST_NAME = 0

        if len(self.name.split(" ")) >= 2:
            return str(
                self.name.split(" ")[FIRST_NAME] +
                " " +
                self.name.split(" ")[LAST_NAME]
            )
        else:
            return str(self.name)

    class Meta:
        """
        Algumas informações adicionais.
        """

        db_table = "accounts"
        ordering = ('email',)