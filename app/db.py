from config import *
import mysql.connector



db = mysql.connector.connect(
        host=os.getenv('myhost'),
        user=os.getenv('myuser'),
        passwd=os.getenv('mypass'),
        port="3306",
        database="eyefvtclr0ydnawm")



cursor = db.cursor()

