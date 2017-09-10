# coding: utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs
from dateutil import parser
import pytz

local_tz = pytz.timezone('UTC')

def get_transactions(driver, bank, pw, birthday):
    driver.get('https://obank.kbstar.com/quics?page=C025255&cc=b028364:b028702')
    submit_button = driver.find_element_by_css_selector('#pop_contents > div.btnArea > span > input[type="submit"]')
    driver.find_element_by_css_selector('#account_num').send_keys('{}'.format(bank))
    driver.find_element_by_css_selector('#비밀번호').send_keys('{}'.format(pw))
    driver.find_element_by_css_selector('#cond_user_num').click()
    driver.find_element_by_css_selector('#user_num').send_keys('{}'.format(birthday))
    driver.find_element_by_css_selector('#divPRO1 > span:nth-child(4) > input[type="button"]').click()
    submit_button.click()
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#pop_contents > table.tType01 > tbody > tr"))
        )
    finally:
        transactions = driver.find_elements_by_css_selector('#pop_contents > table.tType01 > tbody > tr')
    return transactions


def get_balance(PATH, bank, pw, birthday):
    # Developers TODO: Ie('') 안의 위치를 IEDriverServer.exe의 위치로 바꾸어주세요.
    # IE드라이버는 32bit버전을 받아 사용하세요. http://docs.seleniumhq.org/download/
    # 64bit 버전은 "매우매우" 느립니다.
    driver = webdriver.Ie(PATH)
    transactions = get_transactions(driver, bank, pw, birthday)
    transaction_list = []
    detail = {}
    for idx, value in enumerate(transactions):
        soup = bs(value.get_attribute('innerHTML'), 'html.parser')
        tds = soup.select('td')
        if not idx % 2:
            _date = tds[0].text
            _date = _date[:10] + ' ' + _date[10:]
            date = parser.parse(_date).replace(tzinfo=local_tz)  # 날짜: datetime
            amount = -int(tds[3].text.replace(',', '')) or int(tds[4].text.replace(',', ''))  # 입금 / 출금액: int
            balance = int(tds[5].text.replace(',', ''))  # 잔고: int
            detail = dict(date=date, amount=amount, balance=balance)
        else:
            transaction_by = tds[0].text.strip()  # 거래자(입금자 등): str
            tmp = dict(transaction_by=transaction_by)
            transaction_list.append({**detail, **tmp})
    driver.close()
    return transaction_list
