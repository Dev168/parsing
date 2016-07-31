import os

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

PROXY = ["91.229.79.176:43395", "I5pOQeNRl6", "maxberezov@gmail.com"]

DB_HOST = "localhost"

DB_NAME = "betsdb"

DB_USER = "root"

DB_PASSWD = "1234"

LIVENSHTAIN_MIN = 0.35

LOAD_WAIT_TIME = 30

LOG_DIR = os.path.join(PROJECT_PATH, "logs")
