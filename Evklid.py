def euclid_gcd(a, b):
    a, b = abs(a), abs(b)
    steps = []
    while b != 0:
        steps.append(f"{a} = {b} * ({a // b}) + {a % b}")
        a, b = b, a % b
    return steps, a

# Ввод двух чисел
x = int(input("Введите первое число: "))
y = int(input("Введите второе число: "))

steps, result = euclid_gcd(x, y)
print("Шаги решения:")
for s in steps:
    print(s)
print("НОД:", result)