# **testing ai**


# 🌐 Správa sítě v Linuxu

V moderním Linuxu je zásadní změna přišla s přechodem od starého balíku **net-tools** k modernímu **iproute2**. Starý příkaz `ifconfig` byl 
nahrazen robustnější a flexibilnější `ip`, zatímco `netstat` byl nahrazen `ss`. Tato změna umožnila lepší správu sítě a rozšířené možnosti. 


> [!IMPORTANT] Přechod na iproute2 znamená, že některé staré příkazy již nebudou fungovat včetně standardních balíků.

---

## 📋 Přehledová tabulka příkazů

| Účel použití                  | Starý příkaz         | Nový příkaz          | Rychlý příklad                          |
|-------------------------------|----------------------|----------------------|-----------------------------------------|
| Zobrazení IP adresy           | `ifconfig`           | `ip addr show`        | `ip addr show enp0s3`                   |
| Správa routování              | `route`              | `ip route`            | `sudo ip route add default via 192.168.1.1` |
| Kontrola otevřených portů      | `netstat -tuln`      | `ss -tuln`            | `sudo ss -tuln`                         |
| Aktivace síťového rozhraní     | `ifup`               | `ip link set up`      | `sudo ip link set enp0s3 up`           |
| Zobrazení ARP cache           | `arp -a`             | `ip neigh show`       | `ip neigh show`                         |
| Diagnostika dostupnosti hostitele (ICMP) | `ping`              | `ping`              | `ping 8.8.8.8`                          |
| Sledování trasy paketů (Traceroute) | `traceroute`       | `traceroute`         | `traceroute google.com`                 |

---

## 💡 Tipy, triky a další použití

- 🚀 **Použijte `sudo` pro přístup k síťovým příkazům**: Některé příkazy jako `ss -tuln` vyžadují privilégy, proto je potřeba použít 
`sudo`.  
- 🔒 **Zrychlení výpisu pomocí `-n`**: Parametr `-n` ve `ss` a `ip` zkrácí čas na získání výstupu, protože se vyhne překladu portů do 
názvů.  
- ⚡ **Pro sledování změn použijte `watch`**: Příkaz `watch ip addr show` zobrazí aktualizovaný stav rozhraní každých 2 vteřin.

---

## 📚 Zdroje a literatura

- 📖 Linux man-pages  
- 📖 The Linux Documentation Project (TLDP)  
- 📖 RFC 791 - Internet Protocol  
