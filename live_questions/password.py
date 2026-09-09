"""Generate the server's password hash without placing a password in shell history."""

import getpass
import hashlib
import hmac
import secrets

ITERATIONS = 600_000


def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), ITERATIONS)
    return "$".join(("pbkdf2_sha256", str(ITERATIONS), salt, digest.hex()))


def validate_hash(encoded: str) -> None:
    try:
        algorithm, count, salt, digest = encoded.split("$")
        if algorithm != "pbkdf2_sha256" or not ITERATIONS <= int(count) <= 2_000_000:
            raise ValueError
        if len(salt) != 32 or len(digest) != 64 or len(bytes.fromhex(salt)) != 16 or len(bytes.fromhex(digest)) != 32:
            raise ValueError
    except ValueError:
        raise ValueError("Invalid LIVE_PASSWORD_HASH; generate it with python -m live_questions.password") from None


def verify_password(password: str, encoded: str) -> bool:
    _, count, salt, expected = encoded.split("$")
    actual = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), int(count)).hex()
    return hmac.compare_digest(actual, expected)


def main() -> None:
    password = getpass.getpass("Teacher password: ")
    if not password:
        raise SystemExit("The password cannot be empty.")
    if password != getpass.getpass("Repeat password: "):
        raise SystemExit("Passwords do not match.")
    print("LIVE_PASSWORD_HASH=" + hash_password(password))


if __name__ == "__main__":
    main()
