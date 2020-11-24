from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from pprint import pprint
import time

from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
db = client['letters']
collection_letters = db.collection_letters

mail_server = 'https://mail.ru/'
my_mail = 'study.ai_172@mail.ru'
password = 'NextPassword172'

chrome_options = Options()
chrome_options.add_argument('--headless')

driver = webdriver.Chrome(options=chrome_options)
driver.get(mail_server)

elem = driver.find_element_by_id('mailbox:login-input')
elem.send_keys(my_mail)
elem = driver.find_element_by_id('mailbox:submit-button')
elem.click()
elem = driver.find_element_by_id('mailbox:password-input')
elem.send_keys(password)
elem = driver.find_element_by_id('mailbox:submit-button')
elem.click()

driver.get('https://e.mail.ru/inbox')
links = set()
while True:
    len_start = len(links)
    time.sleep(3)
    actions = ActionChains(driver)
    mails = driver.find_elements_by_class_name('js-tooltip-direction_letter-bottom')
    for mail in mails:
        links.add(mail.get_attribute('href'))
    len_end = len(links)
    if len_start == len_end:
        break
    actions.move_to_element(mails[-1])
    actions.perform()

letters = []
for link in links:
    letter = {}
    driver.get(link)

    # time.sleep(3)

    letter_subject = WebDriverWait(driver, 10)
    letter_subject = letter_subject.until(
        EC.presence_of_element_located((By.CLASS_NAME, 'thread__subject'))
    )
    letter_subject = letter_subject.text

    letter_from = WebDriverWait(driver, 10)
    letter_from = letter_from.until(
        EC.presence_of_element_located((By.CLASS_NAME, 'letter-contact'))
    )
    letter_from = letter_from.text

    letter_email = WebDriverWait(driver, 10)
    letter_email = letter_email.until(
        EC.presence_of_element_located((By.CLASS_NAME, 'letter-contact'))
    )
    letter_email = letter_email.get_attribute('title')

    letter_date = WebDriverWait(driver, 10)
    letter_date = letter_date.until(
        EC.presence_of_element_located((By.CLASS_NAME, 'letter__date'))
    )
    letter_date = letter_date.text

    letter_text = WebDriverWait(driver, 10)
    letter_text = letter_text.until(
        EC.presence_of_element_located((By.CLASS_NAME, 'letter__body'))
    )
    letter_text = letter_text.text


    letter['letter_subject'] = letter_subject
    letter['letter_from'] = letter_from
    letter['letter_email'] = letter_email
    letter['letter_date'] = letter_date
    letter['letter_text'] = letter_text

    letters.append(letter)

pprint(letters)

collection_letters.insert_many(letters)