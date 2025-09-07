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
