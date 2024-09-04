from time import sleep

import discord
import disnake
import disnake.utils
import pandas as pd
from discord import Interaction
from discord.ext.commands import Bot
from disnake.ext import commands

import usuario
from connect_database import criar_session
from questao import Questao

xlunar = Bot(command_prefix="!", intents=discord.Intents.all())
session = criar_session()
CATEGORIA_ID_QUESTOES = 1273064071071137802
KEYSPACE = "xlunar"


@xlunar.event
async def on_ready():
    await xlunar.tree.sync()
    await xlunar.change_presence(
        activity=discord.activity.Game(name="IFSP"),
        status=discord.Status.do_not_disturb,
    )
    print("XLunar se apresentando para o serviço @v@")


@xlunar.tree.command(
    name="registrar", description="Registra um usuário no banco de dados"
)
async def registrar(interaction: Interaction):
    usuario_registro = interaction.user
    discord_id = interaction.user.id
    nome_exibicao = interaction.user.display_name
    nome_usuario = interaction.user.name
    if not usuario.ja_registrado(session, discord_id):
        categoria_questao = disnake.utils.get(
            interaction.guild.categories, id=CATEGORIA_ID_QUESTOES
        )
        canal_do_usuario = await interaction.guild.create_text_channel(
            f"Chat de {interaction.user.display_name}",
            category=categoria_questao,
        )
        usuario.registar(
            session, discord_id, nome_exibicao, nome_usuario, canal_do_usuario.id
        )
        await canal_do_usuario.set_permissions(
            usuario_registro,
            view_channel=True,
            manage_channels=True,
            manage_permissions=True,
        )
        mensagem = f":white_check_mark:  **{nome_exibicao} foi registrado com sucesso!** Para você usar o XLunar com a melhor experiência possível, criamos um chat privado para você fazer suas anotações e resolver suas questões sozinho(a) ou com a companhia de alguém. Caso queira que alguém entre em seu chat, basta dar a permissão nas configurações do chat. Não recomendamos que mecha nas permissões já estabelecidas. Você pode customizar o nome do seu chat para ficar com você deseja, apenas não desrespeito nenhuma regra do servidor <#{canal_do_usuario.id}> :white_check_mark:"
    else:
        mensagem = f":x:  Não foi possível registrar: {nome_exibicao}. Verifique se esse usuário já não foi registrado. Se estiver encontrando problemas para registrar, crie um ticket e peça ajuda para um ADM. Para criar um ticket, use o comando /ticket.  :x:"

    await interaction.response.send_message(
        mensagem,
        ephemeral=True,
    )


@xlunar.tree.command(
    name="ticket",
    description="Cria um chat para você ter uma conversa direta com um dos ADMs",
)
async def ticket(interaction: Interaction):
    member = disnake.utils.find(
        lambda m: m.id == interaction.id, interaction.guild.members
    )
    role = interaction.guild.get_role(1196836175063814156)
    categoria_ticket = disnake.utils.get(
        interaction.guild.categories, id=1196836176926093364
    )
    canal_ticket = await interaction.guild.create_text_channel(
        f"Ticket de {interaction.user.display_name}",
        category=categoria_ticket,
    )
    await canal_ticket.set_permissions(member, view_channel=True)
    await interaction.response.send_message(
        f"Seu ticket foi criado com sucesso! Clique aqui <#{canal_ticket.id}>"
    )
    await canal_ticket.send(
        "Esse é o seu ticket. Faça sua pergunta e espere um ADM responder"
    )


