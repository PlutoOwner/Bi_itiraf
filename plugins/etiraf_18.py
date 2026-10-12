from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
    Message,
)
from config import Config
from plugins.dil import LAN
from plugins.etiraf_aciq import TIMEOUT_HATALARI, IPTAL_KELIMELERI
from plugins.start import Kullancı

# Telegram sınırları: açıklama 1024, metin 4096 karakter.
# Başlık (kullanıcı adı vb.) için pay bırakıldı.
MAKS_ACIKLAMA = 800
MAKS_METIN = 3500


def yas_onayli(user_id: int) -> bool:
    kayit = Kullancı.find_one({"user_id": user_id}, {"yas_onay": 1})
    return bool(kayit and kayit.get("yas_onay"))


def secim_butonlari():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text=LAN.BUTTON_OPEN, callback_data="etiraf18_aciq"),
                InlineKeyboardButton(text=LAN.BUTTON_ANON, callback_data="etiraf18_gizli"),
            ]
        ]
    )


async def itiraf18_al(bot: Client, chat_id: int):
    """Metin, fotoğraf veya video (açıklamalı ya da açıklamasız) kabul eder.
    Geçerli mesajı döndürür; iptal veya zaman aşımında None döndürür."""
    try:
        mesaj: Message = await bot.ask(chat_id, LAN.ITIRAF18_YAZ, timeout=300)
        while True:
            uzun_uyari = LAN.ITIRAF18_METIN_UZUN.format(MAKS_ACIKLAMA, MAKS_METIN)

            # Fotoğraf veya video (açıklama isteğe bağlı)
            if mesaj.photo or mesaj.video:
                if mesaj.caption and len(mesaj.caption) > MAKS_ACIKLAMA:
                    mesaj = await bot.ask(chat_id, uzun_uyari, timeout=120)
                    continue
                return mesaj

            # Sadece metin
            if mesaj.text:
                metin = mesaj.text.strip()
                if metin.lower() in IPTAL_KELIMELERI:
                    await mesaj.reply(LAN.ITIRAF_CANCEL)
                    return None
                if metin.startswith("/"):
                    mesaj = await bot.ask(chat_id, LAN.ITIRAF_YAZ_ZAMAN, timeout=30)
                    continue
                if len(metin) > MAKS_METIN:
                    mesaj = await bot.ask(chat_id, uzun_uyari, timeout=120)
                    continue
                return mesaj

            # Sticker, ses, belge vb.
            mesaj = await bot.ask(chat_id, LAN.ITIRAF18_DESTEKLENMEYEN, timeout=60)
    except TIMEOUT_HATALARI:
        await bot.send_message(chat_id, LAN.ITIRAF_ZAMAN_DOLDU)
        return None


def icerik_turu(mesaj: Message) -> str:
    if mesaj.photo:
        return "Fotoğraf + metin" if mesaj.caption else "Fotoğraf"
    if mesaj.video:
        return "Video + metin" if mesaj.caption else "Video"
    return "Metin"


@Client.on_callback_query(filters.regex("^etiraf18$"))
async def etiraf18_menu(bot: Client, query: CallbackQuery):
    if yas_onayli(query.from_user.id):
        await query.edit_message_caption(LAN.ITIRAF18_CHOOSE, reply_markup=secim_butonlari())
        return
    await query.edit_message_caption(
        LAN.YAS_ONAY,
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text=LAN.YAS_EVET, callback_data="yas_evet")],
                [InlineKeyboardButton(text=LAN.YAS_HAYIR, callback_data="yas_hayir")],
            ]
        ),
    )


@Client.on_callback_query(filters.regex("^yas_evet$"))
async def yas_evet(bot: Client, query: CallbackQuery):
    Kullancı.update_one(
        {"user_id": query.from_user.id},
        {"$set": {"user_id": query.from_user.id, "yas_onay": True}},
        upsert=True,
    )
    await query.edit_message_caption(LAN.ITIRAF18_CHOOSE, reply_markup=secim_butonlari())


@Client.on_callback_query(filters.regex("^yas_hayir$"))
async def yas_hayir(bot: Client, query: CallbackQuery):
    await query.edit_message_caption(LAN.YAS_RED, reply_markup=None)


@Client.on_callback_query(filters.regex("^etiraf18_(aciq|gizli)$"))
async def etiraf18_yaz(bot: Client, query: CallbackQuery):
    if not yas_onayli(query.from_user.id):
        await query.answer(LAN.YAS_GEREKLI, show_alert=True)
        return

    gizli = query.data.endswith("gizli")
    user = query.from_user
    chat_id = query.message.chat.id
    await query.message.delete()
    await bot.send_message(chat_id, LAN.ITIRAF18_KURALLAR)

    mesaj = await itiraf18_al(bot, chat_id)
    if mesaj is None:
        return

    tur = "Gizli" if gizli else "Açık"
    await bot.send_message(chat_id, LAN.ITIRAF18_GONDERILDI.format(tur, icerik_turu(mesaj)))

    # Kanala gidecek metin: başlık + (varsa) kullanıcının yazdığı metin
    baslik = LAN.ITIRAF18_ANON_BASLIK if gizli else LAN.ITIRAF18_OPEN_BASLIK.format(user.mention)
    kullanici_metni = mesaj.caption if (mesaj.photo or mesaj.video) else mesaj.text
    kanal_metni = baslik + (LAN.ITIRAF18_METIN_EK.format(kullanici_metni) if kullanici_metni else "")

    butonlar = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text=LAN.ITIRAF_GONDER, callback_data=f"onayla18 {user.id}"),
                InlineKeyboardButton(text=LAN.ITIRAF_SIL, callback_data=f"kapat {user.id}"),
            ]
        ]
    )

    # Adminler gizli itirafta da kimin gönderdiğini görür
    await bot.send_message(
        Config.LOG_ADMINS, text=LAN.ITIRAF18_ADMIN.format(user.mention, user.id)
    )
    if mesaj.photo:
        await bot.send_photo(
            Config.LOG_ADMINS, mesaj.photo.file_id, caption=kanal_metni, reply_markup=butonlar
        )
    elif mesaj.video:
        await bot.send_video(
            Config.LOG_ADMINS, mesaj.video.file_id, caption=kanal_metni, reply_markup=butonlar
        )
    else:
        await bot.send_message(Config.LOG_ADMINS, text=kanal_metni, reply_markup=butonlar)

    print(f"{user.first_name} +18 {tur.lower()} itiraf gönderdi ({icerik_turu(mesaj)})")