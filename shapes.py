n = 5

print("[직각삼각형]")
for i in range(1, n + 1):
    print('*' * i)

print("\n[정삼각형]")
for i in range(1, n + 1):
    print(' ' * (n - i) + '*' * (2 * i - 1))

print("\n[마름모]")
for i in range(1, n + 1):
    print(' ' * (n - i) + '*' * (2 * i - 1))
for i in range(n - 1, 0, -1):
    print(' ' * (n - i) + '*' * (2 * i - 1))
