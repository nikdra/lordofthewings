import pytest

from src.quest7 import parse_data, part1, part2, part3


@pytest.fixture
def sample_data():
    with open("test/fixtures/quest7_3") as file:
        text = file.read()
    return {
        "1": "id=1, energy=5, connections=2,5,7\nid=2, energy=9, connections=6,7\nid=3, energy=3, connections=4\nid=4, energy=8, connections=3\nid=5, energy=1, connections=6,7\nid=6, energy=7, connections=1,7\nid=7, energy=6, connections=5",
        "2": "id=1, energy=5, connections=2,5,7\nid=2, energy=9, connections=6,7\nid=3, energy=3, connections=4\nid=4, energy=8, connections=3\nid=5, energy=1, connections=6,7\nid=6, energy=7, connections=1,7\nid=7, energy=6, connections=5",
        "3": "id=1, energy=5, connections=2,5,7\nid=2, energy=9, connections=6,7\nid=3, energy=3, connections=4\nid=4, energy=8, connections=3\nid=5, energy=1, connections=6,7\nid=6, energy=7, connections=1,7\nid=7, energy=6, connections=5",
        "4": text
    }

def test_parse_data(sample_data):
    parse_data(sample_data)

@pytest.fixture
def parsed_data(sample_data):
    return parse_data(sample_data)

def test_part1(parsed_data):
    assert part1(parsed_data['1']) == 102

def test_part2(parsed_data):
    assert part2(parsed_data['2']) == 1316

def test_part3(parsed_data):
    assert part3(parsed_data['3'], 100) == 187

def test_part3_complicated(parsed_data):
    assert part3(parsed_data['4']) == 34777023