def integrate(func, step, interval):
    left, right = interval
    integral = 0
    x = left
    while x + step <= right:
        integral += step * (func(x).value + func(x + step).value) / 2
        x += step
    if x < right:
        integral += (right - x) * (func(x).value + func(right).value) / 2
    return integral

def bisector_of_area(A, step, interval):
    f = A.membership_function
    total_area = integrate(f, step, interval)
    x = 0
    acc_area = 0
    mid_area = total_area / 2

    while acc_area < mid_area:
        acc_area += step * (f(x).value + f(x + step).value) / 2
        x += step

    return x - step
