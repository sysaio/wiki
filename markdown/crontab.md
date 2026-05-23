---
title: Crontab – plánovnání úloh
category: Automatizace
tags: [linux, automatizace, spousteni]
last_update: 2025-07-09
---

# 🕒 `crontab` – plánování úloh v Linuxu

`cron` je nástroj pro automatické spouštění příkazů nebo skriptů v definovaných intervalech. Pomocí `crontab` si nastavíš, kdy a co se má spustit.

---

## 📘 Základní syntaxe

Každý řádek v `crontab` má tuto podobu:

```cron
* * * * * /cesta/k/příkazu
│ │ │ │ │
│ │ │ │ └── den v týdnu (0–7) (0 nebo 7 = neděle)
│ │ │ └──── měsíc (1–12)
│ │ └────── den v měsíci (1–31)
│ └──────── hodina (0–23)
└────────── minuta (0–59)
```

---

## 📋 Příklad: každodenní záloha pomocí `rsync` ve 2:00 ráno

```cron
0 2 * * * /usr/bin/rsync -av /home/user/ /mnt/backup/home/ >> /var/log/rsync.log 2>&1
```

---

## 🧪 Otevření vlastního crontabu

```bash
crontab -e
sudo crontab -e # pro ulohy provaděné pod rootem
```

Tím otevřeš svůj plán úloh v editoru (např. `nano`, `vim`).

---

## 📄 Výpis naplánovaných úloh

```bash
crontab -l
sudo crontab -l # pro rootovske ulohy
```

---

## ❌ Smazání všech úloh

```bash
crontab -r
```

---

## 🧑‍💻 Příklady použití

| Čas               | Crontab výraz     | Popis                                 |
|-------------------|-------------------|----------------------------------------|
| Každou minutu     | `* * * * *`       | Spustí se každou minutu                |
| Každou hodinu     | `0 * * * *`       | V každou celou hodinu                  |
| Denně ve 3:30     | `30 3 * * *`      | Každý den v 3:30 ráno                  |
| Každou neděli     | `0 9 * * 0`       | V neděli v 9:00                        |
| Každý první den v měsíci | `0 0 1 * *` | Každý první den měsíce o půlnoci       |

---

## 🧠 Speciální zástupci

| Zástupce      | Význam                        |
|---------------|-------------------------------|
| `@reboot`     | Spustí se po startu systému   |
| `@daily`      | Jednou denně (0:00)           |
| `@hourly`     | Každou hodinu (00:00)         |
| `@weekly`     | Jednou týdně (neděle 0:00)    |
| `@monthly`    | Jednou měsíčně (1. den 0:00)  |
| `@yearly`     | Jednou ročně (1. 1. 0:00)     |

📌 **Příklad:**

```cron
@daily /home/user/scripts/daily-backup.sh
```

---

## 📂 Umístění logů

Cron výstup standardně posílá e-mailem uživateli. Pokud systém nemá MTA (Mail Transfer Agent), doporučuje se logovat ručně:

```cron
0 4 * * * /path/to/command >> /var/log/muj_script.log 2>&1
```

---

## 🔄 Tipy

- Používej absolutní cesty ke skriptům a příkazům.
- Ověř si, že skript má právo na spuštění (`chmod +x`).
- Proměnné prostředí v `cron`u nejsou stejné jako v běžném shellu – nastav `PATH` uvnitř skriptu, pokud je potřeba.
- `cron` má vlastní prostředí – spouštěj skripty, které se obejdou bez interaktivního vstupu.

---

## 🔧 Systémové crontaby

- `/etc/crontab` – hlavní crontab s možností definovat uživatele
- `/etc/cron.d/` – individuální crontab soubory
- `/etc/cron.{hourly,daily,weekly,monthly}/` – skripty spouštěné podle plánovaných složek

---

## ✅ Testování úloh

Pro simulaci cron spuštění můžeš spustit příkaz ručně:

```bash
bash /path/to/script.sh
```

---

## 📚 Další odkazy

- [man crontab](https://man7.org/linux/man-pages/man5/crontab.5.html)
- [crontab.guru – online generátor výrazů](https://crontab.guru/)
