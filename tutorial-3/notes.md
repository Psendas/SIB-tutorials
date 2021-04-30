# Homework

- Download the pcap and associated alert files: `misib-2021-hw3_infected.zip`

- Analyzing the alerts, you can easily find that something is going on

- Your task is to verify, whether the alerts are true positive, prepare short summary of machine details, your findings and list all the Indicators of Compromise you can find yout from the pcap file.

## Inspiration

- [MI-SIB_HW3_let-safrata-vojtesek.pdf](MI-SIB_HW3_let-safrata-vojtesek.pdf)

- [misib-hw3-inspiration2.txt](misib-hw3-inspiration2.txt)

## Tutorial

- Suricata and Snort alert files in `pcap analysis - tutorial`

# Solution

- `tcp.stream eq 136` -> stream stahuje `HTTP` požadavkem spustitelný soubor

- export vzorku malwaru: `tshark -r 2020-04-24-traffic-analysis-exercise.pcap -Y "tcp.stream eq 136" -w executable` a smazat zacatek pozadavku (treba v terminalu ve vimu), potreba vypnout Windows Defender

- analyza [https://www.virustotal.com/gui/file/f9599ed974bf7c10895fd1345faf6702f15c6f8d4bf086244154d93e3e579a8e/detection](https://www.virustotal.com/gui/file/f9599ed974bf7c10895fd1345faf6702f15c6f8d4bf086244154d93e3e579a8e/detection)
