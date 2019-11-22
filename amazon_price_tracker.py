import requests
import smtplib
from random import randrange
from email.mime.text import MIMEText
from bs4 import BeautifulSoup

URL = 'https://www.amazon.it/Xiaomi-Mi-4GB-64GB-Version/dp/B07VD3JH2C'


def get_user_agent():
    # Funzione che prende una lista di user agents e ne ritorna uno casuale
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Safari/605.1.15',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36 OPR/64.0.3417.92']

    return user_agents[randrange(len(user_agents))]


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


check_price()
