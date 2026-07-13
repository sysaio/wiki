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

# 2. Hledání správné kombinace Pythonu, CUDA a PyTorch

Na první pohled se může zdát, že instalace prostředí pro ComfyUI je jednoduchá.

Stačí nainstalovat:

- nejnovější Python,
- nejnovější PyTorch,
- nejnovější CUDA,
- ComfyUI.

V případě moderních grafických karet architektury Ada nebo Blackwell to bývá většinou správný postup.

U starší profesionální karty NVIDIA Quadro P5000 však tento přístup vedl k několika problémům.

Tato kapitola popisuje celý proces rozhodování.

---

# První pokus – nejnovější dostupné verze

Původní konfigurace byla postavena na nejnovějších dostupných verzích.

Použit byl:

- Python 3.14
- PyTorch 2.13
- CUDA 13 wheels

Instalace proběhla bez problémů.

ComfyUI se spustilo.

GPU bylo rozpoznáno.

Na první pohled vše vypadalo správně.

Ověření:

```bash
python -c "import torch; print(torch.cuda.is_available())"
```

Výstup:

```text
True
```

Také název grafické karty byl správný.

```bash
python -c "import torch; print(torch.cuda.get_device_name(0))"
```

Výstup:

```text
Quadro P5000
```

Ani zde nebyl žádný problém.

Další kontrola:

```bash
python -c "import torch; print(torch.cuda.get_device_capability())"
```

Výstup:

```text
(6, 1)
```

Compute Capability byla rozpoznána správně.

Zdálo se tedy, že vše funguje.

---

# Proč to ještě neznamená správnou akceleraci

Mnoho návodů na internetu končí právě zde.

Pokud:

- `torch.cuda.is_available()` vrátí `True`,
- GPU je rozpoznáno,
- ComfyUI se spustí,

považují instalaci za hotovou.

To však nemusí znamenat, že PyTorch skutečně obsahuje optimalizované CUDA kernely pro konkrétní architekturu GPU.

Rozhodující je ještě jeden příkaz.

```bash
python -c "import torch; print(torch.cuda.get_arch_list())"
```

Výsledek byl následující:

```text
[
 'sm_50',
 'sm_60',
 'sm_70',
 'sm_75',
 'sm_80',
 'sm_86',
 'sm_90'
]
```

Na první pohled není zřejmé, co tento seznam znamená.

Ve skutečnosti jde o seznam architektur GPU, pro které byl PyTorch zkompilován.

A právě zde se objevil problém.

---

# Chybějící SM 6.1

Quadro P5000 používá architekturu:

```text
SM 6.1
```

V seznamu však byla pouze:

```text
sm_60
```

a poté až

```text
sm_70
```

Architektura **SM61 chyběla**.

To znamenalo, že PyTorch již neobsahuje nativně zkompilované CUDA kernely optimalizované právě pro Pascal.

GPU sice fungovalo.

Výpočty probíhaly na CUDA.

Ale část optimalizací již nebyla k dispozici.

Právě zde padlo první důležité rozhodnutí.

---

# Hledání vhodnější konfigurace

Existovaly dvě možnosti.

## Varianta A

Používat nejnovější PyTorch.

Výhody:

- nejnovější funkce
- dlouhodobá podpora

Nevýhody:

- chybějící optimalizace pro Pascal
- potenciálně nižší výkon
- riziko dalších změn v budoucích verzích

---

## Varianta B

Vrátit se k poslední stabilní verzi PyTorch, která byla vytvořena ještě v době plné podpory Pascal.

Výhody:

- ověřená kompatibilita
- stabilní CUDA kernels
- výborná podpora Stable Diffusion 1.5

Nevýhody:

- chybí některé nejnovější experimentální funkce

Protože cílem projektu byla především stabilita, byla zvolena právě tato cesta.

---

# Proč jsme nepoužili Python 3.14

Další komplikace se objevila při pokusu o instalaci staršího PyTorch.

Při použití Pythonu 3.14 se ukázalo, že požadované binární balíčky (wheel) pro některé kombinace verzí jednoduše neexistují.

Například:

```bash
pip install torch==2.4.1
```

nebylo možné úspěšně dokončit.

Nešlo o chybu instalace.

Wheel pro danou kombinaci Pythonu a CUDA nebyl vůbec vydán.

To je poměrně častý problém u velmi nových verzí Pythonu.

Nové interpretry bývají podporovány až s odstupem několika měsíců.

---

# Přechod na Python 3.12

Po zvážení všech možností padlo rozhodnutí přejít na Python 3.12.

Důvodů bylo několik.

Python 3.12 představuje v současnosti jednu z nejlépe podporovaných verzí pro oblast strojového učení.

Je podporován:

- PyTorch
- ComfyUI
- Hugging Face
- Diffusers
- xFormers
- většinou AI knihoven

Současně je dostatečně nový a přitom velmi stabilní.

Použitá verze:

```text
Python 3.12.13
```

---

# Proč pyenv

Dalším rozhodnutím bylo nepoužívat systémový Python.

Linux distribuce využívá vlastní Python pro řadu systémových nástrojů.

Jeho nahrazení může způsobit obtížně hledatelné problémy.

Proto byl použit:

```text
pyenv
```

Výhody tohoto řešení:

- žádný zásah do systému,
- možnost mít více verzí Pythonu současně,
- jednoduché vytváření nových prostředí,
- snadná obnova po reinstalaci.

Díky tomu lze mít například:

```text
Python 3.10
Python 3.12
Python 3.13
Python 3.14
```

vedle sebe bez jakéhokoliv konfliktu.

