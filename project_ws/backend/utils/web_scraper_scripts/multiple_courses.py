from . import info_courses
from . import pl_info
from enum import Enum

BASE_URL_UDEMY = "https://www.udemy.com/courses/it-and-software/other-it-and-software/?p={}&sort=most-reviewed"
BASE_URL_PLURALSIGHT = "https://www.pluralsight.com/browse?=&sort=newest&course-category=Software%20Development&page={}&ratings=3.0%20and%20up&categories=course"

class WebPlatform(str, Enum):
    udemy = "udemy"
    pluralsight = "pluralsight"

def retrive_mulitiple_courses(web_platform:str, start_page: int=1, end_page:int=1) -> list[dict]:
    """
    Retrieves multiple pages of courses from a specified web platform.

    :param web_platform: The platform to scrape from.
    :param start_page: The starting page number for scraping (inclusive).
    :param end_page: The ending page number for scraping (inclusive).
    :return: A list of dictionaries, where each dictionary represents a cours
    """

    all_courses = []
    
    platform_map = {
        WebPlatform.udemy: {
            "base_url": BASE_URL_UDEMY,
            "scraper": info_courses.retrieve_courses_info,
            "last_page": info_courses.last_page
        },
        WebPlatform.pluralsight: {
            "base_url": BASE_URL_PLURALSIGHT,
            "scraper": pl_info.retrieve_courses_info,
            "last_page": pl_info.last_page
        }
    }
    config = platform_map.get(web_platform.lower().strip())
    if not config:
        print(f"Error: Invalid web platform '{web_platform}' specified.")
        return []

    last_page = config["last_page"](config["base_url"].format(1))

    if end_page > last_page:
        end_page = last_page

    for page in range(start_page, end_page + 1):
        url = config["base_url"].format(page)
        page_of_courses = config["scraper"](url)
        all_courses.extend(page_of_courses)

    return all_courses