def p_surface():
    """@todo: Docstring for p_surface
    
    :arg1: @todo
    :returns: @todo
    """
    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib import cm
    from matplotlib.ticker import LinearLocator, FormatStrFormatter
    import matplotlib.pyplot as plt
    import numpy as np
    from netCDF4 import Dataset
    infile='/home/chris/codescratch/mkmov/examples/cordex24-ERAI01_1d_20040101_20040111_grid_T_2D.nc'
    ifile=Dataset(infile, 'r')
    varone=ifile.variables['zos']
    Z=varone[0,:,:]

    plt.close('all')
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    X = np.linspace(-5, 5, 431)
    Y = np.linspace(-5, 5, 289)
    X, Y = np.meshgrid(X, Y)

    surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.seismic,
                           linewidth=0, antialiased=False,vmin=-1,vmax=1)

    cset = ax.contourf(X, Y, Z, zdir='z', offset=-1.6,
                    levels=np.linspace(-1,1,30),cmap=plt.cm.jet)

    fig.colorbar(surf, shrink=0.5, aspect=5)

    plt.show()

def p_cube():
    """@todo: Docstring for p_cube
    
    :arg1: @todo
    :returns: @todo
    """
    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib import cm
    from matplotlib.ticker import LinearLocator, FormatStrFormatter
    import matplotlib.pyplot as plt
    import numpy as np
    from netCDF4 import Dataset

    #load data 
    infile='/home/chris/codescratch/mkmov/examples/cordex24-ERAI01_1d_19890101_19890105_grid_T_T3D.nc'
    ifile=Dataset(infile, 'r')
    varone=ifile.variables['thetao']
    Z=varone[0,0,:,:]

    plt.close('all')
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    #X = np.arange(-5, 5, 0.25)
    #Y = np.arange(-5, 5, 0.25)

    X = np.linspace(-5, 5, 431)
    Y = np.linspace(-5, 5, 289)
    X, Y = np.meshgrid(X, Y)


    #cset = ax.contourf(X, Y, Z, zdir='z', offset=30,
                    #levels=np.linspace(0,30,30),cmap=plt.cm.jet)

    #t,z,y,x
    Z=varone[4,::-1,:,-5]
    X = np.linspace(-5, 5, 289)
    Y = np.linspace(-5, 5, 75)
    X, Y = np.meshgrid(X, Y)

    cset = ax.contourf(X, Y, Z, offset=5,zdir='z',
                    levels=np.linspace(np.min(Z),np.max(Z),30),cmap=plt.cm.jet)

    #plt.close('all')
    #fig=plt.figure()
    ax=fig.add_subplot(1, 2,1)
    cs1=ax.contourf(X,Y,Z,levels=np.linspace(np.min(Z),np.max(Z),30),cmap='jet')
    fig.colorbar(cs1, shrink=0.5, aspect=5)
    plt.show()



    Z=varone[4,:,5,:]
    X = np.linspace(-5, 5, 431)
    Y = np.linspace(-5, 5, 75)
    X, Y = np.meshgrid(X, Y)

    cset = ax.contourf(X, Y, Z, offset=-5,zdir='y',
                    levels=np.linspace(np.min(Z),np.max(Z),30),cmap=plt.cm.jet)


    #fig.colorbar(surf, shrink=0.5, aspect=5)
    #ax.set_zlim(-1.01, 1.01)

    #ax.zaxis.set_major_locator(LinearLocator(10))
    #ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

    #fig.colorbar(surf, shrink=0.5, aspect=5)

    plt.show()

p_cube()
