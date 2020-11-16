from src.classes import INF

# levels: A list of tuples (min, max, value) which maps the input to value if it belongs to [min, max)
def discretize_and_normalize(levels, input_value):
    for _min, _max, value in levels:
        if input_value >= _min and input_value < _max:
            return value
    raise ValueError(f"There is no level to map the input value {input_value} to")
