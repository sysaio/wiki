---
title: Vytápění domečku
category: IoT
tags: [vytapění, MND, domácnost]
last_update: 2025-08-21
---

# 🏠 Srovnání způsobů vytápění: Hnědé uhlí vs. Plyn vs. Elektřina (invertorová klimatizace)

## Výchozí podmínky
- Venkovní teplota: 0 °C
- Dům: slušně zateplený
- Spotřeba plynu za topnou sezónu: 1 600 m³
- Roční tepelná potřeba: 16 000 kWh
- Cena uhlí: 7 500 Kč/t (výhřevnost 18 MJ/kg ≈ 5 kWh/kg)
- Cena plynu: 2 034,28 Kč/MWh (2,03 Kč/kWh)
- Cena elektřiny: 7 454,56 Kč/MWh (7,45 Kč/kWh)
- Účinnost kotle uhlí: 84,7 %
- Účinnost kotle plyn: 91,2 %
- Klimatizace invertorová COP ~3 (účinnost 300 %)

---

## ⚙️ Vstupní parametry

| Parametr                         | Hodnota             | 💬 Popis                                     |
|----------------------------------|---------------------|----------------------------------------------|
| 🔥 Roční tepelná potřeba         | `16 000 kWh`        | Odvozeno z průměrné spotřeby plynu (1600 m³) |
| ⛏️ Cena uhlí za 1 tunu           | `7 500 Kč`          | Hnědé uhlí s výhřevností 18 MJ/kg            |
| ⛽ Cena plynu za 1 MWh            | `2 034,28 Kč`       | Cena dle MND (včetně DPH a poplatků)         |
| ⚡ Cena elektřiny za 1 MWh        | `7 454,56 Kč`       | Elektřina MND (včetně všeho)                 |
| 🔋 Výhřevnost uhlí               | `18 MJ/kg` (=5 kWh) | Energetický obsah uhlí                       |
| 🛠️ Účinnost kotle na uhlí        | `84,7 %`            | Kotel IV. třídy                              |
| 🔧 Účinnost kotle na plyn        | `91,2 %`            | Atmosférický nový kotel                      |
| ❄️ COP klimatizace               | `3.0` (300 %)       | Výkonový koeficient (účinnost vytápění)      |

---

## 📐 Výpočty

### 🔥 Uhlí
- Roční spotřeba tepla: `16 000 kWh`
- Výhřevnost uhlí: `5 kWh/kg`
- Účinnost: `84,7 %`
**Výpočet spotřeby uhlí:**
Spotřeba = 16 000 ÷ (5 × 0,847) ≈ 3 778 kg
**Roční náklady:**
3 778 kg × (7 500 Kč ÷ 1 000) = 28 335 Kč
**Cena za 1 kWh tepla:**
28 335 Kč ÷ 16 000 kWh = 1,77 Kč/kWh

---

### ⛽ Plyn
- Účinnost kotle: `91,2 %`
**Spotřeba plynu (v kWh):**
16 000 ÷ 0,912 ≈ 17 544 kWh
**Roční náklady:**
17 544 × 2,0343 = 35 688 Kč
**Cena za 1 kWh tepla:**
35 688 ÷ 16 000 = 2,23 Kč/kWh

---

### ⚡ Elektřina (klimatizace)
- COP: `3.0` (účinnost 300 %)
**Spotřeba elektřiny:**
16 000 ÷ 3 = 5 333 kWh
**Roční náklady:**
5 333 × 7,45456 = 39 761 Kč
**Cena za 1 kWh tepla:**
39 761 ÷ 16 000 = 2,49 Kč/kWh

---

## 📊 Srovnávací tabulka - Výpočty spotřeby a nákladů

| 💡 Palivo / systém           | ⚙️ Účinnost / COP | 📦 Roční spotřeba        | 🔥 Tepelná energie | 💰 Roční náklady | 📈 Cena za 1 kWh | 🌍 Emise CO₂ | 💬 Poznámky                               |
|-----------------------------|------------------|--------------------------|--------------------|------------------|------------------|--------------|------------------------------------------|
| ⛏️ Hnědé uhlí (kotel IV.)    | 84,7 %           | 3 778 kg (3,78 t)        | 16 000 kWh         | 28 335 Kč        | **1,77 Kč/kWh**  | Vysoké       | Obsluha, sklady, popel, nutná údržba     |
| ⛽ Plyn (atmosférický kotel) | 91,2 %           | 17 544 kWh (plyn)        | 16 000 kWh         | 35 688 Kč        | **2,23 Kč/kWh**  | Střední      | Komfortní, čistý, bezobslužný            |
| ⚡ Elektřina (klimatizace)   | COP ~3.0         | 5 333 kWh (elektřina)    | 16 000 kWh         | 39 761 Kč        | **2,49 Kč/kWh**  | Nízké        | Největší komfort, nejdražší               |

---

## 🧠 Závěry

- **⛏️ Uhlí** je nejlevnější varianta, ale vyžaduje práci, prostor a údržbu. Nejlevnější topení vychází z uhlí, pokud je k dispozici levné uhlí s vyšší výhřevností a dobrým kotlem.
- **⛽ Plyn** je zlatá střední cesta – komfortní, čistý, ale ne nejlevnější. Plyn je dražší, ale nabízí vyšší komfort a méně starostí.
- **⚡ Elektřina** (přes klimatizaci) je dražší, ale velmi pohodlná a bez starostí. Elektřina s invertorovou klimatizací je nejdražší varianta, ale nabízí nejvyšší komfort a jednoduchost obsluhy.
- Výběr závisí na prioritách: cena, pohodlí, ekologie a dostupnost paliva.

---

## 💡 Tipy

- ✅ Pokud máš levný noční proud, elektřina může být výhodnější.
- 🔁 Kombinace dvou zdrojů (např. elektřina + plyn nebo uhlí + elektřina) může být flexibilní.
- 🔧 Modernizací kotle (plynový kondenzační nebo automat na uhlí) lze výrazně zvýšit účinnost a pohodlí.

---

## Další možnosti

- Snížení nákladů na elektřinu například využitím nočního tarifu.
- Modernizace kotle na uhlí nebo plynový kondenzační kotel pro zvýšení účinnosti.
- Kombinace zdrojů tepla (např. elektřina + kotel na uhlí).

---

## 📎 Licence

Tato stránka je volně k použití a úpravám. Přidej své poznatky nebo uprav parametry podle reálné situace 💬.

---


