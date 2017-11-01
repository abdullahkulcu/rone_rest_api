from flask import Flask

ENV = "DEV"
NLU_USER = ""
NLU_PASS = ""
TONE_USER = ""
TONE_PASS = ""
GOOGLE_TRANSLATE = ""

### DEVELOPMENT ###

DEV_PORT = 9000
DEV_DEBUG = True
DEV_HOST = 'localhost'
DEV_GEOIP_URL = ''
DEV_GEOIP_PORT = '9092'

### PRODUCTION ###

PROD_PORT = 8080
PROD_DEBUG = False
PROD_HOST = '0.0.0.0'
PROD_GEOIP_URL = ''
PROD_GEOIP_PORT = '9092'
DB_USER_NAME = "admin"
DB_PASSWORD = ""
DB_HOST = ""
DB_PORT = 18539
DB_SSL = True
DB_CERT_FILE = 'cert.crt'

app = Flask(__name__)
