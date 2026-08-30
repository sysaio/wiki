---
title: borg – zalohovaci system
category: Počítače
tags: [linux, zalohy, backup]
last_update: 2026-08-30
---

BorgBackup: jak funguje moderní zálohování systému a dokumentů

BorgBackup je nástroj pro vytváření deduplikovaných, komprimovaných a šifrovaných záloh. Na první pohled může připomínat klasické tar nebo rsync, ale jeho princip je výrazně jiný.

Místo toho, aby při každé záloze vytvářel další kompletní kopii všech souborů, rozděluje data na bloky — chunky — a ukládá pouze bloky, které v repozitáři ještě nejsou.

Výsledkem je, že každá záloha může vypadat jako kompletní snapshot systému, ale fyzicky na disku obvykle zabírá pouze prostor odpovídající novým nebo změněným datům.

1. Borg pracuje s repozitářem

Základním prvkem BorgBackup není jednotlivý .tar soubor, ale repository.

V našem případě máme například systémový repozitář:

/mnt/data/0_backup_0/0_backup_LINUX_0

A samostatný repozitář pro dokumenty:

/root/.backup_DOCUMENTS_0

Do repozitáře Borg ukládá jednotlivé archives.

Například:

system-2026-08-27T07:14:33
system-2026-08-27T18:32:05
system-2026-08-28T12:16:53
system-2026-08-29T00:00:04
system-2026-08-30T14:10:30

U dokumentů obdobně:

docs-2026-08-30T14:12:58

Archive je tedy konkrétní bod v čase, ke kterému můžeme data obnovit.

2. Snapshot neznamená další kompletní kopii

To je jedna z nejdůležitějších vlastností Borgu.

Představme si, že máme systém o velikosti přibližně 150 GB.

První záloha může do repozitáře uložit desítky gigabajtů nových dat. Další záloha ale nemusí znovu uložit všech 150 GB.

Pokud se změnily například pouze:

systémové logy,
několik konfiguračních souborů,
aktualizované programy,
několik souborů v /home,

Borg uloží pouze nové chunky.

Proto můžeme mít například:

Archive:
Original size:      150 GB
Compressed size:    108 GB
Deduplicated size:  450 MB

To neznamená, že archiv obsahuje pouze 450 MB dat.

Znamená to, že pro vytvoření tohoto nového snapshotu bylo v repozitáři potřeba uložit pouze přibližně 450 MB nových dat. Ostatní chunky už v repozitáři existovaly.

Každý archive přesto představuje kompletní pohled na zálohovaný strom v daném okamžiku.

3. Deduplikace

Borg rozděluje soubory na chunky a ty identifikuje.

Pokud se stejný obsah objeví ve více souborech nebo v různých archivech, nemusí být uložen znovu.

To je deduplikace.

Výhoda je největší právě u pravidelných záloh systému.

První záloha:

150 GB systému
→ velké množství nových chunků

Druhá záloha:

150 GB systému
→ většina chunků už existuje
→ uloží se pouze nové/změněné chunky

Třetí záloha funguje stejně.

Díky tomu můžeme vytvářet mnoho historických bodů obnovy, aniž bychom potřebovali mnoho násobků velikosti zdrojových dat.

4. Komprese

Borg může data zároveň komprimovat.

V systémovém repozitáři používáme konfiguraci založenou na Borgu a při zálohování dokumentů explicitně používáme:

--compression lz4

Komprese zmenšuje množství dat, která musí být fyzicky uložena.

Je důležité rozlišovat:

Original size
Compressed size
Deduplicated size

Například:

Original size:      150.20 GB
Compressed size:    108.08 GB
Deduplicated size:   81.15 MB

Tato tři čísla popisují různé věci.

5. Šifrování

Systémový repozitář byl vytvořen režimem:

repokey-blake2

Borg tedy chrání obsah repozitáře šifrováním.

Zároveň je potřeba pamatovat na jednu zásadní věc:

Nestačí mít pouze heslo.

U režimu repokey je klíč uložen přímo v repozitáři.

