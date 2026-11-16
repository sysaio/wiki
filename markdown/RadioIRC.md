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

Systém **nepotřebuje žádný centrální server, SIM karty ani internetové připojení**. Využívá otevřený firmware **Meshtastic** nad rádiovou technologií **LoRa (Long Range)** v evropském bezlicenčním pásmu **868 MHz**.

* **Bezestavový přenos (podobný UDP):** Rádia nevytvářejí trvalé TCP spojení. Vysílají binární datagramy (Google Protocol Buffers) s hlavičkou kanálu a šifrováním **AES-256**.
* **Princip IRC místností:** Místo příkazu `/join #kanál` si v zařízeních nadefinuješ až 8 pojmenovaných kanálů (např. `#general`, `#rodina`, `#linux`) s vlastním šifrovacím klíčem. Každý uzel přijímá a dekóduje pouze zprávy z kanálů, které má uložené.
* **Páteřní mesh síť:** Solární uzel na střeše domu funguje jako soběstačný opakovač (*repeater*), který pokrývá celou obec a přemosťuje signál mezi domácí pracovnou a mobilními jednotkami v terénu.

### 🗺️ Topologie sítě

```text
                       [ ☀️ SLUNCE ]
                             │
                             ▼ (dobíjí 4× 18650)
                  ┌─────────────────────┐
                  │  STŘECHA DOMU       │
                  │  SenseCAP Solar P1  │  <-- Hlavní Repeater (868 MHz)
                  │  (nRF52840, IPX6)   │      Pokrytí celé vesnice (3000 obyv.)
                  └──────────┬──────────┘
                             │
             ════════════════╪════════════════   <-- Rádiová MESH síť
            ╱                │                ╲      (LoRa 868 MHz, AES-256)
           ╱                 │                 ╲     Bez internetu a GSM!
          ▼                  ▼                  ▼
┌───────────────────┐ ┌───────────────┐ ┌────────────────────┐
│ DOMA (Pracovna)   │ │ TERÉN / AUTO  │ │ SYNEK (Cesta/Škola)│
│ XIAO nRF52840 Kit │ │ Stávající RPi │ │ LILYGO T-Echo Plus │
│ + 5dBi anténa     │ │ + XIAO Kit    │ │ (e-ink + GPS)      │
└─────────┬─────────┘ └───────┬───────┘ └─────────┬──────────┘
          │ (USB-C)           │ (Wi-Fi AP)        │ (Volitelně BT)
          ▼                   ▼                   ▼
┌───────────────────┐ ┌───────────────┐ ┌────────────────────┐
│ Kubuntu PC        │ │ Notebook/Mobil│ │ Android Telefon    │
│ (Terminál / IRC)  │ │ (SSH / Web)   │ │ (Mapa + Chat app)  │
└───────────────────┘ └───────────────┘ └────────────────────┘
```

---

## 🛒 Hardwarová sestava (4 uzly)