---

# Vytvoření samostatného virtuálního prostředí

Jakmile byl nainstalován Python 3.12, vzniklo nové virtuální prostředí.

To má několik výhod.

Každý projekt může používat vlastní:

- Python,
- PyTorch,
- knihovny,
- závislosti.

Žádná změna se nedotkne ostatních projektů.

Použité umístění:

```text
/mnt/models/envs/comfyui312
```

Název byl zvolen záměrně.

Za několik let bude z názvu okamžitě patrné, že jde o prostředí založené na Pythonu 3.12.

---

# Výběr finální konfigurace

Po několika testech byla jako nejvhodnější zvolena následující kombinace.

| Komponenta | Verze |
|------------|--------|
| Python | 3.12.13 |
| PyTorch | 2.4.1 |
| TorchVision | 0.19.1 |
| TorchAudio | 2.4.1 |
| CUDA Wheels | cu121 |
| GPU | NVIDIA Quadro P5000 |
| Compute Capability | 6.1 |

Právě tato konfigurace byla následně použita pro všechny další kroky dokumentace.

---

# Závěr kapitoly

Nejdůležitější poznatek z této části instalace je jednoduchý.

Skutečnost, že:

- GPU je detekováno,
- CUDA je dostupná,
- ComfyUI se spustí,

ještě neznamená, že používáme optimální konfiguraci.

Vyplatí se věnovat několik desítek minut ověření kompatibility jednotlivých verzí.

V našem případě vedla změna z Pythonu 3.14 na Python 3.12 a přechod na PyTorch 2.4.1 k prostředí, které je stabilní, dobře podporované a vhodné právě pro architekturu NVIDIA Pascal.

# 3. Instalace Pythonu pomocí pyenv a vytvoření izolovaného prostředí

V předchozí kapitole jsme si vysvětlili, proč jsme se rozhodli nepoužít systémový Python a proč jsme zvolili Python 3.12.

V této kapitole projdeme kompletní vytvoření prostředí, které bude sloužit pouze pro ComfyUI.

Výsledkem bude zcela izolovaná instalace, která nebude nijak zasahovat do operačního systému.

---

# Proč nepoužívat systémový Python

Na většině linuxových distribucí je Python používán nejen uživatelem, ale i samotným systémem.

Používají jej například:

- správce balíčků,
- některé grafické nástroje,
- systémové utility,
- různé služby běžící na pozadí.

Instalace nebo aktualizace knihoven přímo do systémového Pythonu může vést ke konfliktům.

Moderní distribuce (včetně Ubuntu a Kubuntu) proto používají mechanismus PEP 668, který instalaci balíčků do systémového prostředí přímo blokuje.

Pokud se pokusíme použít systémový `pip`, můžeme narazit například na chybu:

```text
error: externally-managed-environment
```

To není chyba Pythonu.

Naopak.

Operační systém tím chrání vlastní instalaci.

---

# Proč právě pyenv

Existuje několik možností, jak používat více verzí Pythonu.

Nejčastější jsou:

- systémový Python,
- Docker,
- Conda,
- pyenv.

Pro tento projekt byl zvolen **pyenv**.

Hlavní důvody:

- nezasahuje do systému,
- umožňuje mít více verzí Pythonu současně,
- je jednoduchý,
- používá jej velká část vývojářské komunity.

Například lze mít současně:

```text
Python 3.10
Python 3.11
Python 3.12
Python 3.13
Python 3.14
```

Každý projekt si pak vybere vlastní interpret.

---

# Ověření instalace pyenv

Nejprve ověříme, že je pyenv skutečně nainstalován.

```bash
pyenv --version
```

Příklad výstupu:

```text
pyenv 2.7.3
```

Pokud se zobrazí číslo verze, je vše v pořádku.

---

# Zobrazení dostupných verzí Pythonu

Před instalací lze vypsat všechny podporované verze.

```bash
pyenv install --list | grep "3.12"
```

V době vzniku tohoto dokumentu byl výstup například:

```text
3.12.0
3.12.1
...
3.12.13
```

Použita byla poslední dostupná stabilní verze.

---

# Instalace Pythonu 3.12

Samotná instalace:

```bash
pyenv install 3.12.13
```

Kompilace může podle výkonu procesoru trvat několik minut.

Po dokončení se zobrazí přibližně:

```text
Installed Python-3.12.13
```

---

# Ověření umístění interpretru

Nově nainstalovaný Python se nachází přibližně zde:

```text
~/.pyenv/versions/3.12.13/
```

Konkrétně interpreter:

```text
~/.pyenv/versions/3.12.13/bin/python
```

To znamená, že nebyl přepsán systémový Python.

---

# Vytvoření adresáře pro virtuální prostředí

V tomto projektu jsme se rozhodli ukládat virtuální prostředí mimo domovský adresář.

Použité umístění:

```text
/mnt/models/envs/
```

Vytvoření adresáře:

```bash
mkdir -p /mnt/models/envs
```

Parametr `-p` zajistí vytvoření adresáře pouze tehdy, pokud ještě neexistuje.

---

# Vytvoření virtuálního prostředí

Použijeme interpreter nainstalovaný pomocí pyenv.

```bash
~/.pyenv/versions/3.12.13/bin/python \
    -m venv \
    /mnt/models/envs/comfyui312
```

Po dokončení vznikne kompletní izolované prostředí.

---

# Aktivace prostředí

```bash
source /mnt/models/envs/comfyui312/bin/activate
```

Prompt shellu se obvykle změní například na:

```text
(comfyui312)
```

