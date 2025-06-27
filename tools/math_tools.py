import math

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError('Cannot divide by zero')
    return a / b

def square_root(x):
    if x < 0:
        raise ValueError('Cannot take square root of negative number')
    return math.sqrt(x)

def average(*args):
    if not args:
        raise ValueError('At least one number is required')
    return sum(args) / len(args) 