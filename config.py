import os

# Accessing the database/API configuration from environment variables
dbparam = {
    'user': os.getenv('SUPABASE_AIRQUALITY_DB_USER'),
    'password': os.getenv('SUPABASE_AIRQUALITY_DB_PASSWORD'),
    'host': os.getenv('SUPABASE_AIRQUALITY_DB_HOST'),
    'dbname': os.getenv('SUPABASE_AIRQUALITY_DBNAME'),
    'port': os.getenv('SUPABASE_AIRQUALITY_DB_PORT')
}

token = os.getenv('AQI_API_TOKEN')

# List of cities 
cities = ['Barcelona', 'Madrid', 'Cadiz']

# String conection
connection_string = f"dbname={dbparam['dbname']} user={dbparam['user']} password={dbparam['password']} host={dbparam['host']} port={dbparam['port']}"

