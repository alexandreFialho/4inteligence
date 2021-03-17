def normalize(cls, text: str) -> str:
    if text:
        text = " ".join((word.capitalize()) for word in text.split(" "))
    return text


def check_field_not_empty(text: str) -> str:
    if text == "" or text == "string":
        raise ValueError("Empty strings are not allowed.")
    return text
