---
title: omada – wifi systém od tplink
category: Počítače
tags: [network, sítě, wifi]
last_update: 2026-09-28
---

# Komplexní příručka: TP-Link Omada Controller v6 (Docker & Tří-VLANová síť)

Tato příručka slouží jako kompletní dokumentace pro instalaci, provoz, řešení konfliktů portů a konfiguraci tří oddělených VLAN sítí s kabelovou topologií bez bezdrátového Meshe.

---

## 1. Topologie sítě
*   **Router:** TP-Link Omada ER707-M2 (vstup internetu).
*   **Switch:** Propojuje router, řídicí PC, tiskárnu a přístupové body.
*   **Controller:** Běží v Docker kontejneru na Kubuntu (Host network mód).
*   **Přístupové body (AP):** 3x Omada EAP (1x desktop, 2x stropní), připojené výhradně kabelem (Mesh vypnut).

---

## 2. Instalace a správa Docker kontejneru

Pro bezpečný provoz verze 6.x s fixovaným tagem a dostatečným časem pro korektní vypnutí databáze MongoDB použijte tento příkaz pro sestavení:

```bash
sudo docker run -d \
  --name omada-controller \
  --stop-timeout 60 \
  --restart unless-stopped \
  --ulimit nofile=4096:8192 \
  --net host \
  -e TZ=Europe/Prague \
  -v omada-data:/opt/tplink/EAPController/data \
  -v omada-logs:/opt/tplink/EAPController/logs \
  mbentley/omada-controller:6.3
```

### Řešení konfliktů po restartu (Porty již obsazeny)
Pokud kontejner cykluje ve stavu `Restarting (1)` kvůli tomu, že porty obsadila stará nativní instalace balíčku (`tpeap`), spusťte v terminálu Kubuntu:

```bash
# 1. Natvrdo ukončit polomrtvé procesy systému
sudo killall -9 java mongod

# 2. Opravit práva ve svazcích přepsaná rootem zpět pro uživatele omada (ID 508)
sudo chown -R 508:508 /var/lib/docker/volumes/omada-data/_data
sudo chown -R 508:508 /var/lib/docker/volumes/omada-logs/_data

# 3. Odstranit případný zámek databáze
sudo rm -f /var/lib/docker/volumes/omada-data/_data/db/mongod.lock

# 4. Trvale zamaskovat starou systémovou službu v systemd
sudo systemctl stop omada
sudo systemctl disable omada
sudo systemctl mask omada

# 5. Spustit Docker kontejner
sudo docker start omada-controller
```

---

## 3. Konfigurace VLAN a podsítí (Omada v6.x)

Všechna nastavení se v nové generaci rozhraní provádějí v sekci **Configuration** v levém menu.

kompletní přehled síťové topologie
                      +-----------------------+

                      |       INTERNET        |
                      +-----------+-----------+
                                  |
                                  v [WAN]
                      +-----------+-----------+

                      |     Omada Router      |
                      |       ER707-M2        |
                      +-----------+-----------+
                                  | [LAN 10.20.x.1]
                                  v
                      +-----------+-----------+

                      |     PoE Switch        |
                      +---+---+---+---+---+---+

                          |   |   |   |   |
      +-------------------+   |   |   |   +-------------------+

      |                       |   |   |                       |
      v                       v   v   v                       v
+-----+------+              +-----------+               +-----+------+

| Správní PC |              |  Tiskárna |               |  Stropní   |
| (Kubuntu)  |              | 10.20.1.x |               |    AP 2    |
|            |              +-----------+               |  EAP610    |
|  [Docker]  |                                          | 10.20.1.102|
|  Omada v6  |                                          +-----+------+
| Controller |                                                |
+------------+                                                |
                                                              |
      +-------------------------------------------------------+
      |
      v
+-----+------+              +-----------+

|  Stropní   |              |  Desktop  |
|    AP 1    |              |    AP     |
|  EAP610    |              |  EAP650   |
| 10.20.1.101|              | 10.20.1.103|
+-----+------+              +-----+-----+

      |                           |
      +-------------+-------------+
                    |
                    v
    ================================================================
    DISTRIBUCE SÍTÍ / VLAN SKRZE VŠECHNA AP:
    ================================================================
    [VLAN 1]  SSID: rabuwork       -->  Firma (10.20.1.0/24)  [Plný přístup]
    [VLAN 2]  SSID: rabuhome       -->  Děti/IoT (10.20.2.0/24) [Pouze Internet]
    [VLAN 3]  SSID: www.umicky.cz  -->  Hosté (10.20.3.0/24)  [Izolováno/Guest]
    ================================================================


