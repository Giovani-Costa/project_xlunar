from questao import Questao
from random import choice

# class Usuario:
#     def __init__(
#         self,
#         discord_id: int,
#         nome_exibicao: str,
#         nome_usuario: str,
#         pontuacao: int,
#         questoes_acertadas: list[str],
#         questoes_erradas: list[str],
#     ) -> None:
#         self.discord_id = discord_id
#         self.nome_exibicao = nome_exibicao
#         self.nome_usuario = nome_usuario
#         self.pontuacao = pontuacao
#         self.questoes_acertadas = questoes_acertadas
#         self.questoes_erradas = questoes_erradas


def quantia_acertada() -> int:
    pass


def quantia_a_fazer() -> int:
    pass


def quantia_erradas() -> int:
    pass


def coletar_questao(session, discord_id: int) -> Questao:
    questoes_acertadas = (
        session.execute(
            f"SELECT questoes_acertadas FROM xlunar.usuarios WHERE discord_id = '{discord_id}' ALLOW FILTERING"
        )
        .one()
        .questoes_acertadas
    )
    if questoes_acertadas is None:
        questoes_acertadas = []
    tabela_id_questoes = session.execute("SELECT id FROM xlunar.questoes")
    id_questoes = [str(linha.id) for linha in tabela_id_questoes.all()]
    questoes_possiveis = id_questoes.copy()
    for questao_loop in questoes_acertadas:
        questoes_possiveis.remove(questao_loop)

    questao_escolhida = choice(questoes_possiveis)
    questao_db = session.execute(
        f"SELECT * FROM xlunar.questoes WHERE id={questao_escolhida} ALLOW FILTERING"
    ).one()
    questao = Questao(
        questao_db.enunciado,
        questao_db.alternativas,
        questao_db.alternativa_correta,
        questao_db.ano,
        questao_db.semestre,
        questao_db.materia,
        questao_db.numero,
        questao_db.imagem,
    )
    return questao


def registar(
    session, discord_id: int, nome_exibicao: str, nome_usuario: str, canal_id: int
) -> None:
    session.execute(
        f"""INSERT INTO xlunar.usuarios (id, discord_id, nome_exibicao, nome_usuario, pontuacao, questoes_acertadas, questoes_erradas, canal_id)
VALUES (uuid(), '{discord_id}', '{nome_exibicao}', '{nome_usuario}', 0, [], [], '{canal_id}');"""
    )


def ja_registrado(session, discord_id: int) -> bool:
    usuarios_registrados = session.execute("SELECT discord_id FROM xlunar.usuarios")
    usuarios_registrados = [
        int(linha.discord_id) for linha in usuarios_registrados.all()
    ]
    return discord_id in usuarios_registrados
