import re
import os

import pandas as pd
import json
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

raw_data_path = os.path.join(BASE_DIR, '../datasets/raw/iowa_city_raw_6_29_2025.xlsx')
location_mapping_path = os.path.join(BASE_DIR, '../datasets/raw/iowa_city_location_mapping.json')
processed_df_path = os.path.join(BASE_DIR, '../datasets/processed/cleaned_data.csv')

crimes_excel = pd.read_excel(raw_data_path)
with open(location_mapping_path) as f:
    crime_mapping_dict = json.load(f)

cleaned_data = pd.DataFrame()
DATE_REGEX = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}'

for _, row in crimes_excel.iterrows():
    if pd.isna(row['Associated ID']) or pd.isna(row['Date Reported']) or pd.isna(row['Date/Time Occurred']) or pd.isna(row['General Location']):
        continue

    date = re.search(DATE_REGEX, str(row['Date Reported']))

    general_location = row['General Location'].lower().strip()

    if general_location in crime_mapping_dict and pd.notna(crime_mapping_dict[general_location]) and date.group(0):
        date_dt = datetime.strptime(date.group(0), '%Y-%m-%d %H:%M:%S')

        cleaned_data = pd.concat([cleaned_data, pd.DataFrame([{
            'associated_id': row['Associated ID'],
            'general_location': general_location,
            'natures_of_crime': row['Nature of Crime(s)'],
            'date': date_dt,
            'latitude': crime_mapping_dict[general_location]['coordinates'][0],
            'longitude': crime_mapping_dict[general_location]['coordinates'][1],
        }])])

cleaned_data.to_csv(processed_df_path, index=False)

print(f'Saved cleaned data to {processed_df_path}')