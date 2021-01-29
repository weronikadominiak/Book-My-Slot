import smtplib
import ssl
import schedule
import time

from decouple import config
from selenium import webdriver

emailStr = config("$email")
pwdStr = config("$pwd")


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

    # Find slots
    slots = browser.find_elements_by_class_name("slot-selector--3-week-tab-space")

    # todo: Here put looking for an empty slots once you know how they look
    slots[1].click()


# Send Email

sender_email = "luckyducky.development@gmail.com"
receiver_email = "weronika.dominiak3@gmail.com"
message = """\
From: Lucky Ducky Development <luckyducky.development@gmail.com>
Subject: Yaaay! New Slot!

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
    # Todo: Schedule a job execution
    # https://schedule.readthedocs.io/en/stable/
    def job():
        print("Yooo I'm fine!")

    schedule.every(10).seconds.do(job)
    # schedule.every().day.at("8:01").do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)


open_browser()
send_email()
schedule_job()