Od této chvíle budou všechny instalované balíčky uloženy pouze do tohoto prostředí.

---

# Kontrola použitého Pythonu

Nejdůležitější kontrola.

```bash
python --version
```

Očekávaný výstup:

```text
Python 3.12.13
```

Dále ověříme cestu k interpreteru.

```bash
which python
```

Správný výstup:

```text
/mnt/models/envs/comfyui312/bin/python
```

Pokud se zobrazí například:

```text
/usr/bin/python
```

pak prostředí není aktivní.

---

# Kontrola pip

Stejně důležité je ověřit i správný `pip`.

```bash
which pip
```

Správný výstup:

```text
/mnt/models/envs/comfyui312/bin/pip
```

Pokud se zobrazí systémový `pip`, instalace balíčků nebude probíhat do virtuálního prostředí.

---

# Doporučený způsob práce

Před každou prací s ComfyUI doporučuji provést pouze tři příkazy.

```bash
source /mnt/models/envs/comfyui312/bin/activate

cd /mnt/models/comfyui

python main.py
```

Tím máme jistotu, že:

- používáme správný Python,
- používáme správný PyTorch,
- používáme správné knihovny,
- nedochází ke konfliktu se systémem.

---

# Ověření funkčnosti prostředí

Po vytvoření prostředí doporučuji vždy provést následující kontroly.

Verze Pythonu:

```bash
python --version
```

Interpreter:

```bash
which python
```

Pip:

```bash
which pip
```

Pokud všechny tři příkazy ukazují do adresáře:

```text
/mnt/models/envs/comfyui312/
```

je prostředí připraveno.

---

# Poznámka k budoucím projektům

Velkou výhodou tohoto přístupu je možnost vytvořit další prostředí během několika minut.

Například:

```text
/mnt/models/envs/comfyui312
/mnt/models/envs/fooocus312
/mnt/models/envs/sdnext312
/mnt/models/envs/test313
```

Každé z nich může obsahovat jinou verzi Pythonu nebo jinou verzi PyTorch.

Projekty se navzájem nijak neovlivňují.

Právě tato izolace je jedním z hlavních důvodů, proč je kombinace **pyenv + venv** dnes považována za jeden z nejčistších způsobů práce s Pythonem na Linuxu.

---

# Shrnutí kapitoly

V této kapitole jsme:

- nainstalovali Python 3.12 pomocí pyenv,
- vytvořili samostatné virtuální prostředí,
- ověřili správnou aktivaci prostředí,
- zkontrolovali interpreter Pythonu,
- zkontrolovali správný `pip`.

Nyní máme připravený základ pro instalaci PyTorch a všech dalších knihoven, aniž bychom jakkoliv zasáhli do systémové instalace Linuxu.

# 4. Instalace PyTorch 2.4.1 a ověření CUDA akcelerace

Po vytvoření virtuálního prostředí bylo potřeba nainstalovat samotný PyTorch.

Na první pohled se může zdát, že stačí použít příkaz:

```bash
pip install torch
```

V našem případě by to ale byla chyba.

Cílem nebylo získat nejnovější verzi, ale poslední stabilní kombinaci, která stále dobře podporuje grafické karty architektury Pascal.

---

# Proč právě PyTorch 2.4.1

Po několika testech jsme skončili u následující kombinace:

| Komponenta | Verze |
|------------|--------|
| Python | 3.12.13 |
| PyTorch | 2.4.1 |
| TorchVision | 0.19.1 |
| TorchAudio | 2.4.1 |
| CUDA Wheels | cu121 |

Tato kombinace se ukázala jako nejstabilnější.

Novější verze PyTorch sice fungovaly, ale již neobsahovaly plnou podporu architektury Pascal a při spuštění ComfyUI se objevovala upozornění typu:

```text
WARNING: You need pytorch with cu130 or higher to use optimized CUDA operations.
```

To není kritická chyba.

Pouze informace, že některé novější optimalizace již naše karta využívat nebude.

Pro Stable Diffusion 1.5 to však nepředstavuje praktický problém.

---

# Instalace

Nejprve aktivujeme virtuální prostředí.

```bash
source /mnt/models/envs/comfyui312/bin/activate
```

Poté provedeme instalaci.

```bash
pip install \
    torch==2.4.1 \
    torchvision==0.19.1 \
    torchaudio==2.4.1 \
    --index-url https://download.pytorch.org/whl/cu121
```

Použití oficiálního PyTorch indexu zajistí instalaci balíčků obsahujících podporu CUDA.

---

# Kontrola nainstalovaných balíčků

Po dokončení doporučuji vždy ověřit skutečně nainstalované verze.

```bash
pip list | grep -E "torch|vision|audio"
```

Výstup:

```text
torch          2.4.1+cu121
torchaudio     2.4.1+cu121
torchvision    0.19.1+cu121
```

Přípona `+cu121` potvrzuje, že nejde o CPU variantu.

---

# Ověření verze PyTorch

```bash
python -c "import torch; print(torch.__version__)"
```

Výstup:

```text
2.4.1+cu121
```

---

# Ověření dostupnosti CUDA

```bash
python -c "import torch; print(torch.cuda.is_available())"
```

Výstup:

```text
True
```

Pokud by se zobrazilo:

```text
False
```

PyTorch GPU nevidí.

V takovém případě nemá smysl pokračovat dál, dokud není problém odstraněn.

---

# Ověření grafické karty

```bash
python -c "import torch; print(torch.cuda.get_device_name(0))"
```

Výstup:

```text
Quadro P5000
```

To potvrzuje, že CUDA komunikuje se správným hardwarem.

