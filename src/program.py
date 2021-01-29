from selenium import webdriver
# from selenium.webdriver.common.by import BY
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
from decouple import config

emailStr = config("$email")
pwdStr = config("$pwd")

#Open the browser
browser = webdriver.Chrome()
browser.get(("https://www.tesco.com/groceries/en-GB/slots/delivery"))

#Fill in user data
userField = browser.find_element_by_id('username')
userField.send_keys(emailStr)
pwdFileld = browser.find_element_by_id('password')
pwdFileld.send_keys(pwdStr)

#Find button
loginBtn = browser.find_element_by_class_name("ui-component__button")
loginBtn.click()

#Find slots
slots = browser.find_elements_by_class_name("slot-selector--3-week-tab-space")

### Here put looking for an empty slots once you know how they look
slots[1].click()

