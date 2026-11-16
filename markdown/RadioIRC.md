---
title: Off-grid Radio-IRC síť (Meshtastic / LoRa)
category: Informatika
tags: [Chat, IRC, Radio, Meshtastic, LoRa]
last_update: 2026-11-16
---

# 📡 Výzkumný projekt: Off-grid Radio-IRC síť (Meshtastic / LoRa)

Cílem projektu je vybudovat levnou, přenosnou a zcela decentralizovanou textovou komunikační síť na volném bezlicenčním pásmu **868 MHz (EU)**, která funguje bez internetu, mobilních operátorů a centrálního serveru. Principem odpovídá klasickému **IRC** (místnosti/kanály, čistý text, minimální datová náročnost).

---

## 🏗️ Architektura a princip fungování

**tento systém nepotřebuje žádný centrální server**

Využívá otevřený firmware **Meshtastic** nad rádiovou technologií **LoRa (Long Range)**. Každé rádiové zařízení v síti (tzv. *Node*) funguje zároveň jako vysílač, přijímač i opakovač (repeater). Zprávy skáčou po síti (mesh) z uzlu na uzel na kilometry daleko.

### Topologie naší testovací sestavy (3 uzly):

1. **Uzel A: Raspberry Pi (Přenosný polní terminál & Wi-Fi AP)**
   * Přes USB k němu připojíš LoRa modul (nebo použiješ SPI HAT).
   * RPi vytváří vlastní lokální Wi-Fi hotspot (`hostapd`).
   * Kdokoliv v blízkosti (mobil, notebook) se připojí na Wi-Fi maliny a přes webové rozhraní nebo SSH/CLI píše do rádiové sítě.
2. **Uzel B: PC s Kubuntu (Domácí/základnová stanice)**
   * LoRa modul připojený přes USB-C.
   * Ovládání přes oficiální **Python CLI** (čistý terminál jako `irssi` nebo `WeeChat`) nebo přes webový klient v prohlížeči.
3. **Uzel C: Telefon Android (Mobilní jednotka v terénu)**
   * Kapesní LoRa modul s baterií spárovaný přes Bluetooth.
   * Ovládání přes oficiální Android aplikaci (funguje jako moderní mobilní IRC klient).

> 💡 **Jak fungují IRC kanály v Meshtasticu:**
> Místo příkazu `/join #kanál` si v rádiu nadefinuješ až 8 pojmenovaných kanálů (např. `#general`, `#hry`, `#nouze`) s vlastním šifrovacím klíčem (PSK). Rádio pak v éteru naslouchá pouze paketům, které patří do tvých aktivních kanálů.

---

## 🛒 Nákupní seznam (Hardware pro 3 uzly)

Všechny komponenty jsou dostupné v českých e-shopech (např. LaskaKit, RPishop, Pájeníčko) nebo na AliExpressu. **Důležité: Vždy kupuj verzi pro frekvenci 868 MHz (Evropa)!**

| Položka | Určení v sestavě | Doporučený model | Orientační cena |
| :--- | :--- | :--- | :--- |
| **1. Mobilní uzel (s baterií)** | Pro **Android** (do kapsy / batohu) | **LILYGO T-Beam v1.2 (SX1262, 868 MHz)** nebo **Heltec V3 + krabička** | ~850 – 1 100 Kč |
| **2. USB uzel pro RPi** | Pro **Raspberry Pi** (přes USB) | **Heltec WiFi LoRa 32 V3 (868 MHz)** | ~550 – 650 Kč |
| **3. USB uzel pro PC** | Pro **Kubuntu PC** (přes USB) | **Heltec WiFi LoRa 32 V3 (868 MHz)** | ~550 – 650 Kč |
| **4. Baterie (1–2 ks)** | Pro napájení mobilních uzlů | **Článek Li-Ion 18650** (nechráněný, *flat-top* pro T-Beam) nebo **Li-Po 3.7V** (konektor JST 1.25 pro Heltec) | ~150 – 250 Kč |
| **5. Lepší antény (volitelné)** | Pro zvýšení dosahu z 1 km na 5+ km | **868 MHz anténa se ziskem 3–5 dBi** (konektor SMA + redukce U.FL/IPEX) | ~200 Kč / ks |

> ⚠️ **Upozornění před prvním zapnutím:** Nikdy nezapínej LoRa modul bez připojené antény! Hrozí okamžité spálení vysílacího čipu (SX1262).
> ⚠️ **Poznámka k RPi HATům:** Vyhni se levným *Waveshare SX1262 HATům* přímo na GPIO piny maliny – mají známé hardwarové omezení při delších zprávách. Připojení desky Heltec V3 přes obyčejný USB kabel k malině je stabilnější, levnější a jednodušší.

---

## 🛠️ Implementační postup

### Krok 1: Nahrání firmwaru (Flashování) do všech 3 desek
Nejjednodušší cesta je použít oficiální webový flasher (vyžaduje prohlížeč Chrome / Chromium / Edge na Kubuntu):

