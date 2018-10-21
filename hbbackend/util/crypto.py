"""crypto
Wraps GPG methods
"""

import time
import gnupg

GPG = gnupg.GPG()


def encrypt_data(data, password):
    """Encrypt a string with the given password,
    returns base64 encrypted string
    """

    start = int(round(time.time() * 1000))
    crypt = GPG.encrypt(
        data,
        symmetric='AES256',
        passphrase=password,
        encrypt=False,
        armor=True
    )
    end = int(round(time.time() * 1000))

    return {
        "encrypted_b64": str(crypt),
        "time_ms": end - start,
    }


def decrypt_data(data, password):
    """Decrypts an GPG encrypted string with the given password."""

    start = int(round(time.time() * 1000))
    decrypted = GPG.decrypt(
        data,
        passphrase=password,
    )
    end = int(round(time.time() * 1000))

    return {
        "decrypted": str(decrypted),
        "time_ms": end - start,
    }
