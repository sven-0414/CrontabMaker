# Swehockey Crontab Generator

Detta Python-skript hämtar matchschema från stats.swehockey.se och genererar crontab-rader som kör ett annat skript strax efter att matcherna borde vara slut. Nyttigt för att till exempel uppdatera statistik efter avslutade matcher.

Eftersom skriptet är avsett att köras automatiskt innehåller det inga menyer, utan styrs via ett argument: seriens ID. Det hittar du i URL:en på Swehockey, till exempel:  
https://stats.swehockey.se/ScheduleAndResults/Overview/15986

Skriptet är endast avsett för mina personliga skript som kördes för att uppdatera Wikipedias poängtabeller säsongen 2023/24. All annan användning sker på egen risk.

## Användning
```bash
python3 main.py <serie-id>
```
Exempel på utmatning:

```bash
0-55/5 21 30 3 * /opt/hockeytabeller.zsh
00 23 30 3 * /opt/hockeytabeller.zsh
```

## Installation
```bash
pip install -r requirements.txt
```

## Licens

Koden distribueras under Apache 2.0, vilket i korthet betyder att man får använda, ändra och distribuera koden så länge man inkluderar erkännande till upphovsmannen.