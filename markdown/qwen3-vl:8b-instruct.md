# 🏠 Průvodce instalací lokálního AI prostředí na Lenovo ThinkStation P720

Vítejte v dokumentaci pro nasazení open-source umělé inteligence na vlastním hardwaru. Tento návod slouží jako kompletní, krok za krokem přehled a konfigurační kuchařka pro GitHub Pages. Všechny popsané modely a postupy jsou navrženy pro plně offline provoz, bez odesílání dat na internet a bez licenčních poplatků. Cílem je bezpečná analýza interních dokumentů, historických schémat a 30letého firemního archivu.

---

## 🖥️ Hardwarová a softwarová specifikace

### Hardware
* **Stroj:** Lenovo ThinkStation P720 Tower Workstation
* **Procesor:** 2x Intel Xeon Silver 4210 (Celkem 20 fyzických jader, 40 vláken, NUMA topologie)
* **Operační paměť:** 64 GB DDR4 ECC RAM
* **Grafická karta:** NVIDIA Quadro P5000 (16 GB GDDR5X VRAM, architektura Pascal)
* **Úložiště (Asymetrická AI Topologie):**
  * **Systémové disky:** 2x 256 GB SSD v zapojení ZFS Mirror (RAID 1) – vyhrazeno pro OS a systémové logy.
  * **NVMe Disk 1 (Aktivní Data a RAG):** 2TB M.2 PCIe 3.0 TLC (3100/2200 MB/s, vysoká životnost 1500 TBW) – dedikovaný pro neustálé zápisy vektorových databází, indexy a python prostředí. Namontován na `/mnt/ai-data`.
  * **NVMe Disk 2 (Úložiště LLM Modelů):** 2TB M.2 PCIe 4.0 QLC (4500/4000 MB/s, rychlé čtení, 600 TBW) – dedikovaný pro statické ukládání LLM/GGUF modelů. Využívá maximální rychlost čtení pro okamžité načítání modelů do VRAM. Namontován na `/mnt/ai-models`.
  * **Zálohovací disk:** 1x 8TB 3,5" HDD (plotnový) – určen pro denní inkrementální zálohy a cold-storage obou NVMe disků.

### Software
* **Operační systém:** Ubuntu 26.04 LTS (Noble Numbat – jádro s nativní podporou NUMA a symetrického multiprocessingu)
* **Základy:** Python 3.10+, Git, pip, wget, curl, vim, docker (volitelně)

---

## 🧠 Přehled vhodných Open-Source modelů

Následující modely jsou optimalizovány pro běh v rámci limitů vaší hardwarové konfigurace a 16 GB VRAM karty Quadro P5000.



| Model | Typ | Velikost / Nárok na VRAM | Hlavní využití a doporučení | Rychlé spuštění (Ollama) |
| :--- | :--- | :--- | :--- | :--- |
| Qwen3-VL 8B | Multimodální (Text + Obrázek) | cca 5–7 GB / 8 GB VRAM | Popis schémat, nákresů a logů z 90. let. Výtahy z dokumentů a lokální fine-tuning. | ollama run qwen3-vl |
| LLaVA 7B | Multimodální (Text + Obrázek) | cca 6–7 GB / 8 GB VRAM | Výborná akcelerace na GPU. Popis nákresů, čtení skenovaných PDF a základ pro RAG. | ollama run llava:7b |
| Llama 3 8B (Instruct) | Textový LLM | cca 4.7 GB / 5 GB VRAM | Analýza smluv, e-mailů, běžný firemní chat a generování sumářů textů. | ollama run llama3:8b |
| Mistral 7B (Instruct) | Textový LLM | cca 4.1 GB / 5 GB VRAM | Rychlé odpovědi, generování programovacího kódu, skriptování a logické úlohy. | ollama run mistral:7b |
| Whisper (Large-v3) | Audio -> Text | cca 10 GB / 10 GB VRAM | Automatický přesný přepis starých audiologů, schůzek a diktátů do češtiny. | Nativní Python setup |
| RAG Systém | LLM + Vektorová DB | Využívá 40 CPU vláken + 64 GB RAM | Prohledávání napříč celým 30letým archivem. Nejvýkonnější lokální řešení. | Architektonický celek |

---

## ⚙️ Krok za krokem: Instalace a konfigurace prostředí

