---
title: ESP32 – wifi
category: IoT
tags: [linux, mikrokontrolery, espressif]
last_update: 2025-07-09
---


```markdown
# 📡 ESP32 – Připojení k Wi-Fi pomocí ESP-IDF

Tento návod ukazuje, jak nakonfigurovat a připojit zařízení ESP32 k Wi-Fi síti pomocí ESP-IDF.

---

## 🔧 Použitý příklad

Espressif poskytuje oficiální ukázku `wifi/station`, která se nachází zde:

```bash
cd ~/esp
cp -r $IDF_PATH/examples/wifi/getting_started/station wifi_station
cd wifi_station
```

---

## ⚙️ Konfigurace sítě (menuconfig)

```bash
idf.py menuconfig
```

1. Přejdi do:  
   `Example Configuration`
2. Nastav:
   - *WiFi SSID* – název tvé Wi-Fi sítě
   - *WiFi Password* – heslo

> Nastavení se uloží do `sdkconfig` souboru.

---

## 🛠️ Kompilace a nahrání

```bash
idf.py set-target esp32
idf.py build
idf.py -p /dev/ttyUSB0 flash monitor
```

---

## ✅ Co očekávat v terminálu

Po úspěšném připojení bys měl v `idf.py monitor` vidět něco jako:

```
I (3179) wifi station: WiFi init finished.
I (4319) wifi station: Connected to ap SSID:myssid password:*****
I (4359) wifi station: got ip:192.168.0.105
```

---

## 📌 Tipy

- Pokud máš problémy s připojením, zkontroluj heslo nebo zkus jiné pásmo (např. 2.4 GHz).
- Lze také upravit `sdkconfig.defaults` a přidat SSID/PASS pro snadné sdílení v týmu.
```
