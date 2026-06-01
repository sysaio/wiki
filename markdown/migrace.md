---
title: backup – zálohování do RPi5
category: Počítače
tags: [linux, zalohovani, RPi, kyberbezpečnost]
last_update: 2025-07-19
---

# 🗺️ Kompletní průvodce: Přesun Kubuntu na nové PC a vytvoření zrcadla (RAID 1)

Tento dokument slouží jako ucelený návod pro bezpečné zálohování, fyzický přesun systému Kubuntu na nový hardware a následné vytvoření živého softwarového zrcadla (RAID 1) ze dvou 256GB SATA SSD disků.

---

## 📦 1. Přenesení Linux instalace na jiný počítač (Záloha)

### Krok 1.1: Zjištění označení disků v Live distru
Nabootuj do Live USB Kubuntu, otevři terminál a ověř si aktuální strukturu disků:
```bash
lsblk
```

**Příklad výstupu (output):**
```text
sda           8:0    0 238,5G  0 disk
├─sda1        8:1    0   300M  0 part /boot/efi
└─sda2        8:2    0 238,2G  0 part /
sdb           8:16   0   7,3T  0 disk
└─sdb1        8:17   0   7,3T  0 part /mnt/data
sdc           8:32   1  14,4G  0 disk
├─sdc1        8:33   1  14,4G  0 part /media/liko/YUMI
└─sdc2        8:34   1    32M  0 part
nvme0n1     259:0    0   1,9T  0 disk
└─nvme0n1p1 259:1    0   1,9T  0 part /media/liko/Movie
```
* **`sda`** => Systémový disk (SanDisk 256GB)
* **`sdb`** => Datový disk (WD 8TB)

### Krok 1.2: Připojení (mount) 8TB datového disku
Vytvoř adresář a připoj do něj oddíl z velkého disku, kam se bude záloha ukládat:
```bash
sudo mkdir -p /mnt/data
sudo mount /dev/sdb1 /mnt/data
```

### Krok 1.3: Vytvoření bitové kopie (zálohy)
Tento příkaz vezme celý 256GB SanDisk (`/dev/sda`), za běhu ho zkomprimuje (aby nezabíral zbytečně moc místa) a uloží jako jeden soubor na 8TB disk. V terminálu uvidíš i ukazatel průběhu:

```bash
sudo dd if=/dev/sda status=progress | gzip > /mnt/data/kubuntu_bocxod_20260531.img.gz
```

> ⚠️ **Pozor:** Dvakrát si zkontroluj, že za `if=` dáváš opravdu ten správný 256GB systémový disk (`/dev/sda`), ať si omylem nepřepíšeš data!

### Krok 1.4: Ověření zálohy
Až proces skončí, ověř si, že se soubor na disku úspěšně vytvořil a má platnou velikost:
```bash
ls -lh /mnt/data/kubuntu_bocxod_20260531.img.gz
```
Nyní můžeš počítač vypnout a fyzicky přesunout disky (SanDisk i Micron) do nového PC.

---

## 🛠️ 2. Vytvoření RAID 1 (Zrcadla) zaživa na novém PC

Jakmile nabootuješ stávající systém v novém počítači, ověř si nová písmena disků pomocí `lsblk`. V této části návodu počítáme s tím, že:
* `/dev/sda` = Původní disk **SanDisk** (obsahuje běžící systém Kubuntu).
* `/dev/sdb` = Nový prázdný disk **Micron** (který přidáváme do zrcadla).

### Krok 2.1: Příprava nového disku (Micron)
1. **Zkopírujte tabulku oddílů ze SanDisku na Micron:**
   ```bash
   sudo sfdisk -d /dev/sda | sudo sfdisk /dev/sdb
   ```
2. **Změňte typ hlavního datového oddílu na Micronu na RAID:**
   *(Předpokládáme, že systémový oddíl je číslo 2, tedy `/dev/sdb2`)*
   ```bash
   sudo sgdisk -t 2:fd00 /dev/sdb
   ```

### Krok 2.2: Vytvoření degradovaného RAID pole
Vytvoříme zrcadlo pouze s jedním diskem (Micron). SanDisk zatím necháme jako chybějící (`missing`), protože z něj systém aktuálně běží.
1. **Vytvořte RAID pole `/dev/md0`:**
   ```bash
   sudo mdadm --create /dev/md0 --level=1 --raid-devices=2 missing /dev/sdb2
   ```
2. **Vytvořte na novém RAID poli souborový systém (EXT4):**
   ```bash
   sudo mkfs.ext4 /dev/md0
   ```

