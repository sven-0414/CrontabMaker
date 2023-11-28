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
    unique_date_times = set()
    last_date = None

    for row in rows:
        if len(row) < 2:
            continue  # Skip the row if it doesn't have at least two cells

        date = row[0].strip() if row[0].strip() else last_date
        full_date_time = row[1].strip()

        # Separera datum och tid om full_date_time innehåller båda
        if date in full_date_time:
            time = full_date_time.replace(date, '').strip()
        else:
            time = full_date_time

        date_time_key = f"{date}_{time}"  # Using an underscore as a separator

        unique_date_times.add(date_time_key)
        last_date = date  # Update last_date with the current date

    return unique_date_times

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Skriptet behöver ett argument för seriens idnummer.")
    else:
        liga_id = sys.argv[1]
        resultat = fetchMatchTimes(liga_id)
        rows = extract_table_rows(resultat)
        dates_and_times = process_rows(rows)
        print(dates_and_times)
