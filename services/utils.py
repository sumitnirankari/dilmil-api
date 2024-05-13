from datetime import date, datetime


def calculate_age_from_dob(dob: datetime):
    today = date.today()
    return today.year - dob.year - ((today.month, dob.day) < (dob.month, dob.day))