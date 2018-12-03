from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select

def getFrameSourceAnywhere(username, password):
    with Display():
        return getFrameSource(username, password)

def getFrameSource(username, password):
    print("loading webpage")
    try:
        loginURL = "https://www.my.bham.ac.uk/cp/home/displaylogin"
        actualWebTimeTableURL = """https://onlinetimetables.bham.ac.uk/Timetable/current_academic_year_2/default.aspx"""

        #opens instance of webdriver
        #options = webdriver.FirefoxOptions()
        #options.add_argument('-headless')
        try:
            #driver = webdriver.Firefox(firefox_options=options)
            print("trying to load firefox")
            driver = webdriver.Firefox()
        except:
            print("was unable to open firefox driver.")
            return "was unable to open firefox driver.", True

        #opens google to check things are working
        driver.get("https://www.google.co.uk/")
        print("opened google to check things are working...")
        driver.save_screenshot("screenshot0g.png")
        print("saved screenshot of google home page")

        #opens login page
        driver.get(loginURL)
        print("opened login page...")
        driver.save_screenshot("screenshot0.png")
        print("saved screenshot of login page")

        #navigates through login page
        driver.find_element_by_name("user").send_keys(username)
        driver.find_element_by_name("pass").send_keys(password)
        driver.find_element_by_css_selector("""img[alt=\"Login\"]""").click()
        try:
            driver.find_element_by_link_text("my.timetables").click()
            print("was able to log in")
        except:
            driver.quit()
            return "Login Error.", True
        try:
            driver.get(actualWebTimeTableURL)
        except:
            driver.quit()
            return "Failed to load web timetables page", True

        #will try to log in again
        try:
            driver.find_element_by_name("tUserName").send_keys(username)
            driver.find_element_by_name("tPassword").send_keys(password)
            driver.find_element_by_name("bLogin").click()
        except:
            print("already logged in")

        driver.save_screenshot("screenshot.png")
        #el = driver.find_elements_by_id("LinkBtn_mystudentset")
        try:
            #driver.find_element_by_id("LinkBtn_mystudentset").click()
            #driver.find_element_by_id("LinkBtn_mystudentset").click()
            #driver.find_elements_by_id("LinkBtn_mystudentset").click()
            javascript = "javascript:__doPostBack('LinkBtn_mystudentset','')"
            driver.execute_script(javascript)
            print("clicked element... worked")
            driver.save_screenshot("screenshot3.png")
            #will try to log in again
            try:
                driver.find_element_by_name("tUserName").send_keys(username)
                driver.find_element_by_name("tPassword").send_keys(password)
                driver.find_element_by_name("bLogin").click()
                driver.execute_script(javascript)
                driver.save_screenshot("screenshot3b.png")
            except:
                print("already logged in")
        except:
            driver.quit()
            return "Failed to goto 'My Timetable'.", True

        #selects options from drop downs:
        try:
            el = driver.find_element_by_id("lbWeeks")
            for option in el.find_elements_by_tag_name('option'):
                if option.text == '*All Term Time':
                    actionChains = ActionChains(driver)
                    actionChains.double_click(option).perform()
                    option.click()
            print("selected weeks")

            el = driver.find_element_by_id("lbDays")
            for option in el.find_elements_by_tag_name('option'):
                if option.text == 'All Week':
                    actionChains = ActionChains(driver)
                    actionChains.double_click(option).perform()
                    option.click()
            print("selected days")

            select = Select(driver.find_element_by_id("dlPeriod"))
            driver.save_screenshot("screenshot3c.png")
            select.select_by_visible_text('All Day (08:00 - 22:00)')
            print("selected period")

            try:
                el = driver.find_element_by_id("dlType")
                print("found dlType by ID")
            except:
                try:
                    el = driver.find_element_by_name("dlType")
                    print("found dlType by name")
                except:
                    try:
                        el = driver.find_element_by_css_selector("#dlType")
                        print("found dlType by CSS")
                    except:
                        print("Failed to find element 3 time")
            el.click()
            driver.save_screenshot("screenshot3d.png")
            select = Select(el)
            print("selected dlType")
            driver.save_screenshot("screenshot3e.png")
            select.select_by_visible_text('List Timetable (with calendar dates)')
            print("selected view type")
        except:
            driver.save_screenshot("screenshot3f.png")
            driver.quit()
            return "Failed to select correct view options.", True

        #gets calendar list view
        driver.find_element_by_id("bGetTimetable").click()

        #gets page source
        frameHTML = driver.page_source
        driver.save_screenshot("screenshot4.png")
        driver.quit()

        return frameHTML, False

    finally:
        driver.quit()
