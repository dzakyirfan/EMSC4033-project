def project_documentation():
    markdown_documentation= """ This is the documentation to give description of contained
    functions. These functions were constructed to perform data visualization from velocity subsurface of a region. The functions have different purpose, including for importing database, arranging dataset which are visualization-ready, and subsetting dataset to create two-dimensional slice of subsurface volume.

# Subsurface Velocity of Basin
Velocity data that have been acquired can be visualized to illustrate the velocity distribution as one of important geological parameters to indicate basin lithology and/or structure. The visualization is important to be done in two- or three-dimensional to see the distribution pattern for further analysis

## Importing data
The data is usually obtained from numerous measurements in the same point as well as different point. It leads to hundreds of large-sized database that should be imported. In order to import the data effectively, the dedicated function of importing file was constructed to acquire and merge different files into one single database

## Dataset for Plotly Visualization
Plotly is a Python visualization package that require grid data as the input. The unified database will be further tailored to follow the required structure that is plotly-friendly

## Create Slice Data
While Matplotlib and Plotly can execute 3D visualization, 2D plots are also needed to display clearer velocity parameters in certain orientations. This project will create two-dimensional slices in constant latitude (east-west), constant longitude (north_south), as well as diagonal direction

## Iso-velocity contour
Create depth contour map of constant velocity value (for example, visualize depth contour from V = 1.0 km/s or V = 2.5 km/s) 
    """
    
    return markdown_documentation

def import_file(filenames):   
    """
    Input parameter: list of .dat or .txt file
    Function purpose: Read and import multiple files in which a single file correspond to an individual location with given latitude and longitude. Each file will be structured, stacked, and arranged into one 2D numpy array
    Return: A 2D numpy array with four columns which consist of latitude, longitude, depth, and velocity, respectively
    """
    #Import module
    import numpy as np
    
    #Raise exception
    if not type(filenames) is list:
        raise TypeError("Your input data should be list of external files")
    
    #Empty list
    vs_array_list = []
    
    #Generate numpy arrays from individual files
    for file in filenames:
        #Import a single. dat file
        vs_velarray = np.genfromtxt(file, skip_header=1, usecols=1)
        vs_deptharray = np.genfromtxt(file, skip_header=1, usecols=0)
        vs_darray = np.negative(vs_deptharray)

        vs_lat = np.genfromtxt(file, usecols=1, max_rows=1)
        vs_lon = np.genfromtxt(file, usecols=0, max_rows=1)
    
        vs_latarray = np.full(len(vs_darray), vs_lat)
        vs_lonarray = np.full(len(vs_darray), vs_lon)

        #Join 1D arrays of lat, lon, depth, and shear wave into a 2D array
        single_location_data = np.stack((vs_latarray, 
                                         vs_lonarray, 
                                         vs_darray, 
                                         vs_velarray), 
                                        axis=1)
    
        #Append 2D array of one measurement site to the vs_arraylist
        vs_array_list.append(single_location_data)
     
    #Join all 2D arrays into one single 2D arrays    
    vs_array = np.concatenate(vs_array_list)
    
    return vs_array

def parameter_list(array):
    """Input parameter: 2D Numpy array of merged velocity dataset
    Function purpose: Create list of values of latitude, longitude, and depth through subsetting the array input and using numpy unique function
    Return: Lists of unique values
    """
    #Import module
    import numpy as np
    
    #Exception handling
    if type(array) != np.ndarray:
        raise TypeError("Input must be a numpy array")
    if array.shape[1] < 3:
        raise Exception("Inadequate number of columns to generate unique value lists")
    
    #Subsetting vs_array vertically
    latitude = array[:,0]
    longitude = array[:,1]
    depth = array[:,2]
    shearvel = array[:,3]

    #Obtain unique value of coordinate and depth
    lat_list = np.unique(latitude)
    long_list = np.unique(longitude)
    d_list = np.unique(depth)
        
    return lat_list, long_list, d_list

