from plugins.emoji import e

# Not: Premium emoji (e(...)) yalnızca özel mesajlarda ve admin grubunda kullanılır.
# Buton yazıları, bildirim pencereleri (query.answer) ve kanala giden metinler
# normal emoji ile kalmalı; oralarda premium emoji çalışmaz.


class LAN:
    BOT_START = f"{e('selam')} Merhaba {{}}\n{e('bilgi')} Ben bir itiraf robotuyum\n{e('el')} Aşağıdaki ``İtiraf et`` düğmesine tıklayarak itirafta bulunun"
    BOT_ITIRAF_BUTTON_1 = "İtiraf et"
    BOT_ITIRAF_BUTTON_2 = "📣 +18 İtiraf Kanalımız"
    BOT_ITIRAF_BUTTON_3 = "📣 İtiraf Kanalımız"
    LOG_DATABASE = "[LOG] {} botu başlattı"
    BUTTON_OPEN = "Açık itiraf"
    BUTTON_ANON = "Gizli İtiraf"
    ITIRAF_SILINDI = f"{e('asagi')} Aşağıdaki itiraf {{}} tarafından silindi {e('asagi')}"
    ITIRAF_SILINDI_ADMINS = f"{e('cop')} İtiraf {{}} tarafından silindi"
    ITIRAF_KABUL_EDILMEDI = f"{e('zil')} İtirafınız kabul edilmedi."
    ITIRAF_CHOOSE = f"{e('el')} Nasıl itiraf edeceksiniz?"
    ITIRAF_CHANNEL_TEXT = "📣 İtiraf Kanalımız"
    # ONAYLA (query.answer'da da kullanıldığı için düz emoji)
    ITIRAF_ACCEPT = "✅ İtiraf kanalına gönderildi"
    ITIRAF_OPEN_ACCEPT = f"{e('zil')} İtirafınız kabul edilmiştir."
    ITIRAF_CHANNEL_TEXT_BUTTON = "💭 Kendi itirafını yaz"
    # OPEN VE ANON
    ITIRAF_YAZ = f"{e('duyuru')} İtirafınızı yazın:\nİptal etmek için `iptal` yazın."
    ITIRAF_YAZ_ZAMAN = "Komut göndermeyin, 30 saniye içinde itirafınızı yazın."
    ITIRAF_SADECE_METIN = f"{e('uyari')} Lütfen itirafınızı sadece metin olarak yazın.\nİptal etmek için `iptal` yazın."
    ITIRAF_ZAMAN_DOLDU = f"{e('kum_saati')} Süre doldu, itiraf iptal edildi. Tekrar denemek için /start yazın."
    ITIRAF_CANCEL = f"{e('iptal')} İtiraf iptal edildi."
    ITIRAF_GONDERILDI = f"{e('tamam')} İtiraf bize ulaştı. Onaylandıktan sonra kanala gönderilecektir.\n\nKullanıcı: {{}}\nİtiraf türü: Açık\nİtiraf mesajı: {{}}"
    ITIRAF_GONDERILDI_ADMIN_OPEN = f"Kullanıcı: {{}}\nKullanıcı İD: {{}}\n\n{e('asagi')} Kanalın mesajı otomatik olarak aşağıya yazıldı. {e('asagi')}"
    # Kanala kopyalanan mesaj -> düz emoji
    ITIRAF_GONDERILDI_OPEN_MESAJ = (
        "📣 İtiraf türü: Açık\n🕵️ İtiraf eden: {}\n\n💬 İtiraf mesajı: {}"
    )
    ITIRAF_GONDER = "✅ Onayla"
    ITIRAF_SIL = "🗑 Sil"
    ITIRAF_GONDERILDI_ANON = f"{e('tamam')} İtiraf bize ulaştı. Onaylandıktan sonra kanala gönderilecektir.\n\nKullanıcı: {{}}\nİtiraf türü: Gizli\nİtiraf mesajı: {{}}"
    ITIRAF_GONDERILDI_ADMIN_ANON = f"Kullanıcı: {{}}\nKullanıcı İD: {{}}\n\n{e('asagi')} Kanalın mesajı otomatik olarak aşağıya yazıldı. {e('asagi')}"
    ITIRAF_GONDERILDI_ANON_MESAJ = (
        "📣 İtiraf türü: Gizli\n🕵️ Kullanıcı: Anonim\n\n💬 İtiraf mesajı: {}"
    )
    # +18 İTİRAF
    BUTTON_18 = "🔞 +18 İtiraf"
    YAS_ONAY = f"{e('yas')} Bu bölüm yalnızca 18 yaş ve üzeri kullanıcılar içindir.\n\n18 yaşından büyük olduğunuzu onaylıyor musunuz?"
    YAS_EVET = "✅ Evet, 18 yaşından büyüğüm"
    YAS_HAYIR = "❌ Hayır"
    YAS_RED = f"{e('yasak')} +18 itiraflar yalnızca 18 yaş ve üzeri kullanıcılar içindir.\nNormal itiraf için /start yazabilirsiniz."
    YAS_GEREKLI = "Önce yaşınızı onaylamanız gerekiyor. /start yazıp tekrar deneyin."
    ITIRAF18_CHOOSE = f"{e('yas')} +18 itirafınızı nasıl paylaşacaksınız?"
    ITIRAF18_KURALLAR = (
        f"{e('kurallar')} +18 İtiraf Kuralları\n\n"
        "• Reşit olmayan biriyle ilgili hiçbir içerik kabul edilmez.\n"
        "• Rıza dışı veya zorlama içeren içerik kabul edilmez.\n"
        "• Başkalarının adı, kullanıcı adı ya da kimliğini ele verecek bilgi yazılamaz.\n"
        "• Fotoğraf veya video gönderirseniz, görüntüdeki herkesin 18 yaşından büyük "
        "olduğunu ve paylaşılmasına izin verdiğini beyan etmiş olursunuz. "
        "Başkasının izni olmadan çekilmiş veya paylaşılmış görüntüler yasaktır.\n"
        "• Kurallara uymayan itiraflar reddedilir."
    )
    ITIRAF18_GONDERILDI = f"{e('tamam')} +18 itirafınız bize ulaştı. Onaylandıktan sonra +18 kanalına gönderilecektir.\n\nİtiraf türü: {{}}\nİçerik: {{}}"
    ITIRAF18_ADMIN = f"{e('yas')} +18 İTİRAF\nKullanıcı: {{}}\nKullanıcı İD: {{}}\n\n{e('asagi')} Kanalın mesajı otomatik olarak aşağıya yazıldı. {e('asagi')}"
    # Kanala kopyalanan mesaj -> düz emoji
    ITIRAF18_OPEN_BASLIK = "🔞 +18 İtiraf · Açık\n🕵️ İtiraf eden: {}"
    ITIRAF18_ANON_BASLIK = "🔞 +18 İtiraf · Gizli\n🕵️ Kullanıcı: Anonim"
    ITIRAF18_METIN_EK = "\n\n💬 İtiraf mesajı: {}"
    ITIRAF18_ACCEPT = "✅ +18 kanalına gönderildi"
    ITIRAF18_CHANNEL_TEXT = "🔞 +18 Kanalımız"
    ITIRAF18_YAZ = (
        f"{e('duyuru')} +18 itirafınızı gönderin:\n\n"
        "• Sadece metin yazabilirsiniz\n"
        "• Bir fotoğraf veya video gönderebilirsiniz\n"
        "• Fotoğraf veya videoya açıklama olarak metin ekleyebilirsiniz\n\n"
        f"{e('uyari')} Albüm değil, tek bir fotoğraf veya video gönderin.\n"
        "İptal etmek için `iptal` yazın."
    )
    ITIRAF18_DESTEKLENMEYEN = f"{e('uyari')} Sadece metin, fotoğraf veya video gönderebilirsiniz.\nİptal etmek için `iptal` yazın."
    ITIRAF18_METIN_UZUN = f"{e('uyari')} Metin çok uzun. Fotoğraf/video açıklaması en fazla {{}} karakter, düz metin en fazla {{}} karakter olabilir. Lütfen kısaltıp tekrar gönderin."