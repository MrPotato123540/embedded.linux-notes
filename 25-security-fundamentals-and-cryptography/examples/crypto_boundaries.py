#!/usr/bin/env python3
"""Host-only teaching lab. No files, network, hardware or production keys.

Requires Python 3 and the cryptography package. This is an API/ownership
exercise, not a cryptographic implementation, benchmark or device test.
"""

import hashlib
import hmac
import os

from cryptography.exceptions import InvalidSignature, InvalidTag
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def check(condition, message):
    if not condition:
        raise RuntimeError(message)
    print("PASS:", message)


def rejected(operation, expected_exception, message):
    try:
        operation()
    except expected_exception:
        print("PASS:", message)
    else:
        raise RuntimeError("Unexpected acceptance: " + message)


def main():
    payload = b"board=teaching-board;release=7;payload=example"
    changed = payload.replace(b"release=7", b"release=8")
    check(hashlib.sha256(payload).digest() != hashlib.sha256(changed).digest(),
          "a payload change changes its SHA-256 digest")

    mac_key = os.urandom(32)
    mac = hmac.digest(mac_key, payload, "sha256")
    check(hmac.compare_digest(mac, hmac.digest(mac_key, payload, "sha256")),
          "HMAC accepts the original bytes with the same key")
    check(not hmac.compare_digest(mac, hmac.digest(mac_key, changed, "sha256")),
          "HMAC rejects changed bytes against the original tag")

    aes = AESGCM(AESGCM.generate_key(bit_length=256))
    nonce = os.urandom(12)  # One encryption only under this fresh key.
    aad = b"purpose=guide-lab;device=teaching-board"
    sealed = aes.encrypt(nonce, payload, aad)
    check(aes.decrypt(nonce, sealed, aad) == payload,
          "AES-GCM accepts the original ciphertext and context")
    damaged = sealed[:-1] + bytes([sealed[-1] ^ 1])
    rejected(lambda: aes.decrypt(nonce, damaged, aad), InvalidTag,
             "AES-GCM rejects a modified authentication tag")
    rejected(lambda: aes.decrypt(nonce, sealed, b"different-device"), InvalidTag,
             "AES-GCM rejects the wrong associated context")
    rejected(lambda: aes.decrypt(nonce, sealed[:-1], aad), InvalidTag,
             "AES-GCM rejects truncated input")

    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    scheme = padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
                         salt_length=padding.PSS.MAX_LENGTH)
    signature = private_key.sign(payload, scheme, hashes.SHA256())
    public_key.verify(signature, payload, scheme, hashes.SHA256())
    print("PASS: RSA-PSS accepts the original signed bytes")
    rejected(lambda: public_key.verify(signature, changed, scheme, hashes.SHA256()),
             InvalidSignature, "RSA-PSS rejects changed signed bytes")
    wrong_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    rejected(lambda: wrong_key.public_key().verify(signature, payload, scheme,
                                                   hashes.SHA256()),
             InvalidSignature, "RSA-PSS rejects the wrong verification key")


if __name__ == "__main__":
    main()
