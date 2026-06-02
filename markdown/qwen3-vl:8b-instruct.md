# 🏠 Průvodce instalací lokálního AI prostředí na Lenovo ThinkStation P720

Vítejte v dokumentaci pro nasazení open-source umělé inteligence na vlastním hardwaru. Tento návod slouží jako kompletní, krok za krokem přehled a konfigurační kuchařka. Všechny popsané modely a postupy jsou navrženy pro plně offline provoz, bez odesílání dat na internet a bez licenčních poplatků.

---

## 🖥️ Hardwarová a softwarová specifikace

### Hardware
* **Stroj:** Lenovo ThinkStation P720 Tower Workstation
* **Procesor:** 2x Intel Xeon Silver 4210 (Celkem 20 fyzických jader, 40 vláken, NUMA topologie)
* **Operační paměť:** 64 GB DDR4 ECC RAM
* **Grafická karta:** NVIDIA Quadro P5000 (16 GB GDDR5X VRAM, architektura Pascal)
* **Úložiště:** 2x256GB ZFS mirror system disk, 2x 2TB NVMe SSD data

### Software
* **Operační systém:** Ubuntu 26.04 LTS (Noble Numbat – jádro s nativní podporou NUMA a symetrického multiprocessingu)
* **Základy:** Python 3.10+, Git, pip, wget, curl, vim, docker (volitelně)

---

## 🧠 Přehled vhodných Open-Source modelů

Následující modely jsou optimalizovány pro běh v rámci limitů hardwarové konfigurace a 16 GB VRAM karty Quadro P5000.


| Model | Typ | Velikost / Nárok na VRAM | Hlavní využití a doporučení | Rychlé spuštění (Ollama) |
| :--- | :--- | :--- | :--- | :--- |
| **Qwen3-VL 8B** | Multimodální (Text + Obrázek) | cca 5–7 GB / 8 GB VRAM | Popis schémat, nákresů a logů z 90. let. Výtahy z dokumentů a lokální fine-tuning. | `ollama run qwen3-vl` |
| **LLaVA 7B** | Multimodální (Text + Obrázek) | cca 6–7 GB / 8 GB VRAM | Výborná akcelerace na GPU. Popis nákresů, čtení skenovaných PDF a základ pro RAG. | `ollama run llava:7b` |
| **Llama 3 8B (Instruct)** | Textový LLM | cca 4.7 GB / 5 GB VRAM | Analýza smluv, e-mailů, běžný firemní chat a generování sumářů textů. | `ollama run llama3:8b` |
| **Mistral 7B (Instruct)** | Textový LLM | cca 4.1 GB / 5 GB VRAM | Rychlé odpovědi, generování programovacího kódu, skriptování a logické úlohy. | `ollama run mistral:7b` |
| **Whisper (Large-v3)** | Audio ➔ Text | cca 10 GB / 10 GB VRAM | Automatický přesný přepis starých audiologů, schůzek a diktátů do češtiny. | *Nativní Python setup* |
| **RAG Systém** | LLM + Vektorová DB | Využívá 40 CPU vláken + 64 GB RAM | Prohledávání napříč celým 30letým archivem. Nejvýkonnější lokální řešení. | *Architektonický celek* |

---

## ⚙️ Krok za krokem: Instalace a konfigurace prostředí

### Krok 1: Příprava ovladačů GPU (NVIDIA CUDA)
Pro plné využití 16 GB VRAM karty Quadro P5000 pro AI výpočty nainstalujeme produkční ovladače a CUDA toolkit přímo z oficiálních repozitářů.

```bash
# Aktualizace repozitářů a instalace ovladače + CUDA toolkitu
sudo apt update
sudo apt install -y nvidia-driver-550 nvidia-utils-550 cuda-toolkit-12-4

# Ověření úspěšné instalace a ověření aktivity grafické karty
nvidia-smi
```

### Krok 2: Příprava systému a systémových závislostí
Nainstalujeme potřebné systémové knihovny pro práci s grafikou, kompilaci kódů a Pythonem.

