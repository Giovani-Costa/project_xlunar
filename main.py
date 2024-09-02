from bot import XLunarBot
from connect_database import criar_session
from key import key

session = criar_session()
token = key.get("token")
xlunar = XLunarBot(token=token, session=session)

xlunar.start()