Proto je pro obnovu potřeba mít k dispozici:

samotný Borg repozitář,
Borg key,
heslo ke klíči.

Proto jsme také vytvořili zálohu Borg klíče.

To je stejně důležité jako samotné zálohy.

6. Proč nestačí zálohovat pouze heslo

Představme si havárii datového disku.

Máme:

Borg repository

ale nemáme exportovaný key.

Nebo naopak máme key, ale neznáme jeho passphrase.

V obou případech může být obnova prakticky nemožná.

Proto je vhodné mít zabezpečené kopie:

Borg repository
+
Borg key
+
passphrase

A tyto tři věci neskladovat pouze na stejném disku.

7. Borg archive jako bod v čase

Každý archive můžeme chápat jako snapshot systému.

Například:

system-2026-08-27T07:14:33
system-2026-08-27T18:32:05
system-2026-08-28T12:16:53
system-2026-08-29T00:00:04
system-2026-08-30T14:10:30

Můžeme si tedy vybrat, ke kterému okamžiku chceme systém nebo soubor vrátit.

Například:

borg list /mnt/data/0_backup_0/0_backup_LINUX_0

nám zobrazí dostupné snapshoty.

8. Retence

Počet snapshotů nemusí růst do nekonečna.

Proto používáme:

borg prune

V našem případě systémová záloha používá například:

keep-daily 30
keep-monthly 12

Borg potom rozhoduje, které archive zachovat a které odstranit.

Důležité je, že prune nemaže bezhlavě data potřebná pro ostatní snapshoty.

Protože Borg používá deduplikované chunky, odstranění archive znamená odstranění pouze těch dat, která už nejsou potřebná žádným zachovaným archivem.

Po prune může následovat:

borg compact

který umožní repozitáři uvolnit prostor, který už není potřeba.

9. Proč tedy nepotřebujeme každý měsíc fyzický full backup?

Klasický systém může být navržen například takto:

pondělí → inkrementální
úterý → inkrementální
...
1. den měsíce → full backup

Borg tento koncept nepotřebuje stejným způsobem.

Každý archive se chová jako kompletní snapshot, ale díky deduplikaci není nutné pokaždé fyzicky ukládat celý systém.

Můžeme tedy mít:

30 denních bodů obnovy
+
12 měsíčních bodů obnovy

bez toho, aby každý z nich byl samostatnou 150GB kopií systému.

To je jedna z hlavních výhod Borgu.

10. Systém a dokumenty jsou dva různé typy dat

V naší architektuře jsou zálohovány dvě důležité oblasti.

Systém

Zdroj:

/

s vynecháním pseudo-filesystémů a dalších oblastí, které nemají být zálohovány:

/proc
/sys
/dev
/run
/tmp
/mnt
/media
/lost+found

Cíl:

/mnt/data/0_backup_0/0_backup_LINUX_0
Dokumenty

Zdroj:

/mnt/data/0_docum_0

Cíl:

/root/.backup_DOCUMENTS_0

Oddělení repozitářů je záměrné.

Systémová záloha je uložena na datovém disku, zatímco dokumentová záloha je umístěna na systémovém NVMe.

Tím vzniká určitá redundance i mezi samotnými úložišti.

11. Automatické zálohování

Ruční spuštění zálohy je možné:

sudo /root/bin/borg-linux-backup.sh

Ale cílem je, aby zálohování běželo automaticky.

Systémová záloha je proto spuštěna pomocí:

borg-linux-backup.service

a:

borg-linux-backup.timer

Timer je aktivní například jako:

borg-linux-backup.timer
    active (waiting)

a naplánuje spuštění služby.

Výhodou systemd oproti jednoduchému cron jobu je například dobrá integrace do systémového logování.

Historii běhu můžeme zobrazit:

sudo journalctl -u borg-linux-backup.service

nebo například posledních 50 řádků:

sudo journalctl -u borg-linux-backup.service -n 50 --no-pager
12. Jak poznat, že záloha proběhla

Nestačí pouze věřit, že timer existuje.

Kontrolujeme několik věcí.

Timer:

