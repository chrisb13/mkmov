
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

plt.close('all')
fig = plt.figure()
ax = fig.gca(projection='3d')

############################################
#  plotting the 'top' layer works okay...  #
############################################

X = np.linspace(-5, 5, 43)
Y = np.linspace(-5, 5, 28)
X, Y = np.meshgrid(X, Y)

varone=np.random.rand(75,28,43)
Z=varone[0,:,:]
cset = ax.contourf(X, Y, Z, zdir='z', offset=1,
                levels=np.linspace(np.min(Z),np.max(Z),30),cmap='jet')
plt.show()

#################################################
#  but now trying to plot a vertical slice....  #
#################################################

plt.close('all')
fig = plt.figure()
ax = fig.gca(projection='3d')

Z=varone[::-1,:,-1]
X = np.linspace(-5, 5, 28)
Y = np.linspace(-5, 5, 75)
X, Y = np.meshgrid(X, Y)

#this 'projection' doesn't result in what I want, I really just want to rotate it
cset = ax.contourf(X, Y, Z, offset=5,zdir='x',
                levels=np.linspace(np.min(Z),np.max(Z),30),cmap='jet')

#here's what it should look like....
ax=fig.add_subplot(1, 2,1)
cs1=ax.contourf(X,Y,Z,levels=np.linspace(np.min(Z),np.max(Z),30),cmap='jet')
plt.show()
