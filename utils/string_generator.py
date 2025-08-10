import random
import string

def generate_random_string(length=10):
    """Generate a random string of specified length using letters and digits"""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))
