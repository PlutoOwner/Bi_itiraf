from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
    InputMediaAnimation,
)
from config import Config
from pymongo import MongoClient
from plugins.dil import LAN

mongo_client = MongoClient(Config.MONGO_URI)
db = mongo_client["Kozmikİtiraf"]
Kullancı = db["kullanıcılar"]


@Client.on_message(filters.command(["start"], ["/", "!"]))
async def start(_, msg: Message):
    await _.send_animation(
        chat_id=msg.chat.id,
        animation="https://te.legra.ph/file/2ec7302acc70ea68d7ad3.gif",
        caption=LAN.BOT_START.format(msg.from_user.mention),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text=LAN.BOT_ITIRAF_BUTTON_1, callback_data="etiraf_button"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=LAN.BOT_ITIRAF_BUTTON_2,
                        url=f"{Config.ITIRAF_18_LINK}",
                    ),
                    InlineKeyboardButton(
                        text=LAN.BOT_ITIRAF_BUTTON_3,
                        url=f"http://t.me/{Config.ITIRAF_CHANNEL}",
                    ),
                ],
            ]
        ),
    )
    await _.send_message(
        chat_id=Config.LOG_DATABASE,
        text=LAN.LOG_DATABASE.format(msg.from_user.first_name),
    )
    Kullancı.update_one(
        {"user_id": msg.from_user.id},
        {
            "$set": {
                "user_id": msg.from_user.id,
                "first_name": msg.from_user.mention,
                "username": msg.from_user.username,
            }
        },
        upsert=True,
    )
    print(f"{msg.from_user.first_name} start etti")


@Client.on_callback_query(filters.regex("^etiraf_button$"))
async def cb_info(bot: Client, query: CallbackQuery):
    butonlar = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text=LAN.BUTTON_OPEN, callback_data="etiraf_aciq"),
                InlineKeyboardButton(text=LAN.BUTTON_ANON, callback_data="etiraf_gizli"),
            ],
            [InlineKeyboardButton(text=LAN.BUTTON_18, callback_data="etiraf18")],
        ]
    )
    await query.edit_message_media(
        media=InputMediaAnimation("https://te.legra.ph/file/796e259cd8d37c4f85d32.gif"),
        reply_markup=butonlar,
    )
    await query.edit_message_caption(caption=LAN.ITIRAF_CHOOSE, reply_markup=butonlar)


@Client.on_callback_query(filters.regex(r"^kapat \d+$"))
async def _reddetme(bot: Client, query: CallbackQuery):
    user_id = int(query.data.split()[1])

    # Önce butonları kaldır (kopyada da buton olmasın, tekrar basılamasın)
    await query.edit_message_reply_markup(None)

    await bot.send_message(
        Config.LOG_SILINMIS, text=LAN.ITIRAF_SILINDI.format(query.from_user.mention)
    )
    # copy_message metin, fotoğraf ve video için aynı şekilde çalışır
    await bot.copy_message(
        chat_id=Config.LOG_SILINMIS,
        from_chat_id=query.message.chat.id,
        message_id=query.message.id,
    )
    await query.message.reply(LAN.ITIRAF_SILINDI_ADMINS.format(query.from_user.mention))
    await query.answer()

    try:
        await bot.send_message(user_id, text=LAN.ITIRAF_KABUL_EDILMEDI)
    except Exception as e:
        print(f"Red bildirimi {user_id} kullanıcısına gönderilemedi: {e}")