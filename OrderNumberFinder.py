from selenium import webdriver
import os
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import tkinter as tk
import configparser

# Create the main window
window = tk.Tk()
window.title("Enter Oder ID")
window.geometry("400x300")

# Label
tk.Label(window, text="Enter Order ID").pack()

# Create a StringVar to store the user input
order_id_var = tk.StringVar()

# Entry widget for user input
tk.Entry(window, textvariable=order_id_var).pack()

# Function to get the input and print it (or use it later)
def submit():
    order_id = order_id_var.get()
    print(f"Order ID entered: {order_id}")
    # You can now use the order_id variable in your program
    
    # Step 1: Set up the Selenium WebDriver
    driver = webdriver.Chrome()
    driver.maximize_window()

   # Step 2: Navigate to the website (substitute order ID dynamically)
    url = f'REDACTED/{order_id}'
    driver.get(url)
    driver.implicitly_wait(5)


    # Step 3: Locate the username and password fields using the `name` attribute
    username_field = driver.find_element('name', 'username')
    password_field = driver.find_element('name', 'password')

    # Step 4: Enter your username and password
    username_field.send_keys('REDACTED')
    password_field.send_keys('REDACTED')

    # Step 5: Submit the form (you can press Enter in the password field or find the submit button)
    password_field.send_keys(Keys.RETURN)

    time.sleep(5)
    try:
        # Switch to the iframe
        WebDriverWait(driver, 20).until(
            EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe"))
        )
        # Click the correct "Automated Notes" button for Production Notes
        production_notes_section = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//strong[text()='Production Notes']/following-sibling::a[contains(@ng-click, 'toggleAutomatedProductionNotes')]"))
        )
        '''driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", production_notes_section)
        time.sleep(1)  # Optional: small delay to ensure smooth scrolling'''
        production_notes_section.click()
            
        #time.sleep(5)
        # Locate all elements with class 'notes-body'
        notes_bodies = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "notes-body"))
        )

        # Process each 'notes-body' element to extract the file path
        for index, notes_body in enumerate(notes_bodies):
            text_content = notes_body.text.strip()

            # Remove the "Production Files located in:" prefix
            if "Production Files located in:" in text_content:
                file_path = text_content.replace("Production Files located in:", "").strip()
                print(f"File path {index + 1}: {file_path}")

                # Step 6: Open the path in Windows File Explorer
                if os.path.exists(file_path):
                    os.startfile(file_path)
                else:
                    print(f"Path does not exist for file path {index + 1}.")
            else:
                print(f"Text in notes-body {index + 1} does not contain a file path.")
        #print(file_path.split('Production Files located in:\n'))
        print('File Path:' + file_path)

        # Step 4: Open the path in Windows File Explorer
        if os.path.exists(file_path):
            os.startfile(file_path)
        else:
            print("Path does not exist.")

    finally:
        driver.quit()
# Button to submit the input
tk.Button(window, text="Submit", command=submit).pack()

# Start the Tkinter event loop
window.mainloop()

