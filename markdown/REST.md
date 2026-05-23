---
title: Přehled REST API – jednoduchý průvodce
category: Informatika
tags: [internet, REST, HTTP, programování]
last_update: 2025-07-29
---

# 🧭 Přehled REST API – jednoduchý průvodce

## 🌐 Co je REST API?  
REST (Representational State Transfer) je architektonický styl API, který definuje, jak komunikovat mezi klientem a serverem přes internet. REST se zaměřuje na **práci se zdroji (resources)** pomocí standardních HTTP metod a podporuje:  
- 🌀 bezstavovost  
- ⚙️ škálovatelnost  
- 🔄 snadnou rozšiřitelnost  

Na rozdíl od SOAP nebo RPC neorientuje komunikaci na volání funkcí, ale na práci s daty.
Pro REST pravděpodobně nenajdeme žádnou normu, ale vřele se doporučuje níže uvedené dodržovat.

## 🏗️ Úrovně REST API (Richardsonova škála)  

### 0️⃣ Nultá úroveň – Přenos dat  
- Přenos dat bez jasně definovaného API.  
- REST není limitován pouze HTTP, ale dnes je HTTP dominantní protokol díky dostupnosti a vlastnostem.

### 1️⃣ První úroveň – Zdroje (Resources)  
- Každý zdroj má unikátní URL.  
- Příklad:  
  - `GET /articles` – seznam článků  
  - `GET /articles/1/comments` – komentáře ke článku s ID 1  
- Důležité je konzistentní pojmenování (např. množné číslo).

### 2️⃣ Druhá úroveň – HTTP metody (Verbs)  
- Akce se vyjadřují pomocí HTTP metod, nikoli v URL.  

| 🔹 Metoda  | 🎯 Účel                         |  
|------------|--------------------------------|  
| GET        | Načtení dat                    |  
| POST       | Vytvoření nového zdroje        |  
| PUT        | Kompletní aktualizace zdroje   |  
| PATCH      | Částečná aktualizace           |  
| DELETE     | Smazání zdroje                 |  

- PATCH snižuje datový tok, přenáší jen změněná data.

### 3️⃣ Třetí úroveň – Stavové kódy HTTP  
- Informují o výsledku požadavku. Nejčastější:  

| 🏷️ Kód | Význam                          |  
|--------|---------------------------------|  
| 200    | OK – požadavek úspěšný          |  
| 201    | Created – nový zdroj vytvořen   |  
| 204    | No Content – bez obsahu          |  
| 400    | Bad Request – špatný požadavek  |  
| 401    | Unauthorized – neautorizovaný   |  
| 403    | Forbidden – přístup zakázán     |  
| 404    | Not Found – zdroj nenalezen     |  
| 405    | Method Not Allowed – metoda nepovolená |  
| 415    | Unsupported Media Type – nepodporovaný formát |  
| 429    | Too Many Requests – překročen limit požadavků | 
| 500    | Internal Server Error – to je asi jasné |
| 503    | Service Unavailable – nedostupnost služby na kterou je zaslán požadavek (GET) |
| 504    | Gateway Timeout – pravděpodobně odpojená (filtrovaná FW) URL  |
| 501    | Not Implemented – nebyla rozpoznána metoda |

### 4️⃣ Čtvrtá úroveň – Bezstavovost  
- Server nesmí uchovávat stav klienta mezi požadavky.  
- Každý požadavek musí obsahovat potřebná ověřovací data (např. token).

### 5️⃣ Pátá úroveň – HATEOAS (Hypermedia as the Engine of Application State)  
- Server ve své odpovědi poskytuje klientovi **odkazy na další akce a zdroje**.  
- Klient zná pouze základní URL a dále „kliká“ na odkazy, které API vrací.  
- Výhody:  
  - URL se mohou měnit bez nutnosti měnit klienta  
  - Snadná rozšiřitelnost  
- V praxi zatím méně rozšířené kvůli složitosti a nedostatku nástrojů.

## 🛠️ Praktické tipy pro implementaci REST API 

