import matplotlib.pyplot as plt
import numpy as np
N = 5
I_ideal = []
I_out_c = []
G_wire = 0.1

for j in range (1): # iterating over specific set of values in order to plot the graph. 
    #Vin = np.random.uniform(0,1,N) # random voltage generation # random voltage generation
    #G = np.random.uniform(10e-6,100e-6,(N,2)) # random conductance of wire generation
    Vin = np.array([0.43952533,0.95081007,0.6997988,0.47337552,0.47337552])
    G = np.array([[1/12185.8355,1/10714.89335],[1/42817.5668,1/19611.1468],[1/46245.3308,1/11813.7758],[1/12790.88,1/18324.811],[1/12790.88,1/18324.811]])
    I = np.zeros(N)
    for i in range(N): 
        I[i] = Vin[i]*G[i][1] # branch currents in ideal situations

    current_coeff_matrix_lhs = np.zeros((N,N))
    current_matrix_lhs = np.zeros((N,1))
    branch_current_matrix_lhs = np.zeros((N,1))

    for i in range(N):
        for j in range(N):
            if (i==j and i==0 and j==0):
                current_coeff_matrix_lhs[i][j] = G[i][0]+G_wire
            if (i==j and i>0 and j>0):
                current_coeff_matrix_lhs[i][j] = G[i][0]+2*G_wire
            if (j==i+1 and j<N):
                current_coeff_matrix_lhs[i][j] = -G_wire
            if (j==i-1 and j>=0):
                current_coeff_matrix_lhs[i][j] = -G_wire
    
    current_coeff_matrix_rhs = np.zeros((N,N))
    current_matrix_rhs = np.zeros((N,1))
    branch_current_matrix_rhs = np.zeros((N,1))
    for i in range(N):
        for j in range(N):
            if (i==j and i==0 and j==0):
                current_coeff_matrix_rhs[i][j] = ((G[i][1]*G_wire)/(G[i][1]+G_wire))+G_wire
            if (i==j and i>0 and j>0):
                current_coeff_matrix_rhs[i][j] = ((G[i][1]*G_wire)/(G[i][1]+G_wire))+2*G_wire
            if (j==i+1 and j<N):
                current_coeff_matrix_rhs[i][j] = -G_wire
            if (j==i-1 and j>=0):
                current_coeff_matrix_rhs[i][j] = -G_wire

    print("current coefficient matrix", current_coeff_matrix_rhs)
    for i in range(N):
        current_matrix_rhs[i] = Vin[i]*((G[i][1]*G_wire)/(G[i][1]+G_wire))

    branch_current_matrix = np.linalg.solve(current_coeff_matrix_rhs,current_matrix_rhs)
    print("branch_current_matrix", branch_current_matrix)
    total_current_value = branch_current_matrix[N-1]*G_wire
    I_out_c.append(np.sum(total_current_value))
    I_ideal.append(np.sum(I))


plt.scatter(I_ideal,I_out_c)
plt.xlabel('I_ideal')
plt.ylabel('I_out_c')
plt.title('I_out_c vs I_ideal')
plt.show()