import pytest

from src.quest4 import parse_data, part1, part2, part3


@pytest.fixture
def sample_data():
    with open("test/fixtures/quest4_3") as file:
        text = file.read()
    return {
        '1': "id=1 quest=1 part=1 time=187\nid=3 quest=1 part=1 time=413\nid=5 quest=1 part=3 time=744\nid=2 quest=1 part=3 time=745\nid=4 quest=1 part=2 time=558\nid=1 quest=1 part=2 time=299\nid=1 quest=1 part=3 time=362\nid=4 quest=1 part=3 time=1268\nid=4 quest=1 part=1 time=457\nid=5 quest=1 part=1 time=257\nid=2 quest=1 part=1 time=192\nid=3 quest=1 part=3 time=1168\nid=5 quest=1 part=2 time=346\nid=3 quest=1 part=2 time=455\nid=2 quest=1 part=2 time=562",
        '2': "id=2 quest=1 part=1 time=100\nid=4 quest=2 part=1 time=150\nid=1 quest=2 part=1 time=140\nid=1 quest=1 part=2 time=180\nid=2 quest=2 part=1 time=130\nid=4 quest=1 part=1 time=110\nid=1 quest=2 part=2 time=210\nid=2 quest=2 part=2 time=240\nid=1 quest=2 part=3 time=330\nid=2 quest=1 part=2 time=170\nid=3 quest=1 part=1 time=90\nid=4 quest=1 part=2 time=175\nid=3 quest=2 part=1 time=120\nid=1 quest=1 part=1 time=120\nid=3 quest=2 part=2 time=220\nid=2 quest=2 part=3 time=350\nid=3 quest=1 part=2 time=160",
        '3': "id=2 quest=1 part=1 time=90\nid=4 quest=2 part=1 time=150\nid=1 quest=2 part=1 time=130\nid=1 quest=1 part=2 time=180\nid=2 quest=2 part=1 time=130\nid=4 quest=1 part=1 time=110\nid=1 quest=2 part=2 time=210\nid=2 quest=2 part=2 time=220\nid=1 quest=2 part=3 time=330\nid=2 quest=1 part=2 time=170\nid=3 quest=1 part=1 time=90\nid=4 quest=1 part=2 time=170\nid=3 quest=2 part=1 time=120\nid=1 quest=1 part=1 time=120\nid=3 quest=2 part=2 time=220\nid=2 quest=2 part=3 time=350\nid=3 quest=1 part=2 time=170",
        '4': text 
    }

def test_parse_data(sample_data):
    parse_data(sample_data)


def test_part1(sample_data):
    data = parse_data(sample_data)
    assert part1(data['1']) == 27598

def test_part2(sample_data):
    data = parse_data(sample_data)
    # print(data['2'])
    print(data['2'][1])
    assert part2(data['2']) == 6470

def test_part3(sample_data):
    data = parse_data(sample_data)
    assert part3(data['3']) == 3004

def test_part3_complicated(sample_data):
    data = parse_data(sample_data)
    assert part3(data['4']) == 6232480