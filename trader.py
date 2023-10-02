from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numpy as np
import re
import time
import pickle
from selenium.webdriver.common.keys import Keys
import sys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import ElementNotInteractableException

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager



def create_cookies():
    driver = webdriver.Firefox(
        executable_path="../FUT_BOT/geckodriver")
    driver.get("https://www.ea.com/ea-sports-fc/ultimate-team/web-app/")
    foo = input()
    pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))

def load_cookie(driver, path):
    with open(path, 'rb') as cookiesfile:
        cookies = pickle.load(cookiesfile)
        for cookie in cookies:
            driver.add_cookie(cookie)

def attempt_click_xpath(xpath, driver):
    btn = None
    attempts = 0
    while attempts < 5:
        try:
            btn = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, xpath)))
            btn.click()
            attempts = 0
            break
        except (ElementClickInterceptedException, StaleElementReferenceException, NoSuchElementException):
            pass
        attempts = attempts + 1

    return btn


def attempt_click_css(css, driver):
    btn = None
    attempts = 0
    while attempts < 5:
        try:
            btn = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, css)))
            btn.click()
            attempts = 0
            break
        except (ElementClickInterceptedException, StaleElementReferenceException, NoSuchElementException):
            pass
        attempts = attempts + 1

    return btn


def unassigned_items(css, driver):

    attempts = 0
    while attempts < 2:
        try:
            unassigned = WebDriverWait(driver, 0.3).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, css)))
            unassigned.click()
            return True
        except (NoSuchElementException, TimeoutException):
            pass
        attempts = attempts + 1
    return False

def check_exists_by_css(css,driver):
    time.sleep(2)
    try:
        elem = driver.find_element(By.CSS_SELECTOR,css)
    except NoSuchElementException:
        return False

    if elem.get_attribute("style") == "display: none;":
        return False

    return True

if __name__ == "__main__":



    email = sys.argv[1]
    passw = sys.argv[2]


    options = webdriver.ChromeOptions()

    # options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # options = Options()
    # options.headless = True
    # driver = webdriver.Firefox(options=options, executable_path=GeckoDriverManager().install())
    # driver = webdriver.Chrome(
    #     executable_path="/Users/andreas/desktop/FUT_BOT/chromedriver")
    driver.get("https://www.ea.com/ea-sports-fc/ultimate-team/web-app/")

    load_cookie(driver, "cookies.pkl")

    driver.get("https://www.ea.com/ea-sports-fc/ultimate-team/web-app/")

    login_btn = attempt_click_xpath(
        '/html/body/main/div/div/div/button[1]', driver)  # Login btn

    email_input = attempt_click_xpath('//*[@id="email"]', driver)

    email_input.send_keys(email)

    passw_input = attempt_click_xpath('//*[@id="password"]', driver)
    passw_input.send_keys(passw)

    attempt_click_xpath('//*[@id="logInBtn"]', driver)

    attempt_click_css("body > main > section > nav > button.ut-tab-bar-item.icon-transfer",driver)
    time.sleep(0.3)
    attempt_click_css("body > main > section > section > div.ut-navigation-container-view--content > div > div > div.tile.ut-tile-view--with-gfx.col-2-3-md.col-1-1.ut-tile-transfer-market > div.tileContent",driver)
    time.sleep(0.3)
    attempt_click_css("body > main > section > section > div.ut-navigation-container-view--content > div > div.ea-filter-bar-view > div > button:nth-child(4)",driver)
    time.sleep(0.3)
    attempt_click_css("body > main > section > section > div.ut-navigation-container-view--content > div > div.ut-pinned-list-container.ut-content-container > div > div.ut-pinned-list > div.ut-item-search-view > div:nth-child(2) > div",driver)
    time.sleep(0.3)
    attempt_click_css("body > main > section > section > div.ut-navigation-container-view--content > div > div.ut-pinned-list-container.ut-content-container > div > div.ut-pinned-list > div.ut-item-search-view > div.inline-list-select.ut-search-filter-control.has-image.is-open > div > ul > li:nth-child(2)",driver)
    time.sleep(0.3)
    attempt_click_css("body > main > section > section > div.ut-navigation-container-view--content > div > div.ut-pinned-list-container.ut-content-container > div > div.ut-pinned-list > div.ut-item-search-view > div:nth-child(2) > div",driver)
    time.sleep(0.3)
    attempt_click_css("body > main > section > section > div.ut-navigation-container-view--content > div > div.ut-pinned-list-container.ut-content-container > div > div.ut-pinned-list > div.ut-item-search-view > div.inline-list-select.ut-search-filter-control.has-image.is-open > div > ul > li:nth-child(1)",driver)
    time.sleep(0.3)
    attempt_click_css("body > main > section > section > div.ut-navigation-container-view--content > div > div.ut-pinned-list-container.ut-content-container > div > div.ut-pinned-list > div.ut-item-search-view > div:nth-child(4) > div",driver)
    time.sleep(0.3)
    attempt_click_css("body > main > section > section > div.ut-navigation-container-view--content > div > div.ut-pinned-list-container.ut-content-container > div > div.ut-pinned-list > div.ut-item-search-view > div.inline-list-select.ut-search-filter-control.has-default.has-image.is-open > div > ul > li:nth-child(20)",driver)
    time.sleep(0.3)
    

    lowest_price = 3300
    changePriceBit = 0
    while True:
        price_input = attempt_click_css("body > main > section > section > div.ut-navigation-container-view--content > div > div.ut-pinned-list-container.ut-content-container > div > div.ut-pinned-list > div.search-prices > div:nth-child(6) > div.ut-numeric-input-spinner-control > input",driver)
        time.sleep(0.1)
        price_input.send_keys(Keys.BACK_SPACE)
        time.sleep(0.1)
        price_input.send_keys(lowest_price-(100*changePriceBit))


        attempt_click_css("body > main > section > section > div.ut-navigation-container-view--content > div > div.ut-pinned-list-container.ut-content-container > div > div.button-container > button.btn-standard.call-to-action",driver)

        if check_exists_by_css("body > main > section > section > div.ut-navigation-container-view--content > div > div > section > div > div.ut-no-results-view > div",driver):
            attempt_click_css("body > main > section > section > div.ut-navigation-bar-view.navbar-style-landscape.currency-purchase > button.ut-navigation-button-control",driver)
        else:
            attempt_click_css("body > main > section > section > div.ut-navigation-container-view--content > div > div > section.ut-navigation-container-view.ui-layout-right > div > div > div.DetailPanel > div.bidOptions > button.btn-standard.buyButton.currency-coins",driver)
            attempt_click_css("body > div.view-modal-container.form-modal > section > div > div > button:nth-child(1)",driver)
            attempt_click_css("body > main > section > section > div.ut-navigation-bar-view.navbar-style-landscape.currency-purchase > button.ut-navigation-button-control",driver)
        if changePriceBit == 0:
            changePriceBit = 1
        else:
            changePriceBit = 0