> [!TIP]
> **🛒 Kde pořídit použitý hardware (RPishop.cz):**
> * [Seeed Studio XIAO nRF52840 & Wio-SX1262 Kit pro Meshtastic](https://rpishop.cz/694263/seeed-studio-xiao-nrf52840-wio-sx1262-kit-pro-meshtastic/)
> * [LILYGO® T-Echo Plus 868 MHz](https://rpishop.cz/687248/lilygo-t-echo-plus-868-mhz/)
> * [SenseCAP Solar Node P1 pro Meshtastic](https://rpishop.cz/675458/sensecap-solar-node-p1-pro-meshtastic-solarne-napajeny-lora-uzel/)

Celá sestava je postavena na moderním, extrémně úsporném čipu **Nordic nRF52840** a citlivém rádiovém transceivery **Semtech SX1262 (868 MHz)**.

| Role v síti | Zvolený hardware | Klíčové vlastnosti a napájení |
| :--- | :--- | :--- |
| **1. Páteřní střešní uzel** | **Seeed Studio SenseCAP Solar Node P1** | Vodotěsný venkovní box (IPX6) s **5W solárním panelem**. Osazen 4× vlastními články **Li-Ion 18650** (*button-top*, paralelně). Bez GPS (nižší spotřeba, poloha zadána pevně). |
| **2. Terénní komunikátor** | **LILYGO® T-Echo Plus 868 MHz** | Kapesní „pager“ na batoh s **1,54" e-ink displejem**, GPS, vibracemi, bzučákem a **2400 mAh** baterií (výdrž 5–7 dní). Umožňuje číst zprávy bez mobilu a sledovat GPS polohu. |
| **3. Domácí základna (PC)** | **Seeed Studio XIAO nRF52840 & Wio-SX1262 Kit** | Připojeno přes **USB-C** ke Kubuntu PC. Doplněno o externí anténu **868 MHz (5 dBi)** s kablíkem U.FL/IPEX pro spolehlivý průchod signálu z pracovny na střechu. |
| **4. Mobilní brána (RPi)** | **Seeed Studio XIAO nRF52840 & Wio-SX1262 Kit** | Připojeno přes **USB-C** k Raspberry Pi (headless). RPi vytváří lokální Wi-Fi AP pro připojení dalších stanic v terénu přes SSH nebo webové rozhraní. |

> ⚠️ **Důležité hardwarové zásady:**
> * **Nikdy nezapínej modul bez připojené antény!** Hrozí okamžité zničení koncového zesilovače rádia.
> * **Baterie 18650 do SenseCAP Solar P1:** Použij články s vystouplým plusovým pólem (*button-top*). Před vložením musí mít všechny 4 články **shodné napětí** (nabij je všechny naplno v externí nabíječce), protože jsou zapojeny paralelně.
> * **Vertikální polarizace:** Všechny antény (zejména na střeše a v pracovně) musí směřovat kolmo vzhůru k obloze.

---

## 🛠️ Implementační a konfigurační postup

### Krok 1: Sjednocení firmwaru (Web Flasher)
Před nasazením nahraj do všech čtyř zařízení stejnou, nejnovější stabilní verzi Meshtasticu přes prohlížeč Chromium/Chrome na Kubuntu:

1. Otevři [Meshtastic Web Flasher](https://meshtastic.org).
2. Připoj jednotlivé moduly přes datový USB-C kabel a vyber odpovídající profil:
   * Pro moduly XIAO a SenseCAP P1: **`Seeed XIAO nRF52840`**
   * Pro kapesní komunikátor: **`LILYGO T-Echo`**
3. Po nahrání nastav u všech uzlů region **`EU_868`**.

---

### Krok 2: Konfigurace střešního uzlu (`SenseCAP Solar P1`)
Střešní uzel má klíčovou roli – přeposílá zprávy po celé vesnici. Aby nezahltil vysílací limit (*Duty Cycle* 10 % v EU) a ne vybíjel ostatní uzly:

1. Spáruj P1 přes Bluetooth s telefonem (PIN je výchozí `123456` nebo dle dokumentace).
2. **Role zařízení (Device Role):** Nastav na **`ROUTER_LATE`** (nebo `CLIENT`). *Poznámka: Klasickou roli `ROUTER` používej jen na extrémně vysokých kótách/horách; `ROUTER_LATE` zajistí, že střešní uzel přepošle zprávu až ve chvíli, kdy ji nezachytí přímý příjemce.*
3. **Pevná poloha (Fixed Position):** Protože P1 nemá GPS modul, zadej v aplikaci ručně přesné GPS souřadnice střechy a zapni *Fixed Position*.
4. **Šetření baterie:** Vypni Bluetooth vypínačem po dokončení konfigurace (nebo nastav automatické vypnutí BT po neaktivitě).

---

### Krok 3: Konfigurace kapesního uzlu (`LILYGO T-Echo Plus`)
1. **Role zařízení:** Nastav na **`CLIENT`** (nebo `CLIENT_MUTE`, pokud nechceš, aby z batohu opakoval cizí provoz a šetřil tak baterii).
2. **GPS a sledování polohy:** Zapni *Smart Position* (odešle polohu při pohybu o více než 50–100 m, jinak udržuje klidový interval např. 15 minut).
3. **Rychlé odpovědi bez mobilu (*Canned Messages*):** V nastavení aktivuj modul *Canned Messages* a nadefinuj předvolby (např. `OK | Jdu domu | Jsem ve skole | Zavolej mi`), které lze odeslat stiskem bočního tlačítka.

---

### Krok 4: Konfigurace Kubuntu PC (Terminálové IRC rozhraní)
Na Kubuntu nainstalujeme oficiální CLI nástroj pro ovládání připojeného modulu XIAO z terminálu:

```bash
# 1. Práva pro sériový port (USB)
sudo usermod -a -G dialout \$USER
# (Nutné odhlášení a přihlášení)

# 2. Instalace Meshtastic Python CLI
pip install --upgrade "meshtastic[cli]"

# 3. Základní nastavení uzlu a soukromých IRC kanálů
meshtastic --set lora.region EU_868
meshtastic --set-owner "Domaci_Zakladna" --set-owner-short "DOMA"

# Vytvoření soukromého šifrovaného kanálu (obdoba #kanál)
meshtastic --ch-add "rodina"

# Výpis kanálů a vygenerování QR kódu / URL pro naskenování do mobilu
meshtastic --info
```

#### Používání z příkazové řádky:
```bash
# Odeslání zprávy do primárního kanálu (index 0)
meshtastic --sendtext "Test site z pracovny"

# Odeslání zprávy do kanálu #rodina (index 1)
meshtastic --ch-index 1 --sendtext "V 19:00 at jsi doma"

# Sledování příchozích zpráv a telemetrie v reálném čase
meshtastic --listen
```
*(Tip: Pro plnohodnotný terminálový chat s oddělenými okny kanálů jako v `irssi` nainstaluj komunitní TUI klient `contact` nebo `meshtastic-curses`.)*

---

### Krok 5: Konfigurace přenosného Raspberry Pi (Wi-Fi AP & Gateway)
Malina slouží jako mobilní polní terminál bez displeje (headless). Po připojení druhého modulu XIAO přes USB-C:

```bash
# Vytvoření lokálního Wi-Fi hotspotu pro okolní stanice
sudo nmcli dev wifi hotspot ifname wlan0 ssid "RadioIRC-AP" password "tajneheslo"
sudo nmcli connection modify Hotspot connection.autoconnect yes
```
Uživatelé v terénu se připojí k Wi-Fi `RadioIRC-AP`, přes SSH se přihlásí na malinu a v relaci `tmux` / `screen` komunikují přes `meshtastic` CLI.

---

## 📚 Reference a užitečné zdroje

* [Meshtastic – Oficiální dokumentace a průvodce rolemi uzlů](https://meshtastic.org)
* [Meshtastic Web Flasher (nahrávání firmwaru z prohlížeče)](https://meshtastic.org)
* [Seeed Studio Wiki – SenseCAP Solar Node P1](https://seeedstudio.com)
* [LILYGO Wiki – Dokumentace k T-Echo Plus](https://lilygo.cc)
* [Česká Meshtastic komunita (Wiki, rady pro EU_868 a mapa uzlů)](https://meshtastic.cz)

---
*Vytvořeno s laskavou pomocí AI (Gemini)*
