def gram_schmidt(V):
    U = matrix(QQ, V.nrows(), V.ncols())
    U.set_row(0, V[0])
    for i in range(1, V.nrows()):
        mu = [V[i].dot_product(U[j]) / U[j].dot_product(U[j]) for j in range(i)]
        U.set_row(i, V[i] - sum([muj * Uj for muj, Uj in zip(mu, [U[j] for j in range(i)])]))
    return U

V = matrix(QQ,[
    [4,1,3,-1],
    [2,1,-3,4],
    [1,0,-2,7],
    [6,2,9,-5]
])

print(round(float(gram_schmidt(V)[3][1])), 5)