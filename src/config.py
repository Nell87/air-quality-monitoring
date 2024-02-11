import os

# Accessing the supabase database/API configuration ... from environment variables
# Supabase parameters
dbparam = {
    'user': os.getenv('SUPABASE_AIRQUALITY_DB_USER'),
    'password': os.getenv('SUPABASE_AIRQUALITY_DB_PASSWORD'),
    'host': os.getenv('SUPABASE_AIRQUALITY_DB_HOST'),
    'dbname': os.getenv('SUPABASE_AIRQUALITY_DBNAME'),
    'port': os.getenv('SUPABASE_AIRQUALITY_DB_PORT')
}

# API token
token = os.getenv('AQI_API_TOKEN')

# List of cities 
cities = ['Barcelona', 'Madrid', 'Cadiz']

# String connection
connection_string = f"dbname={dbparam['dbname']} user={dbparam['user']} password={dbparam['password']} host={dbparam['host']} port={dbparam['port']}"

# MongoDB Connection
mongodbparam = {
    'user': os.getenv('MONGODB_AIRQUALITY_USER'),
    'password': os.getenv('MONGODB_AIRQUALITY_PASSWORD')
}


