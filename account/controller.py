import secrets


def generateToken():
    return secrets.token_hex(32)