systemctl status borg-linux-backup.timer --no-pager

Poslední běh služby:

systemctl status borg-linux-backup.service --no-pager

Historii:

sudo journalctl -u borg-linux-backup.service -n 50 --no-pager

A skutečný obsah repozitáře:

sudo env BORG_PASSCOMMAND='cat /root/.config/borg/passphrase' \
    borg list /mnt/data/0_backup_0/0_backup_LINUX_0

Tím ověřujeme nejen to, že timer existuje, ale že skutečně vznikají nové archivy.

13. Borg versus rsync

rsync nám dlouhou dobu dobře sloužil.

Je jednoduchý, rychlý a výborný pro synchronizaci adresářů.

Například:

zdroj → přesná kopie cíle

Borg ale přináší jiný model:

zdroj
  ↓
snapshot
  ↓
deduplikace
  ↓
komprese
  ↓
šifrování
  ↓
historie snapshotů

Proto jsme se rozhodli přejít na Borg jako jednotný zálohovací mechanismus.

rsync tedy není potřeba dále používat jako hlavní backup engine. Historické skripty a zkušenosti s ním ale mají smysl zachovat jako dokumentaci vývoje systému.

14. Co Borg neřeší

Borg není kompletní disaster-recovery řešení sám o sobě.

Neřeší například:

dostupnost záložního disku,
požár nebo krádež celého počítače,
ztrátu všech kopií uložených na jednom místě,
ztrátu Borg key,
ztrátu passphrase,
automatické znovunainstalování operačního systému.

Proto je skutečná strategie:

Borg
+
bezpečně uložený key
+
bezpečně uložená passphrase
+
samostatné úložiště / další kopie
+
otestovaný postup obnovy

Nejdůležitější část posledního bodu je slovo otestovaný.

Záloha, kterou jsme nikdy nezkusili obnovit, není stejně důvěryhodná jako záloha, jejíž obnovu jsme ověřili.

15. Shrnutí

BorgBackup nám umožňuje používat jednoduchý model:

             ┌────────────────────┐
             │      SYSTÉM        │
             │         /          │
             └─────────┬──────────┘
                       │
                       ▼
                 Borg archive
                       │
              deduplikace + komprese
                       │
                       ▼
          /mnt/data/.../LINUX_0

a současně:

          /mnt/data/0_docum_0
                    │
                    ▼
              Borg archive
                    │
           deduplikace + komprese
                    │
                    ▼
          /root/.backup_DOCUMENTS_0

Výsledkem není pouze jedna kopie dat.

Výsledkem je historie bodů obnovy, ze kterých můžeme podle potřeby obnovit jednotlivé soubory, adresáře nebo celý systém.

A právě proto je Borg velmi vhodný jako centrální backup engine pro koncept ZXLK.

Obnova dat pomocí BorgBackup po havárii

Zálohování má smysl pouze tehdy, pokud víme, jak data skutečně obnovit.

Tento návod popisuje obnovu jednotlivých souborů i kompletního systému ze záloh BorgBackup používaných v systému ZXLK.

Princip je jednoduchý:

Borg repository
      ↓
vybraný archive
      ↓
borg extract
      ↓
obnovené soubory

Při havárii celého systému je postup rozšířen o spuštění záchranného systému, připojení disků a následnou obnovu systémového stromu.

1. Co potřebujeme k obnově

Pro obnovu zašifrovaného Borg repozitáře potřebujeme:

Borg repository,
Borg key,
passphrase.

V našem systému je systémový repozitář:

/mnt/data/0_backup_0/0_backup_LINUX_0

Borg repozitář je šifrovaný režimem:

repokey-blake2

Proto je nutné mít bezpečně uložený také exportovaný Borg key.

2. Nejprve zjistíme dostupné zálohy

Pokud systém ještě běží, můžeme vypsat archivy:

sudo env BORG_PASSCOMMAND='cat /root/.config/borg/passphrase' \
    borg list /mnt/data/0_backup_0/0_backup_LINUX_0

Výsledek může vypadat například:

