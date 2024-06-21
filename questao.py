from typing import Optional


class Questao:
    def __init__(
        self,
        enunciado: str,
        alternativas: list[str],
        alternativa_correta: int,
        ano: int,
        semestre: int,
        materia: str,
        numero: int,
        imagem: Optional[str] = None,
    ) -> None:
        self.enunciado = enunciado
        self.alternativas = alternativas
        self.alternativas_correta = alternativa_correta
        self.ano = ano
        self.semestre = semestre
        self.materia = materia
        self.numero = numero
        self.imagem = imagem

    def responder(self, alternativa: int) -> bool:
        return alternativa == self.alternativas_correta
