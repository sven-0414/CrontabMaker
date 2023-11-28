from bs4 import BeautifulSoup
import requests
import sys

# Koppa upp mot swehockey och hämta Schdule and Result från en serie
def fetchMatchTimes(liga_id):
    try:
        url = f"https://stats.swehockey.se/ScheduleAndResults/Schedule/{liga_id}"
        response = requests.get(url)
        response.raise_for_status()  # Detta kommer att kasta ett undantag om statuskoden inte är 200
        return response.text         # eller response.json() om svaret är JSON
    except requests.RequestException as e:
        return f"Kunde inte hämta data: {e}"

# från den hemsida som hämtats utvinna tabellraderna där matcherna redovisas
def extract_table_rows(page_content):
    soup = BeautifulSoup(page_content, 'html.parser')
    table = soup.find('table', class_='tblContent') #hämtar tabellen "tblContent"

    if not table:
        return "No table found."

    rows = []
    for tr in table.find_all('tr'):
        if tr.find('th'):  # Hoppa över raden om den innehåller <th>
            continue
        row_data = [td.get_text(strip=True) for td in tr.find_all('td')]
        rows.append(row_data)
    return rows

def process_rows(rows):
    unique_date_times = {}  # Dictionary för att lagra datum-tid och eventuell ytterligare information

    for row in rows:
        if len(row) < 2:
            continue

        date, time = row[0], row[1]
        if not date:
            continue

        date_time = f"{date} {time}"

        if date_time not in unique_date_times:
            unique_date_times[date_time] = (date, time)  # eller annan relevant information

    return unique_date_times

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Skriptet behöver ett argument för seriens idnummer.")
    else:
        liga_id = sys.argv[1]
        resultat = fetchMatchTimes(liga_id)
        rows = extract_table_rows(resultat)
        datesAndTimes = process_rows(rows)
        for date_time, values in unique_date_times.items():
            print(f"Date-Time: {date_time}, Values: {values}")