system-2026-08-27T07:14:33
system-2026-08-27T18:32:05
system-2026-08-28T12:16:53
system-2026-08-29T00:00:04
system-2026-08-30T14:10:30

Každý řádek představuje jeden bod obnovy.

Při obnově vybíráme konkrétní archive.

3. Obnova jednoho souboru

Nejbezpečnější způsob, jak si ověřit funkčnost zálohy, je obnovit nejprve jediný soubor do dočasného adresáře.

Například:

rm -rf /tmp/borg-restore-test
mkdir -p /tmp/borg-restore-test
cd /tmp/borg-restore-test

Potom spustíme Borg:

sudo env BORG_PASSCOMMAND='cat /root/.config/borg/passphrase' \
    borg extract \
    /mnt/data/0_backup_0/0_backup_LINUX_0::system-2026-08-30T14:10:30 \
    home/liko/bin/README.md

Důležitá věc:

borg extract nepoužívá parametr --destination.

Borg extrahuje soubory do aktuálního pracovního adresáře.

Proto je správný postup:

cd /tmp/borg-restore-test

a teprve potom:

borg extract ...
4. Proč se v příkazu nepíše /home/liko/...

Cesta předaná borg extract je relativní cesta uvnitř archive.

Proto používáme:

home/liko/bin/README.md

a ne:

/home/liko/bin/README.md

Borg potom vytvoří:

/tmp/borg-restore-test/home/liko/bin/README.md
5. Kontrola obnoveného souboru

Po obnově můžeme porovnat hash původního a obnoveného souboru:

sha256sum /home/liko/bin/README.md
sha256sum /tmp/borg-restore-test/home/liko/bin/README.md

Pokud jsou SHA-256 hodnoty stejné, obsah souborů je identický.

Ještě přímější kontrola je:

cmp -s \
    /home/liko/bin/README.md \
    /tmp/borg-restore-test/home/liko/bin/README.md \
    && echo "OK - soubor je identický" \
    || echo "CHYBA - soubor se liší"
6. Pozor na oprávnění při testovací obnově

Pokud použijeme:

sudo borg extract ...

Borg může obnovit metadata a vlastníka odpovídající původnímu systému.

Proto může být obnovený soubor vlastněný například root.

Při testovací obnově do /tmp je možné po extrakci změnit vlastníka:

sudo chown -R "$USER:$USER" /tmp/borg-restore-test

Potom už můžeme soubory pohodlně číst jako běžný uživatel.

U skutečné obnovy systému ale není správné plošně měnit vlastníky na běžného uživatele. Tam chceme zachovat původní vlastníky, skupiny a oprávnění.

7. Obnova celého adresáře

Stejným způsobem můžeme obnovit například celý adresář:

cd /tmp/borg-restore-test

sudo env BORG_PASSCOMMAND='cat /root/.config/borg/passphrase' \
    borg extract \
    /mnt/data/0_backup_0/0_backup_LINUX_0::system-2026-08-30T14:10:30 \
    home/liko/bin

Borg obnoví strom:

/tmp/borg-restore-test/home/liko/bin/
8. Obnova dokumentů

Dokumenty mají vlastní Borg repozitář:

/root/.backup_DOCUMENTS_0

Nejdříve zobrazíme dostupné snapshoty:

sudo env BORG_PASSCOMMAND='cat /root/.config/borg/passphrase' \
    borg list /root/.backup_DOCUMENTS_0

Můžeme potom například obnovit dokumenty do dočasného adresáře:

rm -rf /tmp/borg-documents-restore
mkdir -p /tmp/borg-documents-restore
cd /tmp/borg-documents-restore

A spustit:

sudo env BORG_PASSCOMMAND='cat /root/.config/borg/passphrase' \
    borg extract \
    /root/.backup_DOCUMENTS_0::docs-2026-08-30T14:12:58

Po dokončení bude obnovený strom odpovídat cestě uložené v archive.

9. Obnova celého systému

Obnova celého Linuxového systému je jiná než obnova jednoho souboru.

Pokud operační systém stále funguje, můžeme některé části obnovovat přímo.

