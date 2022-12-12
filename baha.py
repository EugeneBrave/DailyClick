import config, cookies
from datetime import datetime
from browser import Browser
from os.path import exists
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


def login(browser, username, password):
    driver = browser.driver
    wait = browser.wait
    driver.get(config.URL_LOGIN)
    try:
        wait.until(EC.url_changes(config.URL_LOGIN))
    except:
        pass
    curUrl = driver.current_url
    if curUrl == config.URL_HOMENoAD or curUrl == config.URL_HOME or curUrl == config.URL_HOME2:
        print("已經登入")
        return True
    else:
        user = driver.find_element(By.NAME, "userid")
        user.send_keys(username)
        pwd = driver.find_element(By.NAME, "password")
        pwd.send_keys(password)
        pwd.send_keys(Keys.RETURN)	
        try:
            try:
                wait.until(EC.url_changes(config.URL_HOME))
            except:
                pass
            try:
                wait.until(EC.url_changes(config.URL_HOMENoAD))
            except:
                pass
            try:
                wait.until(EC.url_changes(config.URL_HOME2))
            except:
                pass
            wait.until(EC.presence_of_element_located((By.ID, "signin-btn")))
            print("登入成功")
            return True
        except Exception as e:
            print(e)
            return False


def signIn(browser, cookiepath):
    driver = browser.driver
    wait = browser.wait
    try:
        signInBtn = wait.until(
            EC.presence_of_element_located((By.ID, "signin-btn"))
        )
        if "每日簽到已達成" in signInBtn.text:
            print("每日簽到已達成")
        else:
            try:
                wait.until(
                    EC.presence_of_element_located((By.CLASS_NAME, "popup-dailybox__title"))
                )
            except:
                signInBtn.click()
            driver.get_screenshot_as_file(f"{cookiepath}/Screenshots/success.png")
        return True
    except Exception as e:
        now=datetime.strftime(now,'%Y-%m-%d %H:%M:%S')
        driver.get_screenshot_as_file(f"{cookiepath}/Screenshots/error_{now}.png")
        print(e)
        return False

def runBot(args):
    browser = cookies.loadCookies(Browser(args.webdriver, args.remoteip), args.cookiepath)
    if login(browser, args.username, args.password):
        cookies.saveCookies(browser, args.cookiepath)
        signIn(browser, args.cookiepath)
    browser.driver.close()
