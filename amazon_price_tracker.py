import requests
import smtplib
import json
import os
import sys
import time
from random import randrange
from email.mime.text import MIMEText
from bs4 import BeautifulSoup

URL = 'https://www.amazon.it/Xiaomi-Mi-4GB-64GB-Version/dp/B07VD3JH2C'


def get_user_agent():
    # Funzione che legge gli user agents da un file json
    with open(os.path.join(sys.path[0], 'user_agents.json')) as json_file:
        user_agents = json.load(json_file)

    return (user_agents[randrange(len(user_agents))]['useragent'])


def check_price():
    # Funzione che controlla il prezzo
    # Se il prezzo è minore di x, chiama il metodo send_email()
    headers = {"User-agent": get_user_agent()}

    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    title = soup.find(id="productTitle").get_text()
    price = soup.find(id="priceblock_ourprice").get_text()

    converted_price = float(price[0:6].replace(',', '.'))
    # print("Title is: {}".format(title.strip()))
    # print("Price is: {}".format(converted_price))

    if (converted_price < 1155):
        send_email(title.strip(), converted_price)

    print(title.strip())
    print(converted_price)


def send_email(title, price):

    # Funzione per l'invio di email
    # @title = titolo del oggetto da controllare
    # @price = prezzo dell'oggetto

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('***REMOVED***', '***REMOVED***')

    subject = 'Il prezzo di {} e\' {}'.format(title, price)
    body = 'Controlla subito su Amazon al link \n {}'.format(URL)

    msg = "Subject: {} \n\n {}".format(subject, body)

    server.sendmail(
        # From
        '***REMOVED***',
        # To
        '***REMOVED***',
        msg
    )
    print('EHI! HO SPEDITO L\'EMAIL')
    server.quit()


while True:
    check_price()
    time.sleep(5 * 60)