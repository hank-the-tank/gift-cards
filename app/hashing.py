from passlib.context import CryptContext

hashing = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash:
    def bcrypt(*, password: str):
        return hashing.hash(password)
