import re
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from fastapi import HTTPException
from .. import selenium_loader
from .exceptions import *

@selenium_loader.scrape_with_browser
def last_page(driver: WebDriver) -> int:
    """
    Find the last page number in a paginated course list.

    This function uses a Selenium WebDriver to locate all elements with a `data-page` attribute,
    extracts their integer values, and returns the highest value found.

    :param driver: Selenium WebDriver instance used for scraping.
    :type driver: WebDriver
    :return: The highest page number found (at least 1).
    :rtype: int
    """

    pagination_elements = driver.find_elements(By.XPATH, '//span[contains(@class,"pagination-page__number"])')

    max_page = 1
    for el in pagination_elements:
        try:
            page = int(el.get_attribute("data-page"))
            if page > max_page:
                max_page = page
        except (ValueError, TypeError):
            continue
    return max_page

@selenium_loader.scrape_with_browser
def retrieve_courses_info(driver: WebDriver) -> list[dict]:
    """
    Scrape Pluralsight labs/course information from a search results page.
    """
    # try:
    #     # A more robust way to handle the cookie button
    #     accept_btn = WebDriverWait(driver, 10).until(
    #         EC.element_to_be_clickable((By.XPATH, '//button[text()="Accept all cookies" or contains(text(), "Accept")]'))
    #     )
    #     accept_btn.click()
    #     print("Accepted cookies")
    # except Exception:
    #     print("No cookie popup detected")
    actions = ActionChains(driver)

    # Press the Enter key
    actions.send_keys(Keys.ENTER)

    # Perform the action
    actions.perform()
    time.sleep(3)
    driver.save_screenshot("debug.png")
    try:
        WebDriverWait(driver, 40).until(
            EC.presence_of_all_elements_located((By.XPATH, '//li[contains(@class,"browse-search-results-item")]'))
        )
    except Exception as e:
        print("Courses did not load properly:", e)
        driver.quit()
        raise HTTPException(status_code=500, detail="Courses did not load properly")
    print("Course cards loaded successfully.")
    
    course_cards = driver.find_elements(By.XPATH, '//li[contains(@class,"browse-search-results-item")]')
    print(f"Found {len(course_cards)} course cards.")
    time.sleep(2)

    list_courses = []
    for card in course_cards:
        list_courses.append(extract_course_data(card))

    print("Courses information retrieved successfully.")
    return list_courses


# def extract_course_data(card: WebElement) -> dict:
#     """
#     Extract information from a single Pluralsight course/lab search result <li>.
#     Returns Udemy-like structure for database compatibility.
#     """

#     title = None
#     target_url = None
#     authors_list = None
#     rating = None
#     total_students = None
#     current_price = None
#     original_price = None
#     total_hours = None
#     number_of_lectures = None
#     difficulty = None

#     try:
#         try:
#             link_element = card.find_element(By.XPATH, './/a')
#             target_url = link_element.get_attribute("href")
#         except Exception as e:
#             raise URLExtractionError(f"Failed to extract course URL: {e}")

#         try:
#             title = card.find_element(By.XPATH, './/div[contains(@class,"course-details__title")]').text
#         except Exception as e:
#             raise TitleExtractionError(f"Failed to extract course title: {e}")

#         try:
#             author = card.find_element(By.XPATH, './/div[contains(@class,"course-details__author")]').text.replace("by ","")
#             authors_list = [author]
#         except Exception as e:
#             raise AuthorExtractionError(f"Failed to extract authors: {e}")

#         try:
#             difficulty = card.find_element(By.XPATH, './/span[@id="courseLevel"]').text
#         except Exception:
#             difficulty = None

#         try:
#             duration_text = card.find_element(By.XPATH, './/span[contains(@class,"duration")]').text
#             # convert "46m" or "2h 30m" to total hours float
#             hours = re.findall(r'(\d+(?:\.\d+)?)h', duration_text)
#             mins = re.findall(r'(\d+)m', duration_text)
#             total_hours = float(hours[0]) if hours else (float(mins[0]) / 60 if mins else None)
#         except Exception:
#             total_hours = None

#     except CourseExtractionError as e:
#         print(str(e))

#     finally:
#         return {
#             "title": title,
#             "target_url": target_url,
#             "author": authors_list,
#             "rating": rating,
#             "total_students": total_students,
#             "current_price": current_price,
#             "original_price": original_price,
#             "hours_required": total_hours,
#             "lectures_count": number_of_lectures,
#             "difficulty": difficulty
#         }

def extract_course_data(card: WebElement) -> dict:
    """
    Extract information from a single Pluralsight course/lab search result <li>.
    Returns Udemy-like structure for database compatibility.
    """

    title = None
    target_url = None
    authors_list = None
    rating = None
    total_students = None
    current_price = None
    original_price = None
    total_hours = None
    number_of_lectures = None
    difficulty = None

    try:
        try:
            link_element = card.find_element(By.XPATH, './/a')
            target_url = link_element.get_attribute("href")
        except Exception as e:
            raise URLExtractionError(f"Failed to extract course URL: {e}")

        try:
            title = card.find_element(By.XPATH, './/div[@class="course-details__title"]').text
        except Exception as e:
            raise TitleExtractionError(f"Failed to extract course title: {e}")

        try:
            author = card.find_element(By.XPATH, './/div[@class="course-details__author"]').text.replace("by ", "")
            authors_list = [author]
        except Exception as e:
            raise AuthorExtractionError(f"Failed to extract authors: {e}")

        try:
            difficulty = card.find_element(By.XPATH, './/span[@id="courseLevel"]').text
        except Exception:
            difficulty = None

        try:
            duration_text = card.find_element(By.XPATH, './/span[@class="duration course-details__level"]').text
            # convert "2h 36m" to float
            hours = re.findall(r'(\d+(?:\.\d+)?)h', duration_text)
            mins = re.findall(r'(\d+)m', duration_text)
            total_hours = float(hours[0]) if hours else (
                float(mins[0]) / 60 if mins else None
            )
        except Exception:
            total_hours = None

        # ⭐ Rating and students extraction without contains()
        try:
            stars = card.find_elements(By.XPATH, './/i[@class="fa fa-star"]')
            rating = float(len(stars)) if stars else None
        except Exception:
            rating = None

        try:
            students_span = card.find_element(By.XPATH, './/div[@class="course-details__rating"]/span')
            students_text = students_span.text
            total_students = (
                int(re.sub(r"[^\d]", "", students_text)) if students_text else None
            )
        except Exception:
            total_students = None

    except CourseExtractionError as e:
        print(str(e))

    finally:
        return {
            "title": title,
            "target_url": target_url,
            "author": authors_list,
            "rating": rating,
            "total_students": total_students,
            "current_price": current_price,
            "original_price": original_price,
            "hours_required": total_hours,
            "lectures_count": number_of_lectures,
            "difficulty": difficulty,
        }

