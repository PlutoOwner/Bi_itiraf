from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)
from config import Config
from plugins.dil import LAN
from plugins.etiraf_aciq import itiraf_metni_al


@Client.on_callback_query(filters.regex("^etiraf_gizli$"))
async def etiraf_gizli(bot: Client, query: CallbackQuery):
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
        # Düzeltme: önceden burada itiraf yerine kullanıcı ID'si gösteriliyordu
        text=LAN.ITIRAF_GONDERILDI_ANON.format(query.from_user.mention, itiraf),
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
        text=LAN.ITIRAF_GONDERILDI_ADMIN_ANON.format(
            query.from_user.mention, query.from_user.id
        ),
    )
    await bot.send_message(
        Config.LOG_ADMINS,
        text=LAN.ITIRAF_GONDERILDI_ANON_MESAJ.format(itiraf),
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
    print(f"{query.from_user.first_name} gizli itiraf yazdı")