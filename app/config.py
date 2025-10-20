from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SQLITE_PATH = BASE_DIR / 'sqlite3.db'
SCHEMA_PATH = BASE_DIR / 'schema.sql'


class Config:
    API_TITLE = 'BadAuth API'
    API_VERSION = 'v1'
    OPENAPI_VERSION = '3.1.1'
    OPENAPI_URL_PREFIX = '/api/v1'
    OPENAPI_SWAGGER_UI_PATH = '/docs'
    OPENAPI_SWAGGER_UI_URL = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'
    
