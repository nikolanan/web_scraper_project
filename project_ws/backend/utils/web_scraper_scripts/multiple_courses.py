from . import info_courses

def retrive_mulitiple_courses(page_number: int=1) -> list[dict]:
    """
    Iteratates through all pages until `page_number`.
    Uses `retrieve_courses_info` which scrapes all
    course cards in the given page.

    :param page_number: The last page to iterato to, defaults to 1
    :type page_number: int, optional
    :return: All courses
    :rtype: list[dict]
    """

    base_url = "https://www.udemy.com/courses/it-and-software/other-it-and-software/?p={}&sort=most-reviewed"

    all_courses = []

    for page in range(1,page_number + 1):
        url = base_url.format(page)
        page_of_courses = info_courses.retrieve_courses_info(url)
        all_courses.extend(page_of_courses)

    return all_courses