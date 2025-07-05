from dataclasses import dataclass


@dataclass(frozen=True)
class CategoryVO:
    """
    Value Object for Category.
    This class encapsulates the category and ensures its validity.
    """

    name: str

    def __str__(self):
        return self.name

    @staticmethod
    def is_valid_name(name: str) -> bool:
        """
        Validate the name format.
        For simplicity, let's assume a valid name is a non-empty string.
        """
        return isinstance(name, str) and len(name) > 0


@dataclass(frozen=True)
class ScoreVO:
    """
    Value Object for Score.
    This class encapsulates the score and ensures its validity.
    """

    score: int

    def __str__(self):
        return str(self.score)

    @staticmethod
    def is_valid_score(score: int) -> bool:
        """
        Validate the score format (between 1 and 5)
        """
        return isinstance(score, int) and 1 <= score <= 5