def basin_scatterplot(array):
    """Input parameter: 2D Numpy array of merged velocity dataset
    Function purpose: Visualize the velocity distribution in a given coordinate and depth through 3D scatterplot using Matplotlib
    Return: 3D Matplotlib visualization
    """
    #Import module
    import numpy as np
    import matplotlib.pyplot as plt
    
    #Raise exception 
    if type(array) != np.ndarray:
        raise TypeError("Input must be a numpy array")
    if array.shape[1] < 4:
        raise Exception("Insufficient data size for 3D plotting")
    elif array.shape[1] > 4:
        raise Exception("Data size exceeding required size for 3D plotting")
    
    latitude = array[:,0]
    longitude = array[:,1]
    depth = array[:,2]
    shearvel = array[:,3]
    
    fig = plt.figure(figsize=(12, 12))
    ax = plt.axes(projection='3d')

    basin_plot = ax.scatter3D(latitude, longitude, depth, c=shearvel, cmap='rainbow_r')

    colorbar = plt.colorbar(basin_plot, pad=0.2)
    colorbar.ax.set_ylabel('Shear wave (km/s)')

    ax.set_xlabel('Latitude')
    ax.set_ylabel('Longitude')
    ax.set_zlabel('Depth')

    ax.invert_xaxis()

    return plt.show()

def plotly_friendly_dataframe(filled_array):
    """Input parameter: 2D Numpy array of merged velocity dataset
    Function purpose: Arrange new dataset in Pandas DataFrame type that can be readily plotted for 
    3D plotly visualization. The dataset in the form of array should be rearranged to follow the grid pattern in order to be plotly-friendly
    Return: Velocity dataset in the form of Pandas DataFrame"""
    
    #Import modules
    import numpy as np
    import pandas as pd
    
    #Raise exception
    if type(filled_array) != np.ndarray:
        raise TypeError("Input must be a numpy array")
    if filled_array.shape[1] < 4:
        raise Exception("Insufficient data size to convert to Pandas DataFrame")
    elif filled_array.shape[1] > 4:
        raise Exception("Data size exceeding the required size to convert to Pandas DataFrame")
    
    #Call parameter_list() to generate lists of values
    lat_value, lon_value, d_value = parameter_list(filled_array)
    
    #Create coordinate grids
    lon_grid, lat_grid, d_grid = np.meshgrid(lon_value, lat_value, d_value)

    #Create initial grid for vs
    vel_grid = np.full(lon_grid.shape, -99.99)
    
    #Create 2D array from horizontally-stacked flattened grids
    grid_array = np.stack((lat_grid.flatten(), 
                           lon_grid.flatten(), 
                           d_grid.flatten(), 
                           vel_grid.flatten()), 
                          axis=1) #Stacking order should be the same with vs_array
    
    #Concatenate vs_array with grid_array
    first_concatenation = np.concatenate((filled_array, grid_array), axis=0)
    
    #Convert the first concatenation to Dataframe
    concatenation_df = pd.DataFrame(first_concatenation, 
                                      columns=['Latitude', 'Longitude', 'Depth', 'Vs'])

    #Drop flattened grid that has the same coordinate from vs_array
    vs_dataframe = concatenation_df.drop_duplicates(subset=["Latitude", "Longitude", "Depth"],
                                                     keep='first')
    
    #Sort dataframe by latitude, longitude, and depth respectively 
    vs_database = vs_dataframe.sort_values(by=['Latitude', 'Longitude', 'Depth'])
    
    #replace grid with no values with null
    vs_database['Vs'] = vs_database['Vs'].replace(-99.99, np.nan)
    
    return vs_database

