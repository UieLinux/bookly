import re
from wtforms import ValidationError

isbn_pattern = re.compile('^(?:ISBN[-:]? ?)?(?:(?:\d+[- ]?){3}[\dX]|(?:\d+[- ]?){4}\d)$', re.I)


def extract_digits_from_value(value):
    """
    Creates a list with all the digits found inside value.
    """
    digits = [int(char) for char in value if char.isdigit()]

    # In ISBN-10 the last char can be sometimes X which is the roman number ten
    if len(digits) == 9 and re.match('[xX]$', value):
        digits.append(10)

    return digits


def validate_isbn10_checksum(digits):
    """
    For details see the Wikipedia article
    http://en.wikipedia.org/wiki/International_Standard_Book_Number#ISBN-10_check_digit_calculation
    """
    return (sum((10 - i) * digit for i, digit in enumerate(digits)) % 11) == 0


def validate_isbn13_checksum(digits):
    """
    For details see the Wikipedia article
    http://en.wikipedia.org/wiki/International_Standard_Book_Number#ISBN-13_check_digit_calculation
    """
    return ((sum(digits[::2]) + sum(x * 3 for x in digits[1::2])) % 10) == 0


def validate_checksum(digits):
    """
    ISBN-10 and ISBN-13 don't use the same algorithm
    """
    if len(digits) == 10:
        return validate_isbn10_checksum(digits)
    else:
        return validate_isbn13_checksum(digits)


def valid_isbn(form, field):
    """
    International Standard Book Number (ISBN) Validator.

    This validator works with both the ten an thirteen digits variants of the ISBN code. The first
    check uses a regexp to see if the value of the field looks valid. If the regexp matches then
    the checksum is calculated and confronted with the check digit.
    """
    if not isbn_pattern.match(field.data):
        raise ValidationError('Does not looks like an ISBN code')

    digits = extract_digits_from_value(field.data)

    if not (len(digits) == 10 or len(digits) == 13):
        raise ValidationError('Wrong number of digits')

    if not validate_checksum(digits):
        raise ValidationError('Wrong checksum')
