from enum import Enum


class ParsingMode(Enum):
    NO_FETCHING = 1 # Parse all data
    READ_FIRST_ALL = 2 # Parse all data but fetch only the data that is not stored locally
    UPDATE = 3 # Parse all data but fetch only data from this year and last year
    ALL = 4 # Fetch all data