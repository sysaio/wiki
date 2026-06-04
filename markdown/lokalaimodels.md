# Lokální LLM modely pro Ollama (Lenovo ThinkStation P720)

Tato stránka obsahuje doporučené AI modely pro nástroj **Ollama**, optimalizované pro hardwarovou konfiguraci této pracovní stanice.

## Hardwarový profil stanice
* **Grafická karta (GPU):** NVIDIA Quadro P5000 (16 GB VRAM)
* **Procesor (CPU):** 2x Intel Xeon Silver 4210 (Celkem 20 jader / 40 vláken)
* **Operační paměť (RAM):** 64 GB

> [!TIP]
> Pro maximální rychlost generování (tokenů za sekundu) je klíčové, aby se celý model vešel do **16 GB VRAM** grafické karty. Pokud model tuto kapacitu překročí, Ollama jej rozdělí mezi GPU a systémovou RAM, což výrazně sníží rychlost kvůli limitům propustnosti sběrnice.

---

## 🚀 Doporučené modely podle kategorií

### 1. Univerzální a konverzační modely
Ideální pro každodenní úkoly, kreativní psaní, sumarizaci textů a obecné dotazy. Všechny tyto modely běžící kompletně ve VRAM jsou extrémně rychlé.


| Příkaz pro spuštění | Model | Velikost | Využití VRAM | Hlavní výhody |
| :--- | :--- | :---: | :---: | :--- |
| `ollama run llama3.1:8b` | Llama 3.1 (Meta) | 8B | ~5 GB | Špičkový standard, skvělá čeština, velmi rychlá odezva. |
| `ollama run qwen2.5:14b` | Qwen 2.5 (Alibaba) | 14B | ~9 GB | Vynikající logické uvažování, perfektní gramatika a styl v češtině. |
| `ollama run mistral:7b` | Mistral (Mistral AI) | 7B | ~4 GB | Prověřený, rychlý a efektivní evropský model. |

### 2. Modely pro vývoj a programování (Coding)
Slouží jako lokální, bezpečný a plně soukromý asistent pro psaní, analýzu a refaktorování kódu (náhrada za GitHub Copilot).


| Příkaz pro spuštění | Model | Velikost | Využití VRAM | Hlavní výhody |
| :--- | :--- | :---: | :---: | :--- |
| `ollama run qwen2.5-coder:14b` | Qwen 2.5 Coder | 14B | ~9 GB | Aktuální král otevřených coding modelů. Zvládá i komplexní architekturu. |
| `ollama run codegemma:7b` | CodeGemma (Google) | 7B | ~5 GB | Odlehčený model od Google optimalizovaný na doplňování kódu (completion). |

### 3. Modely s pokročilým uvažováním (Reasoning)
Modely typu "O1", které před samotnou odpovědí generují interní myšlenkový proces (chain-of-thought). Jsou ideální na složitou matematiku, logické hádanky a hloubkovou analýzu chyb v kódu.


| Příkaz pro spuštění | Model | Velikost | Využití VRAM | Hlavní výhody |
| :--- | :--- | :---: | :---: | :--- |
| `ollama run deepseek-r1:14b` | DeepSeek R1 | 14B | ~9 GB | Perfektní balanc mezi inteligencí a rychlostí na 16GB VRAM. |

### 4. Maximální zátěž (Experimentální limit)
Pokud potřebujete maximální možnou inteligenci modelu a nevadí vám nižší rychlost generování (jednotky slov za sekundu). Tyto modely využijí kombinaci GPU a masivní 64 GB systémové RAM spolu s 40 vlákny procesorů Xeon.

* **`ollama run deepseek-r1:32b`** (Zabere ~20 GB paměti – část poběží v RAM)
* **`ollama run llama3.1:70b`** (Zabere ~40 GB paměti – vyžaduje silnou asistenci CPU a RAM)

---

## 🛠️ Užitečné příkazy pro monitoring

Během toho, co model generuje odpověď v terminálu, doporučujeme sledovat využití hardwaru:

* **Sledování zatížení GPU a VRAM:**
  ```bash
  nvidia-smi
  ```
  *(Ověříte zde, zda Ollama správně alokovala model do paměti grafické karty a kolik VRAM zbývá.)*

* **Sledování zatížení CPU a RAM:**
  ```bash
  htop
  ```
  *(Užitečné hlavně při spuštění velkých modelů jako 32B/70B pro kontrolu, jak moc jsou vytížena všechna jádra vašich procesorů Xeon.)*
