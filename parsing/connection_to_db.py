import MySQLdb
from settings import DB_HOST, DB_NAME, DB_USER, DB_PASSWD



conn = MySQLdb.connect(host=DB_HOST,
                     user=DB_USER,
                     passwd=DB_PASSWD,
                     db=DB_NAME)



cursor = conn.cursor()
cursor.execute("SELECT * FROM SPORTS")

res = cursor.fetchall()

cursor.close()

conn.close()
