---
title: borg – zalohovaci system
category: Počítače
tags: [linux, zalohy, backup]
last_update: 2026-08-30
---

# BorgBackup na Linuxu: bezpečné zálohování, retence a obnova po havárii

BorgBackup je deduplikační zálohovací nástroj určený pro vytváření efektivních a šifrovaných záloh. V tomto článku si ukážeme praktický návrh zálohování Linuxového systému pomocí BorgBackup, automatizaci přes systemd, retenční politiku a především postup obnovy souborů i celého systému po havárii.

Cílem není pouze vytvořit zálohu, ale navrhnout systém tak, aby bylo možné data **spolehlivě obnovit i ve chvíli, kdy původní systém přestane fungovat**.

---

## 1. Proč BorgBackup

Klasická záloha často znamená vytvoření další úplné kopie dat. Borg přistupuje k problému jinak.

Při každé záloze vytvoří nový **archiv**, ale data ukládá do repozitáře pomocí deduplikace. Pokud se určitá část souborů mezi dvěma zálohami nezměnila, Borg ji nemusí ukládat znovu.

Výsledkem může být například:

```text
Záloha 1: 100 GB
Záloha 2: +500 MB nových dat
Záloha 3: +200 MB nových dat
Záloha 4: +800 MB nových dat
```

Logická velikost všech archivů tedy může být několik set GB, zatímco skutečně spotřebované místo je výrazně menší.

Borg navíc podporuje:

* deduplikaci,
* kompresi,
* šifrování,
* kontrolu integrity,
* retenční politiku,
* inkrementální ukládání změn,
* obnovu jednotlivých souborů,
* obnovu celých adresářových struktur,
* automatizaci pomocí systemd.

---

# 2. Základní terminologie

Je důležité rozlišovat dvě věci:

## Repository

**Repository** je úložiště, do kterého Borg ukládá zálohovaná data.

Například:

```text
/backup/borg/linux
```

Repository obsahuje Borg metadata, šifrovací klíč a samotné deduplikované datové chunky.

---

## Archive

**Archive** je jeden konkrétní stav zálohovaného systému.

Například:

```text
system-2026-08-30T02:00:00
```

Repository může obsahovat mnoho archivů:

```text
system-2026-08-28T02:00:00
system-2026-08-29T02:00:00
system-2026-08-30T02:00:00
```

Každý archiv představuje pohled na systém v určitém okamžiku.

Díky deduplikaci ale neznamená, že každý archiv obsahuje kompletní fyzickou kopii systému.

---

# 3. Šifrování repository

Při vytváření repository je vhodné použít šifrování:

```bash
borg init --encryption=repokey-blake2 /backup/borg/linux
```

Použitý režim znamená, že:

* data v repository jsou šifrovaná,
* klíč je uložen v repository,
* přístup je chráněn passphrase,
* bez správného klíče a passphrase nelze zálohy jednoduše použít.

Po inicializaci Borg výslovně upozorní, že je nutné bezpečně uložit **Borg key i passphrase**.

To je kriticky důležité.

## Záloha Borg key

Klíč je možné exportovat například:

```bash
borg key export /backup/borg/linux borg-key-backup
```

Případně lze vytvořit i textovou nebo QR reprezentaci podle potřeby.

### Důležité

Borg key **není totéž co passphrase**.

Pro obnovu potřebujete obě části:

```text
Borg key
    +
passphrase
    =
přístup k šifrovanému repository
```

Proto je vhodné mít jejich záložní kopie **mimo samotný zálohovací disk**.

---

# 4. Co zálohovat

Při zálohování celého Linuxového systému typicky nechceme zahrnout virtuální a dočasné filesystemy.

Například:

```text
/proc
/sys
/dev
/run
/tmp
/mnt
/media
/lost+found
```

Tyto adresáře mohou obsahovat:

* dynamické informace poskytované kernelem,
* zařízení,
* runtime data,
* dočasné soubory,
* připojené filesystemy,
* jiné zálohovací cíle.

Typická záloha systému proto může vypadat například takto:

