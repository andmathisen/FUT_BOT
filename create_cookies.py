from selenium import webdriver
import pickle



def create_cookies():
    driver = webdriver.Firefox(
        executable_path="../FUT_BOT/geckodriver")
    driver.get("https://www.ea.com/ea-sports-fc/ultimate-team/web-app/")
    foo = input()
    pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))



create_cookies()