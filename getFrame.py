from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select

def getFrameSource(username, password):
    loginURL = "https://www.my.bham.ac.uk/cp/home/displaylogin"
    actualWebTimeTableURL = """https://onlinetimetables.bham.ac.uk/Timetable/current_academic_year_2/default.aspx"""
    
    #opens instance of webdriver
    options = webdriver.FirefoxOptions()
    options.add_argument('-headless')
    driver = webdriver.Firefox(firefox_options=options)

    #opens login page
    driver.get(loginURL)

    #navigates through login page
    driver.find_element_by_name("user").send_keys(username)
    driver.find_element_by_name("pass").send_keys(password)
    driver.find_element_by_css_selector("""img[alt=\"Login\"]""").click()
    try:
        driver.find_element_by_link_text("my.timetables").click()
    except:
        driver.quit()
        return "Login Error.", True
    try:
        driver.find_element_by_css_selector("strong > span").click()
        driver.get(actualWebTimeTableURL)
        driver.find_element_by_id("LinkBtn_mystudentset").click()
        driver.find_element_by_id("LinkBtn_mystudentset").click()
    except:
        driver.quit()
        return "Failed to click 'My Timetable' button.", True

    #selects options from drop downs:
    try:
        el = driver.find_element_by_id("lbWeeks")
        for option in el.find_elements_by_tag_name('option'):
            if option.text == '*All Term Time':
                actionChains = ActionChains(driver)
                actionChains.double_click(option).perform()
        
        el = driver.find_element_by_id("lbDays")
        for option in el.find_elements_by_tag_name('option'):
            if option.text == 'All Week':
                actionChains = ActionChains(driver)
                actionChains.double_click(option).perform()
        
        select = Select(driver.find_element_by_id("dlPeriod"))
        select.select_by_visible_text('All Day (08:00 - 22:00)')

        select = Select(driver.find_element_by_id("dlType"))
        select.select_by_visible_text('List Timetable (with calendar dates)')
    except:
        driver.quit()
        return "Failed to select view correct options.", True

    #gets calendar list view
    driver.find_element_by_id("bGetTimetable").click()

    #gets page source
    frameHTML = driver.page_source

    driver.quit()

    return frameHTML, False

