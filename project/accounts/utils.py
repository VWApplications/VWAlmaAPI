import hashlib
import string
import random


def random_key(size=5):
    """
    Gera a chave com caracteres randomicos
    """

    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for x in range(size))


def generate_hash_key(info, random_str_size=5):
    """
    Função para gerar a chave de hash a partir de uma informação do usuário.
    """

    random_str = random_key(random_str_size)
    text = random_str + info
    return hashlib.sha224(text.encode('utf-8')).hexdigest()