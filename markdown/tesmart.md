---
title: TESmart – přepínání více počítačů na dva monitory
category: Počítače
tags: [přepínání, příslušenství, zobrazení, display, KVM]
last_update: 2026-10-26
---
# TESmart PKS0802A10 - GitHub Wiki Dokumentace

Tato stránka slouží jako technická dokumentace a provozní příručka pro zapojení 4-portového Dual-Monitor DisplayPort 1.4 KVM přepínače **TESmart PKS0802A10** do specifického CAD pracoviště kombinujícího Windows (firemní notebook s VPN) a Linux (stolní PC).

---

## 1. Architektura a topologie zapojení stolu

Z důvodu restriktivní politiky firemní VPN (*Full Tunneling* na straně Cisco Secure Client) je síťové propojení obou počítačů (PuTTY, RDP, VNC) nemožné. Pracoviště je proto izolováno čistě na hardwarové úrovni. 

Obraz se přepíná přímo na monitorech EIZO (využití více hardwarových vstupů), zatímco KVM přepínač zajišťuje inteligentní sdílení periferií a zachování CAD rozložení oken díky integrované emulaci EDID.

### Schéma zapojení:
```text
  [ Firemní Notebook - Windows ]             [ Stolní PC - Linux ]
                 |                                      |
       (1x USB-C kabel s PD)                     (Grafická karta)
                 v                                      |
    [ i-tec Docking Station ]                           |
        |               |                               |
    (2x DP)          (1x USB)                        (2x DP)
        |               |                               |
        v               v                               v
  +-----------------------------------------------------------------+
  |                TESmart PKS0802A10 KVM Switch                    |
  +-----------------------------------------------------------------+
     |       |                                            |      |
  (2x DP) (1x USB)                                     (2x DP) (1x USB)
     |       |                                            |      |
     v       v                                            v      v
[ EIZO Monitor 1 ]                                    [ EIZO Monitor 2 ]
  - Vstup 1: Notebook                                   - Vstup 1: Notebook
  - Vstup 2: Linux PC                                   - Vstup 2: Linux PC
                                 |  |
                                 v  v
                         [ Klávesnice & Myš ]
                        (Porty s ikonou klávesnice)
```

---

## 2. Hardwarová specifika a CAD kompatibilita

* **Podpora rozlišení:** Zařízení nativně podporuje standard DisplayPort 1.4 (až 4K@60Hz). Pro CAD monitory EIZO s rozlišením **1920x1200 (WUXGA)** má switch obrovskou výkonnostní rezervu, což zaručuje nulové blikání a perfektní ostrost hran.
* **EDID Emulace:** KVM v sobě neustále udržuje paměťový profil monitorů EIZO. Při přepnutí periferií na druhý počítač si grafické karty stále myslí, že jsou k monitorům připojeny. **Okna, panely nástrojů a CAD lišty se nikdy nepřeskládají ani nerozházejí.**

---

## 3. Popis specifických prvků (Přední a zadní panel)

### Přední panel: Tlačítka SET, MIN a SEC
Tato tlačítka slouží výhradně ke konfiguraci funkce **Auto Scan Mode** (automatické cyklické přepínání mezi počítači pro monitoring bez zásahu uživatele).
* **MIN:** Cyklicky mění interval v rozsahu 0–59 minut.
* **SEC:** Cyklicky mění interval v rozsahu 0–59 sekund (minimum je 5 sekund).
* **Set:** Potvrdí a uloží navolený časový interval do interní paměti KVM.

### Zadní panel: Svorkovnice TX / GND / RX (RS232 port)
Sériové rozhraní typu RS232 určené pro **pokročilé automatizované a programové ovládání KVM**.
* **Využití:** Umožňuje posílat hexadecimální příkazy přímo z operačního systému (např. pomocí skriptu v Linuxu) přes sériovou linku s konfigurací: *Baud rate 9600 bps, Stop bit 1, Data 8 bit, Parity None*.
* Pomocí skriptu lze programově přepínat vstupy, vypínat bzučák nebo aktivovat režimy, aniž by uživatel musel mačkat klávesnici.

---

## 4. Ovládání a klávesové zkratky (Hotkey)

Pro správnou funkčnost klávesových zkratek musí být klávesnice zapojena do **vyhrazeného USB portu na přední/zadní straně s ikonou klávesnice** (emulovaný HID port).

### Aktivace přepínání přes dvojitý Ctrl:
Z výroby může mít starší model nastaven jako hlavní spouštěč klávesu `Scroll Lock`. Změnu na vámi požadovaný **Pravý Ctrl** provedete dvěma způsoby:
* **Metoda softwarová:** Stiskněte sekvenci `[Scroll Lock]` -> `[Scroll Lock]` -> `[F1]`. KVM přepne monitorovací čip na Ctrl.
* **Metoda hardwarová (Reset):** Do 10 sekund po zapnutí KVM hlavním vypínačem stiskněte a podržte tlačítko `[Set]` na předním panelu, dokud KVM nepípne. Poté zařízení restartujte. Od té chvíle reaguje na Ctrl.

### Postup přepínání:
Pro přepnutí periferií mezi Windows a Linuxem stiskněte:
`[Pravý Ctrl]` -> `[Pravý Ctrl]` -> `[Číslo portu 1 až 2]`

---

## 5. Správa režimu Auto Scan (Automatické přepínání)

Funkce automatického skenování portů je ve výchozím stavu vypnutá. 

* **Spuštění přes klávesnici:** `[Pravý Ctrl]` -> `[Pravý Ctrl]` -> `[Mezerník]` (Space).
* **Spuštění přes dálkový ovladač:** Stisknutím dedikovaného tlačítka s **ikonou rotujících šipek** (vpravo dole).

### Jak Auto Scan zrušit a zastavit (Vypnutí):
Pokud se KVM začne samo cyklicky přepínat, režim okamžitě zrušíte jedním z následujících kroků:
1. Stisknutím klávesy **`[Esc]`** na klávesnici (nejrychlejší cesta).
2. Stisknutím jakéhokoliv číselného tlačítka **`[1]` až `[4]`** na předním panelu KVM (přepne natvrdo na dané PC a skenování vypne).
3. Opětovným stisknutím tlačítka s **ikonou rotujících šipek** na dálkovém ovladači.
