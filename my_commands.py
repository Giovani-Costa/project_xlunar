import pandas as pd
from discord.ext import commands
from interactions import SlashContext, slash_command

from bot import XLunarBot


class MyCommands(commands.Cog):
    def __init__(self, bot: XLunarBot):
        self.bot = bot

    @slash_command(name="hi")
    async def hi(self, ctx: SlashContext):
        tabela_usuarios = self.bot.session.execute(
            "SELECT nome_exibicao, pontuacao FROM test_discord_bot.usuarios"
        )
        dados = [
            {"nome_exibicao": linha.nome_exibicao, "pontuacao": linha.pontuacao}
            for linha in tabela_usuarios.all()
        ]
        tabela_rank = pd.DataFrame(dados)
        ordenada = tabela_rank.sort_values(by="pontuacao", ascending=False)
        top_10 = ordenada["nome_exibicao"].head(10).to_list()
        await ctx.send(f"{top_10}", ephemeral=True)

    # ... Your other commands ...


async def setup(bot: XLunarBot):
    await bot.add_cog(MyCommands(bot))