```bash
borg create \
    --stats \
    /backup/borg/linux::system-{now} \
    / \
    --exclude /proc \
    --exclude /sys \
    --exclude /dev \
    --exclude /run \
    --exclude /tmp \
    --exclude /mnt \
    --exclude /media \
    --exclude /lost+found
```

Tím vznikne nový archiv obsahující stav systému v okamžiku vytvoření zálohy.

---

# 5. Co znamená deduplikace v praxi

Borg nerozhoduje pouze podle toho, zda je soubor nový nebo starý.

Data rozděluje na **chunks**.

Pokud například změníme několik KB uvnitř velkého souboru, nemusí být nutné znovu ukládat celý soubor.

Borg znovu použije nezměněné části a uloží pouze nové chunky.

To je jeden z důvodů, proč může být například:

```text
Original size:
150 GB
```

ale:

```text
Deduplicated size:
500 MB
```

pro další archiv.

`Original size` tedy není množství nově uložených dat.

Je to logická velikost dat obsažených v daném archivu.

Pro sledování skutečné spotřeby je důležitější:

```text
Deduplicated size
```

---

# 6. Vytvoření zálohy

Základní příkaz:

```bash
borg create \
    --stats \
    /backup/borg/linux::system-{now} \
    /
```

S výjimkami například:

```bash
borg create \
    --stats \
    /backup/borg/linux::system-{now} \
    / \
    --exclude /proc \
    --exclude /sys \
    --exclude /dev \
    --exclude /run \
    --exclude /tmp \
    --exclude /mnt \
    --exclude /media \
    --exclude /lost+found
```

Borg vypíše například:

```text
Original size
Compressed size
Deduplicated size
```

Tyto hodnoty nám umožní sledovat efektivitu zálohování.

---

# 7. Kontrola záloh

Seznam archivů:

```bash
borg list /backup/borg/linux
```

Informace o repository:

```bash
borg info /backup/borg/linux
```

Kontrola integrity:

```bash
borg check /backup/borg/linux
```

Je dobré rozlišovat:

```text
borg create
```

= vytvoření zálohy

```text
borg list
```

= seznam archivů

```text
borg info
```

= informace o repository

```text
borg check
```

= kontrola integrity

---

# 8. Retenční politika

Postupem času by repository bez omezení rostlo.

Proto je nutné definovat retenční politiku.

Například:

```text
30 denních
12 měsíčních
```

Pomocí:

```bash
borg prune \
    --keep-daily 30 \
    --keep-monthly 12 \
    /backup/borg/linux
```

Pro komplexnější politiku můžeme použít například:

```bash
borg prune \
    --keep-daily 7 \
    --keep-weekly 4 \
    --keep-monthly 12 \
    /backup/borg/linux
```

Před ostrým použitím je vhodné politiku nejprve otestovat:

```bash
borg prune \
    --list \
    --dry-run \
    --keep-daily 30 \
    --keep-monthly 12 \
    /backup/borg/linux
```

`--dry-run` nic nemaže.

Pouze ukáže, které archivy by byly zachovány a které by byly odstraněny.

---

# 9. Proč po prune použít compact

`borg prune` odstraní archivy podle retenční politiky.

Fyzické uvolnění prostoru je ale samostatná operace.

Proto lze následně použít:

```bash
borg compact /backup/borg/linux
```

Typický postup je tedy:

```text
borg create
      ↓
borg prune
      ↓
borg compact
```

Nejdříve vytvoříme zálohu, potom odstraníme staré archivy a nakonec zkompakujeme repository.

---

# 10. Automatizace přes systemd

Zálohování je nejlepší automatizovat.

Nestačí mít perfektní zálohovací skript, pokud si člověk musí každý den vzpomenout, že ho má spustit.

Typická struktura může být:

```text
/root/bin/borg-linux-backup.sh
        │
        ▼
borg-linux-backup.service
        │
        ▼
borg-linux-backup.timer
```

Timer například spouští službu jednou denně.

Kontrola timeru:

```bash
systemctl status borg-linux-backup.timer
```

Seznam naplánovaných timerů:

```bash
systemctl list-timers --all
```

Kontrola služby:

```bash
systemctl status borg-linux-backup.service
```

Log:

