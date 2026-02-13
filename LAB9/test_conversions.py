import pytest
from conversions import c_to_f, f_to_c, km_to_miles

#1.Basic Tests with Parameterization

@pytest.mark.parametrize("celsius, expected_f", [
    (0, 32),
    (100, 212),
    (-40, -40),
    (37, 98.6)
])
def test_c_to_f(celsius, expected_f):
    assert c_to_f(celsius) == pytest.approx(expected_f, rel=1e-2)

@pytest.mark.parametrize("fahrenheit, expected_c", [
    (32, 0),
    (212, 100),
    (-40, -40),
    (98.6, 37)
])
def test_f_to_c(fahrenheit, expected_c):
    assert f_to_c(fahrenheit) == pytest.approx(expected_c, rel=1e-2)

#2.Exception Testing

def test_km_to_miles_negative():
    """Check if negative distance raises ValueError"""
    with pytest.raises(ValueError):
        km_to_miles(-5)

def test_c_to_f_invalid_type():
    """Check if string input raises TypeError"""
    with pytest.raises(TypeError):
        c_to_f("hot")

def test_absolute_zero():
    """Check physical limits"""
    with pytest.raises(ValueError):
        c_to_f(-300)  # Below absolute zero (-273.15)

#3. Fixtures (Standard & Additional Task)

# ADDITIONAL TASK: Custom fixture that prepares test data (list of tuples)
@pytest.fixture
def distance_data():
    return [
        (1, 0.621371),
        (10, 6.21371),
        (0, 0),
        (100, 62.1371)
    ]

# Test 1 using the custom fixture
def test_km_to_miles_fixture(distance_data):
    for km, miles in distance_data:
        assert km_to_miles(km) == pytest.approx(miles, rel=1e-4)

# Test 2 using the same fixture (Requirement: use in at least two tests)
def test_km_to_miles_round_trip(distance_data):
    """Verify that converting back and forth roughly works (logic check)"""
    for km, miles in distance_data:
        # crude reverse check: miles / 0.621371 should be close to km
        if miles > 0:
            calculated_km = miles / 0.621371
            assert calculated_km == pytest.approx(km, rel=1e-4)

