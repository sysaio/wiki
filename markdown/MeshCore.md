---
title: Off-grid LoRa Mesh síť (MeshCore / Meshtastic) – Šardice
category: Informatika
tags: [Chat, Radio, LoRa, MeshCore, Meshtastic, Kubuntu]
last_update: 2026-11-23
---

# 📡 Výzkumný projekt: Off-grid LoRa Mesh síť (Šardice)

Cílem projektu je vybudovat levnou, spolehlivou a zcela decentralizovanou textovou komunikační síť na volném bezlicenčním pásmu **868 MHz (EU)**, která funguje bez internetu, mobilních operátorů a centrálních serverů. 

Sestava kombinuje **střešní/půdní opakovač (Repeater)** ve 3. patře pro překonání terénního profilu údolí v Šardicích a **stolní USB stanici (Client/Companion)** připojenou ke Kubuntu PC v přízemí.

---

## 🏗️ Architektura a volba protokolu

Hardware je 100% kompatibilní s oběma hlavními open-source systémy (**MeshCore** i **Meshtastic**). Firmware lze kdykoliv během 2 minut přehrát přes webový prohlížeč.

* **MeshCore (Primární volba pro tuto topologii):** Odděluje kapesní/stolní zařízení (*Companion*) od pevných opakovačů (*Repeater*). Klientská zařízení nezahltí éter zbytečným přeposíláním a zprávy mají spolehlivé potvrzení doručení (ACK).
* **Meshtastic (Alternativa):** Největší komunita v ČR (přes 1 100 uzlů), vhodné pro okamžité spojení s okolními turisty bez nutnosti složitého nastavování.
* **Lokalita Šardice (cca 183 m n. m.):** Obec leží v údolí obklopeném vinařskými svahy Kyjovské pahorkatiny. Z přízemí není přímá viditelnost na okolní uzly (Hodonín ~17 km, Dambořice ~14 km). Umístění repeateru na stožár ve 3. patře (10–12 m nad zemí) tento handicap řeší.

### 🗺️ Živé mapy a sledování provozu (Live paketů)

