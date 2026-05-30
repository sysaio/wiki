---
title: fdupes – hledání a mazání duplicitních souborů
category: Počítače
tags: [linux, mazani, soubory, duplicity]
last_update: 2026-05-30
---

# 🗂️ fdupes – hledání a mazání duplicitních souborů

`fdupes` je nástroj pro Linux určený k vyhledávání a odstraňování duplicitních souborů. Porovnává obsah souborů a dokáže najít identické kopie bez ohledu na jejich název nebo umístění.

---

## 📦 Instalace

### Debian / Ubuntu

```bash
sudo apt install fdupes
Fedora
sudo dnf install fdupes
Arch Linux
sudo pacman -S fdupes
🔍 Vyhledání duplicit

Vyhledání duplicit v jednom adresáři:

fdupes /cesta/k/adresari

Rekurzivní prohledání včetně podadresářů:

fdupes -r /cesta/k/adresari
📊 Zobrazení velikosti duplicit (-S)

Pro zobrazení velikosti duplicitních souborů a odhad úspory místa použijte:

fdupes -rS /cesta/k/adresari
Kombinace parametrů
fdupes -rS ~/Downloads

Výstup bude obsahovat:

📄 seznam duplicitních souborů
📏 velikost jednotlivých skupin
💾 odhad ušetřeného diskového prostoru
🗑️ Interaktivní mazání duplicit

Po nalezení duplicit lze spustit interaktivní mazání:

fdupes -rd /cesta/k/adresari
Nejčastější přepínače
Parametr	Význam
-r	📂 Rekurzivní prohledávání podadresářů
-d	🗑️ Interaktivní mazání duplicit
-N	⚡ Automaticky ponechá první soubor
-S	📊 Zobrazí velikost duplicit a úsporu místa
⚠️ Automatické mazání bez potvrzení

Používejte pouze pokud máte zálohu dat.

fdupes -rdN /cesta/k/adresari

Tento příkaz:

📂 prohledá všechny podadresáře
🔍 najde duplicity
✅ ponechá první nalezenou kopii
🗑️ odstraní ostatní bez potvrzení
💡 Doporučený postup
1️⃣ Nejprve zkontrolujte duplicity
fdupes -rS /data
2️⃣ Poté proveďte interaktivní mazání
fdupes -rd /data
3️⃣ Automatické mazání používejte opatrně
fdupes -rdN /data
🧪 Praktické příklady

Vyhledání duplicit ve složce Downloads:

fdupes -rS ~/Downloads

Interaktivní odstranění duplicit:

fdupes -rd ~/Downloads

Automatické odstranění duplicit:

fdupes -rdN ~/Downloads

📚 Dokumentace

man fdupes

nebo

fdupes --help
🚨 Doporučení

Před použitím parametrů -d nebo -N si vždy ověřte nalezené duplicity a mějte aktuální zálohu důležitých dat. 💾

## 🔄 Porovnání dvou disků nebo adresářů

`fdupes` umožňuje porovnat dva adresáře nebo disky a vyhledat soubory se shodným obsahem.

### Základní porovnání

```bash
fdupes -r /mnt/disk1 /mnt/disk2
```

Příklad:

```bash
fdupes -r /data /backup
```

Výstup zobrazí všechny soubory, které existují na obou místech a mají identický obsah.

---

### 📊 Porovnání včetně velikostí (-S)

Pro zobrazení velikosti duplicit a odhadu možné úspory místa:

```bash
fdupes -rS /data /backup
```

Výstup obsahuje:

* 📄 seznam duplicitních souborů
* 📏 velikosti jednotlivých skupin
* 💾 odhad ušetřeného diskového prostoru

---

### 🚚 Ověření migrace na nový disk

Po kopírování dat na nový disk lze ověřit, že jsou soubory skutečně identické:

```bash
fdupes -r /mnt/stary_disk /mnt/novy_disk
```

Pokud se soubory zobrazí jako duplicity, jejich obsah je shodný.

---

### 🗑️ Odstranění duplicit ze zálohy

Po ověření dat lze odstranit nadbytečné kopie:

```bash
fdupes -rd /data /backup
```

nebo automaticky:

```bash
fdupes -rdN /data /backup
```

⚠️ Před použitím parametrů `-d` nebo `-N` vždy ověřte výsledek a mějte aktuální zálohu důležitých dat.

---

### 🔍 Kontrola rozdílů pomocí rsync

Pokud potřebujete zjistit, které soubory mezi adresáři chybí nebo se liší, použijte:

```bash
rsync -avhn --delete /mnt/stary_disk/ /mnt/novy_disk/
```

Parametry:

| Parametr   | Význam                      |
| ---------- | --------------------------- |
| `-a`       | Archivní režim              |
| `-v`       | Podrobný výpis              |
| `-h`       | Čitelné velikosti           |
| `-n`       | Simulace bez změn           |
| `--delete` | Zobrazí přebývající soubory |

Pokud příkaz nevypíše žádné změny, adresáře jsou obsahově shodné.

---

### ⭐ Alternativa pro velká úložiště

Pro velmi rozsáhlá datová úložiště může být vhodný nástroj `rdfind`:

```bash
rdfind -makeresultsfile false /mnt/disk1 /mnt/disk2
```

Výhody:

* 🚀 rychlé zpracování velkých objemů dat
* 📊 podrobné statistiky
* 🔗 podpora hardlinků
* 🧹 efektivní práce s duplicitami

---

# 📖 Literatura a zdroje

ADRIAN LOPEZ ROCHE. *fdupes – Identify or delete duplicate files*. GitHub. Dostupné z: https://github.com/adrianlopezroche/fdupes [cit. 2026-05-30].

FDUPES. *Manual Page*. Linux Manual Pages. Dostupné z: https://manpages.debian.org/fdupes [cit. 2026-05-30].

TOM'S HARDWARE. *How to Find and Delete Duplicate Files in Linux Using fdupes*. Dostupné z: https://www.tomshardware.com/how-to/delete-duplicate-files-in-linux-fdupes [cit. 2026-05-30].

RSYNC PROJECT. *rsync Documentation*. Dostupné z: https://rsync.samba.org/documentation.html [cit. 2026-05-30].

RDFIND PROJECT. *rdfind Documentation*. Dostupné z: https://rdfind.pauldreik.se [cit. 2026-05-30].





