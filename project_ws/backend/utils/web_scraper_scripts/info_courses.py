from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from fastapi import HTTPException
from .. import selenium_loader

URL = "https://www.udemy.com/courses/it-and-software/other-it-and-software/?p=1&sort=most-reviewed"

@selenium_loader.scrape_with_browser(URL)
def retrieve_courses_info(driver):
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//*[contains(@class, "course-list_card__")]'))

        )
    except Exception as e:
        print("Courses did not load properly:", e)
        driver.quit()
        raise HTTPException(status_code=500, detail="Courses did not load properly")
    print("Course cards loaded successfully.")
    # Get course cards using XPath
    course_cards = driver.find_elements(By.XPATH, '//*[contains(@class, "course-list_card__")]')
    print(f"Found {len(course_cards)} course cards.")
    # Extract title from each card
    list_courses = []
    for card in course_cards:
        try:
            title = card.find_element(By.XPATH, './/a').text
            author = card.find_element(By.XPATH, './/div[@class="course-card-instructors_instructor-list__helor"]').text
            rating = card.find_element(By.XPATH, './/span[contains(@class, "ud-heading-sm star-rating_rating-number")]').text
            details = card.find_elements(By.XPATH, './/div[contains(@class, "course-meta-info")]')
            regular_price = card.find_element(By.XPATH, './/div[contains(@class, "course-card_price-text-container")]').text

            list_courses.append({
                "title": title,
                "author": author,
                "rating": rating,
                "regular_price": regular_price,
                "details": [detail.text for detail in details]
            })

        except Exception as e:
            print("Error extracting course title:", e)
    print("Courses information retrieved successfully.")
    return list_courses