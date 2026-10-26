---
title: TESmart PKS0802A10 – návod k použití (zapojení a ovládání)
category: Počítače
tags: [TESmart, KVM, home-office, monitory, USB, DisplayPort]
last_update: 2026-10-26
---

# TESmart PKS0802A10 – návod k použití (zapojení a ovládání)

Tato stránka popisuje KVM přepínač **TESmart PKS0802A10** s firemním notebookem na Windows, pracovní tower stanicí na Linux, dvěma monitory EIZO, klávesnicí a myší.

Cílem je rychle zjistit:

- jak jsou zařízení propojena,
- jak přepnout ovládání mezi počítači,
- co dělat, když se obraz nebo periferie nechovají očekávaně.

Zapojení níže vychází z potvrzeného zapojení tohoto pracoviště.

## 1. Rychlý návod

### Přepnutí klávesnice a myši

Pokud je jako spouštěcí klávesa nastaven **pravý Ctrl**:

- Stiskni **pravý Ctrl** dvakrát rychle za sebou.
- Stiskni číslo vstupu, na který chceš přepnout: **1–4**.

Příklad: `Pravý Ctrl` → `Pravý Ctrl` → `2`

Tím se přepne vybraný vstup KVM. Při běžném režimu se oba monitory přepnou na vybraný počítač.

