import re

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from supabase import Client

from utils.connection import get_client
from utils.datetime import dateToCentralISO

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

def insert_scraped_data(scraped_crimes: list[str], client: Client) -> None:
    supabase = client
    all_scraped_crimes = []

    for associated_id, natures_of_crime, date_time_occurred, date_reported, general_location, _ in scraped_crimes:
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
        supabase.table('unlinked_crimes').upsert(all_scraped_crimes, on_conflict='associated_id').execute()

def run_scrape():
    supabase_client = get_client()

    soup = get_page_soup()
    crimes = parse_html_crimes(soup)

    insert_scraped_data(crimes, supabase_client)

    print('Data scraping completed')
