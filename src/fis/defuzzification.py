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

def bisector_of_area(A, step):
    f = A.membership_function
    total_area = integrate(f, step, A.domain)
    x = A.domain[0]
    acc_area = 0
    mid_area = total_area / 2

    while acc_area < mid_area:
        acc_area += step * (f(x).value + f(x + step).value) / 2
        x += step

    return x - step

def center_of_area(A, step):
    f = A.membership_function
    left, right = A.domain
    x = left
    sum1, sum2 = 0, 0

    while x <= right:
        sum1 += x * f(x).value
        sum2 += f(x).value
        x += step

    return sum1 / sum2

def mean_of_maximum(A, step):
    f = A.membership_function
    left, right = A.domain
    x = left
    maximum = f(x).value

    while x <= right:
        maximum = max(f(x).value, maximum)
        x += step
    if x < right:
        maximum = max(f(right).value, maximum)

    k = 0
    _sum = 0
    x = left
    while x <= right:
        if f(x).value == maximum:
            _sum += x
            k += 1
        x += step
    if x < right and f(right) == maximum:
        _sum += right
        k += 1
    print(_sum / k)
    return _sum / k
