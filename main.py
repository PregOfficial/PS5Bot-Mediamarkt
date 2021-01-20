from selenium import webdriver
from bs4 import BeautifulSoup
import time
import requests
import sys

### Setup ###
user_email = "EMAIL"
user_password = "PASSWORD"
bot_token = ""
chat_id = ""
success_message = "Available!!"
refresh_rate = 5 # Seconds
##############

### Webdriver ###
#browser = webdriver.Firefox()
browser = webdriver.Chrome()
#################

browser.get('https://www.mediamarkt.at/de/myaccount/login?redirectURL=https://www.mediamarkt.at/checkout')
time.sleep(1)
username = browser.find_element_by_id('mms-login-form__email')
password = browser.find_element_by_id('mms-login-form__password')

username.clear()
password.clear()
username.send_keys(user_email)
password.send_keys(user_password)

browser.find_element_by_id('mms-login-form__login-button').click()

time.sleep(5)

while True:
    try:
        html_source = browser.page_source
        soup = BeautifulSoup(html_source)

        btn = str(soup.find('button', string="Zur Kasse gehen"))

        if 'disabled=""' not in btn:
            requests.get(f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id=@{chat_id}&text={success_message}')
        
        browser.refresh()
        time.sleep(refresh_rate)
    except KeyboardInterrupt:
        browser.stop_client()
        browser.close()
        sys.exit()

