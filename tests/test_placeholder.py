from src.eda_utils import calculate_margin

def test_calculate_margin():
    premium = 1000
    claims = 400

    margin = premium - claims

    assert margin == 600
