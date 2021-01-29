import smtplib
import ssl

from decouple import config
from selenium import webdriver

emailStr = config("$email")
pwdStr = config("$pwd")

# Open the browser
browser = webdriver.Chrome()
browser.get(("https://www.tesco.com/groceries/en-GB/slots/delivery"))

#Fill in user data
userField = browser.find_element_by_id('username')
userField.send_keys(emailStr)
pwdFileld = browser.find_element_by_id('password')
pwdFileld.send_keys(pwdStr)

# Find button
loginBtn = browser.find_element_by_class_name("ui-component__button")
loginBtn.click()

# Find slots
slots = browser.find_elements_by_class_name("slot-selector--3-week-tab-space")

### todo: Here put looking for an empty slots once you know how they look
slots[1].click()

# Email sending
sender_email = "luckyducky.development@gmail.com"
receiver_email = "weronika.dominiak3@gmail.com"
message = """\
From: Lucky Ducky Development <luckyducky.development@gmail.com>
Subject: Yaaay! New Slot!

Hello, I booked a slot for you!

This message is sent from Python."""

port = 465  # for SSL

# Create a secure SSL context
context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login(sender_email, pwdStr)
    server.sendmail(sender_email, receiver_email, message)
