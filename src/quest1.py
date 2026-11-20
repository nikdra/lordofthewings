from math import ceil, sqrt

from ecd import get_inputs, submit


def parse_data(data: dict[str, str]) -> dict[str, list[int]]:
    return {k: list(map(int, v.split(','))) for k, v in data.items()}

def part1(data: list[int]) -> int:
    return sum((ceil(sqrt(x)))**2 - x for x in data)

def frame(number: int) -> int:
    if number < 9:
        return 8 - number
    size = ceil((number + 4) / 4)
    return size**2 - (size - 2)**2 - number

def part2(data: list[int]) -> int:
    return sum(frame(x) for x in data)

def filled(number: int) -> int:
    if number < 9:
        return 8 - number
    candidate = ceil(sqrt(number))
    candidate = candidate + 1 if candidate % 2 == 0 else candidate
    if candidate**2 == number:
        candidate += 2
    return candidate**2 - number - 1

def part3(data: list[int]) -> int:
    return sum(filled(x) for x in data)

if __name__ == "__main__":
    data = parse_data(get_inputs(quest=1, event=2026))
    submit(quest=1, event=2026, part=1, answer=part1(data['1']))
    submit(quest=1, event=2026, part=2, answer=part2(data['2']))
    submit(quest=1, event=2026, part=3, answer=part3(data['3']))