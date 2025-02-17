import selenium
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import datetime
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def run_script():
    try:
        # Path to chromedriver
        service = Service(r"C:\Users\mokin\ChromeDriver\chromedriver-win64\chromedriver-win64\chromedriver.exe")

        # Initialize Chrome driver
        driver = webdriver.Chrome(service=service)
        driver.maximize_window()

        # Step 2: Navigate to the website (substitute order ID dynamically)
        url = f'https://app.periscopedata.com/app/rush-order-tees/1226565/Ninja-Transfers-Shipping'
        driver.get(url)

        # Step 3: Locate the username and password fields using the `name` attribute
        username_field = driver.find_element('id', 'email')
        password_field = driver.find_element('id', 'password')

        # Step 4: Enter your username and password
        username_field.send_keys('productionfloor@printfly.com')
        password_field.send_keys('Printer1234%')

        # Step 5: Submit the form
        password_field.send_keys(Keys.RETURN)

        # Wait for the page to fully load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@data-tooltip='Refresh']")))

        print("Successfully logged in and page loaded.")

        # Step 6: Continuous refresh loop
        while True:
            current_time = datetime.datetime.now()
            try:
                refresh_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "div.refresh.dashboard.header-icon.longer"))
                )
                refresh_button.click()
                print(f"Refresh button clicked at {current_time.strftime('%H:%M:%S')}!")
            except Exception as e:
                print("Error clicking the refresh button:", e)
                break

            # Wait for 20 minutes before refreshing again
            time.sleep(1200)

    except Exception as e:
        print("Error during initial loading or interaction:", e)

    finally:
        driver.quit()
        print("Browser closed. Will restart tomorrow.")

while True:
    run_script()