```bash
# Instalace vývojových nástrojů a knihoven pro zpracování obrazu a audia
sudo apt install -y git wget curl vim build-essential libgl1 libglib2.0-0 libsm6 libxext6 libxrender-dev libxinerama-dev libxi6

# Instalace Pythonu 3.10 a nástrojů pro virtuální prostředí
sudo apt install -y python3.10 python3.10-venv python3.10-pip
```

### Krok 3: Vytvoření virtuálního prostředí a instalace PyTorch
Pro izolaci projektů vytvoříme virtuální prostředí. Protože karta Quadro P5000 staví na starší architektuře Pascal, použijeme pro maximální stabilitu PyTorch s CUDA 11.8.

```bash
# Vytvoření a aktivace virtuálního prostředí
python3.10 -m venv ~/local-ai-venv
source ~/local-ai-venv/bin/activate

# Upgrade správce balíčků pip
python3.10 -m pip install --upgrade pip

# Instalace PyTorch s podporou CUDA 11.8 (klíčové pro akceleraci přes GPU)
pip install torch torchvision torchaudio --index-url https://pytorch.org

# Instalace knihoven pro práci s LLM, optimalizaci, RAG a finetuning
pip install transformers accelerate bitsandbytes sentencepiece peft safetensors trl datasets evaluate
```

### Krok 4: Správa modelů přes Ollama (Doporučený přístup)
Ollama je nejjednodušší nástroj pro lokální správu, kvantizaci a spouštění modelů.

```bash
# Instalace nástroje Ollama pomocí oficiálního skriptu
curl -fsSL https://ollama.com | sh

# Stažení a okamžité spuštění multimodálního modelu Qwen3
ollama pull qwen3-vl
ollama run qwen3-vl
```

### Krok 5: Alternativní spuštění v Dockeru
Pokud preferujete kontejnerizaci, můžete Ollama provozovat izolovaně s plným přístupem ke grafické kartě.

```bash
# Instalace Dockeru a Docker Compose
sudo apt install docker.io docker-compose -y
sudo usermod -aG docker $USER
newgrp docker

# Vytvoření adresáře pro ukládání stažených modelů
mkdir -p ~/ai-models

# Spuštění Ollama kontejneru s povolením GPU (příznak --gpus=all)
docker run -d --name ollama -p 11434:11434 -v ~/ai-models:/root/.ollama/models --gpus=all ollama/ollama
```

### Krok 6: Skript pro nativní spuštění Qwen3-VL v Pythonu
Chcete-li model integrovat do vlastních skriptů či aplikací, vytvořte soubor `run_qwen3_vl.py`:

```python
import torch
from PIL import Image
from transformers import AutoTokenizer, AutoProcessor, AutoModelForVision2Seq

# Definice modelu
model_name = "Qwen/Qwen3-VL-8B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)
processor = AutoProcessor.from_pretrained(model_name)

# Načtení modelu s automatickým mapováním na GPU v bfloat16
model = AutoModelForVision2Seq.from_pretrained(model_name, torch_dtype=torch.bfloat16, device_map="auto")

# Definice vstupu (obrázek a textový dotaz)
prompt = "Popiš podrobně toto historické schéma a vypiš z něj textové logy."
image = Image.open("historicky_log_1995.jpg")

# Zpracování dat a odeslání na GPU
inputs = processor(images=image, text=prompt, return_tensors="pt").to("cuda")
outputs = model.generate(**inputs, max_new_tokens=256)

# Výpis výsledku
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
```

### Krok 7: Spuštění přepisu audia pomocí Whisper (Large-v3)
Pro lokální převod nahrávek ze schůzek a historických audiologů nainstalujte Whisper přímo z repozitáře OpenAI.

```bash
# Klonování a instalace knihovny Whisper
git clone https://github.com
cd whisper
pip install -e .

# Spuštění přepisu nahrávky do výstupního adresáře na GPU
python3 examples/translate.py --model large-v3 --output_dir ./vystup_texty --input stare_hlasove_zaznamy.wav
```

### Krok 8: Pokročilé lokální dotrénování (Fine-Tuning)
Máte-li připravená strukturovaná data z vašeho archivu ve formátu JSON, můžete model Qwen3-VL doučit specifickým historickým pojmům.

