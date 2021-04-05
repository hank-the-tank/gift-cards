from passlib.context import CryptContext

hashing = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash:
    def bcrypt(*, password: str):
        return hashing.hash(password)

    def verify(*, hashed_password, unhassed_password):
        return hashing.verify(unhassed_password, hashed_password)
