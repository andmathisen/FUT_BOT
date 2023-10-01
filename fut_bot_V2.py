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


    mode = sys.argv[1]
    email = sys.argv[2]
    passw = sys.argv[3]


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

    tot_n_packs = 0
    tot_profit = 0
    tot_players_sent_to_club = 0
    results = open("results.txt", "a")

    if mode == "bpm":

        while True:
            pack_profit = 0
            if check_exists_by_css("body > main > section > section > div.ut-navigation-bar-view.navbar-style-landscape.currency-purchase > button.ut-navigation-button-control",driver):
                attempt_click_css("body > main > section > section > div.ut-navigation-bar-view.navbar-style-landscape.currency-purchase > button.ut-navigation-button-control",driver)
            attempt_click_css("body > main > section > nav > button.ut-tab-bar-item.icon-store", driver)  # Store button
            attempt_click_css("body > main > section > section > div.ut-navigation-container-view--content > div > div > div.tile.ut-tile-view--with-gfx.col-1-2.packs-tile.storehub-tile", driver)  # Packs button
            
            if check_exists_by_css("body > main > section > section > div.ut-navigation-container-view--content > div > div.ut-store-hub-view--content > div.ut-unassigned-tile-view.tile",driver):
                attempt_click_css("body > main > section > section > div.ut-navigation-container-view--content > div > div.ut-store-hub-view--content > div.ut-unassigned-tile-view.tile",driver)
            else:
                classic = attempt_click_css("body > main > section > section > div.ut-navigation-container-view--content > div > div.ea-filter-bar-view > div > button:nth-child(2)",driver) # Classic Packs
                if classic.text != "Classic Packs":
                    attempt_click_css("body > main > section > section > div.ut-navigation-container-view--content > div > div.ea-filter-bar-view > div > button:nth-child(3)",driver)
                attempt_click_css("body > main > section > section > div.ut-navigation-container-view--content > div > div.ut-store-hub-view--content > div:nth-child(2) > div.ut-store-pack-details-view--footer > button",driver) #Bronze Pack buy button   
                attempt_click_css("body > div.view-modal-container.form-modal > section > div > div > button:nth-child(1)",driver) # OK
                
            if check_exists_by_css("body > main > section > section > div.ut-navigation-container-view--content > div > div > section.ut-unassigned-view.ui-layout-left > section:nth-child(2) > header > h2",driver):
                ulElem = WebDriverWait(driver, 20).until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, "body > main > section > section > div.ut-navigation-container-view--content > div > div > section.ut-unassigned-view.ui-layout-left > section:nth-child(2) > ul")))
                all_li_elements = ulElem.find_elements(
                    By.TAG_NAME, "li")

                pack_items = [li for li in all_li_elements if len(li.get_attribute("class").replace(" ", "")) > 1]
                
                counter = 1
                for _ in range(len(pack_items)):
                    time.sleep(0.5)

                    item = WebDriverWait(driver, 20).until(
                            EC.visibility_of_element_located((By.XPATH, "/html/body/main/section/section/div[2]/div/div/section[1]/section[2]/ul/li["+str(
                                counter) + "]")))
                    
                    try:
                        item.click()
                    except (StaleElementReferenceException,ElementClickInterceptedException):
                        counter = counter - 1
                        
                # driver.find_element(By.XPATH,"/html/body/main/section/section/div[2]/div/div/section[1]/section/ul/li["+str(i+1-c)+"]").click()
                    item_type = WebDriverWait(driver, 20).until(
                                EC.visibility_of_element_located((By.XPATH, "/html/body/main/section/section/div[2]/div/div/section[1]/section[2]/ul/li["+str(max(counter,1))+"]/div/div[1]/div[1]"))).get_attribute("class")

                    if "player" in item_type or "manager" in item_type:
                        lowest_price = 100000
                        attempt_click_css("body > main > section > section > div.ut-navigation-container-view--content > div > div > section.ut-navigation-container-view.ui-layout-right > div > div > div.DetailPanel > div.ut-button-group > button:nth-child(9)",driver)
                        ulElem_tl = WebDriverWait(driver, 20).until(
                                    EC.element_to_be_clickable((By.CSS_SELECTOR, "body > main > section > section > div.ut-navigation-container-view--content > div > div > section.ut-navigation-container-view.ui-layout-right > div.ut-navigation-container-view--content > section > div.paginated-item-list.ut-pinned-list > ul")))
                        all_li_elements_tl = ulElem_tl.find_elements(
                            By.TAG_NAME, "li")
                        
                        for transferlist_item in all_li_elements_tl:
                            if len(transferlist_item.text.split("\n")) > 1:
                                price = int(transferlist_item.text.split("\n")[-3] if "," not in transferlist_item.text.split("\n")[-3] else transferlist_item.text.split("\n")[-3].replace(",",""))
                                if price < lowest_price:
                                    lowest_price = price
                                    if lowest_price == 200:
                                        break
                            
                            # if lowest_price < 250:
                            #     attempt_click_css("body > main > section > section > div.ut-navigation-container-view--content > div > div > section.ut-navigation-container-view.ui-layout-right > div.ut-navigation-bar-view.navbar-style-secondary > button",driver)
                            #     time.sleep(0.2)
                            #     send_to_club = WebDriverWait(driver, 10).until(
                            #                 EC.element_to_be_clickable((By.XPATH, "/html/body/main/section/section/div[2]/div/div/section[2]/div[2]/div/div[2]/div[3]/button[6]")))
                                
                            #     send_to_club_tag = send_to_club.text

                            #     if send_to_club_tag == "Bytt dublett fra klubb":
                            #         attempt_click_css("body > main > section > section > div.ut-navigation-container-view--content > div > div > section.ut-navigation-container-view.ui-layout-right > div > div > div.DetailPanel > div.ut-button-group > button:nth-child(10)""body > main > section > section > div.ut-navigation-container-view--content > div > div > section.ut-navigation-container-view.ui-layout-right > div > div > div.DetailPanel > div.ut-button-group > button:nth-child(10)",driver)
                            #         attempt_click_css("body > div.view-modal-container.form-modal > section > div > div > button:nth-child(1)",driver)
                            #         counter = counter - 1


                            #     else:
                            #         attempt_click_css("body > main > section > section > div.ut-navigation-container-view--content > div > div > section.ut-navigation-container-view.ui-layout-right > div.ut-navigation-container-view--content > div > div.DetailPanel > div.ut-button-group > button:nth-child(6)",driver)
                            #         counter = counter - 1

                            # else:
                            attempt_click_css("body > main > section > section > div.ut-navigation-container-view--content > div > div > section.ut-navigation-container-view.ui-layout-right > div.ut-navigation-bar-view.navbar-style-secondary > button",driver)
                            attempt_click_css("body > main > section > section > div.ut-navigation-container-view--content > div > div > section.ut-navigation-container-view.ui-layout-right > div.ut-navigation-container-view--content > div > div.DetailPanel > div.ut-quick-list-panel-view > div.ut-button-group > button",driver)
                            price_input = attempt_click_css("body > main > section > section > div.ut-navigation-container-view--content > div > div > section.ut-navigation-container-view.ui-layout-right > div.ut-navigation-container-view--content > div > div.DetailPanel > div.ut-quick-list-panel-view > div.panelActions.open > div:nth-child(3) > div.ut-numeric-input-spinner-control > input",driver)
                            time.sleep(0.4)
                            price_input.send_keys(Keys.BACK_SPACE)
                            time.sleep(0.4)
                            price_input.send_keys(str(lowest_price-100))
                            pack_profit = pack_profit + lowest_price-100
                            attempt_click_css("body > main > section > section > div.ut-navigation-container-view--content > div > div > section.ut-navigation-container-view.ui-layout-right > div.ut-navigation-container-view--content > div > div.DetailPanel > div.ut-quick-list-panel-view > div.panelActions.open > button",driver)
                            counter = counter - 1
                                
                    elif item_type == "small misc item common" or item_type == "small misc item rare":
                        attempt_click_css("body > main > section > section > div.ut-navigation-container-view--content > div > div > section.ut-navigation-container-view.ui-layout-right > div.ut-navigation-container-view--content > div > div.DetailPanel > div.ut-button-group > button:nth-child(2)",driver)
                        pack_profit = pack_profit + 100
                        counter = counter - 1

                attempt_click_css("body > main > section > section > div.ut-navigation-container-view--content > div > div > section.ut-unassigned-view.ui-layout-left > section > div > button",driver)
                attempt_click_css("body > div.view-modal-container.form-modal > section > div > div > button:nth-child(1)",driver)
            
                if check_exists_by_css("body > main > section > section > div.ut-navigation-bar-view.navbar-style-landscape.currency-purchase > button.ut-navigation-button-control",driver):
                    attempt_click_css("body > main > section > section > div.ut-navigation-bar-view.navbar-style-landscape.currency-purchase > button.ut-navigation-button-control",driver)  
            ulElem = WebDriverWait(driver, 20).until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, "body > main > section > section > div.ut-navigation-container-view--content > div > div > section.ut-unassigned-view.ui-layout-left > section > ul")))
            all_li_elements = ulElem.find_elements(
                By.TAG_NAME, "li")

            pack_items = [li for li in all_li_elements if len(li.get_attribute("class").replace(" ", "")) > 1]
            
            counter = 1
            for _ in range(len(pack_items)):
                time.sleep(0.5)
                try:
                    item = WebDriverWait(driver, 20).until(
                            EC.visibility_of_element_located((By.XPATH, "/html/body/main/section/section/div[2]/div/div/section[1]/section/ul/li["+str(
                                counter) + "]")))
                except TimeoutException:
                    item = WebDriverWait(driver, 20).until(
                            EC.visibility_of_element_located((By.XPATH, "/html/body/main/section/section/div[2]/div/div/section[1]/section/ul/li["+str(
                                counter+1) + "]")))
                try:
                    item.click()
                except (StaleElementReferenceException,ElementClickInterceptedException):
                    counter = counter - 1
                    
                    
            # driver.find_element(By.XPATH,"/html/body/main/section/section/div[2]/div/div/section[1]/section/ul/li["+str(i+1-c)+"]").click()
                item_type = WebDriverWait(driver, 20).until(
                            EC.visibility_of_element_located((By.XPATH, "/html/body/main/section/section/div[2]/div/div/section[1]/section/ul/li["+str(max(counter,1))+"]/div/div[1]/div[1]"))).get_attribute("class")

                if "player" in item_type or "manager" in item_type:
                    lowest_price = 100000
                    attempt_click_css("body > main > section > section > div.ut-navigation-container-view--content > div > div > section.ut-navigation-container-view.ui-layout-right > div > div > div.DetailPanel > div.ut-button-group > button:nth-child(9)",driver)
                    ulElem_tl = WebDriverWait(driver, 20).until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, "body > main > section > section > div.ut-navigation-container-view--content > div > div > section.ut-navigation-container-view.ui-layout-right > div.ut-navigation-container-view--content > section > div.paginated-item-list.ut-pinned-list > ul")))
                    all_li_elements_tl = ulElem_tl.find_elements(
                        By.TAG_NAME, "li")
                    
                    for transferlist_item in all_li_elements_tl:
                        if len(transferlist_item.text.split("\n")) > 1:
                            price = int(transferlist_item.text.split("\n")[-3] if "," not in transferlist_item.text.split("\n")[-3] else transferlist_item.text.split("\n")[-3].replace(",",""))
                            if price < lowest_price:
                                lowest_price = price
                                if lowest_price == 200:
                                    break
                    # if lowest_price < 250:
                    #     attempt_click_css("body > main > section > section > div.ut-navigation-container-view--content > div > div > section.ut-navigation-container-view.ui-layout-right > div.ut-navigation-bar-view.navbar-style-secondary > button",driver)
                    #     time.sleep(0.2)

                    #     send_to_club = WebDriverWait(driver, 10).until(
                    #                 EC.element_to_be_clickable((By.XPATH, "/html/body/main/section/section/div[2]/div/div/section[2]/div[2]/div/div[2]/div[3]/button[6]")))
                        
                    #     send_to_club_tag = send_to_club.text

                    #     if send_to_club_tag == "Bytt dublett fra klubb":
                    #         attempt_click_css("body > main > section > section > div.ut-navigation-container-view--content > div > div > section.ut-navigation-container-view.ui-layout-right > div > div > div.DetailPanel > div.ut-button-group > button:nth-child(10)""body > main > section > section > div.ut-navigation-container-view--content > div > div > section.ut-navigation-container-view.ui-layout-right > div > div > div.DetailPanel > div.ut-button-group > button:nth-child(10)",driver)
                    #         attempt_click_css("body > div.view-modal-container.form-modal > section > div > div > button:nth-child(1)",driver)
                    #         counter = counter - 1


                    #     else:
                    #         attempt_click_css("body > main > section > section > div.ut-navigation-container-view--content > div > div > section.ut-navigation-container-view.ui-layout-right > div.ut-navigation-container-view--content > div > div.DetailPanel > div.ut-button-group > button:nth-child(6)",driver)
                    #         counter = counter - 1

                    # else:
                    attempt_click_css("body > main > section > section > div.ut-navigation-container-view--content > div > div > section.ut-navigation-container-view.ui-layout-right > div.ut-navigation-bar-view.navbar-style-secondary > button",driver)
                    attempt_click_css("body > main > section > section > div.ut-navigation-container-view--content > div > div > section.ut-navigation-container-view.ui-layout-right > div.ut-navigation-container-view--content > div > div.DetailPanel > div.ut-quick-list-panel-view > div.ut-button-group > button",driver)
                    price_input = attempt_click_css("body > main > section > section > div.ut-navigation-container-view--content > div > div > section.ut-navigation-container-view.ui-layout-right > div.ut-navigation-container-view--content > div > div.DetailPanel > div.ut-quick-list-panel-view > div.panelActions.open > div:nth-child(3) > div.ut-numeric-input-spinner-control > input",driver)
                    time.sleep(0.4)
                    price_input.send_keys(Keys.BACK_SPACE)
                    time.sleep(0.4)
                    price_input.send_keys(str(lowest_price-100))
                    pack_profit = pack_profit + lowest_price-100
                    attempt_click_css("body > main > section > section > div.ut-navigation-container-view--content > div > div > section.ut-navigation-container-view.ui-layout-right > div.ut-navigation-container-view--content > div > div.DetailPanel > div.ut-quick-list-panel-view > div.panelActions.open > button",driver)
                    counter = counter - 1
                   

                elif item_type == "small misc item common" or item_type == "small misc item rare":
                    attempt_click_css("body > main > section > section > div.ut-navigation-container-view--content > div > div > section.ut-navigation-container-view.ui-layout-right > div.ut-navigation-container-view--content > div > div.DetailPanel > div.ut-button-group > button:nth-child(2)",driver)
                    pack_profit = pack_profit + 100
                    counter = counter - 1


                counter = counter + 1

            if not check_exists_by_css("body > main > section > section > div.ut-navigation-container-view--content > div > div > section.ut-unassigned-view.ui-layout-left > section > div > button",driver):
                attempt_click_css("body > main > section > section > div.ut-navigation-bar-view.navbar-style-landscape.currency-purchase > button.ut-navigation-button-control",driver)
                if check_exists_by_css("body > main > section > section > div.ut-navigation-container-view--content > div > div.ut-store-hub-view--content > div.ut-unassigned-tile-view.tile",driver):
                    attempt_click_css("body > main > section > section > div.ut-navigation-container-view--content > div > div.ut-store-hub-view--content > div.ut-unassigned-tile-view.tile",driver)
                else:
                    classic = attempt_click_css("body > main > section > section > div.ut-navigation-container-view--content > div > div.ea-filter-bar-view > div > button:nth-child(2)",driver) # Classic Packs
                    if classic.text != "Classic Packs":
                        attempt_click_css("body > main > section > section > div.ut-navigation-container-view--content > div > div.ea-filter-bar-view > div > button:nth-child(3)",driver)
                    attempt_click_css("body > main > section > section > div.ut-navigation-container-view--content > div > div.ut-store-hub-view--content > div:nth-child(2) > div.ut-store-pack-details-view--footer > button",driver) #Bronze Pack buy button   
                    attempt_click_css("body > div.view-modal-container.form-modal > section > div > div > button:nth-child(1)",driver) # OK
              
            else:
                attempt_click_css("body > main > section > section > div.ut-navigation-container-view--content > div > div > section.ut-unassigned-view.ui-layout-left > section > div > button",driver)
                attempt_click_css("body > div.view-modal-container.form-modal > section > div > div > button:nth-child(1)",driver)
            tot_profit = tot_profit + pack_profit+100-750
            print(tot_profit)