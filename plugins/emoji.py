"""
Premium (özel) emoji sistemi.

Nasıl kullanılır:
1. config.py içine  PREMIUM_EMOJI = True  ekleyin.
   (Bot, Telegram Premium aboneliği olan bir hesapla oluşturulmuş olmalı.)
2. Bota özel mesajdan premium emoji içeren bir mesaj gönderin, o mesajı
   /emojiid komutuyla yanıtlayın. Bot her emojinin ID'sini verir.
3. Aşağıdaki EMOJILER sözlüğünde ilgili satırdaki 0 yerine o ID'yi yazın.
4. /emojiler komutuyla hepsinin nasıl göründüğünü kontrol edin.

ID'si 0 olan veya PREMIUM_EMOJI kapalıyken her emoji normal emoji olarak gösterilir.
Kanala giden mesajlarda ve butonlarda premium emoji kullanılmaz
(Telegram, NFT kullanıcı adı olmayan botlara buna izin vermiyor).
"""
from pyrogram import Client, filters
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message
from config import Config

PREMIUM = getattr(Config, "PREMIUM_EMOJI", True)

# ad: (normal emoji, premium emoji ID'si)
EMOJILER = {
    "selam":     ("👋", 5458904472598095631),
    "bilgi":     ("ℹ️", 5895252942050561938),
    "el":        ("💁", 4967539812841031265),
    "duyuru":    ("📣", 5424818078833715060),
    "tamam":     ("✅", 5260463209562776385),
    "zil":       ("🔔", 5458603043203327669),
    "uyari":     ("⚠️", 5447644880824181073),
    "kum_saati": ("⌛", 5852614259082530343),
    "yasak":     ("🚫", 5240241223632954241),
    "asagi":     ("🔽", 5406745015365943482),
    "cop":       ("🗑",  5445267414562389170),
    "yas":       ("🔞", 5215203655946346044),
    "kurallar":  ("📜", 5956561916573782596),
    "iptal":     ("❌", 5273914604752216432),
}


def e(ad: str) -> str:
    """Emoji adını mesajda kullanılacak metne çevirir."""
    emoji, emoji_id = EMOJILER[ad]
    if PREMIUM and emoji_id:
        return f'<emoji id="{emoji_id}">{emoji}</emoji>'
    return emoji


def _utf16_parca(metin: str, offset: int, uzunluk: int) -> str:
    # Telegram konumları UTF-16 birimiyle verir
    b = metin.encode("utf-16-le")
    return b[offset * 2:(offset + uzunluk) * 2].decode("utf-16-le")


@Client.on_message(filters.command(["emojiid"]) & filters.user(Config.OWNER))
async def emoji_id_bul(client: Client, message: Message):
    hedef = message.reply_to_message
    if not hedef:
        await message.reply("Premium emoji içeren bir mesajı /emojiid ile yanıtlayın.")
        return

    metin = hedef.text or hedef.caption or ""
    varliklar = hedef.entities or hedef.caption_entities or []
    satirlar = []
    for v in varliklar:
        if v.type == MessageEntityType.CUSTOM_EMOJI:
            karakter = _utf16_parca(metin, v.offset, v.length)
            satirlar.append(f"{karakter}  <code>{v.custom_emoji_id}</code>")

    if not satirlar:
        await message.reply(
            "Bu mesajda premium emoji bulunamadı.\n"
            "Not: Emojiyi gönderen hesabın da Premium olması gerekir."
        )
        return
    await message.reply("🆔 Premium emoji ID'leri:\n\n" + "\n".join(satirlar))


@Client.on_message(filters.command(["emojiler"]) & filters.user(Config.OWNER))
async def emoji_listesi(client: Client, message: Message):
    durum = "açık" if PREMIUM else "kapalı (config.py → PREMIUM_EMOJI = True)"
    satirlar = [f"⚙️ Premium emoji: {durum}\n"]
    for ad, (emoji, emoji_id) in EMOJILER.items():
        isaret = "" if emoji_id else "  (ID yok)"
        satirlar.append(f"{e(ad)}  <code>{ad}</code>{isaret}")
    await message.reply("\n".join(satirlar))