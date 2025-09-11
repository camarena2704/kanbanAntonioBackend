import re


class StringHelper:
    @staticmethod
    def normalize_and_validate(value: str) -> str | None:
        """
        Remove unnecessary spaces and validate that the string is not empty.
        Returns the cleaned string or None if it is invalid.
        """
        if not value:
            return None
        clean_value = value.strip()
        return clean_value if clean_value else None

    @staticmethod
    def validate_password_complexity(password: str) -> str:
        """
        Validates that the password meets the complexity requirements:
        - Minimum 8 characters
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one digit
        - At least one special character
        """

        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if not re.search(r"[A-Z]", password):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", password):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not re.search(r"\d", password):
            raise ValueError("Password must contain at least one digit.")
        if not re.search(r"[^\w\s]", password):
            raise ValueError("Password must contain at least one special character.")
        return password