### Krok 1: Příprava ovladačů GPU (NVIDIA CUDA)
Pro plné využití 16 GB VRAM karty Quadro P5000 pro AI výpočty nainstalujeme produkční ovladače a CUDA toolkit přímo z oficiálních repozitářů.

    sudo apt update
    sudo apt install -y nvidia-driver-550 nvidia-utils-550 cuda-toolkit-12-4
    nvidia-smi

### Krok 2: Příprava systému a systémových závislostí
Nainstalujeme potřebné systémové knihovny pro práci s grafikou, kompilaci kódů a Pythonem.

    sudo apt install -y git wget curl vim build-essential libgl1 libglib2.0-0 libsm6 libxext6 libxrender-dev libxinerama-dev libxi6
    sudo apt install -y python3.10 python3.10-venv python3.10-pip

### Krok 3: Konfigurace asymetrických NVMe úložisť
Vytvoříme body připojení. Vysoce odolný TLC disk namontujeme pro databáze a běžné zápisy, zatímco ultra rychlý QQLC disk vyhradíme čistě pro statické soubory modelů.

    # Příprava adresářů a přidělení práv aktuálnímu uživateli
    sudo mkdir -p /mnt/ai-data
    sudo mkdir -p /mnt/ai-models
    sudo chown -R $USER:$USER /mnt/ai-data /mnt/ai-models

    # Poznámka: Zde připojte PCIe 3.0 TLC disk do /mnt/ai-data a PCIe 4.0 QLC disk do /mnt/ai-models přes /etc/fstab

### Krok 4: Vytvoření virtuálního prostředí a instalace PyTorch
Pro virtuální prostředí a kód aplikací využijeme vysoce odolný TLC disk (`/mnt/ai-data`), abychom šetřili životnost druhého QLC disku.

    python3.10 -m venv /mnt/ai-data/local-ai-venv
    source /mnt/ai-data/local-ai-venv/bin/activate
    python3.10 -m pip install --upgrade pip
    pip install torch torchvision torchaudio --index-url https://pytorch.org
    pip install transformers accelerate bitsandbytes sentencepiece peft safetensors trl datasets evaluate

### Krok 5: Správa modelů přes Ollama (Konfigurace na rychlé čtení)
Nástroj Ollama nainstalujeme standardně, ale pomocí systémové proměnné jí přikážeme stahovat a číst modely z ultra rychlého PCIe 4.0 QLC disku (`/mnt/ai-models`). Modely se tak do grafické karty načtou v maximální rychlosti.

    curl -fsSL https://ollama.com | sh
    sudo mkdir -p /etc/systemd/system/ollama.service.d
    echo '[Service]' | sudo tee /etc/systemd/system/ollama.service.d/override.conf
    echo 'Environment="OLLAMA_MODELS=/mnt/ai-models"' | sudo tee -a /etc/systemd/system/ollama.service.d/override.conf
    sudo systemctl daemon-reload
    sudo systemctl restart ollama
    ollama pull qwen3-vl
    ollama run qwen3-vl

### Krok 6: Alternativní spuštění v Dockeru
Pokud preferujete kontejnerizaci, Docker nastavíme tak, aby kontejner běžel na TLC disku, ale modely četl z rychlého QLC disku.

    sudo apt install docker.io docker-compose -y
    sudo usermod -aG docker $USER
    newgrp docker
    docker run -d --name ollama -p 11434:11434 -v /mnt/ai-models:/root/.ollama/models --gpus=all ollama/ollama

### Krok 7: Skript pro nativní spuštění Qwen3-VL v Pythonu
Chcete-li model integrovat do vlastních aplikací, uložte skript na TLC disk do souboru `/mnt/ai-data/run_qwen3_vl.py`.

    import torch
    from PIL import Image
    from transformers import AutoTokenizer, AutoProcessor, AutoModelForVision2Seq

    model_name = "Qwen/Qwen3-VL-8B-Instruct"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    processor = AutoProcessor.from_pretrained(model_name)
    model = AutoModelForVision2Seq.from_pretrained(model_name, torch_dtype=torch.bfloat16, device_map="auto")

    prompt = "Popis podrobne toto historicke schema a vypis z nej textove logy."
    image = Image.open("historicky_log_1995.jpg")

    inputs = processor(images=image, text=prompt, return_tensors="pt").to("cuda")
    outputs = model.generate(**inputs, max_new_tokens=256)
    print(tokenizer.decode(outputs, skip_special_tokens=True))

