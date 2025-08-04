from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import undetected_chromedriver as uc


def setup_driver():
    """
    Setup the Chrome driver with necessary options using undetected_chromedriver.
    """

    options = uc.ChromeOptions()
    options.add_argument('--disable-gpu')
    options.add_argument("--headless=new")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('start-maximized')

    driver = uc.Chrome(options=options, headless=True)
    return driver

# def scrape_with_browser(url):
#     """ 
#     Decorator to scrape a webpage using Selenium.

#     :param url: URL to scrape
#     :type url: str

#     """

#     def decorator(func):
#         def wrapper():
#             driver = setup_driver()
#             try:
#                 driver.get(url)  ## gets the URL to open the page
#                 result = func(driver) ## calls the function, for example, retrieve_courses_info
#             except Exception as e:
#                 print(f"Error loading URL {url}: {e}")
#                 driver.quit()
#                 raise
#             else:
#                 driver.quit()
#                 return result
#         return wrapper
#     return decorator

def scrape_with_browser(func):
    def wrapper(url):
        driver = setup_driver()
        try:
            driver.get(url)
            result = func(driver)
        except Exception as e:
            print(f"Error loading URL {url}: {e}")
            driver.quit()
            raise
        else:
            driver.quit()
            return result
    return wrapper
