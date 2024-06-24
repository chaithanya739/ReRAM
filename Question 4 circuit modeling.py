import numpy as np
import matplotlib.pyplot as plt
def resistor_stamp(matrix,vector,node1,node2,conductance):
    if(node1 != 0):
        matrix[node1-1][node1-1] += conductance
        if (node2 !=0):
            matrix[node1-1][node2-1] -= conductance
    if(node2 != 0):
        matrix[node2-1][node2-1] += conductance
        if (node1 != 0):
            matrix[node2-1][node1-1] -=conductance
    return matrix,vector
    
def voltage_source_stamp(matrix,vector,node1,node2,voltage,num_nodes):
    new_matrix = np.zeros((num_nodes+1, num_nodes+1))
    new_vector = np.zeros(num_nodes+1)
    new_matrix[:num_nodes,:num_nodes]=matrix
    new_vector[:num_nodes]=vector
    if (node1 != 0):
        new_matrix[node1-1][num_nodes] = 1
        new_matrix[num_nodes][node1-1] = 1
    if (node2 != 0):
        new_matrix[node2-1][num_nodes] = -1
        new_matrix[num_nodes][node2-1] = -1

    new_vector[num_nodes]=voltage
    return new_matrix, new_vector

def current_source_stamp(matrix,vector,node_p,node_n,current):
    if (node_p !=0):
        vector[node_p-1] -= current
    if (node_n != 0):
        vector[node_n-1] += current
    return matrix,vector

def voltage_controlled_current_source(matrix,node_out_n,node_out_p,node_control_p,node_control_n,gm):
    if (node_out_p != 0):
        if (node_control_p != 0):
            matrix[node_out_p-1,node_out_p-1] += gm
        if (node_control_n != 0):
            matrix[node_out_p-1,node_out_n-1] -= gm

    if (node_out_n != 0):
        if (node_control_p != 0):
            matrix[node_out_n-1,node_out_p-1] -= gm
        if (node_control_n != 0):
            matrix[node_out_n-1,node_out_n-1] += gm

    return matrix

def mosfet_stamp(matrix,vector,drain,gate,source,Vth,K,Lambda,Vgs,Vds):
    if Vgs<=Vth:
        return
    if Vds >= Vgs-Vth:
        Id = 0.5 * K * (Vgs - Vth)**2 * (1 + Lambda * Vds)
        gm = K * (Vgs - Vth) * (1 + Lambda * Vds)
        gds = 0.5 * K * (Vgs - Vth)**2 * Lambda

    else:
        Id = K * ((Vgs - Vth) * Vds - 0.5 * Vds**2) * (1 + Lambda * Vds)
        gm = K * Vds * (1 + Lambda * Vds)
        gds = K * ((Vgs - Vth) - Vds) * (1 + Lambda * Vds) + K * ((Vgs - Vth) * Vds - 0.5 * Vds**2) * Lambda

    Io= Id-gm*Vgs-gds*Vds

    if(drain != 0):
        vector[drain-1] -= Io
    if(source != 0):
        vector[source-1] += Io

    if (drain !=0 and source !=0):
        matrix[drain-1][source-1] -= gm
    if (drain !=0 and gate != 0):
        matrix[drain-1][gate-1] += gm
    if (source !=0 and source !=0):
        matrix[source-1][source-1] += gm
    if (source != 0 and gate !=0 ):
        matrix[source-1][gate-1] -= gm

    if drain != 0 and drain != 0:
        matrix[drain-1, drain-1] += gds
    if drain != 0 and source != 0:
        matrix[drain-1, source-1] -= gds
    if source != 0 and drain != 0:
        matrix[source-1, drain-1] -= gds
    if source != 0 and source != 0:
        matrix[source-1, source-1] += gds

    return matrix, vector

num_of_nodes = 6
Vdd = 1.2
matrix = np.zeros((num_of_nodes,num_of_nodes))
vector = np.zeros(num_of_nodes)

N = 2
num_nodes = num_of_nodes
Vth = 0.2
K = 1e-3
Lambda = 0.01
Vin = np.array([0.43952533,0.95081007])
max_iterations = 5
mosfet = 0
resistor = 0
Vs = np.zeros(N)
Vd = Vdd

for i in range(2):
    matrix = np.zeros((num_of_nodes,num_of_nodes))
    vector = np.zeros(num_of_nodes)
    matrix,vector = voltage_source_stamp(matrix,vector,1,0,0.8,num_nodes)
    matrix,vector = voltage_source_stamp(matrix,vector,2,0,2,num_nodes+1)
    matrix,vector = mosfet_stamp(matrix,vector,2,1,3,Vth,K,Lambda,Vin[0]-Vs[0],Vdd-Vs[0])
    matrix,vector = mosfet_stamp(matrix,vector,2,1,4,Vth,K,Lambda,Vin[0]-Vs[1],Vdd-Vs[1])
    matrix,vector = resistor_stamp(matrix,vector,3,5,6) 
    matrix,vector = resistor_stamp(matrix,vector,4,6,8)
    matrix,vector = resistor_stamp(matrix,vector,5,0,15)
    matrix,vector = resistor_stamp(matrix,vector,6,0,20)
    branch_current_matrix_rhs = np.linalg.solve(matrix,vector)
    Vs[0] = branch_current_matrix_rhs[2]
    Vs[1] = branch_current_matrix_rhs[3]
print("branch_current_matrix_rhs", branch_current_matrix_rhs)
"""
for j in range(max_iterations):
    for i in range (N):
        matrix,vector = voltage_source_stamp(matrix,vector,i,0,Vin[i],num_nodes)
        num_nodes +=1
    matrix,vector = voltage_source_stamp(matrix,vector,N,0,Vdd,num_nodes)

    for i in range(2*N):
        mosfet +=1
        matrix,vector = mosfet_stamp(matrix,vector,N,i,N+mosfet,Vth,K,Lambda,Vin[i]-Vs[i],Vdd-Vs[i])
    mosfet = 0
    for i in range(2*N+2):
        resistor +=1
        mosfet += 1
        resistor_stamp(matrix,vector,N+mosfet,N+mosfet+resistor,G[i[0]])

"""
    
