import asyncio

from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)
from config import Config
from plugins.dil import LAN

# pyromod 1.5 -> asyncio.TimeoutError, pyromod 2.x -> ListenerTimeout
try:
    from pyromod.exceptions import ListenerTimeout
    TIMEOUT_HATALARI = (asyncio.TimeoutError, ListenerTimeout)
except ImportError:
    TIMEOUT_HATALARI = (asyncio.TimeoutError,)

IPTAL_KELIMELERI = ("iptal", "cancel")


async def itiraf_metni_al(bot: Client, chat_id: int):
    """Kullanıcıdan geçerli bir itiraf metni ister.
    Metni döndürür; iptal veya zaman aşımında None döndürür."""
    try:
        mesaj = await bot.ask(chat_id, LAN.ITIRAF_YAZ, timeout=300)
        while True:
            # Fotoğraf, sticker vb. -> text None olur
            if not mesaj.text:
                mesaj = await bot.ask(chat_id, LAN.ITIRAF_SADECE_METIN, timeout=60)
                continue
            if mesaj.text.startswith("/"):
                mesaj = await bot.ask(chat_id, LAN.ITIRAF_YAZ_ZAMAN, timeout=30)
                continue
            if mesaj.text.strip().lower() in IPTAL_KELIMELERI:
                await mesaj.reply(LAN.ITIRAF_CANCEL)
                return None
            return mesaj.text
    except TIMEOUT_HATALARI:
        await bot.send_message(chat_id, LAN.ITIRAF_ZAMAN_DOLDU)
        return None


@Client.on_callback_query(filters.regex("^etiraf_aciq$"))
async def etiraf_aciq(bot: Client, query: CallbackQuery):
    chat_id = query.message.chat.id
    await query.message.delete()
    await bot.send_animation(
        chat_id, animation="https://te.legra.ph/file/90eb83c88e4b5b93d2d69.gif"
    )

    itiraf = await itiraf_metni_al(bot, chat_id)
    if itiraf is None:
        return

    await bot.send_message(
        chat_id,
        text=LAN.ITIRAF_GONDERILDI.format(query.from_user.mention, itiraf),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text=LAN.ITIRAF_CHANNEL_TEXT,
                        url=f"https://t.me/{Config.ITIRAF_CHANNEL}",
                    )
                ]
            ]
        ),
    )
    await bot.send_message(
        Config.LOG_ADMINS,
        text=LAN.ITIRAF_GONDERILDI_ADMIN_OPEN.format(
            query.from_user.mention, query.from_user.id
        ),
    )
    await bot.send_message(
        Config.LOG_ADMINS,
        text=LAN.ITIRAF_GONDERILDI_OPEN_MESAJ.format(query.from_user.mention, itiraf),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text=LAN.ITIRAF_GONDER,
                        callback_data=f"onayla {query.from_user.id}",
                    ),
                    InlineKeyboardButton(
                        text=LAN.ITIRAF_SIL,
                        callback_data=f"kapat {query.from_user.id}",
                    ),
                ]
            ]
        ),
    )
    print(f"{query.from_user.first_name} açık itiraf yazdı")