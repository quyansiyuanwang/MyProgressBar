class MathModule:
    from math import sqrt


def isprime(x) -> bool:
    for i in range(2, int(MathModule.sqrt(x)) + 1):
        if x % i == 0: return False
    return True


print(*(i for i in range(2, int(input('请输入范围')) + 1) if isprime(i)))
