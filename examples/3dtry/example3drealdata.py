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
    # working from
    # http://stackoverflow.com/questions/36046338/contourf-on-the-faces-of-a-matplotlib-cube
    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib import cm
    from matplotlib.ticker import LinearLocator, FormatStrFormatter
    import matplotlib.pyplot as plt
    import numpy as np
    from netCDF4 import Dataset

    #load data 
    infile='/home/chris/codescratch/mkmov/examples/cordex24-ERAI01_1d_19890101_19890105_grid_T_T3D.nc'
    infile='/srv/ccrc/data42/z3457920/20151012_eac_sep_dynamics/nemo_cordex24_ERAI01/1989/cordex24-ERAI01_1d_19890101_19890105_grid_T_T3D.nc'
    infile='/home/chris/mount_win/cordex24-ERAI01_1d_19890101_19890105_grid_T_T3D.nc'
    ifile=Dataset(infile, 'r')
    varone=ifile.variables['thetao']

    #get global values of varone
    sides=[varone[4,0,:,:],\
            varone[4,::-1,:,5],\
            varone[4,::-1,:,-5],\
            varone[4,::-1,2,:]]

    gmin=[]
    gmax=[]
    for field in sides:
        gmin.append(np.min(field))
        gmax.append(np.max(field))
    levs=np.linspace(np.min(gmin),np.max(gmax),30)


    Z=varone[4,0,:,:]


    plt.close('all')
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    #X = np.arange(-5, 5, 0.25)
    #Y = np.arange(-5, 5, 0.25)

    X = np.linspace(-5, 5, 289)
    Y = np.linspace(-5, 5, 431)
    X, Y = np.meshgrid(Y, X)

    #cset = ax.contourf(X, Y, Z, zdir='z', offset=30,
                    #levels=np.linspace(0,30,30),cmap=plt.cm.jet)

    #t,z,y,x
    #Z=varone[4,::-1,:,-5]
    #X = np.linspace(-5, 5, 289)
    #Y = np.linspace(-5, 5, 75)
    #X, Y = np.meshgrid(X, Y)
    cset = [[],[],[]]

    cset[0] = ax.contourf(X, Y, Z, offset=5,zdir='z',
                    levels=levs,cmap=plt.cm.jet)

    #t,z,y,x
    #5,75,289,431
    Z=varone[4,::-1,:,5]
    X = np.linspace(-5, 5, 75)
    Y = np.linspace(-5, 5, 289)
    X, Y = np.meshgrid(X, Y)

    cset[0] = ax.contourf(Z.T, Y, X, offset=-5,zdir='x',
                    levels=levs,cmap=plt.cm.jet)


    Z=varone[4,::-1,:,-5]
    X = np.linspace(-5, 5, 75)
    Y = np.linspace(-5, 5, 289)
    X, Y = np.meshgrid(X, Y)

    cset[0] = ax.contourf(Z.T, Y, X, offset=5,zdir='x',
                    levels=levs,cmap=plt.cm.jet)


    ##t,z,y,x
    ##5,75,289,431
    Z=varone[4,::-1,2,:]

    X = np.linspace(-5, 5, 431)
    Y = np.linspace(-5, 5, 75)

    X,Y=np.meshgrid(X, Y)

    cset[1] = ax.contourf(X, Z, Y, offset=-5,zdir='y',
                    levels=levs,cmap=plt.cm.jet)

    ## setting 3D-axis-limits:    
    ax.set_xlim3d(-5,5)
    ax.set_ylim3d(-5,5)
    ax.set_zlim3d(-5,5)
    #for one plot...
    #eg
    #cs1=ax.contourf(field,levels=np.linspace(-1,1,50))
    #plt.colorbar(cs1,orientation='vertical')
    plt.colorbar(cset[0],orientation='vertical')

    

    plt.show()
    import ipdb
    ipdb.set_trace()



p_cube()
