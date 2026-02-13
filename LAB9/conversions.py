def c_to_f(celsius):
    """Converts Celsius to Fahrenheit."""
    if not isinstance(celsius, (int, float)):
        raise TypeError("Input must be a number")
    if celsius < -273.15:
        raise ValueError("Temperature below absolute zero")
    return (celsius * 9/5) + 32

def f_to_c(fahrenheit):
    """Converts Fahrenheit to Celsius."""
    if not isinstance(fahrenheit, (int, float)):
        raise TypeError("Input must be a number")
    # Absolute zero in fahrenheit is -459.67
    if fahrenheit < -459.67:
        raise ValueError("Temperature below absolute zero")
    return (fahrenheit - 32) * 5/9

def km_to_miles(km):
    """Converts Kilometers to Miles."""
    if not isinstance(km, (int, float)):
        raise TypeError("Input must be a number")
    if km < 0:
        raise ValueError("Distance cannot be negative")
    # 1km =0.621371 miles
    return km * 0.621371
