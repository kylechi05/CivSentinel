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

sql = '''
CREATE OR REPLACE FUNCTION reset_all_tables()
RETURNS void AS $$
DECLARE
    t RECORD;
BEGIN
    FOR t IN
        SELECT tablename
        FROM pg_tables
        WHERE schemaname = 'public'
    LOOP
        EXECUTE format('TRUNCATE TABLE %I RESTART IDENTITY CASCADE', t.tablename);
    END LOOP;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
'''

cursor.execute(sql)
connection.commit()

cursor.close()
connection.close()

print('Remote stored procedures successfully created.')
