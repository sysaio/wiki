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
