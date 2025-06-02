import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Example: 1D Heat Equation solution
x = np.linspace(0, 1, 100)
t = np.linspace(0, 2, 200)
X, T = np.meshgrid(x, t)
U = np.exp(-np.pi**2 * T) * np.sin(np.pi * X)  # Analytic solution

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.plot_surface(X, T, U, cmap='inferno')
plt.xlabel("x")
plt.ylabel("t")
plt.title("Heat Equation Solution")
plt.show()
