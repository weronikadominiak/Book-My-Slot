import smtplib
import ssl
import schedule
import time

from decouple import config
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

emailStr = config("$email")
pwdStr = config("$pwd")


def init():
    print("Time to start!")
    open_browser()
    schedule_job()


def open_browser():
    browser = webdriver.Chrome()
    browser.get("https://www.tesco.com/groceries/en-GB/slots/delivery")

    # Fill in user data
    user_field = browser.find_element_by_id('username')
    user_field.send_keys(emailStr)
    pwd_field = browser.find_element_by_id('password')
    pwd_field.send_keys(pwdStr)

    # Find button
    login_btn = browser.find_element_by_class_name("ui-component__button")
    login_btn.click()

    # todo: Here put looking for an empty slots once you know how they look
    # temporary action: check html inside the table to see how elements inside look like when they are available
    save_page_content(browser)
    send_email()


def save_page_content(browser):
    file = open("data.html", "a")
    today = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    content = "<h2>{}</h2>".format(today)
    file.write(content)

    browser.implicitly_wait(10)

    # Get fixed slot
    print(" \n I'm going to collect fixed slots data \n")
    go_through_content(browser, file)
    time.sleep(10)

    # Change type of slots
    change_slot_type_xpath = "//*[@class='group-selector--container']//*[@class='group-selector--list-item'][2]//a"
    change_slot_type = browser.find_element(By.XPATH, change_slot_type_xpath)
    print("Changed slot: ", change_slot_type.get_attribute("innerHTML"))
    change_slot_type.click()
    time.sleep(10)

    # Get flexi saver slot
    print("\n I'm going to collect flexi slots  \n")
    go_through_content(browser, file)

    file.close()
    print("I'm going to wait before I close the window")
    time.sleep(20)


def go_through_content(browser, file):
    # Find slots
    format_xpath = "//*[@id='slot-matrix']//ul[@class='tabs-header-container']/li"
    print("I'm done waiting")

    slots = browser.find_elements(By.XPATH, format_xpath)
    print("List has: " + str(len(slots)) + " elements");

    i = 1

    for slot in slots:
        format_xpath = "//*[@id='slot-matrix']//ul[@class='tabs-header-container']/li[{}]".format(i)
        # todo: see if can change to element instead of elements
        element = browser.find_elements(By.XPATH, format_xpath)
        print(i, slot)
        if len(element):
            print(element[0].get_attribute("innerHTML"))
            clickable_slot = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, format_xpath)))
            clickable_slot.click()
            time.sleep(10)
        else:
            print("I didn't have what to click")

        content_tab = browser.find_element_by_class_name("slot-selector--tab-content")
        content_tab_html = content_tab.get_attribute("innerHTML")

        content = "{}<hr />".format(content_tab_html)

        browser.implicitly_wait(10)
        print("I'm done with slot: ", i)
        i += 1
        file.write(content)
    print("Go through content is done")

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

    schedule.every(1).hour.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)


init()
