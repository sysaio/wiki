---
title: dupefind – Hledání duplicitních souborů v Linuxu
category: Počítače
tags: [linux, duplicates, rdfind, cleanup, filesystem, ubuntu, duplicitni-soubory, fdupes]
last_update: 2025-09-12
---
# Návod na rdfind, fdupes a dupeGuru (GUI) a další alternativy pro Ubuntu Linux 🐧✨

Tento návod popisuje instalaci a základní použití tří nástrojů pro hledání duplicitních souborů v Ubuntu Linuxu: rdfind, fdupes a dupeGuru (grafické uživatelské rozhraní). 🚀

---

## 1. rdfind 🔍

### Co je rdfind?  
rdfind (redundant data find) je nástroj pro rychlé vyhledávání duplicitních souborů založený na porovnávání hash hodnot a dalších atributů. 🧩

### Instalace 💻  
Otevřete terminál a spusťte:  
sudo apt update  
sudo apt install rdfind

### Základní použití 🎯  
Vyhledání duplicit ve složce `/cesta/k/slozce`:  
rdfind /cesta/k/slozce

Po dokončení rdfind vypíše přehled duplicit a ponechá originály, přičemž duplicitní soubory lze podle potřeby odstranit ručně. 🧹

### Pokročilé možnosti ⚙️  
- Odstranění duplicit automaticky (pouze pokud si jste jisti):  
rdfind -deleteduplicates true /cesta/k/slozce  
- Ignorovat symbolické odkazy:  
rdfind -ignorelinks true /cesta/k/slozce  
- Zobrazit více informací:  
rdfind -verbose true /cesta/k/slozce

---

## 2. fdupes 🗂️

### Co je fdupes?  
fdupes je jednoduchý nástroj pro hledání a správu duplicitních souborů v příkazové řádce. ⚡

### Instalace 💻  
sudo apt update  
sudo apt install fdupes

### Základní použití 🎯  
Vyhledání duplicit v adresáři:  
fdupes /cesta/k/slozce

### Uživatelské interakce 🤹‍♂️  
- Vypsání duplicit rekurzivně:  
fdupes -r /cesta/k/slozce  
- Interaktivní mazání duplicit (budete vyzváni ke smazání):  
fdupes -rdN /cesta/k/slozce  
Parametry:  
  - `-r` rekurzivně  
  - `-d` mazání duplicit (vyžaduje interakci)  
  - `-N` automaticky vybrat první soubor (bez výzvy)  
- Pouze zobrazit duplicitní soubory (rekurzivně):
fdupes -r /cesta/k/slozce
fdupes -rS /cesta/k/slozce // včetně zobrazení velikosti
fdupes -rSd /cesta/k/slozce // včetně zobrazení velikosti a možnosti výběru které smazat a kreré ponechat

---

## 3. dupeGuru (GUI) 🎨

### Co je dupeGuru?  
dupeGuru je grafický nástroj pro hledání duplicitních souborů s podporou různých režimů porovnávání (název, obsah, hudba). 🎼📸

### Instalace 💻  

1. Z repozitáře Ubuntu:  
sudo apt update  
sudo apt install dupeguru

Pokud není k dispozici v repozitáři, stáhněte si AppImage ze stránek https://dupeguru.voltaicideas.net/

2. Použití AppImage:  
- Stáhněte soubor AppImage  
- Udělejte jej spustitelným:  
chmod +x dupeguru*.AppImage  
- Spusťte:  
./dupeguru*.AppImage

### Použití 🖱️  
1. Spusťte dupeGuru.  
2. Vyberte typ skenování (Standard, Music nebo Picture).  
3. Přidejte složky k prohledání.  
4. Klikněte na "Scan".  
5. Po skončení se zobrazí seznam duplicit.  
6. Označte soubory k odstranění, přesunu nebo ignorování.  
7. Použijte odpovídající tlačítka pro zpracování.

### Tipy 💡  
- Nastavte toleranci pro porovnání názvů souborů.  
- Režim Music porovnává metadata tagů.  
- Ukládejte výsledky pro pozdější analýzu.

---

## 4. Doplnění pro dokonalý návod 🌟

### Zálohování dat před mazáním duplicit 💾  
Vždy si vytvořte zálohu důležitých dat před tím, než začnete duplicitní soubory mazat. Nejlepší je zálohovat celý adresář na externí disk nebo do cloudu.  
Například:  
`rsync -avh /cesta/k/slozce /cesta/k/zaloha_slozky`

### Jak nástroje rozhodují, co je originál a co duplicita? 🧐  
- **rdfind:** primárním souborem je obvykle první nalezený soubor, ale můžete to ovlivnit parametry.  
- **fdupes:** vybere první nalezený soubor jako originál a ostatní označí jako duplicity.  
- **dupeGuru:** nabízí uživateli možnost, jak s duplicitami nakládat.

### Příklady použití – kdy který nástroj? 🎛️  
- **rdfind:** rychlé automatizované čištění velkých adresářů.  
- **fdupes:** vhodný pro interaktivní práci v terminálu s malým množstvím souborů.  
- **dupeGuru:** pokud chcete pohodlné GUI a vizuální kontrolu.

