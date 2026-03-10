from selenium import webdriver
import os
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
#import configparser
import csv

from cryptography.fernet import Fernet

#This script Creates a new user in our in house CRM website based on a CSV file.
# Load the encryption key
with open('secret.key', 'rb') as key_file:
    key = key_file.read()

fernet = Fernet(key)

# Load encrypted credentials
with open("creds.txt", "rb") as f:
    lines = f.read().splitlines()

USERNAME = fernet.decrypt(lines[0]).decode()
PASSWORD = fernet.decrypt(lines[1]).decode()

print("Decryption complete")
# Use these in your Selenium login

first_name = []
last_name = []
passwords = []
email = []
def submit():
    # Step 1: Set up the Selenium WebDriver
    driver = webdriver.Chrome()
    driver.maximize_window()
    # Step 2: Navigate to the website (substitute order ID dynamically)
    url = f'REDACTED'
    driver.get(url)
    driver.implicitly_wait(5)
    # Step 3: Locate the username and password fields using the `name` attribute
    username_field = driver.find_element('name', 'username')
    password_field = driver.find_element('name', 'password')
    # Step 4: Enter your username and password
    username_field.send_keys(USERNAME)
    password_field.send_keys(PASSWORD)
    # Step 5: Submit the form (you can press Enter in the password field or find the submit button)
    password_field.send_keys(Keys.RETURN)
    #6 Locating the CRM fields where new user info will be inputed
    first_name_field = driver.find_element('name', 'firstName')
    last_name__field = driver.find_element('name', 'lastName')
    email_field = driver.find_element('name', 'Email')
    passwords_field = driver.find_element('name', 'Password')
    group_field = driver.find_element('name', 'Group')

    time.sleep(10)
    #proccessing the CSV file and placing their values in the appropriate lists
    try:
        with open('REDACTED.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                first_name.append(row['First Name'])
                last_name.append(row['Last Name'])
                passwords.append(row['pwd'])
                email.append(row['Email of New hire'])
        # Sending the values to the appropriate fields on CRM
        for i in range(len(first_name)):
            # re-locate fresh fields each loop
            first_name_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, 'firstName'))
            )
            last_name_field = driver.find_element(By.NAME, 'lastName')
            email_field = driver.find_element(By.NAME, 'Email')
            passwords_field = driver.find_element(By.NAME, 'Password')
            group_field = driver.find_element(By.NAME, 'Group')
            slack_name_field = driver.find_element(By.NAME, 'slackName')
            User_name_field = driver.find_element(By.NAME, 'Username')

            username = first_name[i] + "." + last_name[i]

            # fill in fields
            first_name_field.clear()
            first_name_field.send_keys(first_name[i])
            last_name_field.clear()
            last_name_field.send_keys(last_name[i])
            email_field.clear()
            email_field.send_keys(email[i])
            passwords_field.clear()
            passwords_field.send_keys(passwords[i])
            time.sleep(3)
            select = Select(group_field)
            select.select_by_value("string:salesrep")
            time.sleep(2)
            slack_name_field.clear()
            slack_name_field.send_keys(username)
            User_name_field.clear()
            User_name_field.send_keys(username)

            # click Save Employee
            save_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(@class,'action-button') and normalize-space()='Save Employee']")
                )
            )
            save_button.click()

            time.sleep(3)

            # now check if the error popup appears
            try:
                # wait up to 3 seconds for the modal title "Employee save error (400)"
                error_modal = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, "//h4[@class='modal-title' and contains(text(),'Employee save error')]"))
                )
                print("Duplicate username – skipping this employee.")
            
                # click the OK button on the modal
                ok_button = driver.find_element(By.XPATH, "//button[@class='btn btn-default' and @data-dismiss='modal']")
                ok_button.click()
            
                # skip to next employee
                continue   # <--- inside your for loop
            
            except TimeoutException:
                # no error modal appeared, so continue normally
                pass

            # click Add Another Employee
            add_another_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(@class,'action-button') and normalize-space()='Add Another Employee']")
                )
            )
            add_another_button.click()

            print(f"{first_name[i]} Completed")
            time.sleep(3)

    finally:
        driver.quit()

submit()        

