import MySQLdb as mysql
from settings import DB_HOST, DB_NAME, DB_USER, DB_PASSWD


def init():
    """Инициализирует базу данных со всеми необходимыми таблицами
    Если база данных с именем DB_NAME уже существует то будет ошибка"""
    conn = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD)

    cursor = conn.cursor()

    sql_code = "CREATE DATABASE IF NOT EXISTS {0}; USE {0}".format(DB_NAME)

    cursor.execute(sql_code)

    with open("db/mysql_create.sql", "r") as f:

        sql_init_code = f.read()

        cursor.execute(sql_init_code)

        print("База данных успешно инициализирована")

        conn.close()


def create_bookmaker(bookmaker_name):
    """Создает нового букмекера"""
    conn = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME)

    cursor = conn.cursor()

    sql_code = 'INSERT INTO bookmakers (Name) VALUES ("{0}")'.format(bookmaker_name)

    try:
        cursor.execute(sql_code)
        conn.commit()
        print("{0} контора успешно создана".format(bookmaker_name))
    except mysql.IntegrityError as err:
        print(err)

    conn.close()

