import string
import random

def generate_pass(length=14):
  chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
  size = length
  return ''.join(random.choice(chars) for x in range(size))

char_set = {'small': 'abcdefghijklmnopqrstuvwxyz',
             'nums': '0123456789',
             'big': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
            }

def check_prev_char(password, current_char_set):
    """Function to ensure that there are no consecutive
    UPPERCASE/lowercase/numbers/special-characters."""

    index = len(password)
    if index == 0:
        return False
    else:
        prev_char = password[index - 1]
        if prev_char in current_char_set:
            return True
        else:
            return False