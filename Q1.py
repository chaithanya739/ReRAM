import matplotlib.pyplot as plt
import numpy as np
N = 100
I_ideal = []
I_out_a = []
for j in range (10):
    Vin = np.random.uniform(0,1,N)
    G = np.random.uniform(10e-6,100e-6,N)
    I = np.zeros(N)
    for i in range(N):
        I[i] = Vin[i]*G[i]
    I_ideal.append(np.sum(I))
print(I_ideal)
# Here in Question 1 I_out_a = I_ideal
I_out_a = I_ideal
plt.scatter(I_out_a,I_ideal)
plt.xlabel('I_ideal')
plt.ylabel('I_out_a')
plt.title('I_out_a vs I_ideal')
plt.show()

