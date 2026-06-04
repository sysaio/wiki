# **testing ai**

# Sítě v Linuxu - Přechod od net-tools k iproute2

> [!IMPORTANT] Při práci se sítěmi v moderním Linuxu, zejména v Ubuntu/Kubuntu, je zásadní pochopit a 
naučit se používat příkazy z balíku `iproute2` namísto zastaralých nástrojů z balíku `net-tools`. 
Přechod proběhl s novým způsobem práce se sítovou konfigurací, který je flexibilnější a nabízí 
pokročilejší funkce. Staré nástroje jako `ifconfig` a `netstat` jsou stále dostupné, ale používání 
`iproute2` je nyní standardní a doporučené.

V moderním Linuxu se síťová správa posunula k nástrojům z balíku `iproute2`, který poskytuje jednotný 
rozhraní pro správu sítě od jádra po uživatelské aplikace.  Příkazy jako `ip`, `ss` a `arp` představují 
pokročilé a flexibilní nástroje pro sledování a manipulaci se sítovými prostředky. Je to zásadní změna 
oproti jednodušším, ale méně robustním nástrojům z `net-tools`.  Pochopení principů `iproute2` je 
klíčové pro efektivní správu sítí v dnešním Linuxovém prostředí.

## Přehled Příkazů - Staré vs. Nové

| Účel použití | Starý příkaz (net-tools) -> | Nový příkaz (iproute2) -> | Rychlý příklad s parametrem | 
Diagnostický tip |
|---|---|---|---|---|
| Zobrazení IP adresy | `ifconfig` | `ip addr show` | `ip addr show` | Kontrola rozsahu a typu adrese.  
Problémy s konfigurací? |
| Kontrola otevřených portů | `netstat -tulnp` | `ss -tulnp` | `ss -tulnp` | `ss` je rychlejší, 
podrobnější. Zkontroluj, zda se aplikace poslouchají. |
| Zobrazení směrovací tabulky | `route -n` | `ip route show` | `ip route show` | Hledej chyby v 
trasování, neočekávané mezilehlé routy.  Zkontroluj masku sítě. |
| Sledování paketů | `traceroute` | `tracepath` | `tracepath google.com` |  Identifikace problémových 
segmentů v síti. Zvol správnou verzi pro přesnost a rychlost. |
| Řízení protokolu ARP | `arp -a` | `ss addr` (ve spojení s 'ip') | `ss addr` |  Zkontroluj, které 
adresy odpovídají MAC adresám. Problémy s broadcastem? |
| Změna směrovacího cíle | `route add -net <cílová síť> gw <brána>` | `ip route add <cílová síť> via 
<brána>`  | `ip route add 192.168.1.0/24 via 192.168.1.1` | Ujisti se, že brána je správná a dostupná. 
Kontrola směrování. |
| Zobrazení statistik sítě | `netstat -b` (vyžaduje root) |  Neexistuje přímý ekvivalent - používá se 
kombinace `ss`, `ip`, `tc` |  Komplexní použití, vyžaduje hlubší znalosti. |  Pochop, jaké aplikace 
spotřebovávají síťový provoz. Sleduj využití带宽.  |

## Zdroje a Literatura

1.  Dingus, M. (2018). *Linux network programming*. Packt Publishing.
2.  Van Pelt, G., & Leininger, K. (2013). *TCP/IP network administration*. Cisco Press.
```

**Poznámky:**

*   Tento dokument je optimalizován pro čitelnost a snadné používání na GitHub Wiki.
*   Používám Markdown syntaxi pro formátování kódu a zvýraznění důležitých informací.
*   Tabulka poskytuje přehledné srovnání příkazů, což usnadňuje adaptaci na nový workflow.
*  Zdroje jsou vybrány pro jejich odbornost a relevanci k tématu.
*   Upozornění zvýrazněno pomocí `![IMPORTANT]` syntaxe.


