#!/usr/bin/env python3
"""

"""
from typing import List
import logging
from re import sub


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str):
    """ Replaces sensitive information in a message """
    for field in fields:
        msg = sub(f'{field}=.*?{separator}',
                  f'{field}={redaction}{separator}', message)
    return msg


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Init the class"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Formate log messages"""
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)
