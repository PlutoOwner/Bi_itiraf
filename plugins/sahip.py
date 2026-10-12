import asyncio
import os
from pyrogram import Client, filters
from pyrogram.types import Message
from config import Config
from plugins.start import Kullancı

@Client.on_message(filters.command(["stat"]) & filters.user(Config.OWNER))
async def stat(client: Client, message: Message):
    user_count = Kullancı.count_documents({})
    await message.reply(f"📊 **İstatistikler**\n\n👤 **Kullanıcı Sayısı:** `{user_count}``")
    
    
    
    


@Client.on_message(filters.command(["duyuru"]) & filters.user(Config.OWNER))
async def duyuru(client: Client, message: Message):
    if not message.reply_to_message:
        await message.reply("Lütfen bir mesajı yanıtlayarak komutu kullanın.")
        return

    duyuru_mesaji = message.reply_to_message
    mesaj_id = duyuru_mesaji.id  # 💥 DÜZGÜN ATTRİBUTE BU!

    basarili = []
    basarisiz = []

    for user in Kullancı.find({}):
        user_id = user["user_id"]
        first_name = user.get("first_name", "Adsız")
        username = user.get("username")
        name_line = f"{first_name}"
        if username:
            name_line += f" (@{username})"
        name_line += f" [{user_id}]"

        try:
            await client.forward_messages(
                chat_id=user_id,
                from_chat_id=message.chat.id,
                message_ids=mesaj_id
            )
            basarili.append(f"- {name_line}")
            await asyncio.sleep(0.1)
        except Exception as e:
            basarisiz.append(f"- {name_line} → {str(e)}")

    log_text = f"✅ Başarılı Gönderimler ({len(basarili)}):\n"
    log_text += "\n".join(basarili) if basarili else "Yok\n"
    log_text += f"\n\n❌ Başarısız Gönderimler ({len(basarisiz)}):\n"
    log_text += "\n".join(basarisiz) if basarisiz else "Yok"

    log_file_path = "duyuru_log.txt"
    with open(log_file_path, "w", encoding="utf-8") as f:
        f.write(log_text)

    await message.reply(f"📤 Duyuru tamamlandı!\n\n✅ Gönderilen: {len(basarili)} kişi\n❌ Gönderilemeyen: {len(basarisiz)} kişi")
    await message.reply_document(log_file_path, caption="📄 Gönderim Raporu")
    os.remove(log_file_path)