### Krok 2.3: Překopírování systému ze SanDisku na RAID
1. **Připojte nové RAID pole do dočasného adresáře:**
   ```bash
   sudo mkdir /mnt/novy_raid
   sudo mount /dev/md0 /mnt/novy_raid
   ```
2. **Překopírujte systém pomocí nástroje rsync:**
   ```bash
   sudo rsync -axHAWXS --numeric-ids --progress / /mnt/novy_raid/
   ```

### Krok 2.4: Aktualizace konfigurace (UUID a Grub)
1. **Zjistěte nové UUID pro `/dev/md0`:**
   ```bash
   sudo blkid /dev/md0
   ```
2. **Upravte soubor fstab na novém disku:**
   ```bash
   sudo nano /mnt/novy_raid/etc/fstab
   ```
   *(Nahraďte staré UUID kořenového adresáře `/` novým UUID pole `/dev/md0`)*
3. **Propojte systémové složky pro chroot (prostředí nového disku):**
   ```bash
   sudo mount --bind /dev /mnt/novy_raid/dev
   sudo mount --bind /proc /mnt/novy_raid/proc
   sudo mount --bind /sys /mnt/novy_raid/sys
   ```
4. **Přepněte se do prostředí nového disku:**
   ```bash
   sudo chroot /mnt/novy_raid
   ```
5. **Uložte konfiguraci RAIDu a aktualizujte zavaděč GRUB:**
   ```bash
   mdadm --detail --scan >> /etc/mdadm/mdadm.conf
   update-initramfs -u
   update-grub
   ```
6. **Ukončete chroot:**
   ```bash
   exit
   ```

### Krok 2.5: První restart do RAIDu
Restartuj počítač a v BIOSu základní desky vyber jako bootovací disk **Micron**. Po naběhnutí ověř funkčnost:
```bash
df -h /
```
*(Měl bys vidět, že kořenový adresář běží z `/dev/md0`)*

### Krok 2.6: Přidání starého SanDisku do zrcadla
1. **Změňte typ oddílu na starém SanDisku na Linux RAID:**
   ```bash
   sudo sgdisk -t 2:fd00 /dev/sda
   ```
2. **Přidejte oddíl do stávajícího RAID pole:**
   ```bash
   sudo mdadm --manage /dev/md0 --add /dev/sda2
   ```
3. **Sledujte průběh synchronizace (zrcadlení) v reálném čase:**
   ```bash
   watch cat /proc/mdstat
   ```

---

## 🧰 3. Tipy pro další postup a užitečné nástroje

Po úspěšném zprovoznění zrcadla a ověření stability systému na novém hardwaru doporučuji doinstalovat tyto balíčky pro správu a údržbu:

### Sledování zdraví a stavu RAID pole
* **`mdadm` monitorovací služba:** Automaticky posílá upozornění, pokud jeden z disků v zrcadle selže.
* **Mailing systému:** Pro nastavení upozornění na e-mail nainstaluj `bsd-mailx` nebo `postfix`.
* **Smartmontools:** Nástroj pro sledování S.M.A.R.T. hodnot (zdraví a opotřebení obou SSD).
  ```bash
  sudo apt install smartmontools
  ```

### Diagnostika a přehled hardwaru v Kubuntu
* **Kinfocenter:** Nativní KDE aplikace, která ti v grafickém rozhraní ukáže podrobný přehled o novém procesoru, pamětech a grafice.
* **GSmartControl:** Grafické rozhraní pro kontrolu zdraví disků.
  ```bash
  sudo apt install gsmartcontrol
  ```
* **Btop / Htop:** Moderní a přehledné terminálové správce úloh pro monitorování zátěže nového procesoru a RAM.
  ```bash
  sudo apt install btop
  ```

### Plánování upgradu systému
* Jakmile systém poběží stabilně v zrcadle na novém hardwaru, můžeš bezpečně spustit upgrade z verze **24.04 LTS** na novější **26.04 LTS s prostředím Plasma 6**.
* Před samotným upgradem stačí zadat:
  ```bash
  sudo do-release-upgrade -m desktop
  ```

---

## 🔗 4. Zdrojové reference

Při řešení problémů nebo hledání pokročilých parametrů konfigurace softwarového RAIDu v Linuxu se můžeš opřít o tyto oficiální zdroje:

* **Mdadm příručka (Ubuntu Manpages):** [://ubuntu.com - mdadm](https://://ubuntu.com/)
* **Linux RAID Wiki:** [raid.wiki.kernel.org](https://kernel.org)
* **Ubuntu Advanced Installation Guide:** Oficiální dokumentace pro správu disků a polí mdadm.
* **GNU Coreutils (dd manual):** Dokumentace k nástroji `dd` pro bezpečné nízkoúrovňové klonování disků.