### 💨 Komprese a formáty  
- Používejte **GZIP** pro snížení objemu dat až o 80 %.  
- Preferujte **JSON** jako hlavní formát, ale podporujte i XML či jiné dle hlavičky `Content-Type`.  
- Možné detekce formátu i přes URL přípony (`.json`, `.xml`), ale hlavička je čistší řešení.

### 🗃️ Cacheování  
- Využívejte HTTP hlavičky **ETag** a **Last-Modified** pro efektivní cache (snížení zátěže serveru).

### 🔗 URL design a relace  
- Intuitivní URL s jasnou hierarchií, např.:  
  - `GET /articles/1/comments` – komentáře ke článku 1  
  - `DELETE /articles/1/comments/5` – smaže komentář 5 u článku 1  

### 📄 Stránkování  
- Používejte HTTP hlavičku **Link** pro navigaci mezi stránkami a **X-Total-Count** pro počet všech položek.

### 🔤 Styl pojmenování polí
- Používejte jednotný styl (snake_case, camelCase či PascalCase).
  - `snake_case` (lépe čitelný)  
  - `camelCase` (přirozenější pro JavaScript) 
- Umožněte klientům volbu, pokud to vaše API podporuje (Fielding, 2000).

## Praktické ukázky HTTP požadavků

### Načtení seznamu článků
GET /articles HTTP/1.1  
Host: example.com  
Accept: application/json  
Authorization: Bearer <token>

### Vytvoření nového článku
POST /articles HTTP/1.1  
Host: example.com  
Content-Type: application/json  
Authorization: Bearer <token>  

{  
  "title": "Nový článek",  
  "content": "Obsah článku..."  
}

### Aktualizace existujícího článku (kompletní)
PUT /articles/1 HTTP/1.1  
Host: example.com  
Content-Type: application/json  
Authorization: Bearer <token>  

{  
  "title": "Aktualizovaný titul",  
  "content": "Aktualizovaný obsah..."  
}

### Částečná aktualizace článku
PATCH /articles/1 HTTP/1.1  
Host: example.com  
Content-Type: application/json  
Authorization: Bearer <token>  

{  
  "title": "Částečně aktualizovaný titul"  
}

### Smazání článku
DELETE /articles/1 HTTP/1.1  
Host: example.com  
Authorization: Bearer <token>

## Vývoj a testování REST API

- Apiary.io – návrh a mockování API (https://apiary.io).  
- cURL – příkazový nástroj pro testování HTTP požadavků, např.  
  curl -X GET https://example.com/articles -H "Authorization: Bearer <token>"  
- Postman – uživatelsky přívětivý nástroj pro testování a dokumentaci API (https://www.postman.com).

## Známé technologie používající REST API

- CouchDB – NoSQL databáze přístupná přes REST (https://couchdb.apache.org).  
- ElasticSearch – fulltextový vyhledávač s REST rozhraním (https://www.elastic.co/elasticsearch).

## Závěr
REST API je efektivní a standardizovaný způsob, jak zpřístupnit data a funkce přes internet. 
Díky:
🔄 bezstavovosti
📡 standardním HTTP metodám
🌍 široké podpoře
je REST vhodný pro webové, mobilní i další aplikace.

## 📚 Literatura a odkazy
Fielding, R.T. (2000). Architectural Styles and the Design of Network-based Software Architectures [online]. [cit. 2025-07-29]. Dostupné z: https://www.ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm  
Hanák, D. (2025). Stopařův průvodce REST API. ITnetwork.cz [online]. [cit. 2025-07-29]. Dostupné z: https://www.itnetwork.cz/programovani/nezarazene/stoparuv-pruvodce-rest-api  
Apiary.io. (n.d.). API design platform. Dostupné z: https://apiary.io  
Postman. (n.d.). API Development Environment. Dostupné z: https://www.postman.com  
Apache CouchDB. (n.d.). The CouchDB Project. Dostupné z: https://couchdb.apache.org  
Elastic. (n.d.). Elasticsearch. Dostupné z: https://www.elastic.co/elasticsearch

*Text je upravený a doplněný na základě původního článku Drahomíra Hanáka pro potřeby této wiki.*