---

# Ověření Compute Capability

Dalším krokem bylo ověřit architekturu GPU.

```bash
python -c "import torch; print(torch.cuda.get_device_capability())"
```

Výstup:

```text
(6, 1)
```

To odpovídá architektuře Pascal (SM 6.1).

---

# Ověření podporovaných architektur

Nakonec jsme zkontrolovali, pro které architektury byl PyTorch zkompilován.

```bash
python -c "import torch; print(torch.cuda.get_arch_list())"
```

Výstup:

```text
['sm_50',
 'sm_60',
 'sm_70',
 'sm_75',
 'sm_80',
 'sm_86',
 'sm_90']
```

Právě zde jsme zjistili, že novější build již explicitně neobsahuje `sm_61`.

To byl jeden z hlavních důvodů, proč jsme se rozhodli zůstat u této ověřené konfigurace místo neustálého honění nejnovějších verzí.

---

# Praktický benchmark GPU

Samotná detekce GPU ještě neznamená, že GPU opravdu pracuje naplno.

Proto jsme provedli jednoduchý výpočet matic.

```python
import torch
import time

device = "cuda"

a = torch.randn((4096,4096), device=device)
b = torch.randn((4096,4096), device=device)

torch.cuda.synchronize()

t0 = time.time()

for _ in range(20):
    c = torch.matmul(a, b)

torch.cuda.synchronize()

print(f"Elapsed: {time.time()-t0:.3f} s")
```

Výsledky se pohybovaly přibližně kolem:

```text
Elapsed: 0.42 s
```

To samo o sobě není důležité.

Důležité bylo sledovat během testu využití GPU.

---

# Dlouhý benchmark

Krátký benchmark trvá méně než sekundu.

GPU proto často ani nestihne zobrazit vysoké vytížení.

Proto jsme připravili delší variantu.

```python
import torch
import time

device = "cuda"

a = torch.randn((4096,4096), device=device)
b = torch.randn((4096,4096), device=device)

torch.cuda.synchronize()

t0 = time.time()

iterations = 600

for _ in range(iterations):
    c = torch.matmul(a, b)

torch.cuda.synchronize()

elapsed = time.time() - t0

print(f"Elapsed: {elapsed:.2f} s")
print(f"Iterations: {iterations}")
print(f"{iterations/elapsed:.2f} matmul/s")
```

Během tohoto testu bylo možné sledovat například pomocí:

```bash
nvidia-smi
```

že vytížení GPU vyskočilo téměř okamžitě na 100 %.

To byl nejlepší důkaz, že výpočty skutečně probíhají na grafické kartě.

---

# Proč benchmark vůbec dělat

Řada uživatelů skončí u informace:

```text
CUDA available: True
```

To však nestačí.

Teprve skutečný výpočet ukáže:

- že GPU opravdu počítá,
- že nejsme omylem na CPU,
- že nejsou problémy s ovladači,
- že výkon odpovídá očekávání.

Je to jednoduchý test, který zabere několik sekund a může ušetřit hodiny hledání chyb.

---

# Shrnutí kapitoly

Po dokončení této části jsme měli ověřeno:

- správnou verzi PyTorch,
- správnou verzi CUDA,
- funkční GPU,
- správně rozpoznanou Quadro P5000,
- Compute Capability 6.1,
- úspěšné provádění výpočtů na GPU,
- reálné vytížení grafické karty během benchmarku.

Tím bylo prostředí připraveno pro samotnou instalaci a spuštění ComfyUI.

# 5. První spuštění ComfyUI

Po úspěšné instalaci Pythonu, PyTorch a CUDA bylo možné přejít k samotnému spuštění ComfyUI.

Tentokrát již ve zcela novém prostředí založeném na:

- Python 3.12.13
- PyTorch 2.4.1 + CUDA 12.1
- NVIDIA Quadro P5000 (Pascal, 16 GB VRAM)

---

# Přechod do projektu

Nejprve aktivujeme virtuální prostředí.

```bash
source /mnt/models/envs/comfyui312/bin/activate
```

Poté přejdeme do adresáře ComfyUI.

```bash
cd /mnt/models/comfyui
```

---

# Kontrola prostředí

Před spuštěním doporučuji vždy zkontrolovat, že používáme správný Python.

```bash
python --version
```

Výstup:

```text
Python 3.12.13
```

Dále ověříme PyTorch.

```bash
python -c "import torch; print(torch.__version__)"
```

Výstup:

```text
2.4.1+cu121
```

Tím máme jistotu, že skutečně používáme nově vytvořené prostředí.

---

# Spuštění ComfyUI

Samotné spuštění je velmi jednoduché.

```bash
python main.py
```

Po několika sekundách začne ComfyUI vypisovat informace o inicializaci.

Většina těchto zpráv je pouze informativní.

Není potřeba se jich lekat.

---

# Informace o grafické kartě

Jedna z nejdůležitějších částí výpisu je tato.

```text
Total VRAM 16264 MB
```

To potvrzuje správnou detekci 16 GB grafické paměti.

Dále:

```text
Device:
cuda:0
Quadro P5000
```

To znamená, že ComfyUI používá CUDA zařízení číslo 0.

---

# Stav VRAM

Ve výpisu se objeví například:

```text
Set vram state to:
NORMAL_VRAM
```

To znamená, že ComfyUI nebude agresivně přesouvat modely mezi RAM a VRAM.

Na kartě s 16 GB je to správná volba.

---

# Async Memory

Další zajímavá informace:

```text
cudaMallocAsync
```

a

