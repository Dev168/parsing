import MySQLdb as mysql
from settings import DB_HOST, DB_NAME, DB_USER, DB_PASSWD


def database_init():
    """Инициализирует базу данных со всеми необходимыми таблицами
    Если база данных с именем DB_NAME уже существует то будет ошибка"""
    conn = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD)

    cursor = conn.cursor()

    with open("db/mysql_create.sql", "r") as f:
        sql_init_code = f.read().replace("DbNameTemplate", DB_NAME)

        cursor.execute(sql_init_code)
