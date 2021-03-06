from nextcord import Embed

from games.util import int_or_null

from .base import CountingGame, ValidationResult, number_matcher, up_matcher


class SevenUpGame(CountingGame):
    @classmethod
    def check_is_up(cls, number: int) -> bool:
        is_up = not number % 7
        while not is_up and number >= 1:
            is_up = number % 10 == 7
            number //= 10

        return is_up

    @classmethod
    def is_valid(cls, to_check: str, number: int) -> ValidationResult:
        is_up: bool = cls.check_is_up(number)
        is_number = not is_up

        has_up = up_matcher.search(to_check) is not None
        numbers = [int_or_null(entered_number) for entered_number in number_matcher.findall(to_check)]

        has_one_number = bool(len(numbers))
        has_correct_numbers = all(entered_number == number for entered_number in numbers)

        if not has_up and not len(numbers):
            # unrelated message
            return ValidationResult.UNRELATED

        return ValidationResult.from_bool(
            (is_up, is_number, not has_one_number or is_number) == (has_up, has_one_number, has_correct_numbers)
        )

    @classmethod
    def get_solution(cls, number: int) -> str:
        return "Up" if cls.check_is_up(number) else str(number)

    @classmethod
    def get_title(cls) -> str:
        return "Seven Up"

    @classmethod
    def get_embed(cls) -> Embed:
        return Embed(
            title=cls.get_title(),
            description="The classic game of 7up!\n"
            + "When a number divides `7`, or includes the number `7`, say `Up`!\n"
            + "Example: `1` -> `1`, `7` -> `Up`, `17` -> `Up`\n"
            + "Per usual: A person cannot say two numbers in a row!",
        )
