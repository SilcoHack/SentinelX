# SentinelX 🛡️

Çoklu siber güvenlik aracı — Port Scanner, DNS Lookup, WHOIS, SSL Inspector, Hash Cracker ve daha fazlası. Tek dosya, sıfır bağımlılık.

## ✨ Özellikler

- 🔍 **Port Scanner** — Çok thread'li TCP tarama (yaygın/aralık/tam)
- 🌐 **DNS Lookup** — A kaydı + reverse PTR
- 📋 **WHOIS** — IANA üzerinden doğru sunucuya yönlendirme
- 🔎 **Subdomain Enumeration** — 60+ yaygın subdomain
- 📡 **Banner Grabber** — Servis banner'ı çekme
- 🛡️ **HTTP Header Analyzer** — Güvenlik başlığı eksik analizi
- 🔐 **SSL Certificate Inspector** — Sertifika zinciri, SAN, issuer
- 📁 **Directory Scanner** — Web yol/dosya keşfi
- #️⃣ **Hash Generator** — 10 farklı algoritma
- 🔓 **Hash Cracker** — Sözlük saldırısı + otomatik algo algılama
- 💪 **Password Strength** — Entropi, puan, öneri
- 🔄 **Encoder/Decoder** — Base64, Hex, URL, ROT13
- 🌍 **IP Geolocation** — Konum, ISP, AS bilgisi
- 📶 **Host Discovery** — TCP Ping Sweep
- 🖥️ **MAC Vendor Lookup** — MAC'ten üretici
- ⚙️ **HTTP Method Tester** — GET/POST/PUT/DELETE testi
- 🧬 **Tech Fingerprinter** — WordPress, React, Nginx vs.
- 🎫 **JWT Decoder** — `alg:none` uyarısıyla
- 🎲 **Password Generator** — Kriptografik güvenli
- 🚧 **WAF Detection** — Cloudflare, Sucuri vs.
- 🔗 **Redirect Chain** — Yönlendirme zinciri
- 📧 **Email Harvester** — Sayfadan e-posta toplama
- 🤖 **robots.txt / sitemap.xml** — Okuma ve analiz
- 🔒 **SSL/TLS Version Scanner** — Hangi protokoller destekli

## 🚀 Kurulum

```bash
git clone https://github.com/SilcoHack/sentinelx.git
cd sentinelx
python sentinelx.py

