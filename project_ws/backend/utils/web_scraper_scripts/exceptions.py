class CourseExtractionError(Exception): pass
class TitleExtractionError(CourseExtractionError): pass
class URLExtractionError(CourseExtractionError): pass
class AuthorExtractionError(CourseExtractionError): pass
class RatingExtractionError(CourseExtractionError): pass
class TotalStudentsExtractionError(CourseExtractionError):pass
class DetailsExtractionError(CourseExtractionError): pass
class PriceExtractionError(CourseExtractionError): pass
class OriginalPriceExtractionError(CourseExtractionError): pass
