import os
import mysql.connector


USE_WEBHOOK = True

test_group = os.getenv('test_group')
test_channel = os.getenv('test_channel')


if USE_WEBHOOK == False:
        from config_pooling import TOKEN, dbase
        TOKEN = TOKEN
        dbase = dbase

else:
        me = os.getenv('me')
        TOKEN = os.getenv('TOKEN')
        PROJECT_NAME = os.getenv('PROJECT_NAME')
        WEBHOOK_HOST = f'https://{PROJECT_NAME}.herokuapp.com'
        WEBHOOK_PATH = '/' + TOKEN
        WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"
        WEBAPP_HOST = '0.0.0.0'
        WEBAPP_PORT = os.environ.get('PORT')

        dbase = mysql.connector.connect(
                host=os.getenv('myhost'),
                user=os.getenv('myuser'),
                passwd=os.getenv('mypass'),
                port=os.getenv('port'),
                database=os.getenv('database') )



