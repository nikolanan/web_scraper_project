import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import random

# Setup headless Chrome
options = uc.ChromeOptions()
# options.add_argument('--headless=new')  # updated headless mode
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("start-maximized")


driver = uc.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Navigate to Udemy
url = "https://www.udemy.com/courses/it-and-software/other-it-and-software/?p=1&sort=most-reviewed"
driver.get(url)


def scroll_to_bottom(driver, pause_time_range=(3, 6), max_scrolls=20):
    last_height = driver.execute_script("return document.body.scrollHeight")
    scroll_count = 0

    while scroll_count < max_scrolls:
        driver.execute_script("window.scrollBy(0, window.innerHeight * 0.75);")
        scroll_count += 1

        # Random pause to mimic human behavior
        pause_time = random.uniform(*pause_time_range)
        time.sleep(pause_time)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

scroll_to_bottom(driver)

print("Scrolled to bottom of the page.")
# Wait until course cards load using XPath
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//*[contains(@class, "course-list_card__")]'))
        
    )
except Exception as e:
    print("Courses did not load properly:", e)
    driver.quit()
    exit()
print("Course cards loaded successfully.")
# Get course cards using XPath
course_cards = driver.find_elements(By.XPATH, '//*[contains(@class, "course-list_card__")]')
print(f"Found {len(course_cards)} course cards.")
# Extract title from each card
for card in course_cards:
    try:
        title = card.find_element(By.XPATH, './/a').text
        author = card.find_element(By.XPATH, './/div[@class="course-card-instructors_instructor-list__helor"]').text
        rating = card.find_element(By.XPATH, './/span[contains(@class, "ud-heading-sm star-rating_rating-number")]').text
        details = card.find_elements(By.XPATH, './/div[contains(@class, "course-meta-info")]')
        regular_price = card.find_element(By.XPATH, './/div[contains(@class, "course-card_price-text-container")]').text

        print("Course Title:", title)
        # print("Author:", author)
        print("Rating:", rating)
        print("Regular Price:", regular_price)
        
        for detail in details:
            print("Detail:", detail.text)

    except Exception as e:
        print("Error extracting course title:", e)

driver.quit()
