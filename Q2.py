import matplotlib.pyplot as plt
import numpy as np
N = 100
I_ideal = []
I_out_b = []
Gwire = 0.1
for j in range (100):
    Vin = np.random.uniform(0,1,N)
    G = np.random.uniform(10e-6,100e-6,N)
    I = np.zeros(N)
    for i in range(N):
        I[i] = Vin[i]*G[i]

    current_coeff_matrix = np.zeros((N,N))
    current_matrix = np.zeros((N,1))
    branch_current_matrix = np.zeros((N,1))
    for i in range(N):
        for j in range(N):
            if (j==i):
                current_coeff_matrix[i][j] = N-i+(Gwire/G[i])
            elif (j<i):
                current_coeff_matrix[i][j] = N-i
            elif (j>i):
                current_coeff_matrix[i][j] = N-j

    for i in range(N):
        current_matrix[i] = Vin[i]*Gwire
    branch_current_matrix = np.linalg.solve(current_coeff_matrix,current_matrix)
    I_out_b.append(np.sum(branch_current_matrix))
    I_ideal.append(np.sum(I))
# Here in Question 1 I_out_a = I_ideal

plt.scatter(I_out_b,I_ideal)
plt.xlabel('I_ideal')
plt.ylabel('I_out_b')
plt.title('I_out_b vs I_ideal')
plt.show()