Pokud je ale systémový disk poškozený nebo systém vůbec nenabootuje, je lepší postupovat z Live Linuxu nebo jiného záchranného systému.

Důvod je jednoduchý:

Neměli bychom se pokoušet přepisovat právě běžící /.

10. Záchranný systém

Po spuštění Live systému nejprve zjistíme disky:

lsblk -f

a filesystémy:

blkid

Následně připojíme:

systémový disk,
disk obsahující Borg repository,
případné další potřebné filesystémy.

Je velmi důležité ověřit, že jsme připojili správné zařízení.

Před jakýmkoli mazáním nebo obnovou systému je vhodné několikrát ověřit:

lsblk -f
findmnt
df -hT
11. Připojení cílového systému

Předpokládejme například, že nový nebo opravený systémový filesystem připojíme do:

/mnt/target

Pak by jeho strom měl vypadat přibližně:

/mnt/target/etc
/mnt/target/home
/mnt/target/usr
/mnt/target/var
/mnt/target/boot
...

Borg ale musí obnovovat data do tohoto stromu.

Proto použijeme:

cd /mnt/target

a následně:

borg extract ...
12. Obnova systémového archive

Po připojení repozitáře a cílového filesystemu vybereme konkrétní archive.

Například:

system-2026-08-30T14:10:30

Potom:

cd /mnt/target

sudo env BORG_PASSCOMMAND='cat /root/.config/borg/passphrase' \
    borg extract \
    /mnt/data/0_backup_0/0_backup_LINUX_0::system-2026-08-30T14:10:30

Borg začne obnovovat celý strom archive do:

/mnt/target/

To znamená například:

/mnt/target/etc
/mnt/target/home
/mnt/target/usr
/mnt/target/var
/mnt/target/opt
...
13. Co bylo ze systémové zálohy vyloučeno

Naše systémová záloha nezahrnuje některé dynamické nebo externě připojené oblasti:

/proc
/sys
/dev
/run
/tmp
/mnt
/media
/lost+found

To je záměrné.

Tyto adresáře není vhodné obnovovat jako běžná statická data.

Po bootu Linux tyto oblasti znovu vytvoří nebo připojí podle aktuální konfigurace.

14. Po obnově systému

Po obnovení dat je potřeba zkontrolovat zejména:

/etc/fstab
/etc/systemd/
/etc/network/
/etc/ssh/
/etc/nut/
/home/

a další konfiguraci, která je pro konkrétní počítač důležitá.

Následně je potřeba ověřit bootloader a případně jej znovu nainstalovat.

U systému s UEFI je nutné také správně připojit EFI System Partition a obnovit případné bootovací soubory.

Přesný postup závisí na rozložení disků a způsobu instalace systému.

15. Obnova není jen borg extract

Kompletní disaster recovery proto vypadá přibližně takto:

Havárie
   │
   ▼
Live / Rescue Linux
   │
   ├── zjistit disky
   ├── připojit cílový systém
   ├── připojit Borg repository
   ├── zpřístupnit Borg key
   ├── zadat passphrase
   │
   ▼
vybrat archive
   │
   ▼
borg extract
   │
   ▼
zkontrolovat filesystem
   │
   ▼
zkontrolovat bootloader
   │
   ▼
restart
   │
   ▼
kontrola systemd služeb
16. Kontrola po restartu

Po úspěšné obnově systému je potřeba ověřit, že Linux normálně naběhl.

Základ:

systemctl --failed

Ideální výsledek je:

0 loaded units listed.

Dále:

systemctl status

a pro důležité služby například:

systemctl status borg-linux-backup.timer --no-pager
systemctl status borg-linux-backup.service --no-pager
systemctl status movie-converter.service --no-pager

Případně:

systemctl list-timers --all --no-pager
17. Kontrola Borgu po obnově

Nejdříve:

borg info /mnt/data/0_backup_0/0_backup_LINUX_0

Potom můžeme provést kontrolu repozitáře:

borg check /mnt/data/0_backup_0/0_backup_LINUX_0

