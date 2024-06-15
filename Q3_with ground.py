import matplotlib.pyplot as plt
import numpy as np
N = 100
I_ideal = []
I_out_b = []
I_out_c = []
Gwire = 0.1
for j in range (100):
    Vin = np.random.uniform(0,1,N)
    G = np.random.uniform(10e-6,100e-6,(N,2))
    I = np.zeros(N)
    for i in range(N):
        I[i] = Vin[i]*G[i][0]

    current_coeff_matrix_lhs = np.zeros((N,N))
    current_matrix_lhs = np.zeros((N,1))
    branch_current_matrix_lhs = np.zeros((N,1))
    for i in range(N):
        for j in range(N):
            if (j==i):
                current_coeff_matrix_lhs[i][j] = N-i+(Gwire/G[i][0])
            elif (j<i):
                current_coeff_matrix_lhs[i][j] = N-i
            elif (j>i):
                current_coeff_matrix_lhs[i][j] = N-j

    for i in range(N):
        current_matrix_lhs[i] = Vin[i]*Gwire
    branch_current_matrix_lhs = np.linalg.solve(current_coeff_matrix_lhs,current_matrix_lhs)
    
# Here in Question 1 I_out_a = I_ideal
    current_coeff_matrix_rhs = np.zeros((N,N))
    current_matrix_rhs = np.zeros((N,1))
    branch_current_matrix_rhs = np.zeros((N,1))
    for i in range(N):
        for j in range(N):
            if (j==i):
                current_coeff_matrix_rhs[i][j] = N+1-i+(Gwire/G[i][1])
            elif (j<i):
                current_coeff_matrix_rhs[i][j] = N-i
            elif (j>i):
                current_coeff_matrix_rhs[i][j] = N-j
    
    for i in range(N):
        current_matrix_rhs[i] = Vin[i]*Gwire
    branch_current_matrix_rhs = np.linalg.solve(current_coeff_matrix_rhs,current_matrix_rhs)
    I_out_b.append(np.sum(branch_current_matrix_lhs))
    I_out_c.append(np.sum(branch_current_matrix_rhs))
    I_ideal.append(np.sum(I))


plt.scatter(I_out_c,I_ideal)
plt.xlabel('I_ideal')
plt.ylabel('I_out_c')
plt.title('I_out_c vs I_ideal')
plt.show()

