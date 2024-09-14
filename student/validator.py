from .models import StudentModel

import re


def is_indian_mobile_number(number):
    pattern = r'^[6-9]\d{9}$'
    match = re.match(pattern, str(number) )
    return bool(match)
