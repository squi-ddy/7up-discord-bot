from nextcord import Embed

from games.util import int_or_null

from .base import CountingGame, ValidationResult, number_matcher, up_matcher


class SevenUpHardGame(CountingGame):
    @classmethod
    def check_number_up(cls, number: int) -> int:
        number_copy = number
        number_up = 0
        while not number_copy % 7:
            number_up += 1
            number_copy //= 7
        while number >= 1:
            number_up += number % 10 == 7
            number //= 10

        return number_up

    @classmethod
    def is_valid(cls, to_check: str, number: int) -> ValidationResult:
        number_up: int = cls.check_number_up(number)
        is_number = not number_up

        number_up_in_str = len(up_matcher.findall(to_check))
        numbers = [int_or_null(entered_number) for entered_number in number_matcher.findall(to_check)]

        has_one_number = bool(len(numbers))
        has_correct_numbers = all(entered_number == number for entered_number in numbers)

        if not len(numbers) and not number_up_in_str:
            # unrelated message
            return ValidationResult.UNRELATED

        return ValidationResult.from_bool(
            (number_up, is_number, not has_one_number or is_number)
            == (number_up_in_str, has_one_number, has_correct_numbers)
        )

    @classmethod
    def get_solution(cls, number: int) -> str:
        return "Up " * no_up if (no_up := cls.check_number_up(number)) else str(number)

    @classmethod
    def get_title(cls) -> str:
        return "Seven Up (Hard Mode)"

    @classmethod
    def get_embed(cls) -> Embed:
        return Embed(
            title=cls.get_title(),
            description="A harder version of 7up!\n"
            + "How many times to say `Up` is now based on how many "
            + "times it breaks the rules!\n"
            + "Basically, it's equal to the number of `7`s in the number "
            + "plus the number of times it is divisible by `7`!\n"
            + "Example: `1` -> `1`, `7` -> `Up Up`, `17` -> `Up`, "
            + "`49` -> `Up Up`, `77` -> `Up Up Up`\n"
            + "Per usual: A person cannot say two numbers in a row!",
        )
