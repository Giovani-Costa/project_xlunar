from cassandra.cluster import Session
from interactions import Client, Intents, Status


class XLunarBot(Client):
    def __init__(self, *args, session: Session, **kwargs) -> None:
        intents = Intents.DEFAULT | Intents.GUILD_MESSAGES
        super().__init__(*args, intents=intents, **kwargs)
        self.session = session

    async def on_ready(self):
        await self.change_presence(
            activity="IFSP",
            status=Status.DO_NOT_DISTURB,
        )
        await self.load_extension("my_commands")
        print("XLunar se apresentando para o serviço @v@")