```text
Using async weight offloading
```

Novější verze PyTorch používají modernější správu CUDA paměti.

Výsledkem bývá:

- menší fragmentace VRAM,
- stabilnější běh,
- rychlejší načítání modelů.

---

# Pinned Memory

Další řádek:

```text
Enabled pinned memory
```

Pinned memory umožňuje rychlejší kopírování dat mezi RAM a VRAM.

Není potřeba nic nastavovat.

Pokud se tato hláška objeví, vše funguje správně.

---

# Pozornost věnujte pouze hláškám ERROR

Ve výpisu se mohou objevit různá upozornění.

Například:

```text
WARNING:
Unsupported Pytorch detected.
DynamicVRAM support requires Pytorch version 2.8 or later.
```

To není chyba.

Pouze informace, že některé nejnovější funkce nejsou dostupné.

Na provoz Stable Diffusion 1.5 to nemá prakticky žádný vliv.

---

# Upozornění na CUDA 13

Objevila se také zpráva:

```text
You need pytorch with cu130 or higher
to use optimized CUDA operations.
```

Ani tato hláška není kritická.

Pouze oznamuje, že některé nové optimalizace byly napsány až pro CUDA 13.

Na architektuře Pascal je jejich význam minimální.

Rozhodli jsme se proto zůstat u stabilnější konfigurace CUDA 12.1.

---

# Databáze

Při prvním spuštění ComfyUI vytvoří interní databázi.

Ve výpisu se objeví například:

```text
Running upgrade...
```

nebo

```text
Database upgraded...
```

To je zcela normální.

Provádí se pouze při prvním spuštění nebo po aktualizaci ComfyUI.

---

# Frontend

Ve výpisu se objeví také informace o webovém rozhraní.

Například:

```text
comfyui-frontend-package
```

To znamená, že byl úspěšně načten grafický frontend.

---

# Webový server

Úplně na konci výpisu se objeví nejdůležitější řádek.

```text
Starting server
```

Po několika okamžicích následuje:

```text
To see the GUI go to:

http://127.0.0.1:8188
```

To znamená, že ComfyUI běží.

Stačí otevřít webový prohlížeč.

```
http://127.0.0.1:8188
```

Pokud se otevírá na stejném počítači, není potřeba nic dalšího nastavovat.

---

# Jak poznat, že je vše v pořádku

Správně spuštěné ComfyUI má obvykle tyto znaky.

✔ Python 3.12

✔ PyTorch 2.4.1

✔ CUDA zařízení nalezeno

✔ Quadro P5000 rozpoznána

✔ Přibližně 16 GB VRAM

✔ Server naslouchá na portu 8188

✔ Žádná hláška ERROR

Pokud platí všechny body výše, je instalace úspěšná.

---

# Co jsme zatím ještě neměli

Po prvním spuštění bylo prostředí připravené, ale stále chyběly samotné modely.

Bez checkpointu neumí ComfyUI generovat obrázky.

To bude cílem následující kapitoly.

---

# Shrnutí kapitoly

V této části jsme:

- poprvé spustili ComfyUI,
- ověřili správnou detekci GPU,
- zkontrolovali VRAM,
- prošli význam jednotlivých hlášek,
- ověřili spuštění webového rozhraní.

Tím byla dokončena samotná instalace prostředí.

V následující kapitole připravíme adresářovou strukturu pro modely, nastavíme `extra_model_paths.yaml` a stáhneme první checkpoint Stable Diffusion.

# 6. Centrální knihovna modelů a první checkpoint

Jakmile bylo ComfyUI úspěšně spuštěno, bylo potřeba vyřešit ještě jednu důležitou věc.

Kam ukládat AI modely?

Na první pohled se nabízí použít výchozí adresáře uvnitř ComfyUI.

Například:

```text
comfyui/models/checkpoints
```

To funguje.

Jenže má jednu zásadní nevýhodu.

Pokud někdy:

- přeinstalujeme ComfyUI,
- budeme chtít používat více AI aplikací,
- budeme testovat novou verzi,

budeme modely zbytečně kopírovat nebo přesouvat.

Proto jsme zvolili jinou architekturu.

---

# Samostatný adresář pro všechny modely

Veškeré modely budou uloženy mimo ComfyUI.

Použili jsme adresář:

```text
/mnt/models/ai-models
```

Výhody tohoto řešení:

- modely existují pouze jednou,
- ComfyUI lze kdykoliv smazat,
- jiná AI aplikace může používat stejné soubory,
- zálohování je jednodušší.

Právě tento přístup používá většina lidí, kteří mají větší sbírku modelů.

---

# Navržená struktura adresářů

Vytvořili jsme následující adresářovou strukturu.

```text
/mnt/models/ai-models
│
├── checkpoints
│   ├── sd15
│   ├── sdxl
│   └── experimental
│
├── loras
│   ├── sd15
│   └── sdxl
│
├── controlnet
├── vae
├── embeddings
└── upscale
```

Jednotlivé části mají jasný význam.

---

## checkpoints

Obsahují celé modely.

Například:

- Stable Diffusion 1.5
- DreamShaper
- Juggernaut
- Realistic Vision
- SDXL Base

Právě odtud se vybírá model v uzlu **Load Checkpoint**.

---

## loras

Sem patří všechny LoRA modely.

Například:

- styl kresby,
- anime,
- realistické obličeje,
- architektura,
- fantasy.

Oddělení podle SD15 a SDXL výrazně zpřehledňuje knihovnu.

---

## controlnet

Sem budou později patřit všechny ControlNet modely.

Například:

