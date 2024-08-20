import discord
import disnake.utils
import usuario
import disnake
from discord.ext.commands import Bot
from discord import Interaction
from questao import Questao
from disnake.ext import commands
from time import sleep

from connect_database import criar_session


xlunar = Bot(command_prefix="!", intents=discord.Intents.all())
session = criar_session()
CATEGORIA_ID_QUESTOES = 1273064071071137802


@xlunar.event
async def on_ready():
    await xlunar.tree.sync()
    await xlunar.change_presence(
        activity=discord.activity.Game(name="IFSP"),
        status=discord.Status.do_not_disturb,
    )
    print("XLunar se apresentando para o serviço @v@")


@xlunar.tree.command(name="teste", description="testeee")
async def teste(interaction: Interaction):
    await interaction.response.send_message(
        """funcionando :)""",
        ephemeral=True,
    )


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

    @discord.ui.button(label="A", style=discord.ButtonStyle.gray)
    async def botao_a(self, interaction: Interaction, button: discord.ui.Button):
        if self.ja_respondido:
            await interaction.response.send_message(
                "Você já respondeu essa questão!", ephemeral=True
            )
        else:
            self.ja_respondido = True
            esta_correto = self.questao.responder(0)
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
            await interaction.response.send_message(self._mensagem(esta_correto))


@xlunar.tree.command(
    name="questão", description="Manda uma questão aleatória do banco de dados"
)
async def questao(interaction: Interaction):
    discord_id = interaction.user.id
    questao = usuario.coletar_questao(session, discord_id)
    view = QuestaoView(timeout=180, questao=questao)
    embed = discord.Embed(
        title=f"Questão {questao.numero} ({questao.ano}.{questao.semestre} - {questao.materia})",
        description="",
        colour=discord.Colour.from_str("#ff5e8d"),
    )

    # embed.set_image(url=questao.imagem)
    embed.add_field(
        name="Enunciado",
        value=questao.enunciado,
        inline=False,
    )
    embed.add_field(
        name="Alternativas",
        value=f"\n\n".join(
            [
                f"{letra}) {alternativa}"
                for letra, alternativa in zip(
                    ["A", "B", "C", "D"], questao.alternativas
                )
            ]
        ),
        inline=False,
    )

    await interaction.response.send_message(embed=embed, view=view)
