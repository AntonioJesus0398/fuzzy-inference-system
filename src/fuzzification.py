def scale_function(f, scaling_func):
    def func(*args):
        scaled_args = [scaling_func(arg) for arg in args]
        return f(*scaled_args)
    return func
