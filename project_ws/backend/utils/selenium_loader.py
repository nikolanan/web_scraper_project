import undetected_chromedriver as uc
from typing import Callable, Any
from selenium.webdriver.remote.webdriver import WebDriver


def setup_driver():
    """
    Setup the Chrome driver with necessary options using undetected_chromedriver.
    The setup is essential to simulate human-like behaviour in order to 
    prevent anti-bot detection.
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

def scrape_with_browser(func: Callable[WebDriver, Any]) -> Callable[[str], Any]:
    """
    Decorator to wrap a scraping function with a Selenium WebDriver.

    This decorator handles the setup and teardown of a Selenium WebDriver
    instance. It opens a browser, navigates to a specified URL, passes the
    driver to the decorated function for scraping, and then gracefully
    closes the browser regardless of whether an error occurred.

    :param func: The inner function that is wrapped inside the wraper
    :type func: Callable[[WebDriver], Any]
    :returns: A new function (the wrapper) that takes a URL as its only
              argument and returns a type of any
    :rtype: Callable[[str], Any]
    """

    def wrapper(url: str) -> Any:
        driver = setup_driver()
        try:
            driver.get(url) ## gets the URL to open the page
            result = func(driver) ## calls the function, for example, retrieve_courses_info
        except Exception as e:
            print(f"Error loading URL {url}: {e}")
            driver.quit()
            raise
        else:
            driver.quit()
            return result
    return wrapper
