# Import Dependencies
from os import system
from time import sleep
from notifiers import get_notifier

import configparser
import sqlite3

# connect to config
config = configparser.ConfigParser()
config.read('config.ini')

# add user ID's and telegram token
TOKEN = config['telegram']['telegram_token']
USER_ID = config['telegram']['user_id']
ADMIN_ID = config['telegram']['admin_id']

# connect to SQL
connection = sqlite3.connect('tmp.sqlite3')
cur = connection.cursor()

USERNAME_TWITTER = str(input('Enter username (example: "https://twitter.com/elonmusk", you need to enter "elonmusk")\n>>>'))
# create table if it doesn't exist
cur.execute('CREATE TABLE IF NOT EXISTS username(screen_name TEXT)')

# select the current value, if any
cur.execute('SELECT screen_name FROM username LIMIT 1')
result = cur.fetchone()

if result is not None:
    # update the value in the database if it already exists
    cur.execute('UPDATE username SET screen_name = ? WHERE rowid = 1', (USERNAME_TWITTER,))
else:
    # insert new value if not
    cur.execute('INSERT INTO username(screen_name) VALUES (?)', (USERNAME_TWITTER,))

# save changes to the database
connection.commit()

# select value from database
user = cur.execute('SELECT screen_name FROM username').fetchone()[0]

connection.close()

# designate which messenger we will use for notifications
telegram = get_notifier('telegram')

if __name__ in '__main__':
    while True:

        # we go into an infinite loop by calling the parser script
        system('python3 scraping_tweets.py')

        # configure a message about which particular user goes to reload
        # (in case of an error in parsing, which mainly occurs due to a
        # decrease in the connection speed with the server)

        notification_about_error = f'[INFO] script is paused... restart through 1 min ({str(user)})'

        # sending messages to the assigned user of this program in the telegram bot
        telegram.notify(token=TOKEN, chat_id=USER_ID, message=notification_about_error)
        telegram.notify(token=TOKEN, chat_id=ADMIN_ID, message=notification_about_error)

        sleep(60)
