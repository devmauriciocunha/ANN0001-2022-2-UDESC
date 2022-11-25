import math
import numpy as np

def legendre(x, n):
    if n == 0:
        return 1
    elif n == 1:
        return x
    else:
        return ((2 * n - 1) * x * legendre(x, n - 1) - (n - 1) * legendre(x, n - 2)) / n

def build_legendre_polynomial(n):
    def temp(t):
        return legendre(t, n)
    return temp

def romberg(coluna_f1):
    coluna_f1 = [i for i in coluna_f1]
    n = len(coluna_f1)
    for j in range(n - 1):
        temp_col = [0] * (n - 1 - j)
        for i in range(n - 1 - j):
            power = j + 1
            temp_col[i] = (4 ** power * coluna_f1[i + 1] - coluna_f1[i]) / (4 ** power - 1)
        coluna_f1[:n - 1 - j] = temp_col
        # print(f'F_{j+2} = {temp_col}')
    return coluna_f1[0]


def trapz_romberg(f, a, b, h):
    n = int((b - a) / h)
    soma = 0

    for k in range(1, n):
        soma += f(a + k * h)

    return (h / 2) * (f(a) + 2 * soma + f(b))


def simps(f, a, b, n):
    if n % 2 != 0:
        print('O valor n deve ser par')
        return None

    num_parabolas = n / 2
    soma = 0
    h = (b - a) / n

    for i in range(int(num_parabolas)):
        x0 = a + (2 * i) * h
        x1 = a + (2 * i + 1) * h
        x2 = a + (2 * i + 2) * h
        soma += f(x0) + 4 * f(x1) + f(x2)

    soma *= h / 3

    return soma


def imprimir_coeffs(c):
    for i in c:
        print(f'{i}, ')
        
def f(x):
    return  math.tanh(3 * x) * math.cos(3 * x)



def best_func(f, funcs, a, b, method: ['trapz', 256]):
    k = len(funcs)

    A = [[0 for _ in range(k)] for _ in range(k)]
    B = []

    for i in range(k):
        for j in range(k):
            if i == j:
                if j >= i:
                    def f_ij(x):
                        return funcs[j](x) * funcs[i](x)

                    if method[0] == 'simps':
                        A[i][j] = simps(f_ij, a, b, method[1])
                    elif method[0] == 'romberg':
                        tam = int(method[1] / 2)
                        hs = [method[2] / 2 ** ki for ki in range(tam)]
                        coluna_f1 = [trapz_romberg(f_ij, a, b, hi) for hi in hs]
                        A[i][j] = romberg(coluna_f1)

                else:
                    A[i][j] = A[j][i]

        def ffi(x):
            return f(x) * funcs[i](x)

        if method[0] == 'simps':
            B.append(simps(ffi, a, b, method[1]))
        elif method[0] == 'romberg':
            tam = int(method[1] / 2)
            hs = [method[2] / 2 ** ki for ki in range(tam)]
            coluna_f1 = [trapz_romberg(ffi, a, b, hi) for hi in hs]
            B.append(romberg(coluna_f1))

    A = np.array(A, dtype=float)
    B = np.array(B, dtype=float)

    return np.linalg.solve(A, B)


if __name__ == '__main__':
    grau = 31
    funcs = [build_legendre_polynomial(i) for i in range(grau)]
    a = -1
    b = 1
    subintervalos = 256
    order = 8
    values = [-0.676,-0.161,0.554]
    h = (b-(a))/10
    method = ['romberg', order, h]
    
    coefs = best_func(f, funcs, a, b, method)

    coefs = [ci for ci in coefs]

    imprimir_coeffs(coefs)

    def g(x):
        return sum(ci * fi(x) for ci, fi in zip(coefs, funcs))


    for x in values:
        print(f'{g(x)}, ')


    def func_erro(x):
        return (f(x) - g(x)) ** 2


    erro = simps(func_erro, a, b, 256)

    print(f'{erro}')