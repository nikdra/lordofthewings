from src.quest1 import parse_data, part1, part2, part3


def test_parse_data():
    data = {
            "1": '3,11,12,16,24,25'
        }
    expected = {
        "1": [3, 11, 12, 16, 24, 25]
    }
    assert parse_data(data) == expected


def test_part1():
    data = {
        "1": [3, 11, 12, 16, 24, 25]
    }
    assert part1(data['1']) == 11


def test_part2():
    data = {
        "2": [3, 11, 12, 16, 24, 25]
    }
    assert part2(data['2']) == 9


def test_part3():
    data = {
        "3": [3, 11, 12, 16, 24, 25]
    }
    assert part3(data['3']) == 61