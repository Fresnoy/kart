from .models import Promotion


# model test
def test_promotion():
    starting_year = 1000
    ending_year = 1001
    promo = Promotion(name="test", starting_year=starting_year, ending_year=ending_year)
    assert promo.starting_year == starting_year
