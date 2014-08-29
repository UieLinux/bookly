import unittest
from wtforms import ValidationError
from isbn import (valid_isbn, extract_digits_from_value, validate_isbn10_checksum,
                  validate_isbn13_checksum, validate_checksum, isbn_pattern)


class MockField:
    def __init__(self, data):
        self.data = data


class IsbnTest(unittest.TestCase):
    VALID_ISBN13_STRING = "ISBN: 978-0-451-45799-8"
    VALID_ISBN13_DIGITS = [9, 7, 8, 0, 4, 5, 1, 4, 5, 7, 9, 9, 8]
    VALID_ISBN10_STRING = "ISBN: 0-471-43809-X"
    VALID_ISBN10_DIGITS = [0, 4, 7, 1, 4, 3, 8, 0, 9, 10]
    WRONG_ISBN13_DIGITS = [9, 7, 8, 1, 1, 2, 6, 4, 1, 8, 9, 0, 1]
    WRONG_ISBN10_DIGITS = [0, 8, 1, 9, 9, 3, 1, 9, 2, 3]

    def test_extract_digits_from_value_ignore_letters(self):
        result = extract_digits_from_value(self.VALID_ISBN13_STRING)
        self.assertListEqual(self.VALID_ISBN13_DIGITS, result)

    def test_extract_digits_from_value_convert_x_to_10(self):
        result = extract_digits_from_value(self.VALID_ISBN10_STRING)
        self.assertListEqual(self.VALID_ISBN10_DIGITS, result)

    def test_extract_digits_from_value_convert_x_to_10_only_for_isbn10(self):
        expected = [9, 7, 8, 0, 4, 4, 1, 4, 4, 4, 1, 1]
        result = extract_digits_from_value("ISBN: 978-0-441-44411-X")
        self.assertListEqual(expected, result)

    def test_isbn13_with_valid_checksum(self):
        self.assertTrue(validate_isbn13_checksum(self.VALID_ISBN13_DIGITS))

    def test_isbn10_with_valid_checksum(self):
        self.assertTrue(validate_isbn10_checksum(self.VALID_ISBN10_DIGITS))

    def test_isbn10_with_wrong_checksum(self):
        self.assertFalse(validate_isbn10_checksum(self.WRONG_ISBN10_DIGITS))

    def test_isb13_with_wrong_checksum(self):
        self.assertFalse(validate_isbn13_checksum(self.WRONG_ISBN13_DIGITS))

    def test_validate_checksum_works_with_isbn10(self):
        self.assertTrue(validate_checksum(self.VALID_ISBN10_DIGITS))

    def test_validate_checksum_works_with_isbn13(self):
        self.assertTrue(validate_checksum(self.VALID_ISBN13_DIGITS))


    def test_isbn_pattern(self):
        values = ['0-00-617276-8', '0-19-284055-X', '0-201-15767-5', '0-262-73009-X',
                  '0-7139-9799-0', '0-8018-7971-X', '0-85404-656-9', '0-943396-61-1',
                  '1-902699-05-X', '0-9542384-3-5', '981-02-0679-8', '981-02-4410-X',
                  '9971-966-07-7', '978-0-00-648043-3', '978-0-241-95318-1', '978-0-7356-2710-9',
                  '978-1-56347-107-0', '978-0-00-648043 3', '978 0 241 95318 1', '9780735627109',
                  '0-00-617276 8', '0 19 284055 X', '0201157675', '026273009x', 'ISBN981-02-0679-8',
                  'ISBN 981-02-0679-8', 'ISBN: 981-02-0679-8', 'isbn-981-02-0679-8']
        for value in values:
            self.assertTrue(isbn_pattern.match(value))

    def test_regexp_must_match(self):
        self.assertRaises(ValidationError, valid_isbn, None, MockField('invalid value'))

    def test_not_10_digits(self):
        self.assertRaises(ValidationError, valid_isbn, None, MockField('0-21-15-5'))

    def test_not_13_digits(self):
        self.assertRaises(ValidationError, valid_isbn, None, MockField('978-10-00-6443-321-3'))

    def test_invalid_checksum(self):
        self.assertRaises(ValidationError, valid_isbn, None, MockField('0-9542111-3-5'))



if __name__ == '__main__':
    unittest.main()