Pokud zkratka nefunguje, zkus výchozí klávesu **Scroll Lock** (viz [Klávesové zkratky](#6-klávesové-zkratky)).

### Přepnutí při zobrazení dvou různých počítačů

Pokud je každý monitor nastaven na jiný počítač, dvojitým stisknutím **pravého Alt** se podle manuálu přepne zaměření klávesnice a myši mezi počítači zobrazenými na monitorech.

### Když se KVM samo přepíná

Automatické skenování vypneš stisknutím **Esc** na připojené klávesnici. Auto Scan je ve výchozím stavu vypnutý.

## 2. Co KVM dělá

TESmart PKS0802A10 je přepínač pro **až čtyři počítače a dva monitory DisplayPort**. Připojuje se k němu také USB klávesnice a myš.

Podporuje dva hlavní režimy:

- **Jeden počítač na obou monitorech** – oba monitory zobrazují stejný počítač; nastavení rozšířené nebo duplicitní plochy se provádí v operačním systému.
- **Dva počítače současně** – jeden monitor zobrazuje jeden počítač a druhý monitor jiný počítač. Klávesnici a myš lze přepnout mezi zobrazenými počítači.

KVM má emulaci EDID, která počítači předává informace o připojeném monitoru i při přepnutí. Výrobce doporučuje ponechat EDID zapnuté.

## 3. Zapojení na tomto pracovišti

### Zařízení

| Označení | Zařízení | Úloha |
|---|---|---|
| Windows | Firemní notebook s VPN | Pracovní počítač |
| Dock | i-tec dokovací stanice | Připojení notebooku k monitorům / KVM a napájení podle konkrétního zapojení |
| Linux | Stolní počítač | Druhý počítač |
| KVM | TESmart PKS0802A10 | Přepínání obrazových vstupů a USB periferií |
| EIZO 1 a 2 | Dva monitory | Zobrazení pracovní plochy |
| Klávesnice a myš | USB periferie | Ovládání právě vybraného počítače |

### Schéma skutečného zapojení

```text
Linux – stolní PC
Grafická karta NVIDIA Quadro P5000
        ├── DisplayPort 1 ──┐
        └── DisplayPort 2 ──┤
                            ▼
                     TESmart KVM
                     vstup [1]
                            │
Windows – firemní notebook │
        │                   │
        └── USB-C PD ── i-tec dok
                         Dual Display Docking Station
                         PD 100 W
                            ├── DisplayPort 1 ──┐
                            └── DisplayPort 2 ──┤
                                                ▼
                                         TESmart KVM
                                         vstup [4]

TESmart KVM – obrazové výstupy
        ├── DisplayPort OUT A ── Monitor EIZO 1
        └── DisplayPort OUT B ── Monitor EIZO 2

Klávesnice a myš ── USB port KVM označený pro klávesnici/myš
```

### Přehled připojení

| Počítač | Cesta obrazu do KVM | Vstup KVM |
|---|---|---:|
| Stolní PC Linux | 2× DisplayPort z grafické karty NVIDIA Quadro P5000 | **1** |
| Firemní notebook Windows | USB-C PD → i-tec Dual Display Docking Station, PD 100 W → 2× DisplayPort | **4** |

Obraz z KVM vede dvěma kabely DisplayPort přímo do monitorů EIZO. Monitory tedy nejsou v tomto zapojení připojené samostatnými obrazovými kabely přímo k počítačům.

> **Důležité:** Každý počítač používá v KVM jednu odpovídající skupinu vstupů. Skupina obsahuje dva DisplayPort vstupy (A a B) a USB port. USB propojení daného počítače je potřeba pro přepínání klávesnice a myši; samotné DisplayPort kabely přenášejí obraz.

## 4. Porty a tlačítka

### Zadní panel

| Označení | K čemu slouží |
|---|---|
| **DC 12V** | Napájecí adaptér KVM |
| **IR extension** | Připojení prodlužovacího IR přijímače pro dálkový ovladač |
| **RS232** | Pokročilé ovládání KVM přes sériové příkazy |
| **DCCI** | Propojení dvou kompatibilních KVM pro sestavu až se čtyřmi monitory; pro běžné zapojení se nepoužívá |
| **Keyboard and mouse input** | Vyhrazené připojení USB klávesnice a myši |
| **DisplayPort outputs A/B** | Obrazové výstupy do monitorů |
| **KVM input groups 1–4** | Vstupy pro počítače; každá skupina má DisplayPort A, DisplayPort B a USB |

### Přední panel

| Prvek | Funkce |
|---|---|
| **Tlačítka 1–4** | Výběr počítače v běžném režimu |
| **MIN / SEC / Set** | Nastavení intervalu automatického skenování |
| **Status LED** | Indikuje, zda je Auto Scan vypnutý nebo zapnutý |
| **Digitální displej** | Zobrazuje číslo vstupu a stav EDID pomocí tečky na displeji |
| **Close** | Krátký stisk vypíná/zapíná obrazové výstupy; podržení přibližně 3 sekundy zapíná/vypíná emulaci EDID |
| **USB 2.0** | Připojení dalších USB zařízení, například adaptéru nebo periferií |
| **Power** | Zapnutí/vypnutí napájení KVM |

## 5. Režimy zobrazení

### Režim A – oba monitory na jednom počítači

Stiskni tlačítko vstupu **1–4** na předním panelu nebo použij klávesovou zkratku. Oba monitory se přepnou na vybraný počítač.

Chceš-li mít rozšířenou plochu, nastav ji v systému Windows nebo Linuxu v nastavení obrazovek.

### Režim B – každý monitor zobrazuje jiný počítač

Na předním panelu nebo dálkovém ovladači:

- Vyber monitor A nebo B.
- Vyber číslo počítače 1–4.

Příklad: `A–4` a `B–2` znamená, že monitor A zobrazuje počítač 4 a monitor B počítač 2.

Manuál upozorňuje, že vstup A patří k výstupu A a vstup B k výstupu B. Obraz z kanálu A tedy nelze jednoduše přesměrovat na výstup B pomocí KVM.

V tomto režimu se zaměření klávesnice a myši přepíná dvojitým stisknutím **pravého Alt**.

## 6. Klávesové zkratky

Klávesové zkratky fungují pouze tehdy, když je klávesnice připojena do vyhrazeného USB portu KVM pro klávesnici a myš.

### Spouštěcí klávesa

Výchozí spouštěcí klávesa podle výrobce je **Scroll Lock**. Alternativou je **pravý Ctrl**.

- Se spouštěcí klávesou **Scroll Lock** začíná zkratka dvěma rychlými stisky `Scroll Lock`.
- Se spouštěcí klávesou **pravý Ctrl** začíná zkratka dvěma rychlými stisky pravého Ctrl.

Po dvojitém stisku KVM krátce pípne; další klávesu stiskni v časovém limitu podle manuálu.

| Funkce | Zkratka při nastaveném Scroll Lock | Zkratka při nastaveném pravém Ctrl |
|---|---|---|
| Vybrat počítač 1–4 a přepnout oba monitory | `Scroll Lock` → `Scroll Lock` → `1–4` | `Pravý Ctrl` → `Pravý Ctrl` → `1–4` |
| Předchozí vstup | `Scroll Lock` → `Scroll Lock` → `Page Up` | Ověřit podle nastavení |
| Další vstup | `Scroll Lock` → `Scroll Lock` → `Page Down` | Ověřit podle nastavení |
| Zapnout Auto Scan | `Scroll Lock` → `Scroll Lock` → `Mezerník` | Ověřit podle nastavení |
| Zapnout/vypnout přepínání kolečkem myši | `Scroll Lock` → `Scroll Lock` → `F6` | Ověřit podle nastavení |
| Zapnout/vypnout zvukové pípnutí | `Scroll Lock` → `Scroll Lock` → `F11` | Ověřit podle nastavení |
| Přepnout zaměření klávesnice/myši v režimu dvou počítačů | `Pravý Alt` → `Pravý Alt` | `Pravý Alt` → `Pravý Alt` |
| Ukončit Auto Scan | `Esc` | `Esc` |

### Přepnutí spouštěcí klávesy na pravý Ctrl

Manuál uvádí dvě možnosti:

**Metoda 1 – klávesová zkratka**

`Scroll Lock` → `Scroll Lock` → `F1`

Tím se spouštěcí klávesa přepne na pravý Ctrl.

**Metoda 2 – tlačítko Set**

- Do 10 sekund po zapnutí KVM stiskni a podrž tlačítko **Set** na předním panelu.
- Drž jej, dokud KVM nezapípá.
- Restartuj KVM.

Pro návrat ze spouštěcí klávesy pravý Ctrl na Scroll Lock manuál uvádí:

`Pravý Ctrl` → `Pravý Ctrl` → `F1`

## 7. Automatické skenování (Auto Scan)

Auto Scan postupně přepíná vstupy, aby bylo možné sledovat připojené počítače. Ve výchozím stavu je vypnutý.

### Zapnutí

- **Klávesnicí:** dvojitý stisk nastavené spouštěcí klávesy → `Mezerník`.
- **Dálkovým ovladačem:** stiskni tlačítko Scan (ikona rotujících šipek).
- **Předním panelem:** použij ovládání podle popisu tlačítek na zařízení.

### Vypnutí

- Stiskni **Esc** na klávesnici.
- Nebo stiskni číslo vstupu **1–4** na předním panelu.
- Nebo znovu stiskni tlačítko Scan na dálkovém ovladači.

### Nastavení intervalu

Výchozí interval je **5 sekund**. Lze jej nastavit tlačítky na předním panelu:

- Tlačítkem **MIN** nastav počet minut (0–59).
- Tlačítkem **SEC** nastav počet sekund (0–59; minimum je 5 sekund).
- Stiskni **Set** pro potvrzení.

Při zapnutém Auto Scan lze interval podle manuálu upravovat také klávesami `+` a `−` po aktivaci sekvence spouštěcí klávesy.

## 8. Emulace EDID

EDID pomáhá počítači zachovat informace o monitoru i při přepínání KVM. Díky tomu se mohou otevřená okna a rozložení plochy chovat stabilněji.

- Emulace EDID je podle výrobce ve výchozím stavu zapnutá.
- Stav ukazuje tečka na pravé straně digitálního displeje KVM.
- Podržením tlačítka **Close** přibližně 3 sekundy lze emulaci EDID zapnout nebo vypnout.
- Výrobce doporučuje ponechat EDID zapnuté. Pokud se objeví problém s obrazem, manuál doporučuje zkusit EDID vypnout a ověřit, zda se chování zlepší.

Pozor: EDID samo o sobě nezaručuje, že se okna za všech okolností nikdy nepřeskládají; výsledek závisí také na grafice, operačním systému a konkrétním zapojení.

## 9. Řešení problémů

### Klávesnice nebo myš neovládá správný počítač

- Přepni KVM na požadovaný vstup 1–4.
- Zkontroluj, zda je USB kabel daného počítače zapojený do stejné skupiny vstupů jako jeho obrazové kabely.
- Zkontroluj, zda je klávesnice/myš zapojena do vyhrazeného portu KVM.
- Pokud jsou na monitorech zobrazené dva různé počítače, zkus dvojitý stisk pravého Alt.

### Klávesová zkratka nefunguje

- Ověř, zda je aktivní spouštěcí klávesa Scroll Lock, nebo pravý Ctrl.
- Stiskni ji dvakrát rychle za sebou.
- Použij klávesnici připojenou přímo do portu KVM pro klávesnici/myš.
- Pokud klávesnice nemá samostatnou klávesu Scroll Lock, použij nastavený pravý Ctrl.

### Obraz se po přepnutí změní nebo zmizí

- Ověř, že jsou všechny DisplayPort kabely pevně zapojené.
- Zkontroluj, zda je zapnutý správný vstup monitoru.
- Ověř stav emulace EDID; výrobce doporučuje mít ji zapnutou.
- Pokud potíže přetrvávají, zkus EDID dočasně vypnout tlačítkem Close podrženým přibližně 3 sekundy a otestuj výsledek.

### KVM samo přepíná vstupy

Pravděpodobně je aktivní Auto Scan. Stiskni **Esc**, vyber vstup 1–4 nebo vypni skenování tlačítkem Scan na ovladači.

## 10. Technické údaje a odkazy

- **Model:** TESmart PKS0802A10
- **Typ:** 4 počítače × 2 monitory (4×2 DisplayPort KVM)
- **Video rozhraní:** DisplayPort 1.4
- **Maximální podporované rozlišení podle manuálu:** až 8K (7680 × 4320) při 60 Hz; podpora závisí také na počítači, kabelech a monitoru
- **Napájení:** 12 V DC
- **Sériové ovládání RS232:** 9600 bps, 8 datových bitů, bez parity, 1 stop bit

RS232 je pokročilá možnost ovládání a pro běžné přepínání není potřeba.

Při problémech nebo pro další technické podrobnosti lze použít [oficiální web TESmart](https://www.tesmart.com/) a původní manuál k modelu PKS0802A10.

---

## Poznámky k provozu

- Automatické skenování (Auto Scan) je popsáno pro úplnost, ale při běžném provozu se nepoužívá.
- Linux je připojen do vstupu **1** a notebook Windows do vstupu **4**.
- Oba monitory EIZO jsou připojené přímo do obrazových výstupů TESmart KVM.
