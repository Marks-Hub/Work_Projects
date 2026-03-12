# inventory.py (Corrected Structure)

import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import socket
import uuid, re
import platform
import wmi
import psutil
import subprocess
import multiprocessing
import cpuinfo
import math
import shutil


# All the code that gathers information is now INSIDE this function
def fill_google_form():
    # --- Start of Moved Code ---
    # Device Information
    username = os.getlogin()
    computerName = socket.gethostname()
    macAddress = (':'.join(re.findall('..', '%012x' % uuid.getnode()))).upper()

    c = wmi.WMI() # Initialize WMI inside the function

    # Get Windows Edition
    try:
        os_info = c.Win32_OperatingSystem()[0]
        windowsVersionInfo = f"{os_info.Caption} {platform.version()}"
    except Exception as e:
        windowsVersionInfo = f"Error: {e}"

    # Get System Info
    my_system = c.Win32_ComputerSystem()[0]
    manufacturer = my_system.Manufacturer
    model = my_system.Model

    # Get Serial Number
    try:
        serialNumber = c.Win32_BIOS()[0].SerialNumber.strip()
    except Exception as e:
        serialNumber = f"Error: {e}"

    # Get CPU, RAM, and Hard Drive Info
    cores = psutil.cpu_count(logical=False)
    cpuInfoandCores = f"{cores} Cores"
    Ram = f"{math.ceil(psutil.virtual_memory().total / (1024 ** 3))} GB"
    system_drive = os.getenv('SystemDrive') or 'C:'
    HardDrive = f"{math.floor(shutil.disk_usage(system_drive).total / (1024 ** 3))} GB"
    cpu_info_data = cpuinfo.get_cpu_info()
    cpu_brand = cpu_info_data['brand_raw']
    physical_cores = psutil.cpu_count(logical=False)
    logical_cores = psutil.cpu_count(logical=True)
    cpu_frequency = psutil.cpu_freq()
    cpu_information = f"{cpu_brand} Physical cores: {physical_cores}, Logical cores: {logical_cores}, Max CPU Frequency {cpu_frequency.max:.2f} MHz"
    # --- End of Moved Code ---

    try:
        driver = webdriver.Chrome()
        driver.maximize_window()

        url = "https://docs.google.com/forms/d/e/1FAIpQLSdF9rWkrnl58lhkT1f3I45UE2I_-bdqyPFEXOzrf5TO972R1g/viewform"
        driver.get(url)
        time.sleep(2)

        # Fill out form fields
        driver.find_element(By.CSS_SELECTOR, 'input[aria-labelledby="i1 i4"]').send_keys("555789")
        driver.find_element(By.CSS_SELECTOR, 'input[aria-labelledby="i21 i24"]').send_keys(username)
        driver.find_element(By.CSS_SELECTOR, 'input[aria-labelledby="i26 i29"]').send_keys(computerName)
        driver.find_element(By.CSS_SELECTOR, 'input[aria-labelledby="i31 i34"]').send_keys(macAddress)
        driver.find_element(By.CSS_SELECTOR, 'input[aria-labelledby="i36 i39"]').send_keys(windowsVersionInfo)
        driver.find_element(By.CSS_SELECTOR, 'input[aria-labelledby="i41 i44"]').send_keys(manufacturer)
        driver.find_element(By.CSS_SELECTOR, 'input[aria-labelledby="i46 i49"]').send_keys(model)
        driver.find_element(By.CSS_SELECTOR, 'input[aria-labelledby="i51 i54"]').send_keys(serialNumber)
        driver.find_element(By.CSS_SELECTOR, 'input[aria-labelledby="i56 i59"]').send_keys(cpu_information)
        driver.find_element(By.CSS_SELECTOR, 'input[aria-labelledby="i61 i64"]').send_keys(Ram)
        driver.find_element(By.CSS_SELECTOR, 'input[aria-labelledby="i66 i69"]').send_keys(HardDrive)

        print("Please complete the remaining parts of the form and submit it.")
        # ... (rest of your wait loop is the same)
 # Wait until the user manually submits the form
        print("Please complete the remaining parts of the form and submit it.")
        while True:
            try:
                # Detect form submission by checking if we're redirected
                if "formResponse" in driver.current_url:  # URL changes after form submission
                    print("Form submitted successfully!")
                    break
            except Exception as e:
                print(f"Error: {e}")
                break

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'driver' in locals() and driver:
            driver.quit()

# This part is the "safety check"
if __name__ == "__main__":
    # This line is REQUIRED for multiprocessing to work in a frozen app.
    # It must be the first line inside this block.
    multiprocessing.freeze_support()
    fill_google_form()