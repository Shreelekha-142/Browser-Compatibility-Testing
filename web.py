import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.common.exceptions import WebDriverException
import time
import requests
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


import re
timeout_seconds = 30
timeout = 10
proxy_extension_path ="proxy.crx"
# Specify the URL of the website you want to test
website_url = "https://www.loc.gov/collections/world-digital-library/about-this-collection/"

def check_website_loaded_slow_connection():
    try:
        # Initialize Chrome web driver with specified options
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        driver = webdriver.Chrome(options=chrome_options)

        # Set network conditions to simulate a slow 3G connection
        driver.set_network_conditions(
            offline=False,
            latency=200,  # 200 ms delay
            download_throughput=250 * 1024,  # 250 KB/s download speed
            upload_throughput=250 * 1024  # 250 KB/s upload speed
        )

        # Load the website
        driver.get(website_url)

        # Wait for the page to load (you can customize the wait time)
        driver.implicitly_wait(10)

        # Check if the page is fully loaded
        fully_loaded = driver.execute_script("return (document.readyState === 'complete')")
        if fully_loaded:
            result_label.config(text="Website fully loaded under a slow connection")
        else:
            result_label.config(text="Website loaded partially under a slow connection")

    except WebDriverException as e:
        result_label.config(text=f"Error: {str(e)}")
    finally:
        driver.quit()

def check_website_rendered():
    try:
        # Launch a headless browser
        browser = webdriver.Chrome()

        # Create a new page
        page = browser.get(website_url)
        time.sleep(10)  # Wait for the page to load

        # Capture a screenshot
        screenshot = browser.get_screenshot_as_png()

        if screenshot:
            result_label.config(text="Website is rendered on a slow connection.")
        else:
            result_label.config(text="Website is not rendered on a slow connection")
    except WebDriverException as e:
        result_label.config(text=f"Error: {str(e)}")
from selenium import webdriver
from selenium.webdriver.common.by import By

def check_important_element_rendering():
    try:
        # Initialize a Chrome web driver
        driver = webdriver.Chrome()

        # Set network conditions to simulate a slow 3G connection
        driver.set_network_conditions(
            offline=False,
            latency=200,  # 200 ms delay
            download_throughput=250 * 1024,  # 250 KB/s download speed
            upload_throughput=250 * 1024  # 250 KB/s upload speed
        )

        # Navigate to the website URL
        driver.get(website_url)

        # Wait for the page to load (you can customize the wait time)
        driver.implicitly_wait(10)

        # Check for the presence of an important element by its ID
        important_element = driver.find_element(By.CLASS_NAME, 'header')

        if important_element.is_displayed():
            result_label.config(text="Important element is rendered on the slow connection.")
        else:
            result_label.config(text="Important element is not rendered on the slow connection.")

    except WebDriverException as e:
        result_label.config(text=f"Error: {str(e)}")
    finally:
        driver.quit()

def open():
        driver = webdriver.Chrome()
        start_time = time.time()
        driver.get(website_url)
        end_time = time.time()
        rendering_time = end_time - start_time
        result_label.config(text=f"Rendering time on slow connection: {rendering_time:.2f} seconds")

        driver.quit()
      
    

def check_isp_speed_affects_rendering():
    timeout_seconds = 30
    try:
        driver = webdriver.Chrome()

        driver.set_network_conditions(
            offline=False,
            latency=100,  # 100 ms latency
            download_throughput=50 * 1024,  # 50 KB/s download speed
            upload_throughput=50 * 1024  # 50 KB/s upload speed
        )

        start_time = time.time()
        driver.get(website_url)
        end_time = time.time()

        rendering_time = end_time - start_time
        result_label.config(text=f"Rendering time on slow connection: {rendering_time:.2f} seconds")

        driver.quit()
    except WebDriverException as e:
        result_label.config(text=f"Error: {str(e)}")

def set_network_conditions(driver, latency, download_throughput, upload_throughput):
    # Enable Chrome DevTools
    driver.execute_cdp_cmd('Network.enable', {})

    # Set network conditions
    driver.execute_cdp_cmd('Network.emulateNetworkConditions', {
        'offline': False,
        'latency': latency,  # Latency in milliseconds
        'downloadThroughput': download_throughput,  # Download speed in bytes per second
        'uploadThroughput': upload_throughput  # Upload speed in bytes per second
    })

