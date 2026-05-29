# 🚀 Návod: Instalace a spuštění Qwen3-VL-8B-Instruct na lokálním serveru (Lenovo ThinkStation P720)

## 📌 Úvod

Tento návod vás provede instalací a spuštěním **Qwen3-VL-8B-Instruct** – multimodálního (text + obrázek) modelu od Alibaba Cloud – na vašem **Lenovo ThinkStation P720**. Využijete jeho výkonnou infrastrukturu (2x Xeon Silver 4210, 64GB RAM, Quadro P5000) pro lokální AI pracovní prostředí bez internetu, vhodné pro práci se citlivými daty (např. 30letý internerý archiv).

## ⚙️ Požadavky

- **OS:** Ubuntu 26.04 LTS
- **Hardware:**
  - 64 GB DDR4 ECC RAM
  - NVIDIA Quadro P5000 (16 GB GDDR5X VRAM)
  - 2x 2TB NVMe SSD (RAID 1)
- **Software:**
  - Python 3.10+
  - NVIDIA drivers (zpracování přes CUDA)
  - CUDA toolkit 11.8+ (kompatibilní s Pascal architekturou)
  - Git, pip, wget, curl, vim, docker (volitelně)

## 📥 1. Nainstalujte požadované závislosti

Otevřete terminál a spusťte:

sudo apt update && sudo apt upgrade -y
sudo apt install -y git wget curl vim build-essential libgl1 libglib2.0-0 libsm6 libxext6 libxrender-dev libxinerama-dev libxi6
sudo apt install -y python3.10 python3.10-venv python3.10-pip
python3.10 -m venv ~/qwen3-venv
source ~/qwen3-venv/bin/activate
python3.10 -m pip install --upgrade pip
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install transformers accelerate bitsandbytes sentencepiece accelerate
pip install -U peft safetensors


> ⚠️ Pokud máte GPU, **nainstalujte PyTorch s CUDA 11.8** → to je největší výhoda pro běh na Quadro P5000.

## 🎨 2. Stáhněte Qwen3-VL-8B-Instruct

mkdir -p ~/qwen3-models
cd ~/qwen3-models
wget https://huggingface.co/Qwen/Qwen3-VL-8B-Instruct/resolve/main/Qwen3-VL-8B-Instruct.safetensors


> ✅ Pokud se rozhodnete používat **GGUF verzi** → zde je návod pro Ollama (použitelný i v Dockeru):  
> [Ollama Qwen3-VL GGUF](https://ollama.com/library/qwen3-vl)

## 🐳 3. (Volitelně) Spuštění v Dockeru

sudo apt install docker.io docker-compose
sudo usermod -aG docker $USER
newgrp docker
docker pull ollama/ollama:latest
docker run -d --name ollama -p 11434:11434 -v /home/ubuntu/qwen3-models:/root/.ollama/models --gpus=all ollama/ollama


> Výhody: snadná instalace, bez potřeby nakonfigurovat vlastní prostředí.

## 🧠 4. (Volitelně) Finetuning vašich dat

pip install trl peft datasets evaluate accelerate
export HF_HOME=/home/ubuntu/.cache/huggingface
python -m trl.scripts.finetune_qwen3 --model_name_or_path Qwen/Qwen3-VL-8B-Instruct --dataset_path your_data.json --output_dir ./fine_tuned_qwen3_vl --per_device_train_batch_size 2 --gradient_accumulation_steps 4 --learning_rate 2e-5 --num_train_epochs 3 --fp16


> ⚠️ Pro finetuning se vám bude vyžadovat **minimálně 12 GB RAM + 8 GB VRAM** – vaše 16 GB VRAM je v pořádku.

## 💬 5. Spuštění modelu v Pythonu

Vytvořte skript `run_qwen3_vl.py`:

```python
from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers import AutoProcessor, AutoModelForVision2Seq
import torch
from PIL import Image

model_name = "Qwen/Qwen3-VL-8B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForVision2Seq.from_pretrained(model_name, torch_dtype=torch.bfloat16, device_map="auto")

prompt = "Popiš tento obrázek."
image = Image.open("your_image.jpg")
processor = AutoProcessor.from_pretrained(model_name)
inputs = processor(images=image, text=prompt, return_tensors="pt").to("cuda")
outputs = model.generate(**inputs, max_new_tokens=128)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))

## 📦 6. Spuštění přes Ollama

curl -fsSL https://ollama.com/install.sh | sh
ollama pull qwen3-vl
ollama run qwen3-vl

Výhody: jednoduché, kompatibilní s více modely, výborně se hodí pro prototypování.

✅ Shrnutí
Vaše Lenovo ThinkStation P720 je úplně vhodné pro:

Lokální běh Qwen3-VL-8B-Instruct
Chatování, překlady, vyhledávání obrázků, finetuning na vašich 30letých datech
Základní modely: využijte GPU Quadro P5000, RAM 64 GB a SSD

📚 Zdroje
Qwen3-VL-8B-Instruct: https://huggingface.co/Qwen/Qwen3-VL-8B-Instruct
PyTorch + CUDA setup: https://pytorch.org/get-started/locally/
Ollama dokumentace: https://ollama.com/docs
Finetuning s trl: https://huggingface.co/docs/trl
GitHub Wiki: https://github.com/yourorg/your-repo/wiki
📎 Citace (Harvard style)
Alibabas Cloud. (2025). Qwen3-VL-8B-Instruct. Hugging Face. https://huggingface.co/Qwen/Qwen3-VL-8B-Instruct
Hugging Face. (2024). Transformers documentation. https://huggingface.co/docs/transformers
PyTorch Team. (2024). PyTorch with CUDA. https://pytorch.org/get-started/locally/
Ollama. (2025). Ollama: run models locally. https://ollama.com
Hugging Face. (2024). Trainer and Finetuning Guide. https://huggingface.co/docs/trl

Začínáme s AI? Nebo už jste už tady?
Váš nápad na lokální AI je správný a významný krok – a já jsem zde, abych vám pomohl pokročit.
💡 Nejde jen o modely, ale o významnou práci s daty, která zůstává u vás.

Díky za důvěru! 🚀🤖

