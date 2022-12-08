def RK2(f, x0, y0, h, n, b):
    a = 1 - b
    p = 1 / (2 * b)
    q = p
    for _ in range(n):
        m1 = f(x0,y0)
        m2 = f(x0+p*h, y0+q*h*m1)
        y0 += (a * m1 + b * m2) * h
        x0 += h
        yield [x0,y0]


#Q11 Prova:
def f(x,y):
    return y*(1-x)+x+2

x0 = 0.7477
y0 = 1.26231
h = 0.18185
b = 0.53344
n = 15
e = RK2(f,x0,y0, h,n, b)
for xi, yi in e:
    print(f'{yi}, ')