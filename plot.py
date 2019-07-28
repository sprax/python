
import matplotlib.pyplot as plt
import numpy as np
import sys

dfile = sys.argv[1] if len(sys.argv) > 1 else 'z_vals_201903130058.txt'
dskip = sys.argv[2] if len(sys.argv) > 2 else 0

darry = np.loadtxt(dfile, skiprows=dskip)
np.random.seed(444)
np.set_printoptions(precision=3)

# An "interface" to matplotlib.axes.Axes.hist() method
d = np.random.laplace(loc=15, scale=3, size=500)
n, bins, patches = plt.hist(x=darry, bins='auto', color='#0504aa', alpha=0.7, rwidth=0.85)
plt.grid(axis='y', alpha=0.75)
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.title('Histogram of Scoop Z-values from ' + dfile)
plt.text(23, 45, r'$\mu=15, b=3$')
maxfreq = n.max()
# Set a clean upper y-axis limit.
plt.ylim(ymax=np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10)
plt.show()
