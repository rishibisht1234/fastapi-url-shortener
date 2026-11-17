import secrets
import string

def generate_short_code(length: int = 8)-> str:
    characters = string.ascii_letters + string.digits

    short_code = ''.join(secrets.choice(characters) for _ in range(length))

    return short_code

# print(generate_short_code())