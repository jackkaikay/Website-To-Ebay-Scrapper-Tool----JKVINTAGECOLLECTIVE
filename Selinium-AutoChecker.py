import time
from selenium import webdriver
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

driver.get("https://www.ebay.co.uk/sh/lst/active")
driver.implicitly_wait(4)
driver.maximize_window()
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


time.sleep(5)
itemList = driver.find_element_by_xpath('//*[@id='"'s0-0-4-16-49-7-filters-advancedSearch[]-generic'"']/input')
itemList.send_keys("(CLOAK1,CLOAK5,CLOAK11,CLOAK55,CLOAK101)")
time.sleep(2)
button = driver.find_element_by_class_name("btn")
button.click()