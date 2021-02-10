import smtplib
import ssl
import schedule
import time

from decouple import config
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

emailStr = config("$email")
pwdStr = config("$pwd")


def init():
    print("Time to start!")
    open_browser()
    schedule_job()


def open_browser():
    browser = webdriver.Chrome()
    browser.maximize_window()
    browser.get("https://www.tesco.com/groceries/en-GB/slots/delivery")

    # Fill in user data
    user_field = browser.find_element_by_id('username')
    user_field.send_keys(emailStr)
    pwd_field = browser.find_element_by_id('password')
    pwd_field.send_keys(pwdStr)

    # Find button
    login_btn = browser.find_element_by_class_name("ui-component__button")
    login_btn.click()
    print('Logged in')

    go_through_slots(browser)


def go_through_slots(browser):
    browser.implicitly_wait(10)

    # Change type of slots
    change_slot_type_xpath = "//*[@class='group-selector--container']//*[@class='group-selector--list-item'][2]//a"
    change_slot_type = browser.find_element(By.XPATH, change_slot_type_xpath)
    print("Changed slot: ", change_slot_type.get_attribute("innerHTML"))
    change_slot_type.click()
    time.sleep(10)

    # Go to last tab
    last_tab_xpath = "//*[@id='slot-matrix']//ul[@class='tabs-header-container']/li[3]"

    try:
        clickable_slot = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, last_tab_xpath)))
        clickable_slot.click()
        time.sleep(2)
    except:
        print("I didn't have what to click")

    available_times = ['09:00 - 13:00', '08:00 - 12:00', '10:00 - 14:00', '11:00 - 15:00', '12:00 - 16:00',
                       '13:00 - 17:00', '14:00 - 18:00', '15:00 - 19:00', '16:00 - 20:00', '17:00 - 21:00',
                       '18:00 - 22:00', '19:00 - 23:00']

    for slot in available_times:
        book(slot, browser)

    print("I'm going to wait before I close the window")
    time.sleep(20)


def get_slot_path(slot):
    return "//table[@class='slot-grid__table'][1]//th[contains(.,'" + slot + "')]/following-sibling::td//*[@class='slot-grid--item available slot-grid--item-oop808']//button"


def book(slot, browser):
    preferred_slot_xpath = get_slot_path(slot)
    preferred_slot = None

    try:
        preferred_slot = browser.find_element(By.XPATH, preferred_slot_xpath)
    except:
        print('No slot for: ', slot)

    if preferred_slot:
        print(preferred_slot.get_attribute("innerHTML"))
        preferred_slot.click()
        send_email()
        return

# Send Email

sender_email = "luckyducky.development@gmail.com"
receiver_email = "weronika.dominiak3@gmail.com"
message = """\
From: Lucky Ducky Development <luckyducky.development@gmail.com>
Subject: Yaaay! Saved contents!

Hello, I booked a slot for you!

This message is sent from Python."""


def send_email():
    port = 465  # for SSL

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender_email, pwdStr)
        server.sendmail(sender_email, receiver_email, message)


def schedule_job():
    # https://schedule.readthedocs.io/en/stable/
    print("I'm scheduling a job")

    def job():
        print("#### Job started ####")
        open_browser()
        print("#### Job finished ####")

    schedule.every(15).minutes.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)


init()
