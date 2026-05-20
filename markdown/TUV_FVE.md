---
title: Solární ostrovní ohřev vody (předehřev pro TČ bojler)
category: Elektronika
tags: [fve, tuv, domácnost, sprchování, voda]
last_update: 2026-05-20
---
# ☀️ Solární ostrovní ohřev vody (předehřev pro TČ bojler)

Tento projekt popisuje realizaci čistě ostrovního (off-grid) fotovoltaického ohřevu teplé užitkové vody (TUV) jako solárního předehřevu před stávající 100l bojler s tepelným čerpadlem. Systém je dimenzován pro proměnlivý provoz (2 až 6 osob) s důrazem na maximální jednoduchost, bezpečnost a absenci drahých baterií.

---

## 🛒 Kompletní nákupní seznam (Materiál)

### 1. Hlavní zařízení a panely
*   **1 ks** Elektrický tlakový bojler **Stiebel Eltron PSH 120 Trend** (objem 120 litrů, příkon 2 kW, mechanický termostat).
*   **1 ks** MPPT střídač pro solární ohřev **Geti GWH02D 4000W** (s displejem a vestavěným sledováním výkonu).
*   **4 ks** Solární panel **450 Wp až 460 Wp** (např. *Jinko Solar Tiger Neo*, *Longi Hi-MO* nebo *Canadian Solar*).
*   **1 ks** Kompletní **hliníková konstrukce na střechu pro 4 panely** (Obsahuje: 4x AL profil, 4x krajní úchyt, 6x středový úchyt, nerezové šrouby a střešní háky/kombi vruty dle typu krytiny).

### 📦 2. Jisticí rozvaděč (Bezpečnostní DC domeček)
*   **1 ks** Plastová rozvodnice na omítku **IP65, 4 až 6 modulů** s průhlednými dvířky (např. *Noark*, *Gewiss* nebo *Tracon*).
*   **1 ks** DC Pojistkový odpínač **2-pólový, 1000V DC** (např. *Noark Ex9FP 2P*).
*   **2 ks** Solární válcová pojistka **gPV 10x38 mm, 15 A** (určená pro fotovoltaiku).
*   **1 ks** DC Přepěťová ochrana **T1+T2 (B+C), 2-pólová, pro napětí 500V až 600V DC** (např. *Noark Ex9UEP 2P 600V* nebo *Saltek*).

### 🔌 3. Kabely a propojovací materiál (Bez nutnosti krimpování)
*   **1 ks** **Solární kabel 6 mm² ČERVENÝ s nalisovaným konektorem MC4** (délka na míru dle trasy ze střechy + 2m rezerva).
*   **1 ks** **Solární kabel 6 mm² ČERNÝ s nalisovaným konektorem MC4** (délka stejná jako u červeného).
*   **X metrů** Ochranná **UV stabilní chránička (např. Kopoflex nebo Monoflex)** pro bezpečné vedení solárních kabelů po střeše a přes průrazy zdí.

### ⚡ 4. Komponenty pro dodatečné uzemnění
*   **1 ks** **Ekvipotenciální svorkovnice (MET)** (malá mosazná svorkovnice s krytem na zeď nebo na DIN lištu).
*   **2 ks** **Nerezová zemnící svorka (typ SR02 nebo Bernard)** pro připojení uzemnění k hliníkovým AL profilům konstrukce.
*   **X metrů** Zemnící kabel **Zelenožlutý CYA / CY 6 mm² nebo 10 mm²** (propojení střechy a přepěťové ochrany se svorkovnicí MET).
*   **X metrů** Robustní zemnící drát **CY 16 mm² (zelenožlutý)** pro propojení nové svorkovnice MET s hlavním domovním uzemněním.

### 🧰 5. Pomocný materiál
*   Plastové stahovací pásky (s UV ochranou – černé).
*   Hmoždinky a vruty (velikost 6 nebo 8 mm).
*   Střešní/klempířský PU tmel na utěsnění průrazů.

---

## 🛠️ Stručný pracovní postup krok za krokem

### Krok 1: Montáž na střeše
1.  **Instalace konstrukce:** Přišroubujte střešní háky (nebo kombi vruty) do krokví a upevněte na ně hliníkové AL profily.
2.  **Uzemnění konstrukce:** Na hliníkový profil přišroubujte nerezovou zemnící svorku a zapojte do ní zelenožlutý kabel vedoucí dolů do domu.
3.  **Uložení panelů:** Položte panely na konstrukci a zajistěte je krajními a středovými příchytkami.
4.  **Sériové propojení:** Propojte panely za sebou v jedné řadě (mínus konektor prvního panelu do plus konektoru druhého panelu atd.).
5.  **Svedení kabelů:** Do prvního volného plusu a posledního volného mínusu řady zacvakněte připravené dlouhé solární kabely (červený a černý). Kabely schovejte do chráničky, stáhněte UV páskami ke konstrukci a protáhněte průrazem do domu.