- Canny
- Depth
- OpenPose
- Tile
- SoftEdge

---

## VAE

Samostatné VAE modely.

Ve většině případů dnes nejsou potřeba.

Je ale dobré mít pro ně připravený adresář.

---

## Embeddings

Textual Inversion.

Malé pomocné modely používané přímo v promptu.

---

## Upscale

Sem budou patřit ESRGAN a další modely pro zvětšování obrázků.

---

# Vytvoření adresářů

Celou strukturu vytvoří jediný příkaz.

```bash
mkdir -p \
/mnt/models/ai-models/{checkpoints/{sd15,sdxl,experimental},loras/{sd15,sdxl},vae,controlnet,embeddings,upscale}
```

Kontrola:

```bash
tree -L 3 /mnt/models/ai-models
```

Výstup by měl být podobný tomuto:

```text
ai-models
├── checkpoints
│   ├── experimental
│   ├── sd15
│   └── sdxl
├── controlnet
├── embeddings
├── loras
│   ├── sd15
│   └── sdxl
├── upscale
└── vae
```

---

# Proč nepoužívat models/

ComfyUI standardně očekává modely zde:

```text
comfyui/models
```

To je vhodné pouze pro malé instalace.

My jsme chtěli mít modely oddělené od aplikace.

Proto využijeme soubor:

```text
extra_model_paths.yaml
```

---

# Vytvoření konfiguračního souboru

Nejprve zkopírujeme vzor.

```bash
cd /mnt/models/comfyui

cp extra_model_paths.yaml.example extra_model_paths.yaml
```

Tím vznikne nový konfigurační soubor.

---

# Nastavení vlastních cest

Do souboru jsme přidali vlastní konfiguraci.

```yaml
ai-models:
  base_path: /mnt/models/ai-models

  checkpoints: |
    checkpoints/sd15
    checkpoints/sdxl
    checkpoints/experimental

  loras: |
    loras/sd15
    loras/sdxl

  vae: vae
  controlnet: controlnet
  embeddings: embeddings
  upscale_models: upscale
```

Po restartu začne ComfyUI automaticky používat tyto adresáře.

Výchozí adresář `models/` uvnitř ComfyUI přitom zůstává zachován.

Lze tedy používat oba způsoby současně.

---

# Instalace Hugging Face CLI

Modely budeme stahovat přímo z Hugging Face.

Nejprve ověříme, že máme nainstalovaný nástroj `hf`.

```bash
hf --help
```

Pokud se zobrazí seznam příkazů, je vše připraveno.

Není nutné se přihlašovat.

Pouze se při stahování zobrazí upozornění na nižší rychlost.

---

# První model

Jako první jsme zvolili model DreamShaper 8.

Jedná se o jeden z nejznámějších modelů postavených na Stable Diffusion 1.5.

Model kombinuje:

- realistické fotografie,
- ilustrace,
- fantasy,
- digitální umění.

Současně je velmi nenáročný na VRAM.

Proto je ideální pro grafické karty architektury Pascal.

---

# Stažení modelu

Po několika pokusech se ukázalo, že správný název souboru je:

```text
DreamShaper_8_pruned.safetensors
```

Po stažení jsme jej uložili do:

```text
/mnt/models/ai-models/checkpoints/sd15/
```

Kontrola:

```bash
ls -lh /mnt/models/ai-models/checkpoints/sd15
```

Výstup:

```text
DreamShaper_8_pruned.safetensors
```

Velikost přibližně:

```text
2 GB
```

---

# Restart ComfyUI

Po přidání nového modelu je vhodné ComfyUI restartovat.

Po opětovném spuštění se nový checkpoint automaticky objeví v seznamu modelů.

Nebyla potřeba žádná další konfigurace.

---

# Ověření

Ve webovém rozhraní otevřeme uzel:

```text
Load Checkpoint
```

V rozbalovacím seznamu by měl být vidět:

```text
DreamShaper_8_pruned
```

Pokud je model v seznamu, znamená to, že:

- `extra_model_paths.yaml` je správně nastaven,
- ComfyUI našlo centrální knihovnu modelů,
- checkpoint je připraven k použití.

---

# Shrnutí kapitoly

V této části jsme:

- vytvořili centrální knihovnu modelů,
- navrhli přehlednou adresářovou strukturu,
- nastavili `extra_model_paths.yaml`,
- připravili Hugging Face CLI,
- stáhli první checkpoint,
- úspěšně jej zpřístupnili v ComfyUI.

V následující kapitole vytvoříme první workflow a vygenerujeme první obrázek pomocí modelu DreamShaper 8.

# 7. První workflow a první vygenerovaný obrázek

Po dokončení instalace a přidání prvního modelu bylo konečně možné vyzkoušet samotné generování obrázků.

Přestože je ComfyUI velmi výkonný nástroj, první spuštění může být pro nového uživatele poněkud matoucí.

Na rozdíl od Automatic1111 nebo Fooocus zde není žádné jednoduché textové pole pro prompt.

Vše se skládá pomocí grafu (workflow), kde jednotlivé uzly představují jednotlivé části procesu generování.

---

# Prázdné prostředí

Po prvním spuštění se může stát, že je pracovní plocha úplně prázdná.

V levé části okna se zobrazí pouze informace:

```text
Empty

No workflows found.
```

To není chyba.

ComfyUI jednoduše ještě neobsahuje žádný uložený workflow.

---

# Kam ukládat workflow

Zjistili jsme, že ComfyUI automaticky hledá workflow v adresáři:

```text
/mnt/models/comfyui/user/default/workflows/
```

