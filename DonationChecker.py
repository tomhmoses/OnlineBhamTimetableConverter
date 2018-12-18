from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
import time

def checkForDonationAnywhere(username):
    with Display():
        return checkForDonation(username)

def checkForDonation(username):
    print("loading donation webpage")
    try:
        pageURL = "https://l2p19.everydayhero.com/uk/tom"

        try:
            print("trying to load firefox")
            driver = webdriver.Firefox()
        except:
            print("was unable to open firefox driver.")
            return False

        #opens donation page
        driver.get(pageURL)

        pageSource = driver.page_source
        driver.quit()

        donated = username.upper() in pageSource.upper()

        return donated

    finally:
        driver.quit()

if __name__ == "__main__":
    responce = ""
    while responce != "done":
        responce = input("enter what you want to find: ")
        print(checkForDonationAnywhere(responce))

