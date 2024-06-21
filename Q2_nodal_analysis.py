import matplotlib.pyplot as plt
import numpy as np
N = 100
I_ideal = []
I_out_b = []
G_wire = 0.1

for j in range (1): # iterating over specific set of values in order to plot the graph. 
    Vin = np.random.uniform(0,1,N) # random voltage generation # random voltage generation
    G = np.random.uniform(10e-6,100e-6,N) # random conductance of wire generation
    I = np.zeros(N)
    for i in range(N): 
        I[i] = Vin[i]*G[i] # branch currents in ideal situations

    current_coeff_matrix = np.zeros((N,N))
    current_matrix = np.zeros((N,1))
    branch_current_matrix = np.zeros((N,1))
    for i in range(N):
        for j in range(N):
            if (i==j and i==0 and j==0):
                current_coeff_matrix[i][j] = G[i]+G_wire
            if (i==j and i>0 and j>0):
                current_coeff_matrix[i][j] = G[i]+2*G_wire
            if (j==i+1 and j<N):
                current_coeff_matrix[i][j] = -G_wire
            if (j==i-1 and j>=0):
                current_coeff_matrix[i][j] = -G_wire

    for i in range(N):
        current_matrix[i] = Vin[i]*G[i]

    branch_current_matrix = np.linalg.solve(current_coeff_matrix,current_matrix)
    total_current_value = branch_current_matrix[N-1]*G_wire
    I_out_b.append(np.sum(total_current_value))
    I_ideal.append(np.sum(I))


plt.scatter(I_ideal,I_out_b)
plt.xlabel('I_ideal')
plt.ylabel('I_out_b')
plt.title('I_out_b vs I_ideal')
plt.show()