def northeast_southwest_slice(array, dataframe):
    """Input: Velocity dataset in the form of numpy array and pandas dataframe
    Function purpose: Subset the velocity dataframe to create new dataframe with data only from northeast-southwest coordinates to make visualization-ready dataset
    Return: New pandas dataframe that store data in northeast-southwest line"""
            
    #Import module    
    import numpy as np
    import pandas as pd
    
    #Raise exception
    if type(array) != np.ndarray and type(dataframe) != pd.core.frame.DataFrame:
        raise TypeError("Invalid type of input")
    if array.shape[1] < 4:
        raise Exception("Insufficient data size to convert to Pandas DataFrame")
    elif array.shape[1] > 4:
        raise Exception("Data size exceeding the required size to convert to Pandas DataFrame")  
    if len(dataframe.columns) != 4:
        raise Exception("Dataframe has no suitable shape for generate sliced dataset")
    
    lat_val, lon_val, d_val = parameter_list(array)
    
    #Pair the coordinate combination for NE-SW diagonal plot
    if len(lat_val) == len(lon_val):
        nesw = np.stack((lat_val, lon_val), axis=1)
    elif len(lat_val) > len(lon_val):
        residue = len(lat_val) - len(lon_val)
        nesw = np.stack((lat_val[:-residue], lon_val), axis=1)
    else:
        residue = len(lon_val) - len(lat_val)
        nesw = np.stack((lat_val, lon_val[:-residue]), axis=1)
    
    #Convert 2D numpy array of coordinate pair into dataframe
    nesw_coordinate = pd.DataFrame(nesw, columns=['Latitude', 'Longitude'])   
    
    #Subset vs_database from northeast-southwest coordinate
    keys = list(nesw_coordinate.columns.values)
    i1 = dataframe.set_index(keys).index
    i2 = nesw_coordinate.set_index(keys).index
    nesw_df = dataframe[i1.isin(i2)]
    
    #Drop null value from the database
    nesw_dataframe = nesw_df.dropna()
    
    return nesw_dataframe

def northwest_southeast_slice(array, dataframe):
    """Input: Velocity dataset in the form of numpy array and pandas dataframe
    Function purpose: Subset the velocity dataframe to create new dataframe with data only from northwest-southeast coordinates to make visualization-ready dataset
    Return: New pandas dataframe that store data in northwest-southeast line"""
            
    #Import modules
    import numpy as np
    import pandas as pd
        
    #Raise exception  
    if type(array) != np.ndarray and type(dataframe) != pd.core.frame.DataFrame:
        raise TypeError("Invalid type of input")
    if array.shape[1] < 4:
        raise Exception("Insufficient data size to convert to Pandas DataFrame")
    elif array.shape[1] > 4:
        raise Exception("Data size exceeding the required size to convert to Pandas DataFrame")
    
    if len(dataframe.columns) != 4:
        raise Exception("Dataframe has no suitable shape for generate sliced dataset")

    lat_val, lon_val, d_val = parameter_list(array)
    
    #Create flipped lat_val
    flipped_lat = np.flip(lat_val)
    
    #Pair the coordinate combination for NW-SE diagonal plot
    if len(flipped_lat) == len(lon_val):
        nwse = np.stack((flipped_lat, lon_val), axis=1)
    elif len(flipped_lat) > len(lon_val):
        res = len(flipped_lat) - len(lon_val)
        nwse = np.stack((flipped_lat[:-res], lon_val), axis=1)
    else:
        res = len(lon_val) - len(flipped_lat)
        nwse = np.stack((flipped_lat, lon_val[:-res]), axis=1)
        
    #Convert 2D numpy array of coordinate pair into dataframe
    nwse_coordinate = pd.DataFrame(nwse, columns=['Latitude', 'Longitude'])   
        
    #Subset vs_database from northeast-southwest coordinate
    keys = list(nwse_coordinate.columns.values)
    i1 = dataframe.set_index(keys).index
    i2 = nwse_coordinate.set_index(keys).index
    nwse_df = dataframe[i1.isin(i2)]
    
    #Drop rows with null Vs
    nwse_dataframe = nwse_df.dropna()
        
    return nwse_dataframe

