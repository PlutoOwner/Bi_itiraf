# 🌌 Telegram İtiraf Botu

> **Dilin susar, kalbin konuşur.**

Kullanıcıların açık, gizli veya +18 itiraf gönderebildiği; itirafların admin onayından geçip kanala düştüğü bir Telegram botu.
[Pyrofork](https://github.com/Mayuri-Chan/pyrofork) ve MongoDB ile çalışır.

[![Geliştirici](https://img.shields.io/badge/Geliştirici-@wlertoxi-2CA5E0?logo=telegram&logoColor=white)](https://t.me/wlertoxi)

---

## ✨ Özellikler

- **Açık itiraf**: İtiraf, gönderenin adıyla kanalda paylaşılır.
- **Gizli itiraf**: Kanalda "Anonim" olarak görünür. Adminler gönderenin kim olduğunu görebilir.
- **🔞 +18 itiraf**
  - Bir kerelik yaş onayı ister.
  - Sadece metin, sadece fotoğraf/video veya fotoğraf/video + metin gönderilebilir.
  - Onaylananlar ayrı bir +18 kanalına gider.
  - Göndermeden önce kurallar gösterilir.
- **Admin onayı**: Her itiraf, admin grubuna **✅ Onayla / 🗑 Sil** butonlarıyla gelir. Butonlar kullanıldıktan sonra kalkar, böylece bir itiraf iki kez onaylanamaz.
- **Kullanıcı bildirimi**: Kullanıcıya itirafının kabul edilip edilmediği bildirilir.
- **Premium emoji**: İsteğe bağlıdır. Bot mesajlarında Telegram premium emojileri kullanılabilir.
- **Sahip komutları**: İstatistik ve tüm kullanıcılara duyuru.
- **Hata dayanıklılığı**
  - `iptal` ile itiraf iptal edilebilir.
  - İtiraf yazarken süre sınırı var.
  - Desteklenmeyen mesajlarda (sticker, ses vb.) bot çökmez, kullanıcıyı uyarır.

## 📋 Komutlar

| Komut | Kim kullanır | Açıklama |
|---|---|---|
| `/start` | Herkes | Botu başlatır, itiraf menüsünü açar |
| `/stat` | Sahip | Kullanıcı sayısını gösterir |
| `/duyuru` | Sahip | Yanıtlanan mesajı tüm kullanıcılara iletir |
| `/emojiid` | Sahip | Yanıtlanan mesajdaki premium emojilerin ID'lerini verir |
| `/emojiler` | Sahip | Premium emoji ayarlarını ve görünümünü listeler |

## 📁 Dosya yapısı

```
itiraf/
├── main.py              # Botu başlatır
├── config.py            # Ayarlar (token, kanal ID'leri vb.)
├── requirements.txt
├── itirafbot.service    # Linux sunucu için systemd servisi
└── plugins/
    ├── start.py         # /start, itiraf menüsü, red (sil) işlemi
    ├── etiraf_aciq.py   # Açık itiraf
    ├── etiraf_gizli.py  # Gizli itiraf
    ├── etiraf_18.py     # +18 itiraf (yaş onayı, medya)
    ├── onayla_button.py # Onaylama işlemi
    ├── sahip.py         # /stat, /duyuru
    ├── emoji.py         # Premium emoji sistemi
    └── dil.py           # Botun tüm metinleri
```

---

## ⚙️ Kurulum

### 1. Hazırlık

| Gerekli | Nereden alınır |
|---|---|
| `API_ID`, `API_HASH` | [my.telegram.org](https://my.telegram.org) → API development tools |
| `BOT_TOKEN` | [@BotFather](https://t.me/BotFather) |
| `MONGO_URI` | [MongoDB Atlas](https://www.mongodb.com/atlas) (ücretsiz plan yeterli) |
| Kanal ve grup ID'leri | Botu ekledikten sonra [@userinfobot](https://t.me/userinfobot) gibi botlarla öğrenilebilir (`-100…` ile başlar) |

**Bot şu yerlerde yönetici olmalıdır:**
- Admin grubu
- İtiraf kanalı
- +18 kanalı

**MongoDB Atlas'ta:** **Network Access** bölümünden sunucunun IP adresine izin verin.

### 2. `config.py`

```python
class Config:
    API_ID = 1234567                    # my.telegram.org
    API_HASH = "api_hash"               # my.telegram.org
    BOT_TOKEN = "123456:ABC..."         # @BotFather
    OWNER = 123456789                   # Bot sahibinin kullanıcı ID'si
    LOG_ADMINS = -100xxxxxxxxxx         # İtirafların onaya düştüğü admin grubu
    ETIRAF_CHANNEL = -100xxxxxxxxxx     # Onaylanan itirafların gittiği kanal
    ETIRAF_CHANNEL_18 = -100xxxxxxxxxx  # Onaylanan +18 itirafların gittiği kanal
    LOG_SILINMIS = -100xxxxxxxxxx       # Reddedilen itirafların kaydı
    LOG_DATABASE = -100xxxxxxxxxx       # /start yapan kullanıcıların kaydı
    BOT_USERNAME = "BotKullaniciAdi"    # @ olmadan
    ITIRAF_CHANNEL = "KanalKullaniciAdi"          # @ olmadan
    ITIRAF_UPDATE_CHANNEL = "GuncellemeKanali"    # @ olmadan
    MONGO_URI = "mongodb+srv://kullanici:sifre@cluster0.xxxxx.mongodb.net/"

    # İsteğe bağlı
    ITIRAF_18_LINK = "https://t.me/+xxxx"   # +18 kanalının davet linki
    PREMIUM_EMOJI = False                    # Premium emoji sistemi
```

> ⚠️ **`config.py` dosyasını asla paylaşmayın ve GitHub'a yüklemeyin.** Token veya şifre sızarsa token'ı @BotFather üzerinden `/revoke` ile, MongoDB şifresini de Atlas panelinden hemen yenileyin.

### 3. Linux sunucu (VPS)

```bash
git clone <repo-adresi> itiraf
cd itiraf
apt update && apt install -y python3-venv
python3 -m venv venv
venv/bin/pip install -U -r requirements.txt
nano config.py               # Ayarları doldurun
venv/bin/python main.py      # Deneme: "@bot başladı!" yazmalı
```

Bot düzgün çalışıyorsa `Ctrl+C` ile durdurun ve servis olarak kurun. Böylece terminal kapansa veya sunucu yeniden başlasa da çalışmaya devam eder:

```bash
# itirafbot.service içindeki klasör yolunu kendi yolunuza göre düzenleyin (varsayılan: /root/itiraf-main)
sed -i "s#/root/itiraf-main#$(pwd)#g" itirafbot.service
cp itirafbot.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable --now itirafbot
```

| İşlem | Komut |
|---|---|
| Durum | `systemctl status itirafbot --no-pager` |
| Canlı log | `journalctl -u itirafbot -f` |
| Yeniden başlat | `systemctl restart itirafbot` |
| Durdur | `systemctl stop itirafbot` |

### 4. Windows (test için)

```powershell
pip install -U -r requirements.txt
python main.py
```

---

## 🎨 Premium emoji (isteğe bağlı)

1. `config.py` içinde `PREMIUM_EMOJI = True` yapın. Bot, **Telegram Premium** üyeliği olan bir hesapla oluşturulmuş olmalıdır.
2. Bota premium emojili bir mesaj gönderin ve o mesajı `/emojiid` ile yanıtlayın.
3. Gelen ID'leri `plugins/emoji.py` içindeki `EMOJILER` listesine yazın:
   ```python
   "selam": ("👋", 5368324170671202286),
   ```
4. Botu yeniden başlatın ve `/emojiler` ile kontrol edin.

ID'si girilmeyen emojiler normal emoji olarak görünür.

**Premium emoji şu yerlerde kullanılamaz:**
- Kanala giden itiraflar
- Butonlar
- Açılır bildirimler

Bunun sebebi Telegram kısıtlamalarıdır.

---

## 🛠 Sık karşılaşılan sorunlar

**Bot başlıyor ama `/start` komutuna cevap vermiyor**

Aynı token başka bir yerde çalışıyor olabilir. Bilgisayarınızda, eski bir sunucuda veya hosting panelinde açık kalmış bot var mı kontrol edin.

Eski bir webhook kalmış olabilir. Silmek için şu adresi açın:
`https://api.telegram.org/bot<TOKEN>/deleteWebhook`

Bot her `/start` komutunda takılıyorsa, sebep büyük ihtimalle MongoDB'nin sunucu IP adresine izin vermemesidir.

**`Peer id invalid`**

Eski `pyrogram` kurulu demektir. Şu komutlarla pyrofork'a geçin:
```bash
pip uninstall pyrogram pyromod -y
pip install pyrofork
```

**`unable to open database file` (Windows)**

`main.py` dosyasındaki oturum adı `":memory:"` olarak kalmış. Bu adı `"itirafbot"` yapın.

**Servis `203/EXEC` hatası veriyor**

`itirafbot.service` içindeki klasör yolu yanlış ya da `venv` oluşturulmamış. Şu komutla kontrol edin:
```bash
grep -E "WorkingDirectory|ExecStart" /etc/systemd/system/itirafbot.service
```

---

## ⚖️ Sorumluluk

+18 bölümündeki yaş onayı, kullanıcının kendi beyanına dayanır. Onaylanan her içerikten bot yöneticileri sorumludur. Şu içerikleri **kesinlikle onaylamayın:**
- Reşit olmayan biriyle ilgili içerik
- Rıza dışı içerik
- Başkalarının izni olmadan çekilmiş veya paylaşılmış görüntüler (Türkiye'de TCK 134 kapsamında suçtur)

+18 kanalını gizli (davet linkli) tutmanız önerilir.

## 📄 Lisans

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

Bu proje **AGPL-3.0** lisanslıdır. Değiştirilmiş sürümü herkese açık olarak çalıştırıyorsanız kaynak kodunu da paylaşmanız gerekir.

## 👨‍💻 Geliştirici

Bu sürüm, orijinal projenin hataları giderilmiş ve yeni özelliklerle genişletilmiş hâlidir.

- 👤 **Düzenleyen:** [@wlertoxi](https://t.me/wlertoxi)
  - 🔞 +18 itiraf bölümü (yaş onayı, fotoğraf/video desteği)
  - 🎨 Premium emoji sistemi
  - 🐛 Onay/red akışı, iptal, zaman aşımı ve çökme hatalarının giderilmesi
  - ⚙️ Pyrofork'a geçiş ve sunucu (systemd) kurulumu

Soru, öneri veya hata bildirimi için Telegram üzerinden [@wlertoxi](https://t.me/wlertoxi) ile iletişime geçebilirsiniz.

## 🙏 Orijinal proje

- 👤 [Guliyev](https://github.com/Guliyev-di)