```bash
# Nastavení mezipaměti pro Hugging Face na rychlý NVMe disk
export HF_HOME=/home/ubuntu/.cache/huggingface

# Spuštění skriptu pro lokální fine-tuning pomocí knihovny TRL
python -m trl.scripts.finetune_qwen3 \
    --model_name_or_path Qwen/Qwen3-VL-8B-Instruct \
    --dataset_path archivni_data_set.json \
    --output_dir ./vyladeny_qwen3_model \
    --per_device_train_batch_size 2 \
    --gradient_accumulation_steps 4 \
    --learning_rate 2e-5 \
    --num_train_epochs 3 \
    --fp16
```
> 💡 *Poznámka k paměti:* Tento proces vyžaduje minimálně 12 GB systémové RAM a 8 GB VRAM. Vaše konfigurace (64 GB RAM / 16 GB VRAM) je pro tento úkol plně dostačující.

---

## 💡 Tipy, triky a optimalizace výkonu pro P720

1. **NUMA Architektura (Non-Uniform Memory Access):** Pracovní stanice ThinkStation P720 obsahuje 2 fyzické procesory Xeon. Systémová RAM je rozdělena mezi ně. Chcete-li zabránit zpomalení při přenosu dat mezi procesory (NUMA cross-talk), spouštějte náročné python skripty nebo indexaci vektorové databáze svázané s konkrétním CPU uzlem pomocí nástroje `numactl`:
   ```bash
   sudo apt install numactl
   numactl --cpunodebind=0 --membind=0 python run_qwen3_vl.py
   ```
2. **Kvantizace modelů (GGUF/AWQ):** Karta Quadro P5000 má 16 GB VRAM. 8B modely v plné přesnosti (FP16) zabírají cca 16 GB a vysoce vytěžují paměť. Spouštění přes Ollama automaticky využívá 4bitovou kvantizaci (GGUF), což snižuje nároky na cca 5 GB VRAM. To vám dává obrovskou výkonnostní rezervu pro kontextové okno a zpracování velkých obrázků.
3. **Přetížení RAM (CPU Offloading):** Pokud byste chtěli experimentovat s většími modely (např. 32B+), Ollama dokáže inteligentně rozdělit vrstvy modelu. Část poběží na GPU (16 GB VRAM) a zbytek se dopočítá na CPU s využitím vašich 64 GB DDR4 RAM. Bude to pomalejší, ale systém nespadne na chybu nedostatku paměti (Out of Memory).
4. **ZFS a NVMe rychlost:** Vaše NVMe SSD zapojené v ZFS RAID 1 (Mirror) poskytují vysokou bezpečnost proti selhání disku a extrémní rychlost čtení. Načítání 10 GB modelů do paměti VRAM při spuštění tak zabere pouhé vteřiny.
5. **Trvalý offline režim:** Jakmile stáhnete modely příkazy `ollama pull` nebo z Hugging Face, můžete server kompletně odpojit od internetu. Lokální AI prostředí je 100% autonomní.

---

## 📚 Reference a dokumentace

* **Projekt Qwen3-VL:** [Hugging Face - Qwen3-VL-8B-Instruct](https://huggingface.co)
* **Dokumentace ekosystému Ollama:** [Ollama API & CLI Docs](https://ollama.com)
* **Instalace lokálního PyTorch:** [PyTorch Start Locally](https://pytorch.org)
* **Knihovna pro finetuning TRL:** [Hugging Face TRL Guide](https://huggingface.co)

### 📎 Citace (Harvard Style)

* Alibaba Cloud. (2025). *Qwen3-VL-8B-Instruct*. Hugging Face. Dostupné na: https://huggingface.co [Přístup 2. června 2026].
* Hugging Face. (2024). *Transformers documentation*. Dostupné na: https://huggingface.co [Přístup 2. června 2026].
* Ollama. (2025). *Ollama: run models locally*. Dostupné na: https://ollama.com [Přístup 2. června 2026].
* PyTorch Team. (2024). *PyTorch with CUDA*. Dostupné na: https://pytorch.org [Přístup 2. června 2026].



