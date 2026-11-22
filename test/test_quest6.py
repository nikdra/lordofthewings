import pytest

from src.quest6 import parse_data, part1, part2, part3


@pytest.fixture
def sample_data():
    return {
        "1": "BRDS:FLWR,SLTT,YSTS\nFLWR:SLTT,YSTS\nSLTT:YSTS,MLKK,BTTR\nNULL:BRDS,FLWR,SLTT\nYSTS:BRDS,FLWR\nMLKK:SPCS,NULL\nHNYN:BRDS,FLWR,SLTT,YSTS",
        "2": "BRDS:FLWR,SLTT,YSTS\nFLWR:SLTT,YSTS\nSLTT:YSTS,MLKK,BTTR\nNULL:BRDS,FLWR,SLTT\nYSTS:BRDS,FLWR\nMLKK:SPCS,NULL\nHNYN:BRDS,FLWR,SLTT,YSTS",
        "3": "MEAL:BRDS,CAKE,DOUG\nBRDS:DOUG,FLWR\nCAKE:DOUG,FLWR,NULLv2,NULLv3\nDOUG:FLWR,YSTS,SLTT,NULLv1\nFLWR:BRDS,DOUG\nYSTS:SPCS\nSOUP:BRDS,CAKE,DOUG,FLWR"
    }

def test_parse_data(sample_data):
    expected = ({'BRDS': ['FLWR', 'SLTT', 'YSTS'], 'FLWR': ['SLTT', 'YSTS'], 'SLTT': ['YSTS', 'MLKK', 'BTTR'], 'NULL': ['BRDS', 'FLWR', 'SLTT'], 'YSTS': ['BRDS', 'FLWR'], 'MLKK': ['SPCS', 'NULL'], 'HNYN': ['BRDS', 'FLWR', 'SLTT', 'YSTS']})
    assert expected == parse_data(sample_data)['1']

@pytest.fixture
def parsed_data(sample_data):
    return parse_data(sample_data)

def test_part1(parsed_data):
    assert part1(parsed_data['1']) == 7

def test_part2(parsed_data):
    assert part2(parsed_data['2']) == 6

def test_part3(parsed_data):
    assert part3(parsed_data['3']) == 3