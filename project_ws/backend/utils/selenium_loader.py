from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def setup_driver():
    """
    Setup the Chrome driver with necessary options.

    :return: WebDriver instance
    :rtype: WebDriver

    """

    options = Options()
    options.add_argument('--disable-gpu')
    options.add_argument("--headless=new")  #new option doesnt work with just headless
    options.add_argument("--user-agent=Mozilla/5.0 ...")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('start-maximized')
    options.binary_location = "/ms-playwright/chromium-1117/chrome-linux/chrome"

    service = Service()  # Only needed if you have a custom chromedriver path
    driver = webdriver.Chrome(options=options)
    return driver


def scrape_with_browser(url):
    """ 
    Decorator to scrape a webpage using Selenium.

    :param url: URL to scrape
    :type url: str

    """

    def decorator(func):
        def wrapper():
            driver = setup_driver()
            try:
                driver.get(url)  ## gets the URL to open the page
                result = func(driver) ## calls the function, for example, retrieve_courses_info
            except Exception as e:
                print(f"Error loading URL {url}: {e}")
                driver.quit()
                raise
            else:
                driver.quit()
                return result 
        return wrapper
    return decorator
