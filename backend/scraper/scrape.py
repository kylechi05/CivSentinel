import re

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from supabase import Client

from connection import get_client
from utils.supabase.datetime import dateToCentralISO

def get_page_soup() -> BeautifulSoup:
    response = requests.get('https://safety.uiowa.edu/crime-log')
    soup = BeautifulSoup(response.text, 'html.parser')

    return soup

def parse_html_crimes(soup: BeautifulSoup) -> list[str]:
    crimes = []

    table = soup.find('table')
    tbody = table.find('tbody')
    for row in tbody.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) != 6:
            continue
        
        data = [cell.get_text(strip=True) for cell in cells]
        crimes.append(data)

    return crimes

def get_last_crime(client: Client) -> str:
    supabase = client

    try:
        most_recent_crime = supabase.table('crimes').select('associated_id', 'date_reported').order('date_reported', desc=True).limit(1).execute()
        most_recent_unlinked = supabase.table('unlinked_crimes').select('associated_id', 'date_reported').order('date_reported', desc=True).limit(1).execute()

        latest_crime_id = ''
                    
        if len(most_recent_crime.data) != 0 and len(most_recent_unlinked.data) != 0:
            if datetime.fromisoformat(most_recent_crime.data[0]['date_reported']) > datetime.fromisoformat(most_recent_unlinked.data[0]['date_reported']):
                latest_crime_id = most_recent_crime.data[0]['associated_id']
            else:
                latest_crime_id = most_recent_unlinked.data[0]['associated_id']
        elif len(most_recent_crime.data) != 0:
            latest_crime_id = most_recent_crime.data[0]['associated_id']
        elif len(most_recent_unlinked.data) != 0:
            latest_crime_id = most_recent_unlinked.data[0]['associated_id']

        return latest_crime_id
    except Exception as e:
        print(f'Error fetching last crime associated ID: {e}')

def match_scraped_dates(date: str) -> str:
    DATETIME_REGEX = r'\d{2}/\d{2}/\d{4} \d{2}:\d{2}'
    DATE_ONLY_REGEX = r'\d{2}/\d{2}/\d{4}'

    datetime_match = re.search(DATETIME_REGEX, date)
    if datetime_match:
        return dateToCentralISO(datetime.strptime(datetime_match.group(), '%m/%d/%Y %H:%M'))

    date_match = re.search(DATE_ONLY_REGEX, date)
    if date_match:
        return dateToCentralISO(datetime.strptime(date_match.group(), '%m/%d/%Y'))
    
    return ''

def insert_scraped_data(scraped_crimes: list[str], latest_crime_associated_id: str, client: Client) -> None:
    supabase = client
    all_scraped_crimes = []

    for associated_id, natures_of_crime, date_time_occurred, date_reported, general_location, _ in scraped_crimes:
        if associated_id == latest_crime_associated_id:
            break

        if not associated_id or not date_time_occurred or not date_reported or not general_location:
            continue

        matched_date_occurred = match_scraped_dates(str(date_time_occurred))
        matched_date_reported = match_scraped_dates(str(date_reported))

        if not matched_date_reported:
            continue

        general_location = general_location.lower().strip()

        data = {
                'associated_id': associated_id,
                'general_location': general_location,
                'natures_of_crime': natures_of_crime,
                'date_time_occurred': matched_date_occurred if matched_date_occurred else matched_date_reported,
                'date_reported': matched_date_reported,
        }
        all_scraped_crimes.append(data)
    
    if len(all_scraped_crimes) > 0:
        supabase.table('unlinked_crimes').insert(all_scraped_crimes).execute()

def main():
    supabase_client = get_client()

    soup = get_page_soup()
    crimes = parse_html_crimes(soup)

    latest_crime_associated_id = get_last_crime(supabase_client)
    insert_scraped_data(crimes, latest_crime_associated_id, supabase_client)
    print('Data scraping completed')

if __name__ == '__main__':
    main()