import datetime, config, cookies
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
    print(f"curUrl={curUrl}")
    if curUrl == config.URL_HOME:
        print("已經登入")
        return True
    else:
        user = driver.find_element(By.NAME, "userid")
        user.send_keys(username)
        pwd = driver.find_element(By.NAME, "password")
        pwd.send_keys(password)
        pwd.send_keys(Keys.RETURN)
        try:
            wait.until(EC.presence_of_element_located((By.ID, "signin-btn")))
            
            print("登入成功")
            return True
        except Exception as e:
            print(e)
            return False


def signIn(browser):
    driver = browser.driver
    wait = browser.wait
    try:
        signInBtn = wait.until(
            EC.presence_of_element_located((By.ID, "signin-btn"))
        )
        print(signInBtn.text)
        signInBtn.click()
        return True
    except Exception as e:
        driver.get_screenshot_as_file("/Screenshots/{today}.png".format(today=datetime.datetime.today))
        print(e)
        return False


def rewardDouble(browser):
    driver = browser.driver
    wait = browser.wait
    try:
        try:
            wait.until(EC.presence_of_element_located((By.XPATH,"//p[text()='廣告能量補充中']")))
            elms = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//a[@class='dialogify__close']")))
            print(elms)
        except:
            pass
        dailyboxBtn = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[contains(@class,'popup-dailybox__btn')]")
            )
        )
        print(dailyboxBtn.text)
        if dailyboxBtn.is_enabled():
            dailyboxBtn.click()
            dialogify = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[contains(@class,'dialogify__body')]/p")
                )
            )
            print(dialogify.text)
            if dialogify.text == "是否觀看廣告？":
                submitBtn = wait.until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            "//button[contains(@class,'btn-primary') and @type='submit']",
                        )
                    )
                )
                submitBtn.click()
                try:
                    adIframe = wait.until(EC.visibility_of_element_located((By.XPATH, "//iframe[@title='3rd party ad content']")))
                    print(adIframe)
                    driver.switch_to.frame(adIframe)
                    rewardResumebutton = driver.find_element(By.CLASS_NAME, "rewardResumebutton")
                    if rewardResumebutton:
                        rewardResumebutton.click()
                        driver.switch_to.default_content()
                except:
                    pass
                sleep(45)
        else:
            print("已領取雙倍巴幣")
    except Exception as e:
        print("發生不預期錯誤!!")
        print(e)
        driver.get_screenshot_as_file("/Screenshots/{today}.png".format(today=datetime.datetime.today))


def runBot(args):
    browser = cookies.loadCookies(Browser("chrome"), args.cookiepath)
    if login(browser, args.username, args.password):
        if signIn(browser):
            rewardDouble(browser)
        cookies.saveCookies(browser, args.cookiepath)
    browser.driver.close()
