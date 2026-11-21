from ecd import get_inputs, submit


def parse_data(data: dict[str, str]):
    return data

def part1(data) -> int:
    return 0

def part2(data) -> int:
    return 0

def part3(data) -> int:
    return 0

if __name__ == "__main__":
    QUEST = 1
    data = parse_data(get_inputs(quest=QUEST, event=2026))
    print(data)
    # submit(quest=QUEST, event=2026, part=1, answer=part1(data['1']))
    # submit(quest=QUEST, event=2026, part=2, answer=part2(data['2']))
    # submit(quest=QUEST, event=2026, part=3, answer=part3(data['3']))