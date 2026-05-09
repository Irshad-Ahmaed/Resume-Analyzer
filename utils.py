from werkzeug.security import generate_password_hash, check_password_hash as wk_check_hash

def generate_hash_password(password):
    """
    Generate a secure hash for a password using werkzeug.security.
    """
    return generate_password_hash(password)

def check_password_hash(hashed_password, password):
    """
    Check if a password matches a given hash using werkzeug.security.
    """
    return wk_check_hash(hashed_password, password)
