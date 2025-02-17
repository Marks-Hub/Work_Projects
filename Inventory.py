import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import socket
import uuid, re
import platform
import wmi
import psutil
#import cpuinfo
import math
import shutil


# Device Information
username = os.getlogin()
computerName = socket.gethostname()
macAddress = (':'.join(re.findall('..', '%012x' % uuid.getnode()))).upper()

def get_windows_edition():
    try:
        c = wmi.WMI()
        os_info = c.Win32_OperatingSystem()[0]
        return f"{os_info.Caption} {platform.version()}"
    except Exception as e:
        return f"Error: {e}"

windowsVersionInfo = get_windows_edition()

c = wmi.WMI()
my_system = c.Win32_ComputerSystem()[0]
manufacturer = my_system.Manufacturer
model = my_system.Model

def get_serial_number():
    try:
        return c.Win32_BIOS()[0].SerialNumber.strip()
    except Exception as e:
        return f"Error: {e}"

serialNumber = get_serial_number()

cores = psutil.cpu_count(logical=False)

'''def get_cpu_info():
    try:
        return cpuinfo.get_cpu_info()['brand_raw']
    except Exception as e:
        return f"Error: {e}"

cpuInformation = get_cpu_info()'''
cpuInfoandCores = f"{cores} Cores"

Ram = f"{math.ceil(psutil.virtual_memory().total / (1024 ** 3))} GB"
HardDrive = f"{math.floor(shutil.disk_usage('/').total / (1024 ** 3))} GB"

def fill_google_form():
    try:
        driver = webdriver.Chrome()  # Add executable_path if needed
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
        driver.find_element(By.CSS_SELECTOR, 'input[aria-labelledby="i56 i59"]').send_keys(cpuInfoandCores)
        driver.find_element(By.CSS_SELECTOR, 'input[aria-labelledby="i61 i64"]').send_keys(Ram)
        driver.find_element(By.CSS_SELECTOR, 'input[aria-labelledby="i66 i69"]').send_keys(HardDrive)

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

            time.sleep(1)  # Check every 1 second

    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    fill_google_form()

'''def get_cpu_info():
    print("CPU Information:")
    print(f"Processor: {platform.processor()}")
    print(f"Machine: {platform.machine()}")
    print(f"System: {platform.system()} {platform.release()}")
    print(f"Architecture: {platform.architecture()[0]}")
    print(f"CPU Cores: {psutil.cpu_count(logical=False)}")  # Physical cores
    print(f"Logical CPUs: {psutil.cpu_count(logical=True)}")  # Logical cores (with hyperthreading)
    print(f"CPU Frequency: {math.floor(psutil.cpu_freq().max)} MHz")  # Max frequency
    print("CPU Usage per Core:")
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        print(f"Core {i + 1}: {percentage}%")
    print(f"Overall CPU Usage: {psutil.cpu_percent()}%")

if __name__ == "__main__":
    get_cpu_info()
'''