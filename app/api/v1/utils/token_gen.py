import datetime
import bcrypt
import jwt


class TokenManager:
    """
    A class to manage TokenManager operations such as hashing and verifying token.
    """

    def encode(self, token: str) -> str:
        """
        Hash a token using a secure hashing algorithm.

        :param password: The token to hash.
        :return: The hashed token.
        """
        return bcrypt.hashpw(token.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def decode(self, token: str, hashed_token: str) -> bool:
        """
        Verify a token against a hashed token.

        :param token: The token to verify.
        :param hashed_token: The hashed token to compare against.
        :return: True if the token matches the hashed token, False otherwise.
        """
        return bcrypt.checkpw(token.encode('utf-8'), hashed_token.encode('utf-8'))
    
token_manager = TokenManager()

def create_access_token(user_id: str, secret_key: str):
    payload = {
        "sub": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    }
    return jwt.encode(payload, secret_key, algorithm="HS256")