def north_south_slice(dataframe, long):
    """Input: Pandas DataFrame of velocity dataset, longitude value from velocity dataset
    Function purpose: Build new Pandas DataFrame for visualization of north-south cross section at constant longitude that are available from the database
    Return: Pandas DataFrame of north-south direction"""
    
    #Import module
    import pandas as pd
    
    #Exception handling
    if type(dataframe) != pd.core.frame.DataFrame:
        raise TypeError("Invalid type of dataset")
    if len(dataframe.columns) != 4:
        raise Exception("Input dataframe has no suitable shape for generate sliced dataset")  
    if type(long) is str:
        raise Exception("Number input of longitude is required!")
    
    #Subset dataframe in desired constant longitude
    north_south_df = dataframe[dataframe['Longitude'] == long]
    north_south_dataframe = north_south_df.dropna()
    
    return north_south_dataframe

def east_west_slice(dataframe, lat):
    """Input: Pandas DataFrame of velocity dataset, latitude value from velocity dataset
    Function purpose: Build new Pandas DataFrame for visualization of east-west cross section at constant latitude that are available from the database
    Return: Pandas DataFrame of east-west direction"""
    
    #Import module
    import pandas as pd
    
    #Exception handling
    if type(dataframe) != pd.core.frame.DataFrame:
        raise TypeError("Invalid type of dataset")
    if len(dataframe.columns) != 4:
        raise Exception("Input dataframe has no suitable shape for generate sliced dataset")   
    if type(lat) is str:
        raise Exception("Number input of latitude is required!")
    
    #Subset dataframe in desired constant longitude
    east_west_df = dataframe[dataframe['Latitude'] == lat]
    east_west_dataframe = east_west_df.dropna()
    
    return east_west_dataframe

def slice_scatterplot(dataframe):
    """Input: Pandas Dataframe of velocity dataset
    Function purpose: Visualize 2D cross-sections of 3D basin volume using Matplotlib. The visualization utilize 3D scatterplot to show the cross-section location in the 3D area
    Return: 3D Matplotlib visualization"""
    
    #Import module
    import matplotlib.pyplot as plt
    
    #Exception handling
    if len(dataframe.columns) != 4:
        raise Exception("Input dataframe has no suitable shape for visualize sliced dataset")
    if list(dataframe.columns) != ['Latitude', 'Longitude', 'Depth', 'Vs']:
        raise Exception("Input dataframe does not contain desired parameters to plot")
    
    fig = plt.figure(figsize=(12,12))
    ax = plt.axes(projection='3d')
    surf = ax.scatter3D(dataframe['Longitude'],
                          dataframe['Latitude'],
                          dataframe['Depth'],
                          c=dataframe['Vs'],
                          cmap='RdBu')

    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_zlabel('Depth')

    colorbar = plt.colorbar(surf)
    colorbar.ax.set_ylabel('Shear Wave (km/s)')

    return plt.show()