### Zlepšení výkonu 🚀  
- Rozdělte rozsáhlé skenování do menších částí, například adresář po adresáři.  
- U rdfind použijte parametr `-ignorelinks true` pro ignorování symbolických odkazů.  
- Snažte se zpracovávat data na rychlých discích (SSD).

### Automatizace a skripty 🤖  
Například jednoduchý cron job s rdfind pro pravidelné čištění:  
`0 3 * * 7 rdfind -deleteduplicates true /home/uzivatel/Dokumenty`

### Jak číst výstupy nástrojů 📄  
- **rdfind:** vypisuje seznam duplicitních skupin s primárními a duplicitními soubory.  
- **fdupes:** vypíše skupiny duplicitních souborů oddělené prázdným řádkem.  
- **dupeGuru:** zobrazuje duplicitní soubory přímo v GUI, včetně podrobností.

### Alternativní nástroje v Ubuntu repozitářích 🔄

### rmlint 🧹

**Popis:** Rychlý a efektivní nástroj pro hledání duplicitních souborů, prázdných adresářů a neplatných symlinků.

**Instalace:**  
sudo apt update  
sudo apt install rmlint

**Použití:**  
Vyhledání duplicit:  
rmlint /cesta/k/slozce  

Generování skriptu pro odstranění duplicit:  
rmlint -o sh /cesta/k/slozce  

Pak spusťte:  
sh rmlint.sh  

---

### czkawka-cli a czkawka-gui 🚀

**Popis:** Moderní nástroj napsaný v Rustu s CLI i GUI verzí. Umí hledat duplicitní soubory, prázdné složky a další.

**Instalace přes snap:**  
sudo snap install czkawka

**Použití CLI:**  
czkawka-cli dup /cesta/k/slozce

Pro GUI spusťte příkaz `czkawka`.

---

### jdupes 🔧

**Popis:** Vylepšená verze fdupes s podporou Unicode a paralelního zpracování.

**Instalace (ze zdroje):**  
sudo apt install build-essential git  
git clone https://github.com/jbruchon/jdupes.git  
cd jdupes  
make  
sudo make install

**Použití:**  
jdupes -r /cesta/k/slozce

---

### duff 🗂️

**Popis:** Jednoduchý a rychlý nástroj na vyhledávání duplicit pomocí hashování.

**Instalace:**  
sudo apt update  
sudo apt install duff

**Použití:**  
duff /cesta/k/slozce

---

### Shrnutí nástrojů 📊

| Nástroj     | GUI  | Terminál | Rychlost | Další funkce                      |
|-------------|------|----------|----------|---------------------------------|
| rdfind      | Ne   | Ano      | Rychlý   | Automatické mazání duplicit     |
| fdupes      | Ne   | Ano      | Střední  | Interaktivní mazání             |
| dupeGuru    | Ano  | Ne       | Střední  | Hudební a obrazové porovnání    |
| rmlint      | Ne   | Ano      | Velmi rychlý | Prázdné složky, symlinky       |
| czkawka     | Ano  | Ano      | Velmi rychlý | Moderní, multi-funkční          |
| jdupes      | Ne   | Ano      | Rychlý   | Unicode, paralelní zpracování   |
| duff        | Ne   | Ano      | Rychlý   | Jednoduchý a efektivní          |

---

## Bezpečnostní upozornění 🚨  
Nikdy neprovádějte automatické mazání duplicit ve složkách systému (např. `/bin`, `/usr`, `/etc`). Mohlo by dojít k poškození systému. Vždy se zaměřte na své osobní data a zálohujte!

---

## Závěr ✅

- **rdfind**, **fdupes** a **rmlint** jsou skvělé pro rychlé a efektivní hledání duplicit v terminálu.  
- **dupeGuru** a **czkawka** jsou ideální pro pohodlnou práci s GUI.  
- **jdupes** je super, pokud chcete lepší a rychlejší verzi fdupes.  
- Vždy zálohujte před mazáním a pečlivě kontrolujte výsledky.  

---

## Citace 📚

- Oficiální stránky rdfind: https://rdfind.pauldreik.se/  
- Fdupes GitHub: https://github.com/adrianlopezroche/fdupes  
- dupeGuru: https://dupeguru.voltaicideas.net/  
- rmlint: https://github.com/sahib/rmlint  
- czkawka: https://github.com/qarmin/czkawka  
- jdupes: https://github.com/jbruchon/jdupes  
- duff: https://github.com/jakejwilliams/duff  
- Dokumentace Ubuntu a osobní zkušenosti  

---

## Licence 🤪

Tento dokument je vydán pod licencí „ChatGPT Free Spirit License“™ – což znamená, že ho můžete volně používat, upravovat a sdílet, ale pokud při tom náhodou objevíte duplicitní soubory, nejdřív se zkuste zasmát a pak je bezpečně odstranit. 🐧✨

---

## ASCII umění: Linux Sluníčko ☀️🐧

       \   /  
        .-.   
     ― (   ) ―  
        `-’   
       /   \  

Ať vám svítí sluníčko i v terminálu! 🌞🐧
