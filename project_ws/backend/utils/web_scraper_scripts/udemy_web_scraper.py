import re
import time
from ..logger import logger_setup
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
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

    pagination_elements = driver.find_elements(By.XPATH, '//*[@data-page]')

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
    Scrape course information from a course listing page.

    Waits for course cards to load, then extracts information from each card using
    the `extract_course_data` function.

    Logging is used to track the procces

    :param driver: Selenium WebDriver instance used for scraping.
    :type driver: WebDriver
    :raises HTTPException: If course cards do not load properly.
    :return: A list of dictionaries, each containing information about a course.
    :rtype: list[dict]
    """

    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, '//*[contains(@class, "course-list_card__")]'))

        )
    except Exception as e:
        logging.error(f"Courses did not load properly: {e}")
        driver.quit()
        raise HTTPException(status_code=500, detail="Courses did not load properly")

    logging.info("Course cards loaded successfully.")

    # Get course cards using XPath
    course_cards = driver.find_elements(By.XPATH, '//*[contains(@class, "course-list_card__")]')
    logging.info(f"Found {len(course_cards)} course cards.")
    ##Delay to load
    time.sleep(2)

    # Extract title from each card
    list_courses = []
    for card in course_cards:
        course_info = extract_course_data(card)
        list_courses.append(course_info)

    logging.info("Courses information retrieved successfully.")
    return list_courses

def extract_course_data(card: WebElement) -> dict:
    """
    Extract detailed information from a single course card element.

    Attempts to extract the course title, URL, authors, rating, number of students,
    hours required, number of lectures, difficulty, current price, and original price.
    Handles and logs extraction errors for each field.

    :param card: Selenium WebElement representing a course card.
    :type card: selenium.webdriver.remote.webelement.WebElement
    :return: A dictionary with course information fields.
    :rtype: dict
    """

    title = None
    target_url = None
    authors_list = None
    rating = None
    total_students = None
    total_hours = None
    number_of_lectures = None
    difficulty = None
    current_price = 0
    original_price = 0

    try:
        try:
            link_element = card.find_element(By.XPATH, './/a')
            target_url = link_element.get_attribute("href")
        except Exception as e:
            raise URLExtractionError(f"Failed to extract course URL: {e}")

        try:
            title = card.find_element(By.XPATH, './/a').text
        except Exception as e:
            raise TitleExtractionError(f"Failed to extract course title: {e}")

        try:
            authors = card.find_element(By.XPATH, './/div[@class="course-card-instructors_instructor-list__helor"]').text
            authors_list = authors.split(", ")
        except Exception as e:
            raise AuthorExtractionError(f"Failed to extract authors: {e}")

        try:
            rating = card.find_element(By.XPATH, './/span[contains(@class, "ud-heading-sm star-rating_rating-number")]').text
        except Exception as e:
            raise RatingExtractionError(f"Failed to extract rating: {e}")

        try:
            total_students = card.find_element(By.XPATH, './/span[contains(@aria-label, "reviews")]').text
            total_students = total_students[1:-1]
        except Exception as e:
            raise TotalStudentsExtractionError(f"Failed to extract number of students {e}")

        try:
            details = card.find_elements(By.XPATH, './/div[contains(@class, "course-meta-info")]')
            lines = details[0].text.split("\n")
            total_hours = re.search(r'\d+(\.\d+)?', lines[0]).group()
            number_of_lectures = re.search(r'\d+(\.\d+)?', lines[1]).group()
            difficulty = lines[2]
        except Exception as e:
            raise DetailsExtractionError(f"Failed to extract details (hours, lectures, difficulty): {e}")

        try:
            current_price_text = card.find_element(By.XPATH, './/div[@data-purpose="course-price-text"]').text
            current_price = current_price_text.split("\n")[-1]
            if current_price == "Free":
                current_price = "0"
        except Exception as e:
            raise PriceExtractionError(f"Failed to extract current price: {e}")

        try:
            original_price_text = card.find_element(By.XPATH, './/div[@data-purpose="course-old-price-text"]').text
            original_price = original_price_text.split("\n")[-1]
            if original_price == "Free":
                original_price = "0"
        except Exception as e:
            original_price = current_price
            raise OriginalPriceExtractionError(f"Failed to extract original price: {e}")

    except CourseExtractionError as e:
        logging.error(f"{str(e)}")
        
    finally:
        card_batch = {
            "title": title,
            "target_url": target_url,
            "author": authors_list,
            "rating": rating,
            "total_students":total_students,
            "current_price": current_price,
            "original_price": original_price,
            "hours_required": total_hours,
            "lectures_count": number_of_lectures,
            "difficulty": difficulty
        }
        logging.info(card_batch)

        return card_batch