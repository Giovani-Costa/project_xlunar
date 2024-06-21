import random
from questao import Questao


class Organanizador:
    def __init__(
        self,
        questoes_acertadas: list[Questao],
        questoes_a_fazer: list[Questao],
        questoes_erradas: list[Questao],
    ) -> None:
        self.questoes_acertadas = questoes_acertadas
        self.questoes_a_fazer = questoes_a_fazer
        self.questoes_erradas = questoes_erradas

    def quantia_acertada(self) -> int:
        return len(self.questoes_acertadas)

    def quantia_a_fazer(self) -> int:
        return len(self.questoes_a_fazer)

    def quantia_erradas(self) -> int:
        return len(self.questoes_erradas)

    def coletar_questao(self) -> Questao:
        return self.questoes_a_fazer[random.randrange(self.quantia_a_fazer())]

    def enviar_para_acertados(self, questao: Questao) -> None:
        self.questoes_acertadas.append(questao)

    def enviar_para_errados(self, questao: Questao) -> None:
        self.questoes_erradas.append(questao)
