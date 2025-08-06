from . import pl_info

def retrive_mulitiple_courses_pl(page_number: int=1) -> list[dict]:
    """
    Iteratates through all pages until `page_number`.
    Uses `retrieve_courses_info` which scrapes all
    course cards in the given page.

    :param page_number: The last page to iterato to, defaults to 1
    :type page_number: int, optional
    :return: All courses
    :rtype: list[dict]
    """

    base_url = "https://www.pluralsight.com/browse?=&sort=newest&course-category=Software%20Development&page={}&ratings=3.0%20and%20up&categories=course"

    all_courses = []

    for page in range(1,page_number + 1):
        url = base_url.format(page)
        page_of_courses = pl_info.retrieve_courses_info(url)
        all_courses.extend(page_of_courses)

    return all_courses