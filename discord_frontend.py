import discord
from discord.ext.commands import Bot
from discord import Interaction
from questao import Questao
from time import sleep

xlunar = Bot(command_prefix="!", intents=discord.Intents.all())


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
    await interaction.response.send_message(
        "Trabaiano nisso :)",
        ephemeral=True,
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
    questao = Questao(
        enunciado="Leia a tira e responda à questão. O pai de Mafalda reage com ironia ao “mundo doente” da filha. Entretanto, ocorre ruptura abrupta em sua opinião:",
        alternativas=[
            """Tragédia (texto 1).,
Deslizamentos (texto 1).,
Atingida (texto 2).,
Grande volume de chuva (texto 2)."""
        ],
        alternativa_correta=0,
        ano=2022,
        semestre=2,
        materia="Português",
        numero=8,
        imagem="https://cdn.discordapp.com/attachments/1197686074164662372/1212918467787751424/image.png?ex=662a4b99&is=6628fa19&hm=7bbe8764fff93ac41a8c659c94537d61b56ec4d519ce7903f3950ea0443373a7&",
    )
    view = QuestaoView(timeout=180, questao=questao)
    embed = discord.Embed(
        title=f"Questão {questao.numero} ({questao.ano}.{questao.semestre} - {questao.materia})",
        description="",
        colour=discord.Colour.from_str("#ff5e8d"),
    )

    embed.set_image(url=questao.imagem)
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
