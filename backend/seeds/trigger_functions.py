import os

import psycopg2
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

connection = psycopg2.connect(
    host=os.getenv('SUPABASE_DB_POOL_HOST'),
    database=os.getenv('SUPABASE_DB_POOL_DATABASE'),
    user=os.getenv('SUPABASE_DB_POOL_USER'),
    password=os.getenv('SUPABASE_DB_POOL_PASSWORD'),
    port=os.getenv('SUPABASE_DB_POOL_PORT'),
)

cursor = connection.cursor()

location_mapping_insert_trigger_fn_sql = '''
CREATE OR REPLACE FUNCTION location_mapping_insert_trigger_fn()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
  INSERT INTO public.crimes (associated_id, general_location, natures_of_crime, date_time_occurred, date_reported)
  SELECT uc.associated_id, uc.general_location, uc.natures_of_crime, uc.date_time_occurred, uc.date_reported
  FROM public.unlinked_crimes uc
  WHERE uc.general_location = NEW.general_location
  ON CONFLICT (associated_id) DO NOTHING;

  DELETE FROM public.unlinked_crimes
  WHERE general_location = NEW.general_location;

  RETURN NEW;
END;
$$
'''

unlinked_crimes_insert_trigger_fn_sql = '''
CREATE OR REPLACE FUNCTION unlinked_crimes_insert_trigger_fn()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
  IF EXISTS (
    SELECT 1 FROM public.location_mapping lm
    WHERE lm.general_location = NEW.general_location
  ) THEN
    INSERT INTO public.crimes (associated_id, general_location, natures_of_crime, date_time_occurred, date_reported)
    VALUES (NEW.associated_id, NEW.general_location, NEW.natures_of_crime, NEW.date_time_occurred, NEW.date_reported)
    ON CONFLICT (associated_id) DO NOTHING;

    DELETE FROM public.unlinked_crimes uc WHERE associated_id = NEW.associated_id;

  END IF;
  RETURN NEW;
END;
$$
'''

cursor.execute(location_mapping_insert_trigger_fn_sql)
cursor.execute(unlinked_crimes_insert_trigger_fn_sql)
connection.commit()

cursor.close()
connection.close()

print('Functions successfully created.')
