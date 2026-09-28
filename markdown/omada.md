---
title: omada – wifi systém od tplink
category: Počítače
tags: [network, sítě, wifi]
last_update: 2026-09-28
---

# Komplexní příručka: TP-Link Omada Controller v Dockeru (Kubuntu / Linux)

Tato příručka pokrývá kompletní proces od čisté instalace Omada Controlleru v prostředí Docker na systému Kubuntu, přes správné provozní postupy a řešení běžných problémů (např. konfliktů s nativní službou), až po pokročilou síťovou diagnostiku prvků z příkazové řádky.

---

## 1. Instalace Dockeru na Kubuntu

Před samotnou instalací Omada Controlleru je nutné mít správně nakonfigurovaný Docker a Docker Compose.

```bash
# Aktualizace indexu balíčků
sudo apt update

# Instalace potřebných závislostí
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common

# Přidání oficiálního GPG klíče Dockeru
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Přidání repozitáře pro Ubuntu (Kubuntu sdílí repozitáře)
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Instalace Docker engine a Compose
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Přidání aktuálního uživatele do skupiny docker (vyžaduje restart/znovu přihlášení)
sudo usermod -aG docker $USER
```

---

## 2. Instalace a nasazení Omada Controlleru

Pro provoz se doporučuje komunitní image `mbentley/omada-controller`. Nejstabilnější metodou pro správu je **Docker Compose** s využitím síťového režimu **Host**, který zaručuje bezproblémovou autodetekci (discovery) Omada zařízení v síti.

> ⚠️ **Důležité varování k verzím:** Nikdy nepoužívejte tag `:latest`. Omada Controller provádí nevratné změny v databázi. Vždy v konfiguraci uzamkněte konkrétní major/minor verzi (např. `6.3`), abyste předešli nechtěným aktualizacím, které mohou zlomit kompatibilitu s vaším hardwarem.

### Vytvoření souboru `docker-compose.yml`

Vytvořte si adresář (např. `~/omada`) a uložte do něj následující konfiguraci:

```yaml
services:
  omada-controller:
    image: mbentley/omada-controller:6.3
    container_name: omada-controller
    network_mode: host
    restart: unless-stopped
    stop_grace_period: 60s
    ulimits:
      nofile:
        soft: 4096
        hard: 8192
    environment:
      - TZ=Europe/Prague
      - SHOW_SERVER_LOGS=true
      - SHOW_MONGODB_LOGS=false
    volumes:
      - omada-data:/opt/tplink/EAPController/data
      - omada-logs:/opt/tplink/EAPController/logs

volumes:
  omada-data:
  omada-logs:
```

### Proč tato konfigurace?
*   **`network_mode: host`**: Zpřístupní kontejner přímo na síťové kartě počítače. Je klíčový pro L2 discovery (vyhledávání prvků přes UDP všesměrové vysílání).
*   **`stop_grace_period: 60s`**: Poskytuje vestavěné databázi MongoDB dostatek času (60 sekund) na bezpečné uložení dat a korektní vypnutí při restartu počítače, čímž předchází korupci databáze.

### Spuštění kontejneru
```bash
docker compose up -d
```
Po spuštění je rozhraní dostupné na adrese: **`https://localhost:8043/#/`** *(Inicializace při prvním startu může trvat 1–2 minuty).*

---

## 3. Řešení problémů: Konflikt portů po restartu systému

Pokud jste v minulosti experimentovali s nativní instalací Omada Controlleru v systému (přes `.deb` balíček od TP-Linku), po restartu PC se tato služba (`tpeap`) může spustit dříve než Docker a obsadit síťové porty.

### Symptomy chybového stavu
*   Stránka `https://localhost:8043/#/` hlásí chybu spojení.
*   Příkaz `docker ps` ukazuje status `Restarting (1) X seconds ago`.
*   Příkaz `docker logs omada-controller` končí chybou:
    `ERROR [...] Port 29810, port 29812, port 29813 [...] are already in use.`

### Řešení (Krok za krokem)

1.  **Ukončení zaseknutých procesů natvrdo:**
    Nativní služba se při pokusu o standardní vypnutí často zasekne v nekonečné smyčce. Vyčistěte systémové procesy:
    ```bash
    sudo killall -9 java mongod
    ```
2.  **Trvalé zablokování a zamaskování nativní služby:**
    Aby k situaci nedošlo při dalším startu Kubuntu, službu v `systemd` nejen vypněte, ale kompletně zamaskujte (přesměruje její spouštěč do `/dev/null`):
    ```bash
    sudo systemctl stop omada
    sudo systemctl disable omada
    sudo systemctl mask omada
    ```
3.  **Opětovné nahození Docker kontejneru:**
    Jakmile jsou porty volné, Docker automaticky (nebo manuálně) kontejner stabilizuje:
    ```bash
    docker start omada-controller
    ```

---

## 4. Síťová diagnostika Omada z příkazové řádky

Při správě sítě a prvků adoptovaných pod Omada Controllerem se často hodí diagnostika přímo z terminálu Kubuntu.

### Kontrola obsazených portů a naslouchajících služeb
Ověření, zda váš počítač skutečně naslouchá na klíčových portech pro komunikaci se switchi a přístupovými body (AP):
```bash
sudo ss -lptn 'sport = :29810 or sport = :29814 or sport = :8043'
```
*   **8043**: HTTPS Webový port pro správu.
*   **29810**: UDP port pro vyhledávání (Discovery) prvků starší/přechodové generace V1.
*   **29814**: TCP port pro management prvků generace V2 (současné firmwary).

### Vyhledávání Omada zařízení v lokální síti (L2 Discovery)
Omada prvky komunikují pomocí UDP broadcastů na portu `29810`. Zda v síti tato komunikace probíhá a zařízení vysílají pakety, můžete ověřit pomocí síťového analyzátoru `tcpdump`:
```bash
sudo tcpdump -ni any udp port 29810 -vv -X
```
*Tento příkaz vám v reálném čase zobrazí surová data (včetně MAC adres a modelů), která se pokoušejí s controllerem spojit.*

### Ruční nasměrování zařízení na Controller (L3 Inform / SSH)
Pokud se přístupový bod (EAP) nebo switch nachází v jiné podsíti nebo se nedaří automatické vyhledání, můžete se k danému prvku připojit přes SSH (výchozí přihlašovací údaje jsou `admin`/`admin`, případně ty, které máte nastavené v Controlleru pod *Site -> Device Account*) a vynutit adopci ručně:

```bash
# Přihlášení na IP adresu AP/Switche
ssh admin@192.168.1.50

# Zobrazení aktuálního stavu informování
clicmd info

# Manuální nastavení IP adresy vašeho Omada Controlleru
clicmd set-inform https://<IP_VASEHO_KUBUNTU>:8043/com.tplink.smb.omada.bootstrap.InformUrl
```

---

## 5. Zálohování a údržba

*   **Zálohování přes Web UI (Doporučeno):** Přejděte do *Settings > Maintenance > Backup* a stáhněte si `.cfg` soubor. Zálohování kopírováním složek za běhu kontejneru může způsobit nekonzistenci databáze MongoDB.
*   **Aktualizace Controlleru:** V případě potřeby přechodu na vyšší verzi (např. z 6.3 na 6.4) stačí upravit tag v `docker-compose.yml`, provést `docker compose pull` a následně `docker compose up -d`. Vždy si před tímto krokem udělejte aplikační zálohu!
