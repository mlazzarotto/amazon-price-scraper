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
# TODO: add check if Amazon shows the captcha
# TODO: 


URL = 'https://www.amazon.it/Xiaomi-Mi-4GB-64GB-Version/dp/B07VD3JH2C'


def get_user_agent():
    # Function that reads user agents from a json file
    try:
        with open(os.path.join(sys.path[0], 'user_agents.json')) as json_file:
            user_agents = json.load(json_file)
    except:
        print ('Cannot read the JSON file')

    return (user_agents[randrange(len(user_agents))]['useragent'])


def check_price():
    # Function that checks price
    headers = {"User-agent": get_user_agent()}

    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    try:
        title = soup.find(id="productTitle").get_text()
        price = soup.find(id="priceblock_ourprice").get_text()
    except:
        print("Cannot get the title or price for the item")
        sys.exit()


    converted_price = float(price[0:6].replace(',', '.'))

    if (converted_price < 1155):
        send_email(title.strip(), converted_price)

    print(title.strip())
    print(converted_price)


def send_email(title, price):

    # Email sending function
    # @title = title of the item
    # @price = price of the item

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('***REMOVED***', '***REMOVED***')

    subject = 'The price for {} is {}'.format(title, price)
    body = 'Check it now on Amazon at link \n {}'.format(URL)

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


while True:
    check_price()
    time.sleep(5 * 60)