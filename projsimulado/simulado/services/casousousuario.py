from simulado.models import Usuario
from django.core.exceptions import ValidationError

class UsuarioService:
    @staticmethod
    def criar_usuario(username, password, nome):
        """
        Cria um novo usuário com as informações fornecidas.
        """
        usuario = Usuario(username=username, password=password, nome=nome)

        usuario.set_password(password)

        try:
            usuario.full_clean()  # Valida os campos antes de salvar
        except ValidationError as e:
            raise e  # Propaga a exceção para ser tratada na view ou serviço superior
        
        usuario.save()
        return usuario