import os
import re

import pandas as pd
from supabase import Client

from utils.connection import get_client
from utils.address import get_street_address, get_city, get_state, get_zip_code
from utils.datetime import dateTimeOccurredToISO, dateReportedToISO

def clear_database(client: Client) -> None:
    supabase = client
    try:
        supabase.rpc('reset_all_tables').execute()

        print('Database cleared successfully.')
    except Exception as e:
        print(f'Error clearing database: {e}')

def seed_mapping(mapping_df: pd.DataFrame, client: Client) -> None:
    supabase = client
    all_mappings = []
    
    try:
        for row in mapping_df.itertuples():
            general_name = row.Index
            full_address = row.address
            coordinates = row.coordinates

            if pd.isna(full_address) or not isinstance(coordinates, list) or len(coordinates) != 2 or any(pd.isna(coord) for coord in coordinates):
                continue
            
            street_address = get_street_address(full_address)
            city = get_city(full_address)
            state = get_state(full_address)
            zip_code = get_zip_code(full_address)

            data = {
                'general_location': general_name,
                'street_address': street_address,
                'city': city,
                'state': state,
                'zip_code': zip_code,
                'location': f'POINT({coordinates[1]} {coordinates[0]})'
            }
            all_mappings.append(data)

        supabase.table('location_mapping').insert(all_mappings).execute()
    
        print('Mapping seeded successfully.')
    except Exception as e:
        print(f'Error inserting mapping: {e}')

def seed_crime_data(crime_df: pd.DataFrame, client: Client) -> None:
    supabase = client
    all_crimes = []

    DATE_OCCURED_REGEX = r'\d{2}/\d{2}/\d{4} \d{1,2}:\d{2} (?:AM|PM)'
    DATE_REPORTED_REGEX = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}'

    try:
        general_locations_res = supabase.table('location_mapping').select('general_location').execute()
        general_locations = {item['general_location'] for item in general_locations_res.data}

        for _, row in crime_df.iterrows():
            if pd.isna(row['Associated ID']) or pd.isna(row['Date Reported']) or pd.isna(row['Date/Time Occurred']) or pd.isna(row['General Location']):
                continue

            matched_date_occurred = re.search(DATE_OCCURED_REGEX, str(row['Date/Time Occurred']))
            matched_date_reported = re.search(DATE_REPORTED_REGEX, str(row['Date Reported']))
            general_location = row['General Location'].lower().strip()

            if not matched_date_reported or general_location not in general_locations:
                continue

            formatedDateReported = dateReportedToISO(matched_date_reported.group(0))
            formattedDateTimeOccurred = dateTimeOccurredToISO(matched_date_occurred.group(0)) if matched_date_occurred else formatedDateReported

            data = {
                'associated_id': row['Associated ID'],
                'general_location': general_location,
                'natures_of_crime': row['Nature of Crime(s)'],
                'date_time_occurred': formattedDateTimeOccurred,
                'date_reported': formatedDateReported,
            }
            all_crimes.append(data)

        supabase.table('crimes').insert(all_crimes).execute()

        print('Crime data seeded successfully.')
    except Exception as e:
        print(f'Error inserting crime data: {e}')

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    mapping_path = os.path.join(script_dir, './datasets/iowa_city/iowa_city_location_mapping.json')
    raw_path = os.path.join(script_dir, './datasets/iowa_city/iowa_city_raw_6_29_2025.xlsx')

    mapping_df = pd.read_json(mapping_path)
    mapping_df = mapping_df.T

    crime_df = pd.read_excel(raw_path)

    supabase_client = get_client()

    clear_database(supabase_client)
    seed_mapping(mapping_df, supabase_client)
    seed_crime_data(crime_df, supabase_client)

if __name__ == '__main__':
    main()
    