### Krok 3.1: Drátové sítě (LAN Rozhraní)
Přejděte do: **Configuration ➔ Network Config ➔ Network Settings ➔ LAN** a nastavte:

| Název sítě | Účel (Purpose) | IP Adresa / Subnet | VLAN ID | DHCP Stav |
| :--- | :--- | :--- | :--- | :--- |
| **Default / LAN** | Interface | `10.20.1.1/24` | `1` | Zapnuto (Firma) |
| **Deti_IoT** | Interface | `10.20.2.1/24` | `2` | Zapnuto (Domov/IoT) |
| **Hosti** | Interface | `10.20.3.1/24` | `3` | Zapnuto (Návštěvy) |

### Krok 3.2: Směrování a Bezpečnost (Gateway ACL)
Omada mezi VLANami nativně provoz povoluje. Pro izolaci přejděte do: **Configuration ➔ Network Config ➔ Security ➔ ACL ➔ Gateway ACL** a vytvořte dvě pravidla typu **LAN -> LAN** s politikou **Deny**:

1.  **Pravidlo `Blokuj_Hosty_do_vnitrni_site`**
    *   *Source:* `Network -> Hosti (VLAN 3)`
    *   *Destination:* `IP Group -> Any`
2.  **Pravidlo `Blokuj_IoT_do_Firmy`**
    *   *Source:* `Network -> Deti_IoT (VLAN 2)`
    *   *Destination:* `Network -> Default/LAN (VLAN 1)`
    *   *Výsledek:* VLAN 1 vidí do VLAN 2 (správa IoT), ale zařízení z VLAN 2 se do firmy nedostanou.

### Krok 3.3: Bezdrátové sítě (WLAN)
Přejděte do: **Configuration ➔ Network Config ➔ WLAN** a vytvořte/upravte Wi-Fi sítě. Mapování do VLAN se provádí rozbalením spodní nabídky **Advanced Settings**:

| SSID (Název Wi-Fi) | Zabezpečení | Možnost VLAN v Advanced Settings | Speciální příznaky |
| :--- | :--- | :--- | :--- |
| **rabuwork** | WPA2-PSK | **Vypnuto** (propadne do VLAN 1) | Plný přístup |
| *[Tvoje volba pro IoT]* | WPA2-PSK | **Zapnuto** ➔ zadej **`2`** | Přístup pouze Internet |
| **www.umicky.cz** | WPA2-PSK / Open | **Zapnuto** ➔ zadej **`3`** | Zaškrtnout **Guest Network** |

*Poznámka: Příznak `Guest Network` u hostovské Wi-Fi hardwarově izoluje klienty na přístupových bodech tak, aby se neviděli ani mezi sebou.*

---

## 4. Správa hardwaru (AP a Switch)

### Statické IP adresy pro Access Pointy
Pro stabilitu a přehlednost přiřaďte APčkům pevné IP adresy. Přejděte do: **Management ➔ Devices** ➔ klikněte na dané AP ➔ v pravém panelu zvolte **Config ➔ IP Settings**:
*   **IP Mode:** `Static`
*   **IP Address:** `10.20.1.101` až `10.20.1.103` (podle zvoleného schématu)
*   **Maska / Brána / DNS:** `255.255.255.0` / `10.20.1.1` / `10.20.1.1`

### Vypnutí funkce MESH
Protože jsou všechna AP připojena kabelem, bezdrátový Mesh je nežádoucí. Globálně ho vypnete v:
**Configuration ➔ Device Config ➔ Mesh** ➔ přepnout na **Disabled**.

---

## 5. Příkazy pro rychlou diagnostiku ze systému Kubuntu

```bash
# Kontrola, zda controller naslouchá na správných portech pro adoptovaná AP
sudo ss -lptn 'sport = :29814 or sport = :8043'

# Odposlech L2 broadcastů z APček pro ověření síťové průchodnosti (Discovery)
sudo tcpdump -ni any udp port 29810 -vv -X

# Kontrola stavu Docker kontejneru v reálném čase
watch -n 2 sudo docker ps
```