Stačilo tedy do tohoto adresáře zkopírovat připravený workflow.

Po restartu nebo obnovení stránky se workflow okamžitě objevilo v nabídce.

Nebylo potřeba nic importovat.

---

# Načtení workflow

Po otevření workflow se zobrazilo několik základních uzlů.

Typicky:

- Load Checkpoint
- CLIP Text Encode (Positive)
- CLIP Text Encode (Negative)
- Empty Latent Image
- KSampler
- VAE Decode
- Save Image

To je nejjednodušší použitelný graf pro Stable Diffusion.

---

# Výběr modelu

V uzlu **Load Checkpoint** jsme vybrali:

```text
DreamShaper_8_pruned
```

Po výběru modelu ComfyUI automaticky načetlo:

- UNet,
- CLIP,
- VAE.

Tyto tři části jsou uvnitř checkpointu uloženy společně.

---

# Připojení CLIP

Jedna z prvních nejasností vznikla u uzlů:

```text
CLIP Text Encode
```

Ty mají vstup:

```text
clip
```

Ten je potřeba propojit s výstupem:

```text
CLIP
```

z uzlu **Load Checkpoint**.

Je potřeba vytvořit dvě spojení.

Jedno pro:

```text
Positive Prompt
```

a druhé pro:

```text
Negative Prompt
```

Bez tohoto propojení nelze prompt zpracovat.

---

# Nastavení promptu

Do pozitivního promptu jsme zadali například:

```text
portrait of a medieval knight,
highly detailed,
cinematic lighting,
8k,
masterpiece
```

Negativní prompt může být například:

```text
low quality,
blurry,
deformed,
bad anatomy,
watermark,
text
```

Model DreamShaper na podobné prompty reaguje velmi dobře.

---

# Nastavení velikosti obrázku

V uzlu:

```text
Empty Latent Image
```

jsme ponechali klasické rozlišení:

```text
512 × 512
```

To odpovídá Stable Diffusion 1.5.

Je to zároveň nejrychlejší varianta.

---

# Nastavení KSampleru

Použili jsme například:

Sampler:

```text
DPM++ 2M Karras
```

Počet kroků:

```text
25
```

CFG Scale:

```text
7
```

Seed:

```text
Random
```

Tyto hodnoty představují velmi dobrý výchozí bod.

---

# Chyba u Save Image

První pokus skončil chybou:

```text
ERROR

Required input is missing
```

Příčina byla jednoduchá.

Uzel **Save Image** neměl připojen vstup:

```text
images
```

Stačilo propojit výstup:

```text
IMAGE
```

z uzlu **VAE Decode**

na vstup:

```text
images
```

u **Save Image**.

Po tomto propojení chyba zmizela.

---

# První spuštění

Po stisknutí tlačítka:

```text
Queue Prompt
```

začala Quadro P5000 okamžitě počítat.

Bylo možné sledovat:

```bash
nvidia-smi
```

kde vytížení GPU vyskočilo téměř na 100 %.

To byl jasný důkaz, že celý pipeline běží na CUDA.

---

# První obrázky

První generování proběhlo bez problémů.

Během několika desítek sekund vzniklo několik obrázků.

Výsledek byl překvapivě kvalitní.

Ukázalo se, že i grafická karta z roku 2017 je stále schopna velmi dobře provozovat Stable Diffusion 1.5.

---

# Kam se obrázky ukládají

Ve výchozím nastavení ComfyUI ukládá obrázky do:

```text
/mnt/models/comfyui/output/
```

Každý obrázek dostane automaticky unikátní název.

Současně se ukládají i metadata.

To umožňuje pozdější rekonstrukci workflow.

---

# Co jsme se během prvního workflow naučili

První generování ukázalo několik důležitých věcí.

- ComfyUI není složité.
- Každý uzel má jasně definované vstupy a výstupy.
- Pokud některý vstup chybí, ComfyUI přesně označí problém.
- Workflow lze velmi snadno rozšiřovat.

Po pochopení několika základních uzlů začíná být práce velmi intuitivní.

---

# Výkon Quadro P5000

Během testování se ukázalo, že Quadro P5000 je pro Stable Diffusion 1.5 stále velmi dobře použitelná.

Výhody:

- 16 GB VRAM
- dostatek CUDA jader
- stabilní ovladače
- nízká pořizovací cena na trhu s použitým hardwarem

Nevýhody:

- nepodporuje nejnovější CUDA optimalizace
- nepodporuje Tensor Core
- SDXL již není tak komfortní jako na novějších kartách

Přesto je pro SD 1.5 výbornou volbou.

---

# Shrnutí kapitoly

Po dokončení této části jsme úspěšně:

- načetli první workflow,
- vybrali model DreamShaper 8,
- správně propojili všechny uzly,
- odstranili chybu u Save Image,
- spustili první generování,
- ověřili zatížení GPU,
- vytvořili první obrázky.

Tím byla základní instalace ComfyUI úspěšně dokončena.

Od této chvíle lze začít experimentovat s dalšími modely, LoRA, ControlNet, upscalery a postupně budovat vlastní knihovnu workflow.

# 8. Doporučené modely pro NVIDIA Pascal (Stable Diffusion 1.5)

Po úspěšném zprovoznění ComfyUI přichází nejzajímavější část.

Výběr modelů.

Na internetu dnes existují desetitisíce checkpointů.

Velká část z nich je však pouze drobnou modifikací jiného modelu nebo krátkodobým experimentem.

Místo nekonečného stahování je mnohem rozumnější postavit si menší, kvalitní knihovnu modelů, které se vzájemně dobře doplňují.

