from email_validator import validate_email, EmailNotValidError


def check_email(email):
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False


emails = []

for email in emails:
    print(email, check_email(email))
