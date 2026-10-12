from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config
from plugins.dil import LAN


@Client.on_callback_query(filters.regex(r"^onayla(18)? \d+$"))
async def _onaylama(bot: Client, query):
    komut, uid = query.data.split()
    user_id = int(uid)
    yetiskin = komut == "onayla18"

    kanal = Config.ETIRAF_CHANNEL_18 if yetiskin else Config.ETIRAF_CHANNEL
    kabul_metni = LAN.ITIRAF18_ACCEPT if yetiskin else LAN.ITIRAF_ACCEPT

    # copy_message metin, fotoğraf ve videoyu aynı şekilde kopyalar,
    # biçimlendirmeyi (mention linki vb.) de korur
    await bot.copy_message(
        chat_id=kanal,
        from_chat_id=query.message.chat.id,
        message_id=query.message.id,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text=LAN.ITIRAF_CHANNEL_TEXT_BUTTON,
                        url=f"https://t.me/{Config.BOT_USERNAME}",
                    )
                ]
            ]
        ),
    )

    # Butonları kaldır (tekrar onaylanamasın), sonucu yanıt olarak yaz
    await query.edit_message_reply_markup(None)
    await query.message.reply(f"{kabul_metni} ({query.from_user.mention})")
    await query.answer(kabul_metni)

    if yetiskin:
        link = getattr(Config, "ITIRAF_18_LINK", None)
        buton_metni = LAN.ITIRAF18_CHANNEL_TEXT
    else:
        link = f"https://t.me/{Config.ITIRAF_CHANNEL}"
        buton_metni = LAN.ITIRAF_CHANNEL_TEXT
    markup = (
        InlineKeyboardMarkup([[InlineKeyboardButton(text=buton_metni, url=link)]])
        if link
        else None
    )

    try:
        await bot.send_message(user_id, text=LAN.ITIRAF_OPEN_ACCEPT, reply_markup=markup)
    except Exception as e:
        print(f"Onay bildirimi {user_id} kullanıcısına gönderilemedi: {e}")