# Import Dependencies
from notifiers import get_notifier
from re import sub

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

import sqlite3

import configparser

import time

import tweepy

# connection to SQL
conn = sqlite3.connect('tmp.sqlite3')
cur = conn.cursor()

# connect to config
config = configparser.ConfigParser()
config.read('config.ini')

# add user ID's and telegram token
TOKEN = config['telegram']['telegram_token']
USER_ID = config['telegram']['user_id']

telegram = get_notifier('telegram')

# tweepy add-ons, tokens and authentication
CONSUMER_KEY = config['twitter']['consumer_key']
CONSUMER_SECRET = config['twitter']['consumer_secret']
ACCESS_TOKEN = config['twitter']['access_token']
ACCESS_TOKEN_SECRET = config['twitter']['access_token_secret']

auth = tweepy.OAuth1UserHandler(
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET,
)
api = tweepy.API(auth)
user = cur.execute('SELECT screen_name FROM "username"').fetchone()[0]
cur.close()
username_object = api.get_user(screen_name=str(user))

# browser add-ons and options
options = webdriver.ChromeOptions()

options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")
options.add_argument("--headless")
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)

PATH = "chromedriver"
driver = webdriver.Chrome(executable_path=PATH, options=options)
wait = WebDriverWait(driver, 1)

# creating dynamic variables to store unique links to a tweet
previous_tweet = []
previous_message = []


# a function that start work with page user
def browser_start():
    return driver.get("https://twitter.com/" + str(user) + "/with_replies")


def expectant_element(elem):
    def reference_point():
        WebDriverWait(driver, 30).until(ec.presence_of_element_located((By.XPATH,
                                                                        '/html/body/div[1]/div/div/div[2]'
                                                                        '/main/div/div/div/div[1]/div/div[3]'
                                                                        '/div/div/section/div/div/div[1]'
                                                                        '/div/div/article/div/div/div[2]'
                                                                        '/div[2]/div[1]/div/div[1]/div/div/div[2]'
                                                                        '/div/div[3]/a')))
        element = elem()
        return element
    return reference_point


# a function that receives a new unique link to a tweet
@expectant_element
def get_tweet():
    current_link = driver.find_element(By.XPATH,
                                       "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]"
                                       "/div/div/section/div/div/div[1]/div/div/article/div/div/div[2]/div[2]"
                                       "/div[1]/div/div[1]/div/div/div[2]/div/div[3]/a").get_attribute('href')

    return current_link


# page refresh function
@expectant_element
def restart_page():

    return driver.refresh()


# function of asynchronously receiving the tweet text and sending the result to the telegram bot
def get_content_and_send_message():
    notification_about_tweet = f'️{user}⬇️'
    for i in api.user_timeline(user_id=username_object.id, screen_name=user, tweet_mode="extended", count=1):
        tweet_text = sub(r"https?://t.co[^,\s]+,?", "", i.full_text)
        if tweet_text not in previous_message:
            telegram.notify(token=TOKEN, chat_id=USER_ID, message=notification_about_tweet)
            telegram.notify(token=TOKEN, chat_id=USER_ID, message=tweet_text)
            previous_message.clear()
            previous_message.append(tweet_text)
            try:
                entities = i.extended_entities
                itr = entities['media']
                for img_dict in range(len(itr)):
                    telegram.notify(token=TOKEN, chat_id=USER_ID,
                                    message=(entities['media'][img_dict]['media_url_https']))
            except:
                pass


def timeit(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(time.time() - start)
        return result

    return wrapper()


# a key feature that checks the identity of unique links to a tweet
def filter_tweet(tweet_link):
    # comparison of the current tweet with the previous one by a unique link to the tweet
    if tweet_link not in previous_tweet[0]:
        previous_tweet.clear()
        get_content_and_send_message()
        previous_tweet.append(tweet_link)
    else:
        pass


def main_mechanism():
    filter_tweet(get_tweet())
    restart_page()


# start script
if __name__ == '__main__':
    browser_start()
    previous_tweet.append(get_tweet())

    for i in api.user_timeline(user_id=username_object.id, screen_name=user, tweet_mode="extended", count=1):
        tweet_text = sub(r"https?://t.co[^,\s]+,?", "", i.full_text)
        previous_message.append(tweet_text)

    # in this infinite loop, the program constantly implements a comparison using the filter_tweet function
    # and shows the time spent on this procedure
    # (optimally 3s)

    while True:
        timeit(main_mechanism)