class QuestaoView(discord.ui.View):
    def __init__(self, *, timeout: float | None = 180, questao: Questao):
        super().__init__(timeout=timeout)
        self.ja_respondido = False
        self.questao = questao

    @staticmethod
    def _mensagem(esta_correto: bool) -> str:
        if esta_correto:
            return "Está correto"
        else:
            return "Está errado"

    @staticmethod
    def _enviar(esta_correto: bool, discord_id: int, questao_id: str) -> None:
        _set_fazendo_questao(discord_id, False)
        if esta_correto:
            usuario.enviar_para_acertadas(session, discord_id, questao_id)
        else:
            usuario.enviar_para_erradas(session, discord_id, questao_id)

    @discord.ui.button(label="A", style=discord.ButtonStyle.gray)
    async def botao_a(self, interaction: Interaction, button: discord.ui.Button):
        if self.ja_respondido:
            await interaction.response.send_message(
                "Você já respondeu essa questão!", ephemeral=True
            )
        else:
            self.ja_respondido = True
            esta_correto = self.questao.responder(0)
            self._enviar(esta_correto, interaction.user.id, self.questao.id)
            await interaction.response.send_message(self._mensagem(esta_correto))

    @discord.ui.button(label="B", style=discord.ButtonStyle.gray)
    async def botao_b(self, interaction: Interaction, button: discord.ui.Button):
        if self.ja_respondido:
            await interaction.response.send_message(
                "Você já respondeu essa questão!", ephemeral=True
            )
        else:
            self.ja_respondido = True
            esta_correto = self.questao.responder(1)
            self._enviar(esta_correto, interaction.user.id, self.questao.id)
            await interaction.response.send_message(self._mensagem(esta_correto))

    @discord.ui.button(label="C", style=discord.ButtonStyle.gray)
    async def botao_c(self, interaction: Interaction, button: discord.ui.Button):
        if self.ja_respondido:
            await interaction.response.send_message(
                "Você já respondeu essa questão!", ephemeral=True
            )
        else:
            self.ja_respondido = True
            esta_correto = self.questao.responder(2)
            self._enviar(esta_correto, interaction.user.id, self.questao.id)
            await interaction.response.send_message(self._mensagem(esta_correto))

    @discord.ui.button(label="D", style=discord.ButtonStyle.gray)
    async def botao_d(self, interaction: Interaction, button: discord.ui.Button):
        if self.ja_respondido:
            await interaction.response.send_message(
                "Você já respondeu essa questão!", ephemeral=True
            )
        else:
            self.ja_respondido = True
            esta_correto = self.questao.responder(3)
            self._enviar(esta_correto, interaction.user.id, self.questao.id)
            await interaction.response.send_message(self._mensagem(esta_correto))


def _selecionar_canal_id(discord_id: int) -> int:
    canal_id = (
        session.execute(
            f"SELECT canal_id FROM {KEYSPACE}.usuarios WHERE discord_id='{discord_id}' ALLOW FILTERING"
        )
        .one()
        .canal_id
    )
    return int(canal_id)


def _selecionar_db_id(discord_id: int) -> str:
    db_id = (
        session.execute(
            f"SELECT id FROM {KEYSPACE}.usuarios WHERE discord_id='{discord_id}' ALLOW FILTERING"
        )
        .one()
        .id
    )
    return str(db_id)


def _set_fazendo_questao(discord_id: int, valor: bool):
    db_id = _selecionar_db_id(discord_id)
    session.execute(
        f"UPDATE {KEYSPACE}.usuarios SET fazendo_questao = {str(valor).lower()} WHERE id = {db_id}"
    )


def _get_fazendo_questao(discord_id: int) -> bool:
    fazendo_questao = (
        session.execute(
            f"SELECT fazendo_questao FROM {KEYSPACE}.usuarios WHERE discord_id = '{discord_id}' ALLOW FILTERING"
        )
        .one()
        .fazendo_questao
    )
    return fazendo_questao


