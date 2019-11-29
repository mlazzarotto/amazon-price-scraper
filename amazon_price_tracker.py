import requests
import smtplib
import json
import os
import sys
import time
from random import randrange
from bs4 import BeautifulSoup

class AmazonItem:
    def __init__(self, name, url, desired_price):
        self.name = name
        self.url = url
        self.desired_price = desired_price


def get_user_agent():
    """ Function that reads user agents from a json file
    The file name be 'user_agents.json'
    To get updated user agenst, visit https://techblog.willshouse.com/2012/01/03/most-common-user-agents
    """
    try:
        with open(os.path.join(sys.path[0], 'user_agents.json')) as json_file:
            user_agents = json.load(json_file)
    except OSError as e:
        print('Cannot read the user_agensts.json file \n', e)
        sys.exit()

    return (user_agents[randrange(len(user_agents))]['useragent'])


def check_price(amazon_item):
    """ Function that checks price
    Takes an AmazonItem instance as parameter
    """
    time.sleep(randrange(30))

    headers = {"User-agent": get_user_agent()}

    page = requests.get(amazon_item.url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    try:
        # price = soup.find(id="priceblock_ourprice").get_text()
        price = soup.find(id="priceblock_dealprice").get_text()
    except AttributeError:
        print("Cannot get the title or price for the item, probably Amazon is showing a captcha\n")
        pass
    else:
        converted_price = float(price[0:6].replace(',', '.'))
        if (converted_price < amazon_item.desired_price):
            send_email(amazon_item, converted_price)

        print(amazon_item.name)
        print(converted_price)


def send_email(amazon_item, price):
    """ Function that sends email
    amazon_item = name of the item from the AmazonItem class
    price = actual price of the item
    """
    # Trying to read JSON file
    try:
        with open(os.path.join(sys.path[0], 'settings.json')) as json_file:
            settings = json.load(json_file)
    except OSError as e:
        print('Cannot read the settings.json file \n', e)
        sys.exit()

    # # Email server settings taken from the JSON file
    email_settings_json = settings['email_settings']
    email_params = {}
    for p in email_settings_json[0]:
        email_params[p] = email_settings_json[0][p]

    # Establishing the connection with the smtp server
    server = smtplib.SMTP(email_params['smtp_server'], email_params['smtp_port'])
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(email_params['smtp_username'], email_params['smtp_password'])

    subject = 'The price for {} is {}'.format(amazon_item.name, price)
    body = 'Check it now on Amazon at link \n {}'.format(amazon_item.url)

    # Combining the subject and body to make the message
    msg = "Subject: {} \n\n {}".format(subject, body)

    server.sendmail(
        email_params['sender'],
        email_params['recipient'],
        msg
    )
    
    print('Hey! I\'ve just sent the email')
    server.quit()
    json_file.close()


# List of Amazon items to check
items_list = []
items_list.append(AmazonItem(
    'MI A3', 'https://www.amazon.it/Xiaomi-Mi-4GB-64GB-Version/dp/B07VD3JH2C', 1550))
items_list.append(AmazonItem('Striscia LED Wifi BRLTX',
                             'https://www.amazon.it/BRTLX-Striscia-Impermeabile-intelligente-controllato/dp/B07KHX5T58', 230))
items_list.append(AmazonItem('Striscia LED Wifi Onforu',
                             'https://www.amazon.it/Onforu-Compatibile-Telecomando-Alimentatore-Illuminazione/dp/B07S15QLT7', 240))
items_list.append(AmazonItem('Striscia LED Wifi Bawoo',
                             'https://www.amazon.it/Impermeabile-Illuminazione-Bawoo-Assistant-Telecomando/dp/B078SNWRS4', 240))

# I try to check the prices
while True:    
    try:
        for item in items_list:
            check_price(item)
    except:
        pass
    time.sleep(0)