U rozsáhlejšího repozitáře může kontrola nějakou dobu trvat.

Je také vhodné zkontrolovat, že existují očekávané archivy:

borg list /mnt/data/0_backup_0/0_backup_LINUX_0
18. Test obnovy je stejně důležitý jako samotná záloha

Jednou z nejlepších kontrol je obnovit náhodně vybraný soubor do /tmp:

rm -rf /tmp/borg-restore-test
mkdir -p /tmp/borg-restore-test

cd /tmp/borg-restore-test

sudo env BORG_PASSCOMMAND='cat /root/.config/borg/passphrase' \
    borg extract \
    /mnt/data/0_backup_0/0_backup_LINUX_0::system-2026-08-30T14:10:30 \
    home/liko/bin/README.md

A potom ověřit:

sha256sum /home/liko/bin/README.md
sha256sum /tmp/borg-restore-test/home/liko/bin/README.md

Stejný hash znamená, že obnovený obsah je identický s originálem.

19. Co dělat při úplné ztrátě počítače

Pokud dojde k úplné fyzické havárii počítače, potřebujeme:

nový disk
   +
Live Linux
   +
Borg repository
   +
Borg key
   +
passphrase

Nejprve nainstalujeme nebo připravíme základní Linuxové prostředí, připravíme filesystémy a následně obnovíme systém z Borg archive.

Důležité je neobnovovat slepě na špatně identifikovaný disk.

Před destruktivními operacemi vždy ověřujeme:

lsblk -f
findmnt
20. Nejdůležitější pravidlo

Borg záloha není pouze soubor někde na disku.

Je to kombinace:

REPOSITORY
+
KEY
+
PASSPHRASE
+
POSTUP OBNOVY

Pokud některá část chybí, může být obnova výrazně komplikovanější nebo nemožná.

Proto by měl být Borg key exportovaný a uložený na bezpečném místě.

Stejně tak musí být bezpečně uložená passphrase.

21. Praktický krizový tahák
Chci obnovit jeden soubor
mkdir -p /tmp/borg-restore-test
cd /tmp/borg-restore-test

sudo env BORG_PASSCOMMAND='cat /root/.config/borg/passphrase' \
    borg extract \
    /mnt/data/0_backup_0/0_backup_LINUX_0::ARCHIVE \
    CESTA/K/SOUBORU
Chci zobrazit snapshoty
sudo env BORG_PASSCOMMAND='cat /root/.config/borg/passphrase' \
    borg list /mnt/data/0_backup_0/0_backup_LINUX_0
Chci obnovit dokumenty
mkdir -p /tmp/borg-documents-restore
cd /tmp/borg-documents-restore

sudo env BORG_PASSCOMMAND='cat /root/.config/borg/passphrase' \
    borg extract \
    /root/.backup_DOCUMENTS_0::ARCHIVE
Chci obnovit celý systém
1. Spustit Live/Rescue Linux
2. Identifikovat disky
3. Připojit cílový systém do /mnt/target
4. Zpřístupnit Borg repository
5. Zpřístupnit Borg key
6. Zajistit passphrase
7. cd /mnt/target
8. borg extract vybraný system archive
9. zkontrolovat bootloader a filesystem
10. restartovat
11. zkontrolovat systemd
12. zkontrolovat Borg
13. provést testovací obnovu souboru
22. Závěr

Smyslem zálohovacího systému není mít krásný výpis:

Backup completed successfully.

Smyslem je být schopen po havárii říct:

„Mám poslední použitelný snapshot, mám Borg key, znám passphrase a vím přesně, jak ho obnovit.“

Právě proto je dobré obnovu pravidelně testovat.

V našem případě máme oddělený Borg repozitář pro systém a dokumenty, automatické vytváření systémových snapshotů pomocí systemd timeru, automatickou retenci a kompakci repozitářů a ověřený postup pro obnovu jednotlivých souborů.

Dalším krokem je otestovat celý řetězec po restartu systému a ověřit, že nejen Borg, ale také všechny důležité služby ZXLK po rebootu normálně naběhnou.