### Krok 2: Příprava v technické místnosti
1.  **Montáž zařízení:** Na zeď upevněte bojler Stiebel Eltron, měnič Geti a jisticí rozvaděč (DC domeček).
2.  **Instalace uzemnění:** Namontujte novou svorkovnici MET a propojte ji tlustým drátem (16 mm²) s hlavním uzemněním domu. Sveďte do ní také zemnící kabel ze střechy.

### Krok 3: Zapojení DC rozvaděče (Bez napětí!)
*⚠️ POZOR: Dokud není kabeláž hotová, nepropojujte na střeše poslední konektor panelů, aby v drátech nebyl proud.*
1.  **Pojistkový odpínač:** Přiveďte červený (+) a černý (-) kabel ze střechy do horních svorek pojistkového odpínače. Do odpínače vložte pojistky, ale **nechte ho otevřený (vypnutý)**.
2.  **Přepěťová ochrana:** Ze spodních svorek odpínače vyveďte kabely do přepěťové ochrany. Z její spodní svorky vyveďte zelenožlutý drát do svorkovnice MET.
3.  **Propojení s měničem:** Ze spodních svorek odpínače vyveďte finální kabely (+) a (-) přímo do spodních solárních svorek měniče Geti.

### Krok 4: Finální oživení a test
1.  **Propojení bojleru:** Zapojte síťový kabel z bojleru Stiebel Eltron do hlavní solární zásuvky (Zásuvka E) na měniči Geti.
2.  **Měření napětí:** Zapojte na střeše poslední konektor panelů (uzavření okruhu). V technické místnosti multimetrem na spodních svorkách pojistkového odpínače ověřte napětí. Mělo by tam být **cca 140 až 160 V DC**.
3.  **Spuštění:** Pokud je napětí správné, **nacvakněte (zavřete) pojistkový odpínač**. Měnič Geti se rozsvítí a začne nahřívat vodu.

---

## 💡 Wiki rady & Tipy pro efektivní provoz

### 🔄 Koncept "Lidského přepínače" sítí
Systém záměrně není připojen k distribuční síti skrze střídač, což odbourává nutnost řešit administrativu a revize pro distributory elektrické energie (ČEZ / EG.D / PRE). 
*   **Od jara do podzimu:** Kabel od bojleru Stiebel Eltron je zapojený v solárním měniči Geti. Ohřev je 100% zdarma ze slunce.
*   **V zimě / Při špatném počasí:** Kabel manuálně vytáhnete z měniče Geti a zapojíte ho do vedlejší klasické zásuvky s nízkým tarifem (NT), čímž je zajištěn spolehlivý doohřev.

### 🌡️ Sériové zapojení bojlerů (Solární předehřev)
Nový solární bojler (120 l) slouží jako **předehřívací nádrž** pro stávající 100l bojler s tepelným čerpadlem (TČ). 
*   Když se někdo sprchuje, do TČ bojleru dotéká horká voda ze soláru, nikoliv ledová voda z vodovodního řadu. V létě tak kompresor TČ bojleru téměř nesepne a jeho běžná spotřeba (2 kWh/den) klesne na minimum.

### ☀️ Zimní slunce a proměnlivá obsazenost
*   **Fyzika vs. Lidé:** V zimním období v domě klesá počet ubytovaných osob (minimum osob). Zároveň bývají jasné mrazivé dny, kdy mají panely vysokou účinnost.
*   Pokud je v zimě azuro, vyplatí se nechat bojler na solárním měniči. 4 panely dokážou 120l objem pro 2 osoby předehřát na cca 35–40 °C, což TČ bojler následně velmi levně doohřeje na finální teplotu.

### 🛡️ Bezpečnost na prvním místě: Termostatický směšovací ventil
*   Protože 4 panely dokážou v létě při nízkém odběru vody nahřát 120 litrů vody na velmi vysokou teplotu (klidně 75 °C+), hrozí riziko opaření nebo poškození vnitřních plastových částí TČ bojleru.
*   **Doporučení:** Mezi solární bojler a TČ bojler nainstalujte termostatický směšovací ventil nastavený na maximálně 45–50 °C.

---
## 📊 Ekonomická bilance
*   **Celková investice do materiálu:** cca 37 000 Kč (ceny roku 2026 včetně DPH a konstrukčních prvků)
*   **Očekávaná roční solární úspora:** cca 1 755 kWh (cca 6 200 Kč při ceně 3,5 Kč/kWh v NT tarifu)
*   **Návratnost investice:** **~ 5,9 roku**
