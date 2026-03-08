---
title: Multicast na linuxu - IGMP
category: Počítače
tags: [linux, IGMP, Multicast, Komunikace]
last_update: 2026-03-08
---

📡
🐧
IGMP experimenty na Linuxu jsou super způsob, jak to pochopit do hloubky. 
Můžeme si nasimulovat multicast skupiny, join/leave, sledovat provoz ve tcpdumpu a případně i generovat vlastní provoz.

# IGMP experimenty na Linuxu

Jednoduché experimenty pro pochopení chování protokolu **IGMP (Internet Group Management Protocol)** na Linuxu.

Tyto experimenty demonstrují:

- multicast group membership
- IGMP reporty
- příjem multicast provozu
- stav multicastu v Linux kernelu

---

# 1. Zjištění aktuální multicast membership

Nejprve zjistíme, do jakých multicast skupin je systém aktuálně přihlášen.

```bash
ip maddr
```

Ukázka výstupu:

```
2: eno1
    link 01:00:5e:00:00:01
    link 01:00:5e:00:00:fb
    link 01:00:5e:7f:ff:fa
    inet 224.0.0.251 users 3
    inet 239.255.255.250
    inet 224.0.0.1
```

Multicast položky se zobrazují ve dvou vrstvách.

## Multicast MAC adresy (Layer 2)

IPv4 multicast se mapuje na MAC adresy ve tvaru:

```
01:00:5e:xx:xx:xx
```

Příklady:

| Multicast IP | Multicast MAC |
|---|---|
| 224.0.0.1 | 01:00:5e:00:00:01 |
| 224.0.0.251 | 01:00:5e:00:00:fb |
| 239.255.255.250 | 01:00:5e:7f:ff:fa |

## Multicast IP adresy (Layer 3)

Tyto adresy reprezentují multicast skupiny, do kterých je host přihlášen.

---

# 2. Běžné multicast skupiny

Některé multicast adresy se objevují téměř na každém Linux systému.

## 224.0.0.1

```
All Hosts Multicast Group
```

Obsahuje všechny IPv4 hosty v lokální síti.

---

## 224.0.0.251

Používá **mDNS (Multicast DNS)**.

Typicky služby:

- Avahi
- Apple Bonjour
- automatická detekce služeb v síti

---

## 239.255.255.250

Používá **SSDP / UPnP**.

Typické použití:

- smart TV
- router discovery
- DLNA zařízení
- automatická konfigurace zařízení

---

# 3. Sledování IGMP provozu

IGMP pakety můžeme sledovat pomocí tcpdump.

```bash
sudo tcpdump -i eno1 igmp
```

Typické pakety:

```
IGMPv3 Membership Report
IGMP Query
```

Běžný průběh komunikace:

```
Router -> IGMP Query
Host -> IGMP Membership Report
```

---

# 4. Manuální připojení do multicast skupiny

Host se může připojit do multicast skupiny pomocí nástroje **socat**.

Instalace:

```bash
sudo apt install socat
```

Spuštění multicast listeneru:

```bash
socat UDP4-RECVFROM:5000,ip-add-membership=239.10.10.10:eno1,fork -
```

Po spuštění:

1. Linux odešle **IGMP Membership Report**
2. Host se připojí do multicast skupiny:

```
239.10.10.10
```

---

# 5. Ověření membership

Znovu zkontrolujeme multicast tabulku:

```bash
ip maddr show dev eno1
```

Měla by se objevit nová skupina:

```
inet 239.10.10.10
```

---

# 6. Odeslání multicast provozu

V jiném terminálu můžeme odeslat multicast paket:

```bash
echo "hello multicast" | socat - UDP4-DATAGRAM:239.10.10.10:5000
```

Listener by měl zprávu přijmout.

---

# 7. IGMP Leave

Po ukončení listeneru:

```
CTRL+C
```

Linux kernel odešle:

```
IGMP Leave Group
```

Tento paket lze vidět v `tcpdump`.

---

# 8. Stav IGMP v Linux kernelu

Linux poskytuje interní informace o multicastu v souboru:

```bash
cat /proc/net/igmp
```

Ukázka výstupu:

```
Idx Device    : Count Querier   Group    Users Timer
2   eno1      :     1     V3
                010000E0     1 0:00000000
```

Význam polí:

| Pole | Význam |
|---|---|
| Device | síťové rozhraní |
| Group | multicast skupina |
| Users | počet procesů používajících skupinu |
| Timer | IGMP timer |

Tento soubor reprezentuje **IGMP state machine uvnitř Linux kernelu**.

---

# 9. Zjištění procesů používajících multicast

Pokud výstup obsahuje například:

```
inet 224.0.0.251 users 3
```

znamená to, že **tři procesy mají otevřený socket v této multicast skupině**.

Procesy lze zjistit pomocí:

```bash
ss -ulpn
```

nebo

```bash
sudo lsof -i
```

---

# 10. Testování IGMP verzí

Linux umožňuje vynutit verzi IGMP.

Zjištění aktuální konfigurace:

```bash
cat /proc/sys/net/ipv4/conf/all/force_igmp_version
```

Možné hodnoty:

| Hodnota | IGMP verze |
|---|---|
| 1 | IGMPv1 |
| 2 | IGMPv2 |
| 3 | IGMPv3 |

Příklad změny:

```bash
sudo sysctl net.ipv4.conf.all.force_igmp_version=2
```

---

# Další experimenty

Další zajímavé experimenty pro studium multicastu:

- simulace **IGMP Querier**
- rozdíly mezi **IGMPv2 a IGMPv3**
- **IGMP report suppression**
- **multicast flooding vs IGMP snooping**
- **source specific multicast (IGMPv3)**

---

# Shrnutí

Linux poskytuje několik velmi užitečných nástrojů pro studium multicastu.

| Nástroj | Funkce |
|---|---|
| `ip maddr` | zobrazení multicast membership |
| `tcpdump` | analýza IGMP paketů |
| `socat` | generování multicast provozu |
| `/proc/net/igmp` | stav multicastu v kernelu |
| `ss` / `lsof` | zjištění procesů používajících multicast |

Tyto nástroje umožňují jednoduše analyzovat **multicast chování přímo na Linux hostu**.
