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
from selenium.common.exceptions import TimeoutException


def create_cookies():
    driver = webdriver.Chrome(
        executable_path="/Users/andreas/desktop/FUT_BOT/chromedriver")
    driver.get("https://www.ea.com/nb-no/fifa/ultimate-team/web-app/")
    foo = input()
    save_cookie(driver, 'cookies.pkl')


def save_cookie(driver, path):
    with open(path, 'wb') as filehandler:
        pickle.dump(driver.get_cookies(), filehandler)


def load_cookie(driver, path):
    with open(path, 'rb') as cookiesfile:
        cookies = pickle.load(cookiesfile)
        for cookie in cookies:
            driver.add_cookie(cookie)


def main():

    quick_sell_disabled = False

    if len(sys.argv) == 3:
        mode = sys.argv[1]
        sbcType = sys.argv[2]

    else:
        mode = sys.argv[1]

    driver = webdriver.Chrome(
        executable_path="/Users/andreas/desktop/FUT_BOT/chromedriver")

    driver.get("https://www.ea.com/nb-no/fifa/ultimate-team/web-app/")

    login = input()

    tot_n_packs = 0
    tot_profit = 0
    tot_players_sent_to_club = 0
    results = open("results.txt", "a")
    if mode == "bpmn":

        while True:

            pack_quick_sell = 0
            pack_item_income = 0
            players_sent_to_club = 0
            attempts = 0
            while attempts < 2:
                try:
                    attempts = 0
                    while attempts < 2:
                        try:
                            storeBtn = WebDriverWait(driver, 20).until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, "body > main > section > nav > button.ut-tab-bar-item.icon-store")))
                            storeBtn.click()
                            attempts = 0
                            break
                        except (ElementClickInterceptedException, StaleElementReferenceException):
                            pass
                        attempts = attempts + 1

                    attempts = 0
                    while attempts < 2:
                        try:
                            mainPackBtn = WebDriverWait(driver, 20).until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, "body > main > section > section > div.ut-navigation-container-view--content > div > div > div.tile.ut-tile-view--with-gfx.col-1-2.packs-tile.storehub-tile")))
                            mainPackBtn.click()
                            attempts = 0
                            break
                        except (ElementClickInterceptedException, StaleElementReferenceException):
                            pass
                        attempts = attempts + 1

                    while attempts < 2:
                        try:
                            classicPackBtn = WebDriverWait(driver, 20).until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, "body > main > section > section > div.ut-navigation-container-view--content > div > div.ea-filter-bar-view > div > button:nth-child(2)")))

                            if classicPackBtn.text != "KLASSISKE PAKKER":
                                classicPackBtn = WebDriverWait(driver, 20).until(
                                    EC.element_to_be_clickable((By.CSS_SELECTOR, "body > main > section > section > div.ut-navigation-container-view--content > div > div.ea-filter-bar-view > div > button:nth-child(3)")))
                                if classicPackBtn.text != "KLASSISKE PAKKER":
                                    classicPackBtn = WebDriverWait(driver, 20).until(
                                        EC.element_to_be_clickable((By.CSS_SELECTOR, "body > main > section > section > div.ut-navigation-container-view--content > div > div.ea-filter-bar-view > div > button:nth-child(4)")))
                            classicPackBtn.click()
                            attempts = 0
                            break
                        except (ElementClickInterceptedException, StaleElementReferenceException):
                            pass
                        attempts = attempts + 1

                    while attempts < 2:
                        try:
                            buyBtn = WebDriverWait(driver, 20).until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, "body > main > section > section > div.ut-navigation-container-view--content > div > div.ut-store-hub-view--content > div:nth-child(2) > div.ut-store-pack-details-view--footer > button")))
                            buyBtn.click()
                            okBtn = WebDriverWait(driver, 20).until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.view-modal-container.form-modal > section > div > div > button:nth-child(1)")))
                            okBtn.click()
                            ulElem = WebDriverWait(driver, 20).until(
                                EC.element_to_be_clickable((By.XPATH, "/html/body/main/section/section/div[2]/div/div/section[1]/section[1]/ul")))
                            all_li_elements = ulElem.find_elements_by_tag_name(
                                "li")
                            attempts = 0
                            break
                        except (ElementClickInterceptedException, StaleElementReferenceException):
                            pass
                        attempts = attempts + 1
                    attempts = 0
                    break
                except TimeoutException:
                    pass
                attempts = attempts + 1

            # time.sleep(0.3)
            pack_items = []

            for li in all_li_elements:
                class_name = li.get_attribute("class")
                class_name = class_name.replace(" ", "")
                if len(class_name) > 1:
                    pack_items.append(li)
                    tmp = li.text
                    tmp = tmp.replace("\n", "")

            # SELL DUPLICATES

            if len(pack_items) < 12:

                dup_ulElem = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "/html/body/main/section/section/div[2]/div/div/section[1]/section[2]/ul")))

                dup_li_elements = dup_ulElem.find_elements_by_tag_name("li")

                # time.sleep(0.3)
                dup_pack_items = []

                for li in dup_li_elements:

                    class_name = li.get_attribute("class")

                    class_name = class_name.replace(" ", "")
                    if len(class_name) > 1:
                        dup_pack_items.append(li)
                        tmp = li.text
                        tmp = tmp.replace("\n", "")

                counter_dup = 1
                for i in dup_pack_items:

                    attempts = 0
                    while attempts < 2:
                        try:
                            item = driver.find_element_by_xpath(
                                "/html/body/main/section/section/div[2]/div/div/section[1]/section[2]/ul/li")
                            time.sleep(0.5)
                            itemtype = item.find_element_by_xpath(
                                "/html/body/main/section/section/div[2]/div/div/section[1]/section[2]/ul/li/div/div[1]/div[1]").get_attribute("class")
                            item.click()
                            attempts = 0
                            break
                        except StaleElementReferenceException:
                            pass

                        attempts = attempts + 1

                    if itemtype == "small player item rare ut-item-loaded" or itemtype == "small player item common ut-item-loaded" or itemtype == "small manager staff item common ut-item-loaded" or itemtype == "small manager staff item rare ut-item-loaded" or itemtype == "small player item specials ut-item-loaded":
                        # time.sleep(0.2)
                        comparePrice = WebDriverWait(driver, 20).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, "body > main > section > section > div.ut-navigation-container-view--content > div > div > section.ut-navigation-container-view.ui-layout-right > div.ut-navigation-container-view--content > div > div.DetailPanel > div.ut-button-group > button:nth-child(9)")))
                        comparePrice.click()

                        time.sleep(0.2)

                        lowestPrice = 100000
                        items = []
                        attempts = 0
                        while len(items) < 1 and attempts < 4:
                            priceList = driver.find_element_by_xpath(
                                "/html/body/main/section/section/div[2]/div/div/section[2]/div[2]/section/div[2]/ul")
                            time.sleep(0.5)
                            items = priceList.find_elements_by_tag_name("li")
                            attempts = attempts + 1

                        for i in items:

                            txt = i.text
                            tmp = txt.split("\n")
                            if len(tmp) > 1:
                                # print("------------------------------------------")
                                # print(txt)
                                if itemtype == "small manager staff item common ut-item-loaded" or itemtype == "small manager staff item rare ut-item-loaded":
                                    price = tmp[7]
                                else:
                                    if len(tmp) == 11:
                                        price = tmp[8]
                                    elif len(tmp) == 9:
                                        price = tmp[6]

                                price = str(price)
                                price = price.replace(" ", "")
                                price = int(price)
                                # print("pris:", price)
                                if price == 200:
                                    lowestPrice = price
                                    break
                                if price < lowestPrice:
                                    lowestPrice = price

                            # print("------------------------------------------")

                        # time.sleep(0.2)
                        backBtn = WebDriverWait(driver, 20).until(
                            EC.element_to_be_clickable((By.XPATH, "/html/body/main/section/section/div[2]/div/div/section[2]/div[1]/button")))

                        backBtn.click()
                        # time.sleep(0.2)
                        if lowestPrice < 300:
                            attempts = 0
                            while attempts < 2:
                                try:
                                    send_to_club = WebDriverWait(driver, 20).until(
                                        EC.element_to_be_clickable((By.XPATH, "/html/body/main/section/section/div[2]/div/div/section[2]/div[2]/div/div[2]/div[3]/button[6]")))
                                    attempts = 0
                                    send_to_club_tag = send_to_club.text
                                    break
                                except StaleElementReferenceException:
                                    pass
                                attempts = attempts + 1

                            if send_to_club_tag == "Bytt dublett fra klubb":
                                if quick_sell_disabled:
                                    list_on_market = WebDriverWait(driver, 20).until(
                                        EC.element_to_be_clickable((By.XPATH, "/html/body/main/section/section/div[2]/div/div/section[2]/div[2]/div/div[2]/div[2]/div[1]/button")))
                                    list_on_market.click()
                                    sell_price_input = WebDriverWait(driver, 20).until(
                                        EC.element_to_be_clickable((By.XPATH, "/html/body/main/section/section/div[2]/div/div/section[2]/div[2]/div/div[2]/div[2]/div[2]/div[3]/div[2]/input")))

                                    sell_price_input.click()
                                    for i in range(6):
                                        time.sleep(0.1)
                                        sell_price_input.send_keys(
                                            Keys.BACK_SPACE)

                                    # print(lowestPrice)
                                    sell_price_input.send_keys(str(200))
                                    confirm_sell = WebDriverWait(driver, 20).until(
                                        EC.element_to_be_clickable((By.XPATH, "/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[2]/div[2]/button")))

                                    confirm_sell.click()
                                    # time.sleep(0.2)

                                else:
                                    attempts = 0
                                    while attempts < 2:
                                        try:
                                            quick_sell = WebDriverWait(driver, 20).until(
                                                EC.element_to_be_clickable((By.CSS_SELECTOR, "body > main > section > section > div.ut-navigation-container-view--content > div > div > section.ut-navigation-container-view.ui-layout-right > div > div > div.DetailPanel > div.ut-button-group > button:nth-child(10)")))

                                            quick_sell_price = quick_sell.find_element_by_css_selector(
                                                "body > main > section > section > div.ut-navigation-container-view--content > div > div > section.ut-navigation-container-view.ui-layout-right > div > div > div.DetailPanel > div.ut-button-group > button:nth-child(10) > span.btn-subtext.currency-coins").text
                                            quick_sell_price = int(
                                                quick_sell_price)
                                            pack_quick_sell = pack_quick_sell + quick_sell_price
                                            quick_sell.click()
                                            quick_sell_confirm = WebDriverWait(driver, 20).until(
                                                EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.view-modal-container.form-modal > section > div > div > button:nth-child(1)")))
                                            quick_sell_confirm.click()
                                            attempts = 0
                                            break
                                        except (ElementClickInterceptedException, StaleElementReferenceException):
                                            pass
                                        attempts = attempts + 1

                                    # time.sleep(0.2)

                            else:
                                attempts = 0
                                while attempts < 2:
                                    try:
                                        send_to_club.click()
                                        attempts = 0
                                        break
                                    except (ElementClickInterceptedException, StaleElementReferenceException):
                                        pass
                                    attempts = attempts + 1

                        else:
                            attempts = 0
                            while attempts < 2:
                                try:
                                    list_on_market = WebDriverWait(driver, 20).until(
                                        EC.element_to_be_clickable((By.XPATH, "/html/body/main/section/section/div[2]/div/div/section[2]/div[2]/div/div[2]/div[2]/div[1]/button")))
                                    list_on_market.click()
                                    sell_price_input = WebDriverWait(driver, 20).until(
                                        EC.element_to_be_clickable((By.XPATH, "/html/body/main/section/section/div[2]/div/div/section[2]/div[2]/div/div[2]/div[2]/div[2]/div[3]/div[2]/input")))
                                    sell_price_input.click()
                                    attempts = 0
                                    break
                                except (ElementClickInterceptedException, StaleElementReferenceException):
                                    pass
                                attempts = attempts + 1

                            for i in range(6):
                                time.sleep(0.1)
                                sell_price_input.send_keys(Keys.BACK_SPACE)

                            # print(lowestPrice)
                            sell_price_input.send_keys(str(lowestPrice-100))

                            confirm_sell = WebDriverWait(driver, 20).until(
                                EC.element_to_be_clickable((By.XPATH, "/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[2]/div[2]/button")))
                            confirm_sell.click()

                            if lowestPrice == 100000 and (itemtype == "small player item rare ut-item-loaded" or itemtype == "small player item common ut-item-loaded"):
                                pack_item_income = pack_item_income + 10000
                            elif lowestPrice == 100000 and (itemtype == "small manager staff item common ut-item-loaded" or itemtype == "small manager staff item rare ut-item-loaded"):
                                pack_item_income = pack_item_income + 5000
                            else:
                                pack_item_income = pack_item_income + lowestPrice-100
                            # time.sleep(0.2)
                    else:
                        attempts = 0
                        while attempts < 2:
                            try:
                                quick_sell = WebDriverWait(driver, 20).until(
                                    EC.element_to_be_clickable((By.CSS_SELECTOR, "body > main > section > section > div.ut-navigation-container-view--content > div > div > section.ut-navigation-container-view.ui-layout-right > div > div > div.DetailPanel > div.ut-button-group > button:nth-child(10)")))
                                quick_sell_price = quick_sell.find_element_by_css_selector(
                                    "body > main > section > section > div.ut-navigation-container-view--content > div > div > section.ut-navigation-container-view.ui-layout-right > div > div > div.DetailPanel > div.ut-button-group > button:nth-child(10) > span.btn-subtext.currency-coins").text
                                quick_sell_price = int(
                                    quick_sell_price)
                                pack_quick_sell = pack_quick_sell + quick_sell_price
                                quick_sell.click()
                                quick_sell_confirm = WebDriverWait(driver, 20).until(
                                    EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.view-modal-container.form-modal > section > div > div > button:nth-child(1)")))
                                quick_sell_confirm.click()
                                attempts = 0
                                break
                            except (ElementClickInterceptedException, StaleElementReferenceException):
                                pass
                            attempts = attempts + 1
                        # time.sleep(0.3)

            counter = 1

            # SELLING NOT DUPLICATE ITEMS
            for i in range(len(pack_items)):
                attempts = 0
                while attempts < 2:
                    try:
                        item = driver.find_element_by_xpath("/html/body/main/section/section/div[2]/div/div/section[1]/section/ul/li["+str(
                            counter) + "]")
                        time.sleep(0.5)
                        itemtype = driver.find_element_by_xpath(
                            "/html/body/main/section/section/div[2]/div/div/section[1]/section/ul/li["+str(counter)+"]/div/div[1]/div[1]").get_attribute("class")
                        item.click()
                        attempts = 0
                        break
                    except (ElementClickInterceptedException, StaleElementReferenceException):
                        pass

                    attempts = attempts + 1

                # print(itemtype)
                if itemtype == "small misc item common" or itemtype == "small misc item rare":

                    # time.sleep(0.3)
                    cash_in = WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "body > main > section > section > div.ut-navigation-container-view--content > div > div > section.ut-navigation-container-view.ui-layout-right > div.ut-navigation-container-view--content > div > div.DetailPanel > div.ut-button-group > button:nth-child(2)")))

                    pack_item_income = pack_item_income + 100
                    cash_in.click()
                    counter = counter - 1

                elif itemtype == "small player item rare ut-item-loaded" or itemtype == "small player item common ut-item-loaded" or itemtype == "small manager staff item common ut-item-loaded" or itemtype == "small manager staff item rare ut-item-loaded" or itemtype == "small player item specials ut-item-loaded":

                    # time.sleep(0.2)
                    comparePrice = WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "body > main > section > section > div.ut-navigation-container-view--content > div > div > section.ut-navigation-container-view.ui-layout-right > div.ut-navigation-container-view--content > div > div.DetailPanel > div.ut-button-group > button:nth-child(9)")))
                    comparePrice.click()

                    time.sleep(0.2)

                    items = []
                    lowestPrice = 100000
                    attempts = 0
                    while len(items) < 1 and attempts < 4:
                        priceList = driver.find_element_by_xpath(
                            "/html/body/main/section/section/div[2]/div/div/section[2]/div[2]/section/div[2]/ul")
                        time.sleep(0.3)
                        items = priceList.find_elements_by_tag_name("li")
                        attempts = attempts + 1

                    for i in items:

                        txt = i.text
                        tmp = txt.split("\n")
                        if len(tmp) > 1:
                            # print("------------------------------------------")
                            # print(txt)
                            if itemtype == "small manager staff item common ut-item-loaded" or itemtype == "small manager staff item rare ut-item-loaded":
                                price = tmp[7]
                            else:
                                if len(tmp) == 11:
                                    price = tmp[8]
                                elif len(tmp) == 9:
                                    price = tmp[6]
                            price = price.replace(" ", "")
                            price = int(price)
                            # print("pris:", price)
                            if price == 200:
                                lowestPrice = price
                                break
                            if price < lowestPrice:
                                lowestPrice = price

                        # print("------------------------------------------")

                    # time.sleep(0.3)
                    attempts = 0
                    while attempts < 2:
                        try:
                            backBtn = WebDriverWait(driver, 20).until(
                                EC.element_to_be_clickable((By.XPATH, "/html/body/main/section/section/div[2]/div/div/section[2]/div[1]/button")))
                            backBtn.click()
                            attempts = 0
                            break
                        except (ElementClickInterceptedException, StaleElementReferenceException):
                            pass
                        attempts = attempts + 1
                    # time.sleep(0.4)
                    if lowestPrice < 300:
                        attempts = 0
                        while attempts < 2:
                            try:
                                send_to_club = WebDriverWait(driver, 20).until(
                                    EC.element_to_be_clickable((By.XPATH, "/html/body/main/section/section/div[2]/div/div/section[2]/div[2]/div/div[2]/div[3]/button[6]")))
                                send_to_club_tag = send_to_club.text
                                attempts = 0
                                break
                            except StaleElementReferenceException:
                                pass
                            attempts = attempts + 1

                        if send_to_club_tag == "Bytt dublett fra klubb":
                            if quick_sell_disabled:
                                list_on_market = WebDriverWait(driver, 20).until(
                                    EC.element_to_be_clickable((By.XPATH, "/html/body/main/section/section/div[2]/div/div/section[2]/div[2]/div/div[2]/div[2]/div[1]/button")))
                                list_on_market.click()
                                sell_price_input = WebDriverWait(driver, 20).until(
                                    EC.element_to_be_clickable((By.XPATH, "/html/body/main/section/section/div[2]/div/div/section[2]/div[2]/div/div[2]/div[2]/div[2]/div[3]/div[2]/input")))

                                sell_price_input.click()
                                for i in range(6):
                                    time.sleep(0.1)
                                    sell_price_input.send_keys(Keys.BACK_SPACE)

                                # print(lowestPrice)
                                sell_price_input.send_keys(str(200))
                                confirm_sell = WebDriverWait(driver, 20).until(
                                    EC.element_to_be_clickable((By.XPATH, "/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[2]/div[2]/button")))

                                confirm_sell.click()
                                # time.sleep(0.3)
                                counter = counter - 1

                            else:
                                attempts = 0
                                while attempts < 2:
                                    try:
                                        quick_sell = WebDriverWait(driver, 20).until(
                                            EC.element_to_be_clickable((By.CSS_SELECTOR, "body > main > section > section > div.ut-navigation-container-view--content > div > div > section.ut-navigation-container-view.ui-layout-right > div > div > div.DetailPanel > div.ut-button-group > button:nth-child(10)")))
                                        quick_sell_price = quick_sell.find_element_by_css_selector(
                                            "body > main > section > section > div.ut-navigation-container-view--content > div > div > section.ut-navigation-container-view.ui-layout-right > div > div > div.DetailPanel > div.ut-button-group > button:nth-child(10) > span.btn-subtext.currency-coins").text
                                        quick_sell_price = int(
                                            quick_sell_price)
                                        pack_quick_sell = pack_quick_sell + quick_sell_price
                                        quick_sell.click()
                                        quick_sell_confirm = WebDriverWait(driver, 20).until(
                                            EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.view-modal-container.form-modal > section > div > div > button:nth-child(1)")))
                                        quick_sell_confirm.click()
                                        attempts = 0
                                        break
                                    except (ElementClickInterceptedException, StaleElementReferenceException):
                                        pass
                                    attempts = attempts + 1
                                counter = counter - 1
                                # time.sleep(0.3)
                        else:

                            while attempts < 2:
                                try:
                                    send_to_club.click()
                                    attempts = 0
                                    break
                                except (StaleElementReferenceException, ElementClickInterceptedException):
                                    send_to_club = WebDriverWait(driver, 20).until(
                                        EC.element_to_be_clickable((By.XPATH, "/html/body/main/section/section/div[2]/div/div/section[2]/div[2]/div/div[2]/div[3]/button[6]")))

                                attempts = attempts + 1
                            players_sent_to_club = players_sent_to_club + 1
                            counter = counter - 1

                    else:
                        attempts = 0
                        while attempts < 2:
                            try:
                                list_on_market = WebDriverWait(driver, 20).until(
                                    EC.element_to_be_clickable((By.XPATH, "/html/body/main/section/section/div[2]/div/div/section[2]/div[2]/div/div[2]/div[2]/div[1]/button")))
                                list_on_market.click()
                                sell_price_input = WebDriverWait(driver, 20).until(
                                    EC.element_to_be_clickable((By.XPATH, "/html/body/main/section/section/div[2]/div/div/section[2]/div[2]/div/div[2]/div[2]/div[2]/div[3]/div[2]/input")))
                                sell_price_input.click()
                                attempts = 0
                                break
                            except (ElementClickInterceptedException, StaleElementReferenceException):
                                pass
                            attempts = attempts + 1

                        for i in range(6):
                            time.sleep(0.1)
                            sell_price_input.send_keys(Keys.BACK_SPACE)

                        # print(lowestPrice)
                        sell_price_input.send_keys(str(lowestPrice-100))

                        attempts = 0
                        while attempts < 2:
                            try:
                                min_price_input = WebDriverWait(driver, 20).until(
                                    EC.element_to_be_clickable((By.XPATH, "/html/body/main/section/section/div[2]/div/div/section[2]/div[2]/div/div[2]/div[2]/div[2]/div[2]/div[2]/input")))
                                min_price_input.click()
                                attempts = 0
                                break
                            except (ElementClickInterceptedException, StaleElementReferenceException):
                                pass
                            attempts = attempts + 1

                        for i in range(6):
                            time.sleep(0.1)
                            min_price_input.send_keys(Keys.BACK_SPACE)

                        # print(lowestPrice)
                        min_price_input.send_keys(str(lowestPrice-200))

                        confirm_sell = WebDriverWait(driver, 20).until(
                            EC.element_to_be_clickable((By.XPATH, "/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[2]/div[2]/button")))

                        confirm_sell.click()
                        counter = counter - 1

                        if lowestPrice == 100000 and (itemtype == "small player item rare ut-item-loaded" or itemtype == "small player item common ut-item-loaded"):
                            pack_item_income = pack_item_income + 10000
                        elif lowestPrice == 100000 and (itemtype == "small manager staff item common ut-item-loaded" or itemtype == "small manager staff item rare ut-item-loaded"):
                            pack_item_income = pack_item_income + 5000
                        else:
                            pack_item_income = pack_item_income + lowestPrice-100
                        # time.sleep(0.3)

                else:
                    pass

                # time.sleep(0.3)
                counter = counter + 1
            attempts = 0
            while attempts < 2:
                try:
                    quick_sell_all = WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "body > main > section > section > div.ut-navigation-container-view--content > div > div > section.ut-unassigned-view.ui-layout-left > section > div > button")))
                    quick_sell_all_amount = quick_sell_all.find_element_by_css_selector(
                        "body > main > section > section > div.ut-navigation-container-view--content > div > div > section.ut-unassigned-view.ui-layout-left > section:nth-child(1) > div > button > span.btn-subtext.currency-coins").text
                    quick_sell_all_amount = int(quick_sell_all_amount)
                    pack_quick_sell = pack_quick_sell + quick_sell_all_amount
                    quick_sell_all.click()
                    quick_sell_all_confirm = WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.view-modal-container.form-modal > section > div > div > button:nth-child(1)")))
                    quick_sell_all_confirm.click()
                    attempts = 0
                    break
                except (StaleElementReferenceException, ElementClickInterceptedException):
                    pass
                attempts = attempts + 1

            tot_n_packs = tot_n_packs + 1
            pack_profit = pack_item_income + pack_quick_sell - 750
            tot_profit = tot_profit + pack_profit
            tot_players_sent_to_club = tot_players_sent_to_club + players_sent_to_club

            text = "Pack number: %s\n\t - Pack profit: %s\n\t - Players sent to club: %s\n\t - Total profit: %s\n\t - Total players sent to club: %s\n-----------------------------\n" % (
                str(tot_n_packs), str(pack_profit), str(players_sent_to_club), str(tot_profit), str(tot_players_sent_to_club))

            results.write(text)

            print(text)

            # time.sleep(0.4)

    elif mode == "sbc":
        sbcBtn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "body > main > section > nav > button.ut-tab-bar-item.icon-sbc")))

        sbcBtn.click()

        sbcCatBtn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "body > main > section > section > div.ut-navigation-container-view--content > div > div.ea-filter-bar-view > div > button:nth-child(6)")))

        sbcCatBtn.click()
        while True:

            if sbcType == "bronze":
                upgradesBtn = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "body > main > section > section > div.ut-navigation-container-view--content > div > div.container > div.layout-hub.grid > div:nth-child(1)")))
            else:
                upgradesBtn = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "body > main > section > section > div.ut-navigation-container-view--content > div > div.container > div.layout-hub.grid > div:nth-child(2)")))

            attempts = 0
            while attempts < 2:
                try:
                    upgradesBtn.click()

                    squadBuilderBtn = WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "body > main > section > section > div.ut-navigation-container-view--content > div > div > section > div > section > div > button:nth-child(3)")))

                    squadBuilderBtn.click()

                    time.sleep(0.2)

                    sortByBtn = WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable((By.XPATH, "/html/body/main/section/section/div[2]/div/div/section/div[2]/div/div[1]/div/div[2]")))

                    sortByBtn.click()

                    mostRecentBtn = WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "body > main > section > section > div.ut-navigation-container-view--content > div > div > section > div.ut-navigation-container-view--content > div > div.ut-squad-builder-view--filters > div > div.inline-list-select.ut-drop-down-control.is-open > div > ul > li:nth-child(5)")))

                    mostRecentBtn.click()

                    rarityBtn = WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "body > main > section > section > div.ut-navigation-container-view--content > div > div > section > div.ut-navigation-container-view--content > div > div.ut-item-search-view > div:nth-child(4) > div > div")))

                    rarityBtn.click()

                    time.sleep(0.2)

                    commonBtn = driver.find_element_by_css_selector(
                        "body > main > section > section > div.ut-navigation-container-view--content > div > div > section > div.ut-navigation-container-view--content > div > div.ut-item-search-view > div.inline-list-select.ut-search-filter-control.has-default.has-image.ui-flip-vertical.is-open > div > ul > li:nth-child(3)")

                    commonBtn.click()

                    buildBtn = WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "body > main > section > section > div.ut-navigation-container-view--content > div > div > section > div.ut-navigation-container-view--content > div > div.button-container > button.btn-standard.call-to-action")))

                    buildBtn.click()
                    time.sleep(0.05)

                    submitBtn = WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "body > main > section > section > div.ut-navigation-container-view--content > div > div > div > div.ut-draggable > button.ut-squad-tab-button-control.actionTab.right.call-to-action")))

                    submitBtn.click()
                    time.sleep(0.05)

                    claimRewardsBtn = WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.view-modal-container.form-modal > div > footer > button")))

                    claimRewardsBtn.click()
                    time.sleep(0.05)

                    claimRewards2ndBtn = WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.view-modal-container.form-modal > div > footer > button")))

                    claimRewards2ndBtn.click()
                    time.sleep(0.05)
                    attempts = 0
                    break
                except (ElementClickInterceptedException, StaleElementReferenceException, NoSuchElementException):
                    pass
                attempts = attempts + 1

    elif mode == "open_rewards":

        while True:
            attempts = 0
            while attempts < 2:
                try:
                    attempts = 0
                    while attempts < 2:
                        try:
                            storeBtn = WebDriverWait(driver, 20).until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, "body > main > section > nav > button.ut-tab-bar-item.icon-store")))
                            storeBtn.click()
                            mainPackBtn = WebDriverWait(driver, 20).until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, "body > main > section > section > div.ut-navigation-container-view--content > div > div > div.tile.ut-tile-view--with-gfx.col-1-2.packs-tile.storehub-tile")))
                            mainPackBtn.click()
                            attempts = 0
                            break
                        except (ElementClickInterceptedException, StaleElementReferenceException):
                            pass
                        attempts = attempts + 1

                    openPackBtn = WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "body > main > section > section > div.ut-navigation-container-view--content > div > div.ut-store-hub-view--content > div:nth-child(2) > div.ut-store-pack-details-view--footer > button")))
                    openPackBtn.click()
                    time.sleep(0.5)
                    attempts = 0
                    break
                except TimeoutException:
                    pass
                attempts = attempts + 1

            ulElem = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/main/section/section/div[2]/div/div/section[1]/section/ul")))

            li_elements = ulElem.find_elements_by_tag_name("li")

            # time.sleep(0.3)
            pack_items = []

            for li in li_elements:

                class_name = li.get_attribute("class")

                class_name = class_name.replace(" ", "")
                if len(class_name) > 1:
                    pack_items.append(li)
                    tmp = li.text
                    tmp = tmp.replace("\n", "")

            if len(pack_items) != 2:
                while attempts < 2:
                    try:
                        quick_sell_dup = driver.find_element_by_xpath(
                            "/html/body/main/section/section/div[2]/div/div/section[1]/section[2]/div/button")
                        time.sleep(0.1)
                        quick_sell_dup.click()
                        time.sleep(0.1)
                        confirm_sell = driver.find_element_by_xpath(
                            "/html/body/div[4]/section/div/div/button[1]/span[1]")
                        confirm_sell.click()
                        attempts = 0
                        break
                    except (ElementClickInterceptedException, StaleElementReferenceException):
                        pass
                    attempts = attempts + 1
            time.sleep(0.1)
            saveAllBtn = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "body > main > section > section > div.ut-navigation-container-view--content > div > div > section.ut-unassigned-view.ui-layout-left > section > header > button")))
            saveAllBtn.click()

    # Not finished
    elif mode == "clean_club":

        while True:
            attempts = 0
            while attempts < 2:
                try:
                    clubBtn = WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "body > main > section > nav > button.ut-tab-bar-item.icon-club")))
                    clubBtn.click()
                    attempts = 0
                    break
                except (ElementClickInterceptedException, StaleElementReferenceException):
                    pass
                attempts = attempts + 1

            while attempts < 2:
                try:
                    playersBtn = WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "body > main > section > section > div.ut-navigation-container-view--content > div > div > div.tile.col-2-3-md.players-tile")))
                    playersBtn.click()
                    attempts = 0
                    break
                except (ElementClickInterceptedException, StaleElementReferenceException):
                    pass
                attempts = attempts + 1
            while attempts < 2:
                try:
                    searchBtn = WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "body > main > section > section > div.ut-navigation-container-view--content > div > div > div > div.ut-list-header > span.ut-list-header-action > button")))
                    searchBtn.click()
                    attempts = 0
                    break
                except (ElementClickInterceptedException, StaleElementReferenceException):
                    pass
                attempts = attempts + 1

            while attempts < 2:
                try:
                    qualityBtn = WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "body > main > section > section > div.ut-navigation-container-view--content > div > div > div > div.ut-pinned-list > div.ut-item-search-view.filter-container > div:nth-child(2) > div > div")))
                    qualityBtn.click()
                    qualitySelectedBtn = WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "body > main > section > section > div.ut-navigation-container-view--content > div > div > div > div.ut-pinned-list > div.ut-item-search-view.filter-container > div.inline-list-select.ut-search-filter-control.has-default.has-image.is-open > div > ul > li:nth-child(2)")))
                    qualitySelectedBtn.click()

                    attempts = 0
                    break
                except (ElementClickInterceptedException, StaleElementReferenceException):
                    pass
                attempts = attempts + 1


if __name__ == '__main__':

    main()
