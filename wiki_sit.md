 # Správa sítě v Linuxu

V moderním Linuxu se přešlo od starého balíku net-tools ke modernímu iprout[6D[K
iproute2, který nabízí rozsáhlejší funkcionalitu a je standardní v dnešních[8D[K
dnešních distribucich. Iprobe2 umožňuje spravovat síťové prostředí s lepší [K
kontrolou přesnějšími nastaveními a nabízí rozsáhlejší možnosti pro diagnos[7D[K
diagnostiku a výkonnostní testy.

-

Viproute2 nahrazuje starý balík net-tools, který je stále k dispozici, ale [K
jeho použití se nepreporučuje v novějších verzích Linuxu. Iprobe2 nabízí ro[2D[K
rozsáhlejší funkcionalitu a je standardní v dnešních distribucich.

 | Účel použití       | Starý příkaz                | Nový příkaz          [K
         | Rychlý příklad              |
|---------------------|-----------------------------|----------------------|---------------------|-----------------------------|------------------------------|----------------------------|
| Zobrazení IP adresy  | ifconfig                    | ip a                [K
         | `ip a`                     |
| Správa routování    | route                       | ip r (nebo ip route) [K
       | `ip r`                     |
| Kontrola otevřených portů| netstat -tuln              | nmap -p<port>    [K
            | `nmap -p80 localhost`      |
| Aktivace síťového rozhraní| ifconfig eth0 up          | ip link set eth0 [K
up         | `ip link set eth0 up`     |
| Zobrazení ARP cache   | arp -a                      | ip nneigh show     [K
          | `ip nneigh show default`  |
| Diagnostika dostupnosti hostitele (ICMP) | ping                         |[1D[K
| ping <host>                  | `ping google.com`          |
| Sledování trasy paketů (Traceroute)| traceroute               | mtr <host[5D[K
<host>                   | `mtr google.com`           |

 ## Tipy, triky a další použití

- Sudo: Používejte `sudo ss` pro zobrazení souborů v síti, které mají opráv[5D[K
oprávnění pouze správce.
- Zrychlení výpisu: Použijte parametr `-n` se službou `ss` (Socket Statisti[8D[K
Statistics) k zrychlení výpisu, který nezobrazuje názvy hostitelů nebo proc[4D[K
procesů.
- Vyhledání portu: Použijte nástroj `lsof` (List Open Files) společně se sl[2D[K
službou `grep` k rychlému vyhledávání otevřených portů v Kubuntu. Například[9D[K
Například `lsof -i :port_number | grep LISTEN`.

 ## Zdroje a literatura

1. Torvalds, L. (2018). man7 - Linux Programmer's Manual. Retrieved from ht[2D[K
https://man7.org/linux/man-pages/man7/

2. The Linux Documentation Project. (n.d.). Main Page. Retrieved from https[5D[K
https://www.tldp.org/