@xlunar.tree.command(
    name="questão", description="Manda uma questão aleatória do banco de dados"
)
async def questao(interaction: Interaction):
    discord_id = interaction.user.id
    canal_id_usuario = _selecionar_canal_id(discord_id)
    canal_id_atual = interaction.channel_id
    if canal_id_atual != canal_id_usuario:
        await interaction.response.send_message(
            "Você só pode chamar esse comando em seu canal privado", ephemeral=True
        )
        return
    if _get_fazendo_questao(discord_id):
        await interaction.response.send_message(
            "Termine a questão que você iniciou", ephemeral=True
        )
        return
    _set_fazendo_questao(discord_id, True)
    questao = usuario.coletar_questao(session, discord_id)
    view = QuestaoView(timeout=180, questao=questao)
    embed = discord.Embed(
        title=f"Questão {questao.numero} ({questao.ano}.{questao.semestre} - {questao.materia})",
        description="",
        colour=discord.Colour.from_str("#ff5e8d"),
    )
    if questao.imagem != "None":
        embed.set_image(url=questao.imagem)
    questao_separada = [
        questao.enunciado[i : i + 1024] for i in range(0, len(questao.enunciado), 1024)
    ]
    embed.add_field(
        name="Enunciado",
        value=questao_separada[0],
        inline=False,
    )
    if len(questao_separada) > 1:
        for pedaco in questao_separada[1:]:
            embed.add_field(name="", value=pedaco, inline=False)

    embed.add_field(
        name="Alternativas",
        value=f"A) {questao.alternativas[0]}",
        inline=False,
    )
    embed.add_field(
        name="",
        value=f"B) {questao.alternativas[1]}",
        inline=False,
    )
    embed.add_field(
        name="",
        value=f"C) {questao.alternativas[2]}",
        inline=False,
    )
    embed.add_field(
        name="",
        value=f"D) {questao.alternativas[3]}",
        inline=False,
    )

    await interaction.response.send_message(embed=embed, view=view)


class PaginaDoRank(discord.ui.View):
    def __init__(
        self,
        usuarios: pd.DataFrame,
        pagina_atual: int = 0,
        *,
        timeout: float | None = 180,
    ):
        super().__init__(timeout=timeout)
        self.pagina_atual = pagina_atual
        self.usuarios = usuarios

    async def send(self, interaction: Interaction):
        await interaction.response.send_message(view=self)

    @discord.ui.button(label=">", style=discord.ButtonStyle.gray)
    async def botao_proximo(self, interaction: Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.pagina_atual += 1
        await self.atulizar_mensagem(interaction)

    @discord.ui.button(label="<", style=discord.ButtonStyle.gray)
    async def botao_anterior(self, interaction: Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.pagina_atual -= 1
        await self.atulizar_mensagem(interaction)

    @discord.ui.button(label="<<", style=discord.ButtonStyle.gray)
    async def botao_primeiro(self, interaction: Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.pagina_atual = 0
        await self.atulizar_mensagem(interaction)

    @discord.ui.button(label=">>", style=discord.ButtonStyle.gray)
    async def botao_ultimo(self, interaction: Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.pagina_atual = 9
        await self.atulizar_mensagem(interaction)

    def criar_embed(self) -> discord.Embed:
        embed = discord.Embed(title="NOME DO USUARIO")
        embed.add_field(
            name="Nome", value=f"{self.usuarios.at[self.pagina_atual, 'nome_exibicao']}"
        )
        embed.add_field(
            name="Pontuação",
            value=f"{self.usuarios.at[self.pagina_atual, 'pontuacao']}",
            inline=False,
        )
        return embed

    async def atulizar_mensagem(self, interaction: Interaction):
        embed = self.criar_embed()
        await interaction.edit_original_response(embed=embed, view=self)


@xlunar.tree.command(
    name="rank",
    description="rank",
)
async def rank(interaction: Interaction):
    tabela_usuarios = session.execute(
        f"SELECT nome_exibicao, pontuacao FROM {KEYSPACE}.usuarios"
    )
    dados = [
        {"nome_exibicao": linha.nome_exibicao, "pontuacao": linha.pontuacao}
        for linha in tabela_usuarios.all()
    ]
    tabela_rank = pd.DataFrame(dados)
    ordenada = tabela_rank.sort_values(by="pontuacao", ascending=False).reset_index(
        drop=True
    )
    view = PaginaDoRank(ordenada)
    view.send(interaction)
    await interaction.response.send_message(view=view)
