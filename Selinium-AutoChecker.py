import time
import random
from selenium import webdriver
from pyvirtualdisplay import Display
import undetected_chromedriver as uc

'''
driver = uc.Chrome()
print(driver.execute_script('return navigator.webdriver'))
driver.get('https://distilnetworks.com') # starts magic
print(driver.execute_script('return navigator.webdriver'))
'''
'''
profile = webdriver.FirefoxProfile('C:\\Users\\jackk\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\zhln8k0l.default-release')

PROXY_HOST = "12.12.12.123"
PROXY_PORT = "1234"
profile.set_preference("network.proxy.type", 1)
profile.set_preference("network.proxy.http", PROXY_HOST)
profile.set_preference("network.proxy.http_port", int(PROXY_PORT))
profile.set_preference("dom.webdriver.enabled", False)
profile.set_preference('useAutomationExtension', False)
profile.update_preferences()


driver = webdriver.Firefox(firefox_profile=profile,executable_path=r'C:\Program Files (x86)\geckodriver.exe' )
'''

'''
options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--disable-extensions')
options.add_argument('--profile-directory=Default')
options.add_argument("--incognito")
options.add_argument("--disable-plugins-discovery");
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options, executable_path=r'C:\Program Files (x86)\chromedriver.exe')
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
print(driver.execute_script("return navigator.userAgent;"))



driver.delete_all_cookies()
driver.set_window_size(800,800)
driver.set_window_position(0,0)

'''
unavailable_list = []


print(len(unavailable_list))





def EbayAuto(Items):
    if not Items:
        print("No Items To Delete")
        pass

    if len(Items) == 1:
        print('running 1 ')
        bob = "(" + str(Items) + ")"

    print(len(Items))
    if len(Items) >= 2:
        print('running 2 ')
        Items = "(" + str(Items) + ")"



EbayAuto(unavailable_list)
'''

driver.get("https://www.google.com")#

driver.implicitly_wait(random.randint(4,6))
driver.get("https://www.ebay.co.uk/sh/lst/active")
driver.implicitly_wait(random.randint(4,6))
time.sleep(3)

user = driver.find_element_by_id("userid")
user.send_keys("jackkaybuiss@hotmail.com")
time.sleep(1.5)
signIn = driver.find_element_by_id("signin-continue-btn")
signIn.click()


time.sleep(5)


password = driver.find_element_by_id("pass")
password.send_keys("Trendme22!")
time.sleep(1.5)
signIn2 = driver.find_element_by_id("sgnBt")
signIn2.click()


driver.implicitly_wait(random.randint(4,7))
itemList = driver.find_element_by_xpath('//*[@id='"'s0-0-4-16-49-7-filters-advancedSearch[]-generic'"']/input')
itemList.send_keys("('', '')")
time.sleep(random.randint(2,4))
button = driver.find_element_by_xpath("//*[@id='"'s0-0-4-16-49-7-filters'"']/form/div[4]/button[1]")
button.click()
time.sleep(random.randint(6,10))
selectAll = driver.find_element_by_xpath("//*[@id='"'shui-dt-checkall'"']")
selectAll.click()
time.sleep(random.randint(6,10))

preEnd1 = driver.find_element_by_xpath("/html/body/div[6]/div[2]/div[1]/div/div[3]/div/div[2]/div[3]/div[3]/div[1]/div/div[3]/span/span/button")
preEnd1.click()
time.sleep(random.randint(6,10))

preEnd2 = driver.find_element_by_xpath("//*[@id='"'s0-0-4-16-49-bulkActionsV2-component-5-0-content-menu'"']/a[1]")
preEnd2.click()
time.sleep(random.randint(6,10))

endItems = driver.find_element_by_xpath("/html/body/div[2]/div/div/div/form[3]/table[3]/tbody/tr/td[2]/table/tbody/tr[2]/td[1]/input")
endItems.click()

'''

