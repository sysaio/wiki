---
title: ESP IDF setup – moderní vývojové prostředí
category: IoT
tags: [linux, mikrokontrolery, espressif]
last_update: 2025-07-09
---


```markdown
# 🚀 ESP-IDF – Instalace a základní použití

Návod pro vývoj na ESP32 pomocí oficiálního frameworku Espressif – ESP-IDF.

---

## 🛠️ Instalace závislostí (Linux / Ubuntu / Kubuntu)

```bash
sudo apt-get install git wget flex bison gperf python3 python3-pip python3-venv cmake ninja-build ccache libffi-dev libssl-dev dfu-util libusb-1.0-0
python3 --version  # mělo by být >= 3.7
```

---

## 📥 Stažení a instalace ESP-IDF

```bash
mkdir -p ~/esp
cd ~/esp
git clone --recursive https://github.com/espressif/esp-idf.git
cd ~/esp/esp-idf
./install.sh all
```

---

## 🧠 Nastavení prostředí

```bash
. $HOME/esp/esp-idf/export.sh
```

> Nezapomeň přidat do `~/.bashrc`:

```bash
alias get_idf='. $HOME/esp/esp-idf/export.sh'
```

---

## ✅ Testovací projekt – Hello World

```bash
cd ~/esp
cp -r $IDF_PATH/examples/get-started/hello_world .
cd hello_world
idf.py set-target esp32
idf.py menuconfig
idf.py build
idf.py flash monitor
```

---

## 🔌 Zjištění sériového portu

```bash
sudo dmesg | grep tty
ls /dev/ttyUSB*
ls /dev/ttyACM*
watch -n 0.5 ls /dev/ttyUSB* /dev/ttyACM*
```

---

## 🔍 Práce s esptool.py

```bash
esptool.py --port /dev/ttyUSB0 chip_id
esptool.py --port /dev/ttyUSB0 flash_id
esptool.py --port /dev/ttyUSB0 read_mac
esptool.py --port /dev/ttyUSB0 read_flash_status
```

---

## 🧾 Přehled základních příkazů `idf.py`

| Příkaz                  | Popis                                                  |
|-------------------------|--------------------------------------------------------|
| `create-project <jméno>`| Vytvoří nový projekt                                   |
| `set-target <čip>`      | Nastaví cílový čip (esp32, esp32s3, ...)              |
| `menuconfig`            | Spustí textové UI pro konfiguraci                     |
| `build`                 | Přeloží projekt                                        |
| `clean` / `fullclean`   | Smaže výstupy / včetně konfigurace                    |
| `flash`                 | Nahraje firmware                                      |
| `monitor`               | Sériový výstup                                         |
| `flash monitor`         | Kombinace nahrání a spuštění terminálu                |
| `erase-flash`           | Vymaže celý flash čip                                  |
| `reconfigure`           | Znovu vytvoří build systém                             |
| `size` / `size-components` | Ukáže velikost výsledného firmware                  |

---

## ⚙️ Automatické rozpoznání portu

Od ESP-IDF v4.2:

```bash
idf.py flash monitor
```

> Pokud je připojeno více zařízení, přidej `-p /dev/ttyUSB0`.

---

## 🧪 Ukázka celého průběhu

```bash
idf.py create-project hello_world
cd hello_world
idf.py set-target esp32
idf.py menuconfig
idf.py build
idf.py -p /dev/ttyUSB0 flash monitor
```

---

## 🔄 Aktualizace ESP-IDF

```bash
cd ~/esp
git clone -b v5.2 https://github.com/espressif/esp-idf.git esp-idf
cd esp-idf
./install.sh
. ./export.sh
```

---

> 🧠 Poznámka: Při vývoji vždy spusť:
> ```bash
> . $HOME/esp/esp-idf/export.sh
> ```

---

## 📌 Tip

Pro rychlejší vývoj si vytvoř alias:

```bash
alias get_idf='. $HOME/esp/esp-idf/export.sh'
```
```
