from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests
import sys
import re

# Koppa upp mot swehockey och hämta Schdule and Result från en serie
def fetchMatchTimes(liga_id):
    try:
        url = f"https://stats.swehockey.se/ScheduleAndResults/Schedule/{liga_id}"
        response = requests.get(url)
        response.raise_for_status()  # Detta kommer att kasta ett undantag om statuskoden inte är 200
        return response.text         # eller response.json() om svaret är JSON
    except requests.RequestException as e:
        return f"Kunde inte hämta data: {e}"

# utvinna tabellcellerna där matcherna redovisas
def extract_table_rows(page_content):
    soup = BeautifulSoup(page_content, 'html.parser')
    table = soup.find('table', class_='tblContent')  # Hämtar tabellen "tblContent"

    if not table:
        return "No table found."

    date_pattern = re.compile(r'\d{4}-\d{2}-\d{2}')  # Mönster för att identifiera datum (YYYY-MM-DD)
    time_pattern = re.compile(r'\d{2}:\d{2}')       # Mönster för att identifiera tid (HH:MM)
    last_date = None  # Variabel för att lagra det senaste giltiga datumet
    unique_date_times = set()  # Set för att lagra unika datum-tid-kombinationer

    for tr in table.find_all('tr'):
        if tr.find('th'):  # Hoppa över raden om den innehåller <th>
            continue

        cells = tr.find_all('td')
        if len(cells) < 1:
            continue

        cell0 = cells[0].get_text(strip=True)
        cell1 = cells[1].get_text(strip=True) if len(cells) > 1 else ""

        # Hantera datum och tid
        if date_pattern.match(cell0):  # Om cell0 innehåller datum
            date = cell0
            last_date = date  # Uppdatera last_date med det nya datumet
            time = cell1 if time_pattern.match(cell1) else ""  # Använd cell1 som tid om det är en tid
        else:
            date = last_date  # Använd last_date om cell0 inte innehåller ett datum
            time = cell0 if time_pattern.match(cell0) else cell1  # Använd cell0 som tid om det är en tid, annars cell1

        # Skapa en unik kombination av datum och tid
        if date and time:  # Kontrollera att det finns ett giltigt datum och tid
            date_time = f"{date} {time}"
            unique_date_times.add(date_time)  # Lägg till i set för unika värden

    return unique_date_times

def create_crontab_entries(date_times):
    crontab_entries = []
    current_time = datetime.now()  # Hämta nuvarande tid

    for date_time in date_times:
        try:
            dt = datetime.strptime(date_time, '%Y-%m-%d %H:%M')
            end_time = dt + timedelta(hours=2)

            # Kontrollera om tiden redan har passerat
            if end_time <= current_time:
                continue

            if end_time.minute == 0:
                crontab_entry = f"0-55/5 {end_time.hour} {end_time.day} {end_time.month} * /opt/hockeytabeller.zsh"
                crontab_entries.append(crontab_entry)
            else:
                crontab_entry = f"{end_time.minute}-55/5 {end_time.hour} {end_time.day} {end_time.month} * /opt/hockeytabeller.zsh"
                crontab_entries.append(crontab_entry)

                next_hour = (end_time + timedelta(hours=1)).hour
                crontab_entry_next_hour = f"0-{end_time.minute}/5 {next_hour} {end_time.day} {end_time.month} * /opt/hockeytabeller.zsh"
                crontab_entries.append(crontab_entry_next_hour)
        except ValueError as e:
            print(f"Ogiltigt datum/tid-format: {date_time}. Fel: {e}")

    return crontab_entries

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Skriptet behöver ett argument för seriens idnummer.")
    else:
        liga_id = sys.argv[1]
        resultat = fetchMatchTimes(liga_id)
        rows = extract_table_rows(resultat)
        crontab_lines = create_crontab_entries(rows)
        for line in crontab_lines:
            print(line)
