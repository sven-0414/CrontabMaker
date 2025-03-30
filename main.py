from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests
import sys
import re

# Hämta sida från swehockey
def fetch_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        return f"Kunde inte hämta data: {e}"

# Skapa ett objekt för BeautifulSoup
def create_soup(page_content):
    return BeautifulSoup(page_content, 'html.parser')

# Extraherar tabellens innehåll
def extract_table_content(soup, table_class):
    table = soup.find('table', class_=table_class)
    return table if table else "No table found."

# Extraherar de första två cellerna från tabellen
def extract_first_three_cells(table):
    date_pattern = re.compile(r'([0-9]{4}-[0-9]{2}-[0-9]{2})')
    time_pattern = re.compile(r'([0-9]{2}:[0-9]{2})')
    extracted_data = []
    last_date = None

    for tr in table.find_all('tr'):
        cells = tr.find_all('td')
        if len(cells) > 2:
            cell0_text = cells[0].get_text().replace('\xa0', ' ').strip()
            cell1_text = cells[1].get_text().replace('\xa0', ' ').strip()
            cell2_text = cells[2].get_text().strip()

            date = extract_date(cell0_text, date_pattern)
            if not date:
                date, time = parse_date_time(cell1_text, date_pattern, time_pattern)
                date = date or last_date
            else:
                time = None

            if not time:
                time = extract_time(cell2_text, time_pattern)

            if date and time:
                extracted_data.append(f"{date} {time}")
                last_date = date

    return extracted_data


def extract_date(cell_text, date_pattern):
    match = date_pattern.search(cell_text)
    return match.group(1) if match else None


def extract_time(cell_text, time_pattern):
    match = time_pattern.search(cell_text)
    return match.group(1) if match else None


def parse_date_time(cell_text, date_pattern, time_pattern):
    date = extract_date(cell_text, date_pattern)
    time = extract_time(cell_text, time_pattern)
    return date, time

# Skapar crontab-rader
def create_crontab_entry(dt, script_path):
    end_time = dt + timedelta(hours=2)
    crontab_entries = []

    if end_time.minute == 0:
        crontab_entries.append(f"0-55/5 {end_time.hour} {end_time.day} {end_time.month} * {script_path}")
    else:
        crontab_entries.append(f"{end_time.minute}-55/5 {end_time.hour} {end_time.day} {end_time.month} * {script_path}")
        next_hour = (end_time + timedelta(hours=1)).hour
        crontab_entries.append(f"0-{end_time.minute}/5 {next_hour} {end_time.day} {end_time.month} * {script_path}")

    return crontab_entries

# Skapar alla crontab-rader från extraherade datum och tider
def create_all_crontab_entries(date_times, script_path):
    crontab_entries = []
    dates_for_extra_run = set()
    current_time = datetime.now()

    for date_time in date_times:
        try:
            dt = datetime.strptime(date_time, '%Y-%m-%d %H:%M')

            # Hoppa över tider som redan har passerat
            if dt + timedelta(hours=2) <= current_time:
                continue

            entries = create_crontab_entry(dt, script_path)
            crontab_entries.extend(entries)
            dates_for_extra_run.add((dt.day, dt.month))
        except ValueError as e:
            print(f"Ogiltigt datum/tid-format: {date_time}. Fel: {e}")

    # Lägg till en extra körning kl. 23:55 för varje unikt datum
    for day, month in dates_for_extra_run:
        crontab_entries.append(f"00 23 {day} {month} * {script_path}")

    return crontab_entries

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Skriptet behöver ett argument för seriens idnummer.")
    else:
        liga_id = sys.argv[1]
        url = f"https://stats.swehockey.se/ScheduleAndResults/Schedule/{liga_id}"
        page_content = fetch_page(url)  # Rättar till namnet på funktionen

        if "Kunde inte hämta data" not in page_content:
            soup = create_soup(page_content)
            table_content = extract_table_content(soup, 'tblContent')
            if isinstance(table_content, str):
                print(table_content)  # Hanterar felmeddelandet om ingen tabell hittades
            else:
                two_first_rows = extract_first_three_cells(table_content)
                script_path = "/opt/hockeytabeller.zsh"
                crontab_lines = create_all_crontab_entries(two_first_rows, script_path)
                for line in crontab_lines:
                    print(line)
        else:
            print(page_content)  # Skriver ut felmeddelandet om sidan inte kunde hämtas
