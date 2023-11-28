from bs4 import BeautifulSoup
import requests
import sys


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Skriptet behöver ett argument för seriens idnummer.")
    else:
        liga_id = sys.argv[1]
        resultat = fetchMachTimes(liga_id)
        print(resultat)


def fetchMachTimes(liga_id):
    try:
        url = f"https://stats.swehockey.se/ScheduleAndResults/Schedule/{liga_id}"
        response = requests.get(url)
        response.raise_for_status()  # Detta kommer att kasta ett undantag om statuskoden inte är 200
        return response.text         # eller response.json() om svaret är JSON
    except requests.RequestException as e:
        return f"Kunde inte hämta data: {e}"