Přesně takový přístup jsme zvolili i v tomto projektu.

---

# Proč začínat se Stable Diffusion 1.5

Grafická karta NVIDIA Quadro P5000 disponuje:

- 16 GB VRAM,
- architekturou Pascal,
- Compute Capability 6.1.

To znamená, že bez problémů zvládá Stable Diffusion 1.5.

Naopak modely SDXL již vyžadují výrazně více výpočetního výkonu.

Neznamená to, že SDXL nelze používat.

Pouze nebude tak pohodlný jako na novějších kartách.

Proto doporučuji nejprve vybudovat kvalitní knihovnu SD 1.5 modelů.

Jejich kvalita je i po několika letech stále velmi vysoká.

---

# Jak modely vybírat

Při výběru checkpointů jsem se řídil několika jednoduchými pravidly.

Model musí být:

- dlouhodobě prověřený komunitou,
- aktivně používaný,
- kvalitně zdokumentovaný,
- dobře fungovat na SD 1.5,
- mít odlišný charakter než ostatní modely.

Nemá smysl mít deset téměř stejných checkpointů.

Lepší je mít několik opravdu kvalitních.

---

# DreamShaper 8

První model, který jsme nainstalovali.

Charakter:

- univerzální,
- velmi kvalitní,
- rychlý,
- vhodný pro začátečníky.

Silné stránky:

- fantasy,
- portréty,
- ilustrace,
- concept art,
- digitální malba.

Je to ideální první model.

Pokud bych měl doporučit jediný checkpoint pro první měsíc práce s ComfyUI, byl by to právě DreamShaper.

---

# Realistic Vision

Jeden z nejlepších realistických modelů celé generace SD 1.5.

Použití:

- fotografie,
- portréty,
- krajiny,
- architektura,
- produktová fotografie.

Silné stránky:

- přirozené barvy,
- realistická pleť,
- velmi dobré světlo.

Pokud je cílem fotorealismus, je Realistic Vision téměř povinnou součástí knihovny.

---

# Deliberate

Legendární univerzální checkpoint.

Výborně zvládá kombinaci:

- realismu,
- ilustrace,
- fantasy,
- digitálního umění.

Právě díky této univerzálnosti se stal jedním z nejpoužívanějších modelů celé éry SD 1.5.

---

# EpicRealism

Další výborný realistický model.

Ve srovnání s Realistic Vision produkuje často:

- výraznější kontrast,
- dramatičtější světlo,
- filmovější atmosféru.

Je vhodný zejména pro portréty.

---

# AbsoluteReality

Velmi kvalitní model zaměřený na realistické fotografie.

Výhody:

- minimum artefaktů,
- konzistentní výsledky,
- velmi dobrá práce s obličeji.

Často bývá doporučován jako alternativa k Realistic Vision.

---

# Photon

Photon patří mezi novější modely SD 1.5.

Výborně funguje pro:

- produktové fotografie,
- portréty,
- reklamní vizualizace.

Ve srovnání s DreamShaper produkuje čistší a modernější vzhled.

---

# Juggernaut

Juggernaut existuje v několika verzích.

Původně vznikl pro SD 1.5, později přešel na SDXL.

Starší SD 1.5 verze stále stojí za vyzkoušení.

Je vhodná zejména pro:

- fantasy,
- koncepty,
- prostředí,
- detailní ilustrace.

---

# Co zatím nestahovat

Začátečníci často udělají stejnou chybu.

Stáhnou během jednoho večera:

- 150 checkpointů,
- 300 LoRA,
- 50 VAE.

Po týdnu už netuší:

- který model použili,
- proč se obrázky liší,
- co vlastně která LoRA dělá.

Mnohem lepší je postupovat pomalu.

Nejprve opravdu poznat jeden model.

Poté přidat druhý.

Až následně začít experimentovat.

---

# Doporučené pořadí instalace

Pokud bych dnes stavěl novou knihovnu od nuly, postupoval bych přibližně takto.

1. DreamShaper 8
2. Realistic Vision
3. Deliberate
4. EpicRealism
5. AbsoluteReality
6. Photon

Tato šestice pokryje naprostou většinu běžných scénářů.

---

# Organizace checkpointů

Všechny checkpointy ukládáme do:

```text
/mnt/models/ai-models/checkpoints/sd15/
```

Například:

```text
DreamShaper_8_pruned.safetensors

RealisticVisionV60.safetensors

Deliberate_v6.safetensors

EpicRealism.safetensors

AbsoluteReality.safetensors

Photon.safetensors
```

Taková knihovna zůstává přehledná i po několika letech.

---

# Doporučení z praxe

Nejdůležitější poznatek z celého testování je jednoduchý.

Kvalitu obrázků určuje především:

- správný prompt,
- správně zvolený model,
- zkušenosti uživatele.

Ne počet checkpointů uložených na disku.

Je lepší dokonale poznat pět modelů než vlastnit dvě stě modelů, které člověk nikdy nepoužije.

---

# Shrnutí kapitoly

Pro grafickou kartu NVIDIA Quadro P5000 doporučuji jako základ knihovny následující modely:

- DreamShaper 8
- Realistic Vision
- Deliberate
- EpicRealism
- AbsoluteReality
- Photon

Všechny jsou postaveny na Stable Diffusion 1.5, mají dlouhodobě výbornou reputaci a poskytují velmi kvalitní výsledky i na starším profesionálním hardwaru.

Teprve po jejich zvládnutí doporučuji začít experimentovat s SDXL, Flux nebo dalšími modernějšími architekturami.
