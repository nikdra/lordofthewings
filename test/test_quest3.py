import pytest

from src.quest3 import parse_data, part1, part2, part3


@pytest.fixture
def sample_data():
    return {
        '1': 'ISO-3210 7654\nISO-8742 2468\nISO-1111 1111',
        '2': 'ISO-3210 7654\nISO-8742 2468\nISO-1 1111\nISO-13 777\nISO-34 140856\nISO-789 2465112\nISO-2341 945',
        '3': 'ISO2-3 23\nISO2-61 149\nISO2-978 99\nISO2-5887 5923\nISO2-76988 123749\nISO2-435657 929977\nISO2-3949 870737'
    }

def test_parse_data(sample_data):
    expected = [([0, 1, 2, 3], [4, 5, 6, 7]), ([2, 4, 7, 8], [8, 6, 4, 2]), ([1, 1, 1, 1], [1, 1, 1, 1])]
    assert expected == parse_data(sample_data)['1']

def test_part1(sample_data):
    data = parse_data(sample_data)
    assert part1(data['1']) == 1478

def test_part2(sample_data):
    data = parse_data(sample_data)
    assert part2(data['2']) == 1161463

def test_part3(sample_data):
    data = parse_data(sample_data)
    assert part3(data['3']) == 50987
