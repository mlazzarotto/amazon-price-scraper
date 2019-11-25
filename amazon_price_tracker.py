import requests
import smtplib
import json
import os
import sys
import time
from random import randrange
from email.mime.text import MIMEText
from bs4 import BeautifulSoup

# TODO: add the possibility to check multiple Amazon items
# TODO: load the email account info from external file (not hard coded)


class AmazonItem:
    def __init__(self, name, url, desired_price):
        self.name = name
        self.url = url
        self.desired_price = desired_price

def get_user_agent():
    # Function that reads user agents from a json file
    try:
        with open(os.path.join(sys.path[0], 'user_agents.json')) as json_file:
            user_agents = json.load(json_file)
    except OSError as e:
        print('Cannot read the JSON file \n', e)
        sys.exit()

    return (user_agents[randrange(len(user_agents))]['useragent'])

def check_price(amazon_item):
    # Function that checks price
    time.sleep(randrange(0,15))

    headers = {"User-agent": get_user_agent()}

    page = requests.get(amazon_item.url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    try:
        price = soup.find(id="priceblock_ourprice").get_text()
    except AttributeError as e:
        print("Cannot get the title or price for the item, probably Amazon is showing a captcha\n", e)
        print('I\'ll try again in a few minutes')
        pass
    else:
        converted_price = float(price[0:6].replace(',', '.'))
        if (converted_price < amazon_item.desired_price):
            send_email(amazon_item, converted_price)
        
        print(amazon_item.name)
        print(converted_price)

def send_email(amazon_item, price):

    # Email sending function
    # @name = name of the item
    # @price = price of the item

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('***REMOVED***', '***REMOVED***')

    subject = 'The price for {} is {}'.format(amazon_item.name, price)
    body = 'Check it now on Amazon at link \n {}'.format(amazon_item.url)

    msg = "Subject: {} \n\n {}".format(subject, body)

    server.sendmail(
        # From
        '***REMOVED***',
        # To
        '***REMOVED***',
        msg
    )
    print('Hey! I\'ve just sent the email')
    server.quit()


items_list = []
items_list.append(AmazonItem('MI A3', 'https://www.amazon.it/Xiaomi-Mi-4GB-64GB-Version/dp/B07VD3JH2C', 155))
items_list.append(AmazonItem('Striscia LED Wifi BRLTX', 'https://www.amazon.it/BRTLX-Striscia-Impermeabile-intelligente-controllato/dp/B07KHX5T58', 23))
items_list.append(AmazonItem('Striscia LED Wifi Onforu', 'https://www.amazon.it/Onforu-Compatibile-Telecomando-Alimentatore-Illuminazione/dp/B07S15QLT7', 24))
items_list.append(AmazonItem('Striscia LED Wifi Bawoo', 'https://www.amazon.it/Impermeabile-Illuminazione-Bawoo-Assistant-Telecomando/dp/B078SNWRS4', 24))


while True:
    try:
        for item in items_list: 
            check_price(item)
    except:
        pass
    time.sleep(5 * 1)