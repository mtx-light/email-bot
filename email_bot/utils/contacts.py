import re

def get_email(text):
    match = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', text)
    if match:
        return match.group(0)


def get_phone(text):
    match = re.search(r'\+?(\(?\d[ -]?\)?)+', text)
    if match:
        return match.group(0)