def northeast_southwest_contourplot(nesw_dataframe):
    """Input: Pandas Dataframe of northeast-southwest slice dataset
    Function purpose: Visualize 2D cross-sections of 3D basin volume in the form of filled contour plot across northeast - southwest line
    Return: 2D Matplotlib visualization"""
    
    #Exception handling
    if len(nesw_dataframe.columns) != 4:
        raise Exception("Input dataframe has no suitable shape for visualize sliced dataset")
    if list(nesw_dataframe.columns) != ['Latitude', 'Longitude', 'Depth', 'Vs']:
        raise Exception("Input dataframe does not contain desired parameters to plot")
        
    #Import module
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    
    #2D Contourplot
    x_long = nesw_dataframe['Longitude']
    x_lat = nesw_dataframe['Latitude']
    y = nesw_dataframe['Depth']
    z = nesw_dataframe['Vs']
    levels = np.linspace(z.min(), z.max(), 250)

    #Define Plot Matrix
    fig, ax = plt.subplots(2, 1, figsize=(12, 6))
    fig.tight_layout()

    #Plot with respect to longitude
    ax[0].plot(x_long, y, 'o', markersize=0.5)
    cont1 = ax[0].tricontourf(x_long, y, z, levels=levels, cmap='RdBu')
    ax[0].set(xlim=(x_long.min(), x_long.max()), ylim=(y.min(), y.max()))
    ax[0].set_xlabel('Longitude')
    ax[0].set_ylabel('Depth')
    ax[0].set_title('NE - SW Cross Section of Velocity Structure')
    ax[0].annotate('Southwest', (106.74, -3.5), bbox=dict(boxstyle="round", fc="0.9", ec="gray"), size=12)
    ax[0].annotate('Northeast', (106.99, -3.5), bbox=dict(boxstyle="round", fc="0.9", ec="gray"), size=12)

    fig.colorbar(cont1, ax=ax[0])

    #Plot with respect to latitude
    ax[1].plot(x_lat, y, 'o', markersize=0.5)
    cont2 = ax[1].tricontourf(x_lat, y, z, levels=levels, cmap='RdBu')
    ax[1].set(xlim=(x_lat.min(), x_lat.max()), ylim=(y.min(), y.max()))
    ax[1].set_xlabel('Latitude')
    ax[1].set_ylabel('Depth')
    ax[1].annotate('Southwest', (-6.42, -3.5), bbox=dict(boxstyle="round", fc="0.9", ec="gray"), size=12)
    ax[1].annotate('Northeast', (-6.11, -3.5), bbox=dict(boxstyle="round", fc="0.9", ec="gray"), size=12)

    fig.colorbar(cont2, ax=ax[1])

    return plt.show()

def northwest_southeast_contourplot(nwse_dataframe):
    """Input: Pandas Dataframe of northwest-southeast slice dataset
    Function purpose: Visualize 2D cross-sections of 3D basin volume in the form of filled contour plot across northwest - southeast line
    Return: 2D Matplotlib visualization"""
    
    #Exception handling
    if len(nwse_dataframe.columns) != 4:
        raise Exception("Input dataframe has no suitable shape for visualize sliced dataset")
    if list(nwse_dataframe.columns) != ['Latitude', 'Longitude', 'Depth', 'Vs']:
        raise Exception("Input dataframe does not contain desired parameters to plot")
    
    #Import module
    import numpy as np
    import matplotlib.pyplot as plt
    
    #2D Contourplot
    x_long = nwse_dataframe['Longitude']
    x_lat = nwse_dataframe['Latitude']
    y = nwse_dataframe['Depth']
    z = nwse_dataframe['Vs']
    levels = np.linspace(z.min(), z.max(), 250)

    #Define Plot Matrix
    fig, ax = plt.subplots(2, 1, figsize=(12, 6))
    fig.tight_layout()

    #Plot with respect to longitude
    ax[0].plot(x_long, y, 'o', markersize=0.5)
    cont3 = ax[0].tricontourf(x_long, y, z, levels=levels, cmap='RdBu')
    ax[0].set(xlim=(x_long.min(), x_long.max()), ylim=(y.min(), y.max()))
    ax[0].set_xlabel('Longitude')
    ax[0].set_ylabel('Depth')
    ax[0].set_title('NW - SE Cross Section of Velocity Structure')
    ax[0].annotate('Northwest', (106.67, -3.5), bbox=dict(boxstyle="round", fc="0.9", ec="gray"), size=12)
    ax[0].annotate('Southeast', (106.89, -3.5), bbox=dict(boxstyle="round", fc="0.9", ec="gray"), size=12)

    fig.colorbar(cont3, ax=ax[0])

    #Plot with respect to latitude
    ax[1].plot(x_lat, y, 'o', markersize=0.5)
    cont4 = ax[1].tricontourf(x_lat, y, z, levels=levels, cmap='RdBu')
    ax[1].set(xlim=(x_lat.min(), x_lat.max()), ylim=(y.min(), y.max()))
    ax[1].set_xlabel('Latitude')
    ax[1].set_ylabel('Depth')
    ax[1].annotate('Southeast', (-6.40, -3.5), bbox=dict(boxstyle="round", fc="0.9", ec="gray"), size=12)
    ax[1].annotate('Northwest', (-6.12, -3.5), bbox=dict(boxstyle="round", fc="0.9", ec="gray"), size=12)

    fig.colorbar(cont4, ax=ax[1])

    return plt.show()

