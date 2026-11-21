from ecd import get_inputs, submit


def parse_data(data: dict[str, str]) -> dict[str, list[tuple[list[int], list[int]]]]:
    return {k : [iso_vote_split(line, k == '3') for line in v.splitlines()] for k, v in data.items()}

def iso_vote_split(line, iso2 = False) -> tuple[list[int], list[int]]:
    i = 4 if not iso2 else 5
    standard, vote = line[i:].split()
    return list(reversed(list(map(int, standard)))), list(reversed(list(map(int, vote))))


def get_value(standard, vote) -> int:
    return sum(standard[i % len(standard)]**i * v for i, v in enumerate(vote))

def part1(data) -> int:
    return sum(get_value(standard, vote) for standard, vote in data)

def part2(data) -> int:
    return sum(get_value(standard, vote) for standard, vote in data)

def optimum(standard, target) -> str:
    # basically, counting up until we hit the target number.
    i = 0
    while True:
        if target == get_value(standard, map(int, (s for s in reversed(str(i))))):
            return str(i)
        i += 1

def part3(data) -> int:
    return sum(
        target
        for standard, vote in data
        if ''.join(str(v) for v in reversed(vote)) == optimum(standard, target := get_value(standard, vote))
    )

if __name__ == "__main__":
    QUEST = 3
    data = parse_data(get_inputs(quest=QUEST, event=2026))
    submit(quest=QUEST, event=2026, part=1, answer=part1(data['1']))
    submit(quest=QUEST, event=2026, part=2, answer=part2(data['2']))
    submit(quest=QUEST, event=2026, part=3, answer=part3(data['3']))