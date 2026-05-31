import re


EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def require_fields(data, fields):
    missing = [field for field in fields if data.get(field) in (None, "")]
    if missing:
        return "Missing required field(s): " + ", ".join(missing)
    return None


def is_valid_email(email):
    return bool(email and EMAIL_RE.match(email))