```bash
journalctl -u borg-linux-backup.service -n 50 --no-pager
```

Pro delší výpis:

```bash
journalctl -u borg-linux-backup.service --no-pager
```

---

# 11. Passphrase a automatizace

Automatická záloha nemůže čekat na ruční zadání passphrase.

Proto může Borg získávat passphrase například prostřednictvím:

```bash
BORG_PASSCOMMAND
```

Konfigurace s citlivými údaji by měla být:

* přístupná pouze rootovi,
* chráněná vhodnými permissions,
* mimo běžně publikované konfigurace,
* nikdy nezahrnutá do Git repository.

Například:

```bash
chmod 600 /root/.config/borg/linux-backup.conf
```

Samotná passphrase se **nikdy nemá objevit v GitHub Wiki, README, issue, logu ani screenshotu**.

---

# 12. Proč je důležitý test obnovy

Záloha, kterou nikdo nikdy nezkusil obnovit, není ověřená záloha.

Ideální je pravidelně provést alespoň test:

1. vybrat archiv,
2. obnovit jeden soubor,
3. porovnat ho s originálem,
4. případně provést rozsáhlejší test obnovy.

---

# 13. Obnova jednoho souboru

Nejprve zjistíme dostupné archivy:

```bash
borg list /backup/borg/linux
```

Potom si můžeme zobrazit obsah konkrétního archivu:

```bash
borg list /backup/borg/linux::system-2026-08-30T02:00:00
```

Pokud chceme obnovit například:

```text
home/user/example.txt
```

vytvoříme testovací adresář:

```bash
rm -rf /tmp/borg-restore-test
mkdir -p /tmp/borg-restore-test
```

Přejdeme do něj:

```bash
cd /tmp/borg-restore-test
```

A spustíme:

```bash
borg extract \
    /backup/borg/linux::system-2026-08-30T02:00:00 \
    home/user/example.txt
```

## Důležité: Borg nemá `--destination`

Borg `extract` standardně extrahuje soubory do **aktuálního pracovního adresáře**.

Proto je správný postup:

```bash
cd /tmp/borg-restore-test
borg extract ...
```

Výsledkem bude:

```text
/tmp/borg-restore-test/home/user/example.txt
```

---

# 14. Kontrola obnoveného souboru

Po obnově můžeme porovnat checksum:

```bash
sha256sum /home/user/example.txt
sha256sum /tmp/borg-restore-test/home/user/example.txt
```

Pokud jsou hodnoty stejné, obsah souboru je identický.

Automatická kontrola:

```bash
cmp -s \
    /home/user/example.txt \
    /tmp/borg-restore-test/home/user/example.txt \
    && echo "OK - soubor je identický" \
    || echo "CHYBA - soubor se liší"
```

---

# 15. Pozor na vlastnictví obnovených souborů

Pokud spouštíme:

```bash
sudo borg extract ...
```

mohou být obnovené soubory vlastněny rootem.

To je v testovacím adresáři často nežádoucí.

Pokud obnovujeme data pouze pro kontrolu, můžeme po obnově změnit vlastníka:

```bash
sudo chown -R "$USER:$USER" /tmp/borg-restore-test
```

Potom uživatel může obnovené soubory normálně číst.

U skutečné obnovy systému je ale situace jiná — tam je zachování správných vlastníků, skupin a permissions žádoucí a není vhodné mechanicky měnit vlastníka všech obnovených souborů.

---

# 16. Obnova celého systému po havárii

Kompletní obnova je výrazně důležitější než obnova jednoho souboru.

Představme si situaci:

```text
Původní systémový disk
        ↓
      selhal
        ↓
Nový disk
        ↓
Live Linux / instalační prostředí
        ↓
Připojení zálohovacího zařízení
        ↓
Obnova systému z Borg repository
```

Princip je následující.

---

## 16.1 Spustit Live systém

Po havárii je možné spustit například instalační nebo live prostředí Linuxu.

Je nutné mít k dispozici:

* nový nebo opravený systémový disk,
* zálohovací disk,
* BorgBackup,
* Borg repository,
* Borg key,
* passphrase.

---

# 17. Připojení disků

