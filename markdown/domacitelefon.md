---
title: Výměna domácího telefonu Urmet (4+n)
category: Domácnost
tags: [telefon, byt, domácnost]
last_update: 2026-05-23
---

# 🏠 Výměna domácího telefonu Urmet (4+n)

## 📱 Technické specifikace

### Původní zařízení
* **Výrobce:** Urmet
* **Označení základní desky (PCB):** `CS1132-001E`
* **Typ systému:** Analogový audio systém $4+n$
* **Stav:** Nefunkční vyzvánění, utržený reproduktor, mechanické opotřebení.

### Nové zařízení (Přímá náhrada)
* **Model:** **Urmet Miro 1150** (případně verze s jedním servisním tlačítkem navíc **Urmet Miro 1150/1**)
* **Kompatibilita:** Plná hardwarová i schématická kompatibilita s původním systémem 4+n.

---

## 🔌 Schéma a tabulka zapojení vodičů

Zapojení odpovídá stávající barevné konfiguraci vodičů na svorkovnici původní desky `CS1132-001E`. Číslování svorek je u nového modelu **Urmet Miro 1150** identické.


| Funkce | Původní svorka | Barva vodiče v instalaci | Nová svorka (Urmet Miro 1150) |
| :--- | :---: | :---: | :---: |
| **Sluchátko** (příchozí hlas zvenku) | **1** | Bílý ⚪ | **1** |
| **Mikrofon** (odchozí hlas ven) | **2** | Zelený 🟢 | **2** |
| **Společná zem** (GND / COM) | **6** | Modrý 🔵 | **6** |
| **Elektrický zámek** (otevírání dveří) | **9** | Červený 🔴 | **9** |
| **Vyzvánění** (elektronický tón) | **CA** | Hnědý 🟤 | **CA** |

---

## ⚠️ Důležitá upozornění k instalaci

> [!WARNING]
> **Svorka 6 vs. Svorka 10**
> Na staré desce `CS1132-001E` jsou svorky **6** and **10** hardwarově propojené přímo integrovaným plošným spojem. Společný modrý vodič je proto zapojen na pozici 6. U nového telefonu **Urmet Miro 1150** stačí tento modrý vodič zapojit **čistě do svorky 6**. Svorku 10 (pokud je na dané revizi osazena) ponechte prázdnou a nepropojujte ji.

> [!CAUTION]
> **Spolehlivost barevného značení**
> Výše uvedené barvy (bílý, zelený, modrý, červený, hnědý) jsou specifické pro tuto konkrétní instalaci. Při jakémkoliv dalším zásahu do systému v domě nelze na barvy stoprocentně spoléhat bez předchozího ověření multimetrem.

---

## 🛠️ Diagnostika a ověření funkčnosti (pro případné ladění)

Pokud by po zapojení nového telefonu cokoliv nefungovalo, standardní diagnostický postup pro systém 4+n je následující:

1. **Měření vyzváněcího signálu:** Při zazvonění od vchodu se musí na **svorce CA** proti **svorce 6** objevit střídavé napětí v rozsahu **8–12 V AC**.
2. **Otevírání zámku:** Stiskem tlačítka klíče na telefonu dojde k mechanickému propojení **svorky 9** se **svorkou 6** (společná zem), což aktivuje relé zámku u vchodových dveří.
3. **Problém se zavěšením:** Pokud telefon trvale přenáší zvuk a nereaguje na vyzvánění, zkontrolujte, zda plastová vidlice správně domáčkne vnitřní spínač na desce.
