import oracledb
from config import DB_HOST, DB_PASSWORD, DB_PORT, DB_SERVICE_NAME, DB_USER

# Database connection function
def get_db_connection():
    dsn = oracledb.makedsn(DB_HOST, DB_PORT, service_name=DB_SERVICE_NAME)
    return oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=dsn)

