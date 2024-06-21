from organizador import Organanizador
from questao import Questao


class Usuario:
    def __init__(
        self,
        nome_exibicao: str,
        nome_usuario: str,
        organizador_de_questoes: Organanizador,
    ) -> None:
        self.nome_exibicao = nome_exibicao
        self.nome_usuario = nome_usuario
        self.organizador_de_questoes = organizador_de_questoes

    def quantia_acertada(self) -> int:
        return self.organizador_de_questoes.quantia_acertada()

    def quantia_a_fazer(self) -> int:
        return self.organizador_de_questoes.quantia_a_fazer()

    def quantia_erradas(self) -> int:
        return self.organizador_de_questoes.quantia_erradas()

    def coletar_questao(self) -> Questao:
        return self.organizador_de_questoes.coletar_questao()

    def registar(self) -> None:
        pass
