import random
import string

def generate_code(length=6):
    chars = string.digits + string.ascii_letters
    return "".join(random.choices(chars, k=length))
