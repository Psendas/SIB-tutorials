# Homework

- Download the pcap and associated alert files: `misib-2021-hw3_infected.zip`

- Analyzing the alerts, you can easily find that something is going on

- Your task is to verify, whether the alerts are true positive, prepare short summary of machine details, your findings and list all the Indicators of Compromise you can find yout from the pcap file.

## Inspiration

- [MI-SIB_HW3_let-safrata-vojtesek.pdf](MI-SIB_HW3_let-safrata-vojtesek.pdf)

- [misib-hw3-inspiration2.txt](misib-hw3-inspiration2.txt)

## Tutorial

- Suricata and Snort alert files in `pcap analysis - tutorial`

## Solution

- Počítač `10.0.0.167` se v 23:17:42 dotazuje pomocí DNS na doménu `play.astrite.ga`. Adresa v odpovědi na tento dotaz je `158.69.28.93`. Tato adresa patří hostingu `OVH Hosting, Inc.`.

- Filtr podle eventu ET MALWARE: `(ip.src == 10.0.0.167 or ip.dst == 10.0.0.167) and http`

- `tcp.stream eq 125` -> V 23:14:42 posílá počítač `10.0.0.167` požadavek na stažení `VBS` skriptu označného jako `Judgement_04222020_1663.vbs` na počítač `158.69.28.93`. Podle Virustotal se jedná o Downloader/Dropper. ![misib-2021-hw3/virustotal1.png](misib-2021-hw3/virustotal1.png)

- `tcp.stream eq 132` -> Počítač `10.0.0.167` odesílá požadavek na adresu `104.24.111.29` ve kterém jako parametr odesílá base64 zakódovaný string `Windows Defender - 6,21,0|Microsoft Windows 10 Pro`.

- `tcp.stream eq 136` -> `10.0.0.167` stahuje `HTTP` požadavkem spustitelný soubor z adresy `119.31.234.40`. Tento soubor je identifikován jako malware. ![misib-2021-hw3/virustotal2.png](misib-2021-hw3/virustotal2.png)

- export vzorku malwaru: `tshark -r 2020-04-24-traffic-analysis-exercise.pcap -Y "tcp.stream eq 136" -w executable` a smazat začátek požadavku, potřeba vypnout Windows Defender.

- analyza [https://www.virustotal.com/gui/file/f9599ed974bf7c10895fd1345faf6702f15c6f8d4bf086244154d93e3e579a8e/detection](https://www.virustotal.com/gui/file/f9599ed974bf7c10895fd1345faf6702f15c6f8d4bf086244154d93e3e579a8e/detection)

- DNS dotaz na doménu `.co` je na doménové jméno api.sele.co. Tato stránka vrací pouze jedno z následujících slov `Hola Hello Kumusta?`.

- Event označený jako JPEG Rendering Buffer Overflow zahrnuje stavání obrázků z adresy 34.98.72.95 na adresu 10.0.0.149. Přenesené obrázky jsme stáhli jako a jedná se o obrázky spojené s webem, který uživatel navštěvoval (eatingwell.com). User-Agent použitý v požadavcích na stažení těchnto obrázků navíc indikuje použití prohléžeče Mozilla Firefox `User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0`. Event hodnotíme jako false positive.

- Mezi počítači `10.0.0.149` a `10.0.0.167` dochází v 23:31:41 k navázání projení protokolem SMBv1, filtr: `ip.src == 10.0.0.149 and ip.dst == 10.0.0.167 and smb.dialect == "NT LM 0.12"`.

- SVCCTL připojení je zachyceno v tcp streamu 700 `tcp.stream eq 700`. Navazovaná komunikace je šifrovaná a wireshark vyhodnotil první request jako Unknown operation, druhý jako OpenSCManagerW request a response.

## Hosts

### 10.0.0.167

- Hostname: DESKTOP-GRIONXA

- MAC: ac:16:2d:f5:37:e5

- OS: Microsoft Windows 10 Pro

- Browser:  Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0

### 10.0.0.149

- Hostname: DESKTOP-C10SKPY

- MAC: 6c:c2:17:f7:80:b6

- OS: Microsoft Windows 10

- Browser: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0

### 10.0.0.10

- Hostname: STEELCOFFEE-DC

- MAC: a4:1f:72:c2:09:6a

- OS: Windows 7 or 8

- Function: DC, DNS resolver

## Shrnutí

- Po detailní analýze jsme ostatní Eventy nevyhodnotili jako z bezpečnostního hlediska škodlivé.

- Počítač na adrese `10.0.0.167` stahoval nejprve nebezpečný skript a následně škodlivý spustitelný soubor. Eventy zachycené sledovacím nástrojem související s tímto strojem tak hodnotíme jako true possive.

- Bezpečností hrozby nahlášené v souvislosti s strojem `10.0.0.149` hodnotíme jako false possitive.
