from config import Config
from pyrogram import Client, idle
from pyromod import listen  # noqa: F401  (bot.ask için gerekli)
import logging
logging.basicConfig(level=logging.INFO)

# Not: Eskiden oturum adı ":memory:" idi. Pyrogram 2.x bunu dosya adı sanıyor
# ve Windows'ta ":" karakteri dosya adında kullanılamadığı için
# "unable to open database file" hatası veriyordu.
# Artık oturum, proje klasöründe "itirafbot.session" dosyasında tutuluyor.
app = Client(
    "itirafbot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    plugins=dict(root="plugins"),
)

if __name__ == "__main__":
    app.start()
    uname = app.get_me().username
    print(f"@{uname} başladı!")
    idle()
    app.stop()
    print("Bot durdu!")