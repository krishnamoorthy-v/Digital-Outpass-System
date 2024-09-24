import re
import base64


class Validation:

    def __init__(self):
        self.pattern = r'^[6-9]\d{9}$'
        self.email_regex = r"^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}$"
        self.date_regex = r"(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2})"

    def validate_date(self, date):
        match = re.match(self.date_regex, str(date))
        if not match:
            raise Exception("Invalid date format")
        return date

    def validate_mobileNum(self, data):
        match = re.match(self.pattern, str(data))
        if not match:
            raise Exception("Invalid mobile number")
        return data

    def validate_base64(self, value):
        try:
            base64.b64decode(value, validate=True)
            return value
        except Exception:
            raise Exception("Image expected")

    def validate_email(self, email):

        compiled_regex = re.compile(self.email_regex, re.IGNORECASE)
        match = compiled_regex.match(email)
        if bool(match) == True:
            return email
        else:
            raise Exception("Invalid email id")