def check_browser_responsiveness():
    chrome_options = Options()
    # chrome_options.add_argument('--headless')

    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get("https://www.google.com")

        set_network_conditions(driver, latency=75, download_throughput=1024, upload_throughput=512)

        search_box = driver.find_element(By.NAME, 'q')
        search_box.send_keys('Python Selenium')
        search_box.send_keys(Keys.RETURN)

        # Wait for the search results to load (adjust the timeout as needed)
        # seconds
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID, 'search')))

        # Check browser responsiveness
        # You can add additional checks or conditions based on your requirements
        # For example, check if a specific element is present on the page
        if "Python Selenium" in driver.page_source:
            result_text = f"{driver.capabilities['browserName']} browser is responsive to slow connection\n"
            result_label.config(text=result_text)
        else:
            result_text = f"{driver.capabilities['browserName']} browser is not responsive to slow connection\n"
            result_label.config(text=result_text)

    except TimeoutException:
        # If there is a timeout, print a timeout message
        result_text = f"Timeout: The browser did not respond within {timeout} seconds\n"
        result_label.config(text=result_text)

    finally:
        driver.quit()



def test_alternative_browsers():
    alternative_browsers = ["chrome", "edge", "firefox"]
    result_text = ""
    for browser in alternative_browsers:
        try:
            if browser.lower() == "chrome":
                driver = webdriver.Chrome()
            elif browser.lower() == "edge":
                driver = webdriver.Edge()
            elif browser.lower() == "firefox":
                driver = webdriver.Firefox()
            else:
                result_text += f"Unsupported browser: {browser}\n"
                continue

            driver.get(website_url)
            title_element = driver.title
            if title_element:
                result_text += f"{browser} successfully accessed the website.\n"
            else:
                result_text += f"{browser} encountered an error.\n"
            driver.quit()
        except WebDriverException as e:
            result_text += f"Error with {browser}: {str(e)}\n"
    result_label.config(text=result_text)


def access_website_with_proxy_extension(proxy_extension_path):
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_extension(proxy_extension_path)
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(website_url)
        result_label.config(text="Successfully accessed the website using the proxy extension.")
    except WebDriverException as e:
        result_label.config(text=f"Error: {str(e)}")



def check_firewall_block():
    try:
        response = requests.get(website_url, timeout=timeout_seconds)
        if response.status_code == 200:
            result_label.config(text="The website is accessible (not blocked by a firewall).")
        else:
            result_label.config(text=f"The website may be blocked. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        result_label.config(text=f"Failed to access the website: {str(e)}")

# Create a tkinter window
root = tk.Tk()


root.title("Library Search System Test")
# Heading
heading_label = tk.Label(root, text="Browser Compatibility Testing Based on Network Connection", font=('Helvetica', 14, 'bold'), bg='#3498db', fg='white')
heading_label.pack(pady=10)
# Increase font size for buttons and labels
button_font = ('Helvetica', 12)
label_font = ('Helvetica', 10)

# Add space between buttons
button_padding_y = 5

check_partial_button = tk.Button(root, text="Check Partial Loading", command=check_website_loaded_slow_connection, font=button_font)
check_browser_button = tk.Button(root, text="Check Browser Response", command=check_website_rendered, font=button_font)
check_Element_button = tk.Button(root, text="Check Elements Rendered", command=check_important_element_rendering, font=button_font)
check_speed = tk.Button(root, text="Check Speed", command=open, font=button_font)
check_isp_speed_button = tk.Button(root, text="Check ISP Speed Affects Rendering", command=check_isp_speed_affects_rendering, font=button_font)
check_browser_responsive_button = tk.Button(root, text="Check Browser Responsive to Slow Connection", command=check_browser_responsiveness, font=button_font)
test_alternative_browsers_button = tk.Button(root, text="Test Alternative Browsers", command=test_alternative_browsers, font=button_font)
# access_without_proxies_button = tk.Button(root, text="Access Without Proxies/VPN", command=access_website_without_proxies, font=button_font)

access_with_proxies_button = tk.Button(root, text="Access With Proxies Extensions", command=lambda: access_website_with_proxy_extension(proxy_extension_path), font=button_font)

check_firewall_block_button = tk.Button(root, text="Check Firewall Block", command=check_firewall_block, font=button_font)
result_label = tk.Label(root, text="", font=label_font)

# Place the buttons and labels in the window with padding
check_partial_button.pack(pady=button_padding_y)
check_browser_button.pack(pady=button_padding_y)
check_Element_button.pack(pady=button_padding_y)
check_speed.pack(pady=button_padding_y)
check_isp_speed_button.pack(pady=button_padding_y)

test_alternative_browsers_button.pack(pady=button_padding_y)
# access_without_proxies_button.pack(pady=button_padding_y)

access_with_proxies_button.pack(pady=button_padding_y)

check_firewall_block_button.pack(pady=button_padding_y)
check_browser_responsive_button.pack(pady=button_padding_y)
result_label.pack()

# Start the tkinter main loop
root.mainloop()

