---
title: Mobile Device Management (MDM)
category: Informatika
tags: [internet, mobil, politika, aplikace, sifrovani, kyberbezpečnost]
last_update: 2025-07-29
---

## 📱 Mobile Device Management (MDM)

### 🧭 Co je MDM?

Mobile Device Management (MDM) je systém centrální správy mobilních zařízení (telefony, tablety, notebooky), který organizaci umožňuje:

- Nastavit bezpečnostní politiky
- Instalovat / omezit aplikace
- Vynucovat šifrování a přístupová pravidla
- Dálkově smazat nebo uzamknout zařízení
- Segmentovat pracovní vs. soukromá data (BYOD)

> „Mobile device management is essential in a hybrid and remote work world.“  
> – Gartner (2023)

---

### 🏷️ Klíčové funkce MDM systémů

```
    +--------------------------------------+
    |         Klíčové MDM schopnosti       |
    +--------------------------------------+
    | ✅ Politiky PIN/biometrie            |
    | ✅ Dálkové smazání (wipe)            |
    | ✅ Šifrování disku                   |
    | ✅ Oddělení firemních/soukromých dat |
    | ✅ Omezování aplikací (blacklist/whitelist) |
    | ✅ Monitoring stavu a hrozeb         |
    +--------------------------------------+
```

| Funkce              | Popis |
|---------------------|-------|
| 🔐 Šifrování        | Povinné šifrování úložiště (např. File-Based Encryption v Androidu) |
| 📱 Správa aplikací  | Instalace firemních aplikací, zákaz neautorizovaných |
| 📶 VPN / Wi-Fi profily | Nastavení zabezpečeného připojení |
| 🔍 Monitoring        | Stav zařízení, jailbreak/root detekce, bezpečnostní skóre |
| 💣 Remote Wipe       | Dálkové smazání zařízení (ztráta/odchod zaměstnance) |

---

### 🧩 Typy MDM řešení

| Typ řešení        | Popis |
|-------------------|-------|
| **MDM**           | Kompletní správa zařízení |
| **MAM (Mobile App Management)** | Správa pouze aplikací, ne celého zařízení |
| **UEM (Unified Endpoint Management)** | Rozšířený MDM pro všechna zařízení (i notebooky, desktopy) |
| **BYOD**          | "Bring Your Own Device" – vlastní zařízení pod firemní kontrolou (částečnou) |

📌 Pokud firma povoluje BYOD, MDM by mělo zajistit **jasné oddělení firemních a osobních dat**.

---

### 💼 Příklady MDM platforem

| Nástroj                  | Platforma       | Poznámka |
|--------------------------|------------------|----------|
| **Microsoft Intune**     | Android, iOS, Windows | Integrace s Azure, Office 365 |
| **Jamf Pro**             | iOS/macOS        | Oblíbené ve školách a mezi Apple adminy |
| **VMware Workspace ONE** | Multiplatformní  | Pokročilé UEM schopnosti |
| **Google Endpoint Management** | Android, ChromeOS | Součást Google Workspace |
| **Kandji**               | Apple ekosystém  | Automatizace, silná UX |

---

### 🔒 Bezpečnostní doporučení

| Doporučení                     | Proč je to důležité |
|-------------------------------|---------------------|
| ✅ Vynucovat silné heslo nebo biometriku | Základní fyzická ochrana |
| ✅ Povinné šifrování disku    | Chrání data při ztrátě zařízení |
| ✅ Zákaz instalace neověřených aplikací | Minimalizace rizika malware |
| ✅ Oddělení osobních a pracovních profilů | Právní i praktické důvody |
| ✅ Pravidelné aktualizace OS a aplikací | Ochrana před zneužitelnými zranitelnostmi |
| ✅ Možnost dálkového výmazu   | Krádež, ztráta, odchod zaměstnance |

📌 MDM není jen o kontrole – je to **vrstva ochrany** firemních i osobních dat.

---

### 📉 Rizika bez MDM

- Úniky dat z nezabezpečených telefonů
- Ztráta kontroly nad e-maily, cloudovými účty, schůzkami
- Nemožnost reakce na ztracené zařízení
- Neautorizovaná synchronizace dokumentů mimo firmu
- Ransomware nebo malware přes nehlídané appky

---

### 🔐 ASCII diagram – MDM kontrolní tok

```
    +---------------------------+
    |       MDM Server         |
    +------------+-------------+
                 |
          Push konfigurace
                 ↓
    +------------+-------------+
    |     Mobilní zařízení     |
    | (Android / iOS / iPadOS) |
    +------------+-------------+
                 |
       Reporty a stavy zpět
                 ↓
    +---------------------------+
    |    Admin / Dashboard      |
    +---------------------------+
```

---

### 🌍 Důležité standardy a doporučení

- **NIST SP 800-124 Rev.2** – *Guidelines for Managing the Security of Mobile Devices in the Enterprise*  
  [🔗 PDF – https://doi.org/10.6028/NIST.SP.800-124r2](https://doi.org/10.6028/NIST.SP.800-124r2)
- **ISO/IEC 27001:2022** – *Annex A – A.6.2 Mobile Device Policy*
- **CIS Benchmarks** – Doporučené konfigurace pro Android/iOS  

---

### 📚 Citace (Harvard)

- Gartner (2023). *Magic Quadrant for Unified Endpoint Management Tools*.  
- NIST (2020). *SP 800-124 Rev.2 – Mobile Device Security Guidelines*. DOI: https://doi.org/10.6028/NIST.SP.800-124r2  
- Microsoft (2024). *What is Microsoft Intune?* https://learn.microsoft.com/en-us/mem/intune/fundamentals/what-is-intune  
- VMware (2024). *Workspace ONE overview*. https://www.vmware.com/products/workspace-one.html  
- CIS (2023). *iOS Benchmark v2.0.0*. https://www.cisecurity.org/benchmark/apple_ios

---

🔁 Chceš pokračovat? Mohu zpracovat další témata jako:

- 🔍 Forenzní analýza mobilních zařízení  
- 🧯 Incident response pro mobilní flotilu  
- ✈️ Cestování se zabezpečeným mobilem  
- 📤 Šifrovaná komunikace a IM (Signal, Threema, Matrix)

Stačí říct – připravím opět jako jeden kompaktní `.md` blok.