* **[MeshCore CZ – Live mapa](https://mapa.meshcore.cz/):** Interaktivní mapa českých uzlů s animací živých tras paketů, přehledem stavu baterií repeaterů, statistikami a výpočtem přímé viditelnosti (LOS) / pokrytí terénu.
* **[MeshCore CZ – Live Analyzer](https://analyzer.meshcore.cz/#/live):** Detailní živý analyzátor provozu (MQTT feed) pro sledování průchodu zpráv, advertů a trasování (TRACE) v reálném čase.

### 🗺️ Topologie domácí sítě

```topologie
                  ┌─────────────────────────────┐
                  │  3. PATRO / ANTÉNNÍ STOŽÁR  │
                  │  RAK WisBlock (RAK4631)     │ <-- Hlavní Repeater (868 MHz)
                  │  + Externí anténa + záloha  │     Přemosťuje údolí Šardic
                  └──────────────┬──────────────┘
                                 │
                 ════════════════╪════════════════ <-- Rádiová MESH síť
                ╱                │                ╲    (LoRa 868 MHz, bez internetu)
               ▼                 ▼                 ▼
┌─────────────────────┐ ┌─────────────────┐ ┌────────────────────┐
│ PŘÍZEMÍ (Pracovna)  │ │ OKOLNÍ SÍŤ      │ │ TERÉN / MOBIL      │
│ Heltec T114 / V4    │ │ Hodonín /       │ │ Kapesní uzel       │
│ (USB-C ke Kubuntu)  │ │ Dambořice /     │ │ nebo mobil přes BT │
└──────────┬──────────┘ │ Kyjovsko        │ └────────────────────┘
           │            └─────────────────┘
           ▼
┌─────────────────────┐
│ Kubuntu PC          │
│ (Meshy / Web / CLI) │
└─────────────────────┘
```

---

## 🛒 Doporučený hardware (Skladem v ČR)

Veškerý hardware musí být bezpodmínečně určen pro evropské pásmo **868 MHz (EU868)**. Pro páteřní uzel je zvolen úsporný čip **Nordic nRF52840** (minimální spotřeba, nulové zahřívání).

### 1. Páteřní repeater (3. patro / Stožár)
* **Jádro:** **RAKwireless WisBlock (základní deska RAK19007 + modul RAK4631, 868 MHz)**
  * *Dostupnost:* Jako kompletní sada na [Botland.cz – WisBlock Starter Kit](https://botland.cz) nebo po jednotlivých dílech (RAK19007 + RAK4631) na [LaskaKit.cz](https://laskakit.cz) a [RPishop.cz](https://rpishop.cz).
* **Anténa:** Venkovní všesměrová laminátová anténa **868 MHz** (zisk 3–5,8 dBi) + krátký pigtail U.FL/IPEX na SMA/N-konektor.
  * *Pravidlo koaxu:* Na 868 MHz má dlouhý kabel velké ztráty. Krabičku s RAKem dej co nejblíže k anténě (např. vodotěsná krabice IP65 na stožár) nebo použij kvalitní nízkoútlumový kabel (**LMR-400** / **H155**).
* **Napájení a záloha:** Trvalé napájení ze zásuvky v podkroví (5 V adaptér nebo PoE splitter) + 1× Li-Ion článek **18650** (nebo LiPo) připojený přímo do desky RAK jako UPS záloha při výpadku proudu (vydrží běžet několik dní).
* **Ochrana:** Mezi venkovní anténu a desku vřadit koaxiální přepěťovou ochranu (bleskojistku) uzemněnou ke stožáru; venkovní konektory utěsnit samovulkanizační páskou.

### 2. Klientská stanice ke Kubuntu PC (Přízemí)
* **Varianta A (Úsporná, univerzální i do batohu):** **Heltec Mesh Node T114 (868 MHz)** – čip nRF52840, barevný displej, nízká spotřeba. Skladem na [LaskaKit.cz](https://laskakit.cz).
* **Varianta B (Levný stolní základ):** **Heltec WiFi LoRa 32 V3 / V4.3 (868 MHz)** – čip ESP32-S3, OLED displej. Protože je trvale na USB napájení z PC, vyšší spotřeba ESP32 nevadí. Skladem na [LaskaKit.cz](https://laskakit.cz) nebo [Hadex.cz](https://hadex.cz).
* **Anténa:** Pro spojení z přízemí do 3. patra stačí základní malý prut přibalený k desce (případně malá magnetická anténka na stůl).

> ⚠️ **Zlaté pravidlo hardwaru:**
> **Nikdy nezapínej LoRa desku do USB ani k baterii bez připojené antény!** Bez zátěže na anténním výstupu dojde k okamžitému zničení koncového zesilovače rádia.

---

## 🛠️ Konfigurace a uvedení do provozu

### Krok 1: Nahrání firmwaru (Web Flasher)
Připoj desky datovým USB-C kabelem k počítači a otevři webový flasher v prohlížeči založeném na Chromiu (Chrome, Brave, Vivaldi):

* **Pro MeshCore:** Otevři [flasher.meshcore.io](https://meshcore.io)
  * Do horního uzlu (RAK4631) nahraj firmware **`Repeater`**.
  * Do spodního uzlu u PC (Heltec) nahraj firmware **`Companion USB`** (pokud bude připojen kabelem k PC).
* **Pro Meshtastic:** Otevři [flasher.meshtastic.org](https://meshtastic.org) a nahraj aktuální stabilní verzi pro příslušnou desku.

---

### Krok 2: Rádiové nastavení pro ČR

#### Pokud jedeš na MeshCore (Český standard):
V české komunitě se používá specifický preset **CZ Narrow**, který minimalizuje rušení a zvyšuje dosah:
* **Frekvence:** `869,618 MHz`
* **Bandwidth (Šířka pásma):** `62,5 kHz`
* **Spreading Factor:** `SF7`
* **Coding Rate:** `CR5`
* **Pojmenování repeateru:** Před nasazením ověř na [pokryti.meshcore.cz](https://meshcore.cz) nebo na Telegramu, aby 2bajtový prefix tvého repeateru nekolidoval s okolními uzly v JMK.

#### Pokud jedeš na Meshtastic:
* **Region:** `EU_868`
* **Role horního uzlu (3. patro):** `ROUTER_LATE` (nebo `CLIENT`). *Nepoužívej klasický `ROUTER` – ten je vyhrazen pouze pro nejvyšší horské kóty a v zástavbě by zbytečně zahlcoval síť.*
* **Role spodního uzlu (u PC):** `CLIENT_MUTE` (nepřeposílá cizí provoz, jen komunikuje přes horní repeater).

---

### Krok 3: Zprovoznění na Kubuntu PC

#### 1. Oprávnění k sériovému USB portu
Aby klientské aplikace mohly komunikovat s připojenou deskou (`/dev/ttyUSB0` nebo `/dev/ttyACM0`):
```bash
sudo usermod -aG dialout \$USER
```
*(Po spuštění příkazu je nutné se z Kubuntu odhlásit a znovu přihlásit).*

#### 2. Desktopové a webové aplikace pro MeshCore
* **Meshy (Doporučený nativní klient pro Linux):** Grafický klient s podporou map, šifrovaných zpráv a USB/BT připojení. Instalace na Kubuntu přes Flatpak:
  ```bash
  flatpak install flathub page.codeberg.sesivany.Meshy
  ```
* **Webový klient (bez instalace):** Otevři [app.meshcore.nz](https://meshcore.nz) v prohlížeči Chrome/Brave/Vivaldi a připoj desku přes sériový port.
* **Terminálový nástroj (CLI):**
  ```bash
  pip install meshcore-cli
  ```

#### 3. Terminálový klient pro Meshtastic (pokud přepneš na Meshtastic)
```bash
pip install --upgrade "meshtastic[cli]"
meshtastic --set lora.region EU_868
meshtastic --sendtext "Test ze Sardic"
meshtastic --listen
```

---

## 📚 Česká komunita, mapy a užitečné odkazy

* **Český rozcestník a návody (Meshtastic):** [czmesh.cz](https://czmesh.cz) – základní nastavení pro ČR, FAQ, odkazy na mapy.
* **Česká wiki pro MeshCore:** [meshcore.cz](https://meshcore.cz) – dokumentace, doporučené presety, stavba repeaterů.
* **Simulace pokrytí a plánování stožáru:** [pokryti.meshcore.cz](https://meshcore.cz) – nástroj *Coverage Planning* pro výpočet rádiové viditelnosti ze Šardic do okolí.
* **Stavba sítě a antény:** [meshnode.cz](https://meshnode.cz) – praktické rady k solárním a střešním uzlům.
* **Komunitní skupiny (podpora a koordinace):**
  * **Telegram:** `meshtastic_cz` a `meshcore_cz` (nejrychlejší technická podpora a domluva se správci jihomoravských uzlů).
  * **Facebook:** [Meshtastic & MeshCore CZ/SK users group](https://facebook.com)
