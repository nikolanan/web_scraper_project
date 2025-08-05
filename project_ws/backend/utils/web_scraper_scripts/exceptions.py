class CourseExtractionError(Exception):
    """
    Base exception for all errors that occur during course data extraction.
    """
    pass

class TitleExtractionError(CourseExtractionError):
    """
    Raised when the course title cannot be extracted from a course card element.
    This typically happens if the element's XPath is not found or its text is empty.
    """
    pass

class URLExtractionError(CourseExtractionError):
    """
    Raised when the course URL cannot be extracted from a course card.
    Indicates a failure to locate the course's link element.
    """
    pass

class AuthorExtractionError(CourseExtractionError):
    """
    Raised when the author information cannot be correctly extracted.
    This can happen if the author element is missing or its text format is unexpected.
    """
    pass

class RatingExtractionError(CourseExtractionError):
    """
    Raised when the course rating could not be found or extracted.
    This may indicate a change in the page's HTML structure.
    """
    pass

class TotalStudentsExtractionError(CourseExtractionError):
    """
    Raised when the total number of students cannot be extracted.
    This could be due to a missing element or unexpected text formatting.
    """
    pass
    
class DetailsExtractionError(CourseExtractionError):
    """
    Raised when details such as course hours, lecture count, or difficulty
    cannot be extracted. This is often caused by a change in the meta-info block's
    structure or content.
    """
    pass

class PriceExtractionError(CourseExtractionError):
    """
    Raised when the current price of the course cannot be extracted.
    """
    pass

class OriginalPriceExtractionError(CourseExtractionError):
    """
    Raised when the original price of the course cannot be extracted,
    and a fallback to the current price is not possible.
    """
    pass