Nejdříve zjistíme dostupné disky:

```bash
lsblk -f
```

Poté vytvoříme mount pointy:

```bash
sudo mkdir -p /mnt/newroot
sudo mkdir -p /mnt/backup
```

Připojíme nový systémový filesystem:

```bash
sudo mount /dev/NEW_ROOT_DEVICE /mnt/newroot
```

A zálohovací filesystem:

```bash
sudo mount /dev/BACKUP_DEVICE /mnt/backup
```

Konkrétní zařízení se samozřejmě liší podle systému.

**Nikdy nekopírujte slepě `/dev/sdX` z návodu.**

Vždy nejdříve ověřte výstup:

```bash
lsblk -f
```

---

# 18. Obnova systému

Pokud je cílový filesystem připojený například jako:

```text
/mnt/newroot
```

přejdeme do něj:

```bash
cd /mnt/newroot
```

Poté lze použít:

```bash
sudo borg extract \
    /mnt/backup/borg/linux::system-ARCHIVE
```

Borg obnoví strukturu systému relativně k aktuálnímu pracovnímu adresáři.

Proto je příprava cílového adresáře zásadní.

---

# 19. Obnova bootloaderu

Samotné obnovení souborů ještě nemusí znamenat, že systém bude bootovat.

Po obnově je potřeba podle použitého systému zkontrolovat zejména:

* `/boot`,
* EFI System Partition,
* `/etc/fstab`,
* UUID filesystemů,
* initramfs,
* bootloader,
* konfiguraci kernelu.

U systému používajícího GRUB může být nutné bootloader znovu nainstalovat.

Například po vstupu do obnoveného systému přes `chroot`:

```bash
mount --bind /dev /mnt/newroot/dev
mount --bind /proc /mnt/newroot/proc
mount --bind /sys /mnt/newroot/sys
mount --bind /run /mnt/newroot/run
```

Poté:

```bash
sudo chroot /mnt/newroot
```

A následné kroky už závisí na distribuci, způsobu bootování a konfiguraci systému.

---

# 20. Kontrola `/etc/fstab`

Po obnově systému je důležité zkontrolovat:

```bash
cat /etc/fstab
```

a:

```bash
lsblk -f
```

UUID filesystemů musí odpovídat skutečným diskům.

Pokud byl vyměněn disk nebo změněno rozložení partitions, může být nutné `fstab` upravit.

---

# 21. Initramfs

Po obnově systému může být vhodné znovu vytvořit initramfs:

```bash
update-initramfs -c -k all
```

Příkaz je závislý na konkrétní distribuci.

---

# 22. Obnova není totéž co klonování disku

Borg není náhrada za bitovou kopii disku.

Neobnovuje například:

```text
MBR
partition table
GPT metadata
boot sektor
```

jako klasický diskový image.

Borg je především **souborový zálohovací systém**.

Výhodou je ale možnost obnovovat:

* jednotlivé soubory,
* adresáře,
* konfiguraci,
* uživatelská data,
* celý filesystem.

---

# 23. Co když původní systém stále funguje?

Při obnově po havárii je nejlepší nejprve vytvořit nový filesystem a obnovovat do něj.

Není dobré bez rozmyslu extrahovat celý archiv přímo přes běžící systém.

Bezpečnější model je:

```text
nový filesystem
       ↓
mount
       ↓
Borg extract
       ↓
kontrola
       ↓
bootloader
       ↓
restart
       ↓
test systému
```

---

# 24. Kontrola po obnově

Po prvním bootu je vhodné zkontrolovat:

```bash
systemctl --failed
```

Dále:

```bash
systemctl status
```

a například:

```bash
journalctl -b -p err
```

Kontrola disků:

```bash
lsblk -f
```

Kontrola prostoru:

```bash
df -hT
```

Kontrola základních služeb:

```bash
systemctl list-units --failed
```

Pokud žádná služba neselhala:

```text
0 loaded units listed.
```

je to dobrý signál, ale stále je nutné ověřit aplikace a data.

---

# 25. Jak vypadá rozumná zálohovací architektura

Jednoduchý návrh:

```text
                  LINUX SYSTEM
                       │
                       │ borg create
                       ▼
              ┌──────────────────┐
              │   Borg Repository │
              │                  │
              │ encrypted        │
              │ deduplicated     │
              │ compressed       │
              └────────┬─────────┘
                       │
                borg prune
                       │
                       ▼
                Retention policy
                       │
                       ▼
                   borg compact
```

Automatizace:

```text
systemd timer
      │
      ▼
backup service
      │
      ▼
backup script
      │
      ├── borg create
      ├── borg prune
      └── borg compact
```

---

# 26. Co je potřeba chránit stejně jako samotná data

Největší chyba zálohovacího systému může být:

> Mám perfektní zálohu, ale nemám způsob, jak ji odemknout.

Proto musí být chráněny minimálně:

```text
Borg repository
        +
Borg key
        +
Borg passphrase
        +
informace potřebné k obnově
```

Doporučení:

* repository držet na jiném zařízení než systém,
* Borg key uložit na bezpečné oddělené místo,
* passphrase neukládat pouze na zálohovaný systém,
* dokumentovat postup obnovy,
* pravidelně testovat obnovu.

---

# 27. Co nikdy nedávat do veřejného repozitáře

Do GitHub repository ani Wiki nepatří:

```text
Borg passphrase
Borg key
Repository ID, pokud není důvod jej zveřejňovat
interní IP adresy
hostname
osobní adresáře
osobní data
přístupové údaje
API tokeny
SSH private keys
```

Veřejný návod má používat pouze obecné příklady:

```text
/backup/borg/linux
user
example.txt
SERVER
BACKUP_DEVICE
```

Nikoli skutečné údaje produkčního systému.

---

# 28. Doporučený minimální checklist

## Před zálohováním

```bash
borg info /backup/borg/linux
```

## Vytvoření zálohy

```bash
borg create \
    --stats \
    /backup/borg/linux::system-{now} \
    /
```

## Kontrola archivů

```bash
borg list /backup/borg/linux
```

## Retence

```bash
borg prune \
    --dry-run \
    --list \
    --keep-daily 30 \
    --keep-monthly 12 \
    /backup/borg/linux
```

## Údržba

```bash
borg compact /backup/borg/linux
```

## Kontrola integrity

```bash
borg check /backup/borg/linux
```

## Kontrola automatizace

```bash
systemctl status borg-linux-backup.timer
```

## Kontrola posledního běhu

```bash
journalctl -u borg-linux-backup.service -n 50 --no-pager
```

## Test obnovy

```bash
mkdir -p /tmp/borg-restore-test
cd /tmp/borg-restore-test

borg extract \
    /backup/borg/linux::system-ARCHIVE \
    path/to/example.txt
```

---

# 29. Závěr

BorgBackup je velmi praktický způsob, jak vytvořit dlouhodobě použitelný zálohovací systém pro Linux.

Jeho hlavní výhody jsou:

* deduplikace,
* komprese,
* šifrování,
* práce s jednotlivými archivy,
* flexibilní retence,
* kontrola integrity,
* snadná obnova jednotlivých souborů,
* možnost obnovy celého filesystemu,
* automatizace přes systemd.

Nejdůležitější princip ale není žádný konkrétní příkaz.

Je to tento:

> **Záloha není hotová ve chvíli, kdy byla vytvořena. Záloha je hotová ve chvíli, kdy jsme schopni data úspěšně obnovit.**

Proto má smysl nejen pravidelně spouštět:

```text
borg create
```

ale také pravidelně kontrolovat:

```text
borg check
```

a především prakticky testovat:

```text
borg extract
```

Pokud je repository šifrované, je stejně důležité bezpečně uchovat Borg key a passphrase.

Dobře navržený zálohovací systém tak není pouze automatické kopírování dat.

Je to celý proces:

```text
CREATE
  ↓
VERIFY
  ↓
RETAIN
  ↓
COMPACT
  ↓
TEST RESTORE
  ↓
DISASTER RECOVERY
```

A právě schopnost projít posledními dvěma kroky rozhoduje o tom, zda máme skutečnou zálohu, nebo pouze falešný pocit bezpečí.
