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

location_mapping_insert_trigger_sql = '''
CREATE OR REPLACE TRIGGER location_mapping_insert_trigger
AFTER INSERT ON public.location_mapping
FOR EACH ROW
EXECUTE FUNCTION location_mapping_insert_trigger_fn();
'''

unlinked_crimes_insert_trigger_sql = '''
CREATE OR REPLACE TRIGGER unlinked_crimes_insert_trigger
AFTER INSERT ON public.unlinked_crimes
FOR EACH ROW
EXECUTE FUNCTION unlinked_crimes_insert_trigger_fn();
'''

cursor.execute(location_mapping_insert_trigger_sql)
cursor.execute(unlinked_crimes_insert_trigger_sql)
connection.commit()

cursor.close()
connection.close()

print('Triggers successfully created.')