def latitudinal_longitudinal_contourplot(dataframe, coordinate_type):
    """Input: Pandas Dataframe of constant latitude or longitude, and type of coordinate (either 'Latitude' or 'Longitude')
    Function purpose: Visualize 2D cross-sections of 3D basin volume in the form of filled contour plot across north-south or east-west direction
    Return: 2D Matplotlib visualization"""
    
    #Exception handling
    if len(dataframe.columns) != 4:
        raise Exception("Input dataframe has no suitable shape for visualize sliced dataset")
    if list(dataframe.columns) != ['Latitude', 'Longitude', 'Depth', 'Vs']:
        raise Exception("Input dataframe does not contain desired parameters to plot")
    if coordinate_type not in ['Latitude', 'Longitude']:
        raise Exception("Invalid coordinate type")
    
    #Import module
    import numpy as np
    import matplotlib.pyplot as plt
    
    x = dataframe[coordinate_type]
    y = dataframe['Depth']
    vel = dataframe['Vs']
    levels = np.linspace(vel.min(), vel.max(), 250)

    #Define Plot Matrix
    fig, ax = plt.subplots(figsize=(12, 6))
    fig.tight_layout()

    #Plot
    ax.plot(x, y, 'o', markersize=0.5)
    plot_nondiagonal = ax.tricontourf(x, y, vel, levels=levels, cmap='RdBu')
    ax.set(xlim=(x.min(), x.max()), ylim=(y.min(), y.max()))
    ax.set_xlabel(coordinate_type)
    ax.set_ylabel('Depth')
    ax.set_title(coordinate_type + ' Cross Section of Velocity Structure')

    cbar6 = plt.colorbar(plot_nondiagonal)
    cbar6.ax.set_ylabel('Shear wave (km/s)')

    return plt.show()

def isovelocity(filenames, velocity):
    """Input: list of file directories, a velocity value
    Function purpose: built 2D numpy array that contains depth of desired constant velocity to create isovelocity contour map. This 2D numpy array is made through the iteration of available files, interpolate the depth of desired velocity value, and stack all data into one single array
    Return: 2D array of iso-velocity data"""
    
    #Exception Handling
    if not type(filenames) is list:
        raise TypeError("Your input data should be list of external files")
    if not type(velocity) is float:
        raise TypeError("Your input velocity should be float type")
    
    import numpy as np
    
    #empty list
    z_list = []

    #Create numpy array with loop
    for file in filenames:
        #Import a single .dat file
        vs_velarray = np.genfromtxt(file, skip_header=1, usecols=1)
        vs_deptharray = np.genfromtxt(file, skip_header=1, usecols=0)
    
        vs_lat = np.genfromtxt(file, usecols=1, max_rows=1)
        vs_lon = np.genfromtxt(file, usecols=0, max_rows=1)
        
        #Interpolate for obtaining depth location of input velocity (ZVel)
        #For example, Z1.3 is the depth where the shear wave velocity equals 1.3 km per second
        z = np.interp(velocity, vs_velarray, vs_deptharray)
        z_and_coordinate = np.array([vs_lat, vs_lon, z*1000])
        z_list.append(z_and_coordinate)
    
    #Join all arrays in z1_list
    z_array = np.vstack(z_list)
    
    return z_array
