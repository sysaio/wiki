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




