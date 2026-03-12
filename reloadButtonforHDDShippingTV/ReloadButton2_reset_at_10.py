from selenium import webdriver
import datetime
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Step 1: Set up the Selenium WebDriver
driver = webdriver.Chrome()
driver.maximize_window()

# Step 2: Navigate to the website (substitute order ID dynamically)
url = f'REDACTED'
driver.get(url)
#driver.implicitly_wait(5)

# Step 3: Locate the username and password fields using the `name` attribute
username_field = driver.find_element('id', 'email')
password_field = driver.find_element('id', 'password')

# Step 4: Enter your username and password
username_field.send_keys('REDACTED')
password_field.send_keys('REDACTED')

# Step 5: Submit the form (you can press Enter in the password field or find the submit button)
password_field.send_keys(Keys.RETURN)

try:
 # Wait for the page to fully load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@data-tooltip='Refresh']")))

    # Step 6: Wait for the page to load and locate the Refresh button
    while True:
        try:
            refresh_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div.refresh.dashboard.header-icon.longer"))
            )
            refresh_button.click()

            print("Refresh button clicked successfully!")
        except Exception as e:
            print("Error clicking the refresh button:", e)
        # using now() to get current time
        current_time = datetime.datetime.now()
        # get hour of the time
        hour_time = current_time.hour
        print(hour_time)

        #Check if it is past 10pm then close browser
        if hour_time >= 10 and hour_time < 11:
            print("Reset Succesful")
            driver.quit()
            time.sleep(1800)
            driver = webdriver.Chrome()
            driver.maximize_window()

            # Step 2: Navigate to the website (substitute order ID dynamically)
            url = f'REDACTED'
            driver.get(url)
            #driver.implicitly_wait(5)

            # Step 3: Locate the username and password fields using the `name` attribute
            username_field = driver.find_element('id', 'email')
            password_field = driver.find_element('id', 'password')

            # Step 4: Enter your username and password
            username_field.send_keys('REDACTED')
            password_field.send_keys('REDACTED')

            # Step 5: Submit the form (you can press Enter in the password field or find the submit button)
            password_field.send_keys(Keys.RETURN)
             # Wait for the page to fully load
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@data-tooltip='Refresh']")))
        # Wait for 20 minutes before repeating
        time.sleep(1200)
except Exception as e:
    print("Error during initial loading or interaction:", e)

#input("Press Enter to close the browser...")


# Optional: Keep the browser open by not calling driver.quit()

# driver.quit()