### Krok 8: Spuštění přepisu audia pomocí Whisper (Large-v3)
Whisper kód zprovozníme na TLC disku, přičemž mezipaměť pro stažený 10 GB model nasměrujeme na QLC disk `/mnt/ai-models`.

    cd /mnt/ai-data
    git clone https://github.com
    cd whisper
    pip install -e .
    
    # Spuštění s modelem na rychlém disku
    python3 examples/translate.py --model large-v3 --output_dir /mnt/ai-data/vystup_texty --input stare_hlasove_zaznamy.wav

### Krok 9: Pokročilé lokální dotrénování (Fine-Tuning)
Data i skripty pro fine-tuning držíme na TLC disku. Hugging Face cache (kam se stahují surové nekvantizované váhy před trénováním) nasměrujeme na QLC disk.

    export HF_HOME=/mnt/ai-models/.cache/huggingface
    python -m trl.scripts.finetune_qwen3 \
        --model_name_or_path Qwen/Qwen3-VL-8B-Instruct \
        --dataset_path /mnt/ai-data/archivni_data_set.json \
        --output_dir /mnt/ai-data/vyladeny_qwen3_model \
        --per_device_train_batch_size 2 \
        --gradient_accumulation_steps 4 \
        --learning_rate 2e-5 \
        --num_train_epochs 3 \
        --fp16

> Poznámka k paměti: Tento proces vyžaduje minimálně 12 GB systémové RAM a 8 GB VRAM. Vaše konfigurace (64 GB RAM / 16 GB VRAM) je pro tento úkol plně dostačující.

---

## 💡 Tipy, triky a optimalizace výkonu pro P720

1. **NUMA Architektura (Non-Uniform Memory Access):** Pracovní stanice ThinkStation P720 obsahuje 2 fyzické procesory Xeon. Systémová RAM je rozdělena mezi ně. Chcete-li zabránit zpomalení při přenosu dat mezi procesory (NUMA cross-talk), spouštějte náročné python skripty nebo indexaci vektorové databáze svázané s konkrétním CPU uzlem pomocí nástroje numactl:
   
    sudo apt install numactl
    numactl --cpunodebind=0 --membind=0 python /mnt/ai-data/run_qwen3_vl.py

2. **Ochrana QLC disku před opotřebením:** Disky s buňkami QLC mají výrazně nižší limit celkového zapsaného množství dat (600 TBW proti 1500 TBW u TLC). Proto na disk `/mnt/ai-models` nikdy nesměrujte databázové logy, swap, ani dynamické indexy. Využívejte ho výhradně jako "knihovnu" na čtení AI modelů.

3. **Kvantizace modelů (GGUF/AWQ):** Karta Quadro P5000 má 16 GB VRAM. 8B modely v plné přesnosti (FP16) zabírají cca 16 GB a vysoce vytěžují paměť. Spouštění přes Ollama automaticky využívá 4bitovou kvantizaci (GGUF), což snižuje nároky na cca 5 GB VRAM. To vám dává obrovskou výkonnostní rezervu pro kontextové okno a zpracování velkých obrázků.

4. **Strategie zálohování na 8TB HDD:** Jelikož jsou oba NVMe disky nezávislé (nejsou v RAIDu), je nutné v zálohovacím skriptu (např. rsync) zrcadlit oba přípojné body `/mnt/ai-data` i `/mnt/ai-models` na oddělené složky na 8TB pevném disku. Zálohu stačí spouštět jednou týdně pro modely a denně pro databázi.

5. **Trvalý offline režim:** Jakmile stáhnete modely příkazy `ollama pull` nebo z Hugging Face, můžete server kompletně odpojit od internetu. Lokální AI prostředí je 100% autonomní.

---

## 📚 Reference a dokumentace

* Projekt Qwen3-VL: https://huggingface.co
* Dokumentace ekosystému Ollama: https://ollama.com
* Instalace lokálního PyTorch: https://pytorch.org
* Knihovna pro finetuning TRL: https://huggingface.co

### 📎 Citace (Harvard Style)

* Alibaba Cloud. (2025). *Qwen3-VL-8B-Instruct*. Hugging Face. Dostupné na: https://huggingface.co [Přístup 2. června 2026].
* Hugging Face. (2024). *Transformers documentation*. Dostupné na: https://huggingface.co [Přístup 2. června 2026].
* Ollama. (2025). *Ollama: run models locally*. Dostupné na: https://ollama.com [Přístup 2. června 2026].
* PyTorch Team. (2024). *PyTorch with CUDA*. Dostupné na: https://pytorch.org [Přístup 2. června 2026].
