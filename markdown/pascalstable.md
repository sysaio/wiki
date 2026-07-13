---
title: pascalstable – nastavení workstation pro AI
category: Počítače
tags: [linux, AI, ollama, comfyu]
last_update: 2026-07-13
---
# ComfyUI na NVIDIA Quadro P5000 (Pascal) v roce 2026

## Kompletní instalace, optimalizace a ověření funkčnosti

**Autor:** vlastní instalační poznámky

**Verze dokumentu:** 1.0

**Poslední aktualizace:** červenec 2026

---

# Úvod

Tento dokument vznikl během reálné instalace a konfigurace prostředí pro generování obrázků pomocí **ComfyUI** na pracovní stanici **Lenovo ThinkStation P720** vybavené profesionální grafickou kartou **NVIDIA Quadro P5000**.

Na internetu lze nalézt velké množství návodů pro ComfyUI, Stable Diffusion i PyTorch. Většina z nich však předpokládá použití nejnovějšího hardware a nejnovějších verzí software. To je vhodné pro moderní grafické karty architektur Turing, Ampere, Ada nebo Blackwell, nikoliv však pro starší profesionální karty řady Pascal.

Cílem tohoto dokumentu není vytvořit další stručný "how-to", ale podrobně zdokumentovat celý proces instalace, včetně slepých uliček, problémů a důvodů jednotlivých rozhodnutí.

Výsledkem má být prostředí, které bude:

- stabilní,
- reprodukovatelné,
- snadno obnovitelné,
- dobře zdokumentované,
- použitelné i za několik let.

Tento dokument proto vysvětluje nejen **co** bylo provedeno, ale především **proč**.

---

# Filozofie instalace

Během instalace jsme se drželi několika jednoduchých pravidel.

## 1. Stabilita je důležitější než nejnovější verze

V oblasti umělé inteligence vznikají nové verze knihoven prakticky každý měsíc. To ale neznamená, že jsou nejlepší volbou pro starší hardware.

Naopak.

Vývojáři se pochopitelně soustředí především na nejnovější architektury GPU a některé optimalizace pro starší generace postupně mizí.

Proto jsme se rozhodli hledat konfiguraci, která:

- využívá GPU naplno,
- je ověřená v praxi,
- nebude vyžadovat neustálé aktualizace.

---

## 2. Nepoužívat systémový Python

Linuxová distribuce obsahuje vlastní Python, který využívají systémové nástroje.

Jeho nahrazení nebo úprava bývá častým zdrojem problémů.

Proto jsme použili:

- pyenv
- samostatné virtuální prostředí (venv)

Díky tomu lze kdykoliv vytvořit další prostředí s jinou verzí Pythonu, aniž by byla ovlivněna funkčnost operačního systému.

---

## 3. Modely nesmí být svázány s ComfyUI

Samotná aplikace ComfyUI se může kdykoliv přeinstalovat nebo nahradit novější verzí.

Modely však představují největší objem dat.

Proto jsou uloženy mimo adresář ComfyUI.

Výhody:

- jedna knihovna modelů pro více instalací,
- snadné zálohování,
- jednoduchá migrace na nový disk,
- možnost používat stejné modely i z jiných aplikací.

---

## 4. Každý krok musí být ověřitelný

Po každé významnější změně jsme ověřovali, že systém stále funguje.

Nestačí pouze spustit příkaz.

Je potřeba zkontrolovat například:

- verzi Pythonu,
- verzi PyTorch,
- dostupnost CUDA,
- správně rozpoznanou grafickou kartu,
- Compute Capability,
- skutečné vytížení GPU.

Díky tomu lze případné problémy odhalit okamžitě.

---

# Použitý hardware

Instalace byla provedena na následující konfiguraci.

## Pracovní stanice

Lenovo ThinkStation P720

Jedná se o profesionální pracovní stanici určenou pro CAD, 3D grafiku, simulace a vývoj.

Díky dvěma procesorovým paticím, ECC pamětem a kvalitnímu chlazení představuje velmi vhodnou platformu i pro lokální provoz AI modelů.

---

## Procesory

2× Intel Xeon Silver 4210

Celkem:

- 20 fyzických jader
- 40 vláken

Procesory zde nehrají hlavní roli při samotném generování obrázků, ale výrazně pomáhají při:

- načítání modelů,
- kompresi dat,
- práci s více aplikacemi současně,
- provozu dalších služeb (například Ollama nebo Open WebUI).

---

## Operační paměť

64 GB DDR4 ECC

Velká systémová paměť umožňuje bez problémů provozovat současně:

- ComfyUI,
- Ollama,
- Docker,
- Open WebUI,
- běžné vývojové nástroje.

---

## Grafická karta

NVIDIA Quadro P5000

Parametry:

- architektura Pascal
- Compute Capability 6.1
- 16 GB GDDR5X
- profesionální ovladače
- velmi nízká spotřeba v klidu

Přestože byla představena již v roce 2016, stále nabízí dostatek výkonu pro modely Stable Diffusion 1.5 a řadu dalších AI úloh.

Právě této kartě je věnována většina tohoto dokumentu.

---

# Použitý software

Operační systém:

- Kubuntu 26.04 LTS

Python:

- Python 3.12.13

Správa verzí Pythonu:

- pyenv

Virtuální prostředí:

- venv

PyTorch:

- 2.4.1 + CUDA 12.1

ComfyUI:

- 0.27.0

GPU:

- NVIDIA Quadro P5000

CUDA Runtime:

- 13.0

NVIDIA Driver:

- 580.159.03

---

# Co se čtenář v tomto dokumentu dozví

V následujících kapitolách bude krok za krokem popsáno:

- proč nebyl použit Python 3.14,
- proč nebyl použit nejnovější PyTorch,
- jak ověřit skutečnou podporu CUDA,
- jak vytvořit stabilní virtuální prostředí,
- jak správně nainstalovat ComfyUI,
- jak organizovat modely mimo adresář aplikace,
- jak vytvořit první workflow,
- jak ověřit, že GPU skutečně pracuje,
- jaké modely jsou pro Quadro P5000 nejvhodnější,
- jak zabránit tomu, aby budoucí aktualizace funkční prostředí poškodily.

Cílem není pouze zprovoznit ComfyUI, ale vytvořit prostředí, které bude spolehlivě fungovat i po několika letech.