1. Připoj první desku přes USB kabel k PC (nezapomeň na anténu!).
2. Otevři [Meshtastic Web Flasher](https://flasher.meshtastic.org/).
3. Vyber typ desky (např. *Heltec V3* nebo *T-Beam*) a nejnovější stabilní verzi firmwaru.
4. Klikni na **Flash** a vyčkej na dokončení. Opakuj pro všechny tři moduly.

---

### Krok 2: Konfigurace Kubuntu PC (Terminálové IRC rozhraní)
Na Kubuntu si nainstalujeme oficiální CLI nástroj, který umožňuje ovládat rádio čistě z příkazové řádky a psát skripty.

```bash
# 1. Přidání uživatele do skupiny dialout pro přístup k sériovému portu (USB)
sudo usermod -a -G dialout \$USER
# (Pro projevení změny se odhlas a znovu přihlas)

# 2. Instalace Meshtastic Python CLI
pip install --upgrade "meshtastic[cli]"

# 3. Ověření připojení rádia a nastavení evropského regionu (EU_868)
meshtastic --set lora.region EU_868
meshtastic --info
```

#### Základní příkazy v terminálu (náš „IRC klient“):
```bash
# Nastavení přezdívky (nicku) v síti
meshtastic --set-owner "SysOp_Kubuntu" --set-owner-short "SYS"

# Vytvoření soukromého kanálu (obdoba #kanál) s náhodným šifrovacím klíčem
meshtastic --ch-add "linux"

# Výpis aktivních kanálů a jejich indexů (obdoba /list)
meshtastic --info

# Odeslání zprávy do hlavního kanálu (index 0)
meshtastic --sendtext "Ahoj svete pres 868 MHz!"

# Odeslání zprávy do kanálu #linux (např. index 1)
meshtastic --ch-index 1 --sendtext "Zprava do mistnosti #linux"

# Živý poslech příchozích paketů a zpráv v terminálu
meshtastic --listen
```
*(Tip: Pro pohodlnější chatování v terminálu si můžeš nainstalovat komunitní TUI klient v Pythonu, např. `meshtastic-curses` nebo `contact`, který vypadá přesně jako `irssi`.)*

---

### Krok 3: Konfigurace Raspberry Pi (Přenosný Wi-Fi AP & Gateway)
Malina poběží bez monitoru (headless) a vytvoří lokální Wi-Fi síť, přes kterou se kdokoliv v okolí připojí k rádiovému uzlu.

1. **Vytvoření Wi-Fi Hotspotu na RPi (Raspberry Pi OS / Debian Bookworm):**
   Pomocí `NetworkManager` (`nmcli`) vytvoříš AP jedním příkazem:
   ```bash
   sudo nmcli dev wifi hotspot ifname wlan0 ssid "RadioIRC-AP" password "tajneheslo"
   ```
   *(Pro automatický start po zapnutí maliny nastav `connection.autoconnect yes`.)*

2. **Instalace Meshtastic CLI na RPi:**
   Stejný postup jako na Kubuntu (`pip install --upgrade "meshtastic[cli]"`). Připoj k RPi druhý modul Heltec V3 přes USB.

3. **Připojení uživatelů k malině:**
   * Uživatelé v dosahu se připojí na Wi-Fi `RadioIRC-AP`.
   * Mohou se připojit přes **SSH** na malinu a používat terminál (`meshtastic --listen` / `--sendtext` v nástroji `tmux` nebo `screen` – přesně jako starý dobrý `irssi` na shellu!).
   * **Alternativa přes Wi-Fi samotného modulu:** Deska Heltec V3 má vlastní Wi-Fi čip. Můžeš ji nastavit jako Wi-Fi klienta k malině (`meshtastic --set wifi.ssid "RadioIRC-AP" --set wifi.psk "tajneheslo"`) a následně komunikovat přes TCP/IP port `4403` z jakéhokoliv zařízení v síti (`meshtastic --host 192.168.x.x --info`).

---

### Krok 4: Konfigurace Android telefonu (Mobilní uzel)
1. Nainstaluj oficiální aplikaci **Meshtastic** z Google Play nebo F-Droid.
2. Zapni třetí modul (T-Beam / Heltec).
3. V aplikaci spáruj zařízení přes Bluetooth (PIN se zobrazí na malém OLED displeji modulu).
4. Nastav region na **EU_868**.
5. **Sdílení kanálů (klíčů):** V záložce *Channels* na jednom zařízení vygeneruj **QR kód** (nebo URL odkaz) svých kanálů a naskenuj ho telefonem. Tím se všechny uzly synchronizují do stejných „IRC místností“.

---

## 📚 Doporučení a reference pro další výzkum

* **Duty Cycle (Zákonný limit vysílání):** V EU na pásmu 868 MHz platí zákonný limit vysílacího času (*Duty Cycle*) **10 %** (v některých sub-pásmech 1 %). Meshtastic tento limit automaticky hlídá, takže při masivním spamování zpráv pozdrží odesílání. Pro textový chat to ale nepředstavuje žádné omezení.
* **Výběr modemu (rychlost vs. dosah):** Výchozí profil `LongFast` nabízí skvělý dosah (kilometry) při rychlosti cca 1 kbps. Pokud budeš testovat na kratší vzdálenost (stovky metrů) a chceš rychlejší odezvu chatu, přepni všechny uzly na profil `ShortFast`.
* **Pokročilý výzkum (Reticulum):** Až si osaháš Meshtastic, vyzkoušej na stejném hardwaru projekt **Reticulum Network Stack (RNS)** + aplikaci **NomadNet**. Umí vytvořit plnohodnotný off-grid terminálový web, fóra a BBS systémy přes LoRa rádia.

### 🔗 Užitečné odkazy:
* [Oficiální dokumentace Meshtastic](https://meshtastic.org/docs/)
* [Meshtastic Python CLI příručka](https://meshtastic.org/docs/software/python/cli/)
* [Česká Meshtastic komunita (Wiki & Mapa uzlů)](https://meshtastic.cz)
* [Reticulum Network Stack (alternativní síťový protokol pro LoRa)](https://reticulum.network)

---
*Vytvořeno pomocí AI (Gemini)*
