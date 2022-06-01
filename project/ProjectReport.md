# Project Report

## Introduction
This project has developed data structuring and visualization programs for geophysical dataset, especially subsurface geological/geophysical properties. The dataset I have used to develop this project is subsurface velocity of Jakarta Basin. Velocity is one of important subsurface parameter in a given location or geological unit. The subsurface velocity gives information or proxy on other geological parameters, such as porosity, pore fluid, or shear stress. Besides indicating subsurface characteristics, subsurface velocity could tell the information about geological structure, lithology unit, and facies distribution. The velocity data can be harnessed to predict earthquake response or determine suitable site for drilling. 

## List of Dependencies
This project uses Python as a primary programming language, as well as using Jupyter and Anaconda as Python-related platforms. The project also used some dependencies, or Python modules, to facilitate and accelerate code-writing. The dependencies are listed as below:
- `os` : this module provide function to interacting with operating system of user's PC. `os` enable access to file system through directory path. Directory to file system was necessary in this project in order to be able to import input files for building dataset.
- `glob`: this module finds all pathnames that match specified pattern. This module enable access to all necessary files which have same file extension for instantaneous import
- `numpy`: this package will be heavily relied on in the project's functions. `numpy` is a library for the Python programming language, adding support for large, multi-dimensional arrays and matrices, along with a large collection of high-level mathematical functions to operate on these arrays. `numpy` was used to construct data arrays to store large-scale basin dataset, being input for data visualizatiom, as well as performing built-in function such as **interpolation** to create readily-plotted dataset.
- `pandas`: this project depends on this package along with `numpy`. `pandas` are used to construct **Pandas DataFrame** to store two-dimensional basin dataset with more clarity than **Numpy array** in terms of displaying data parameters through the column names. This package will also be applied to executing data manipulation and analysis such as subsetting dataframe to create certain smaller-scale dataset, sorting dataset, removing redundant data, etc.
- `matplotlib`: this package will be used as simple and fundamental library for visualizing basin dataset in the form of 3D volume or its 2D cross-sections.
- `plotly`: this project will also use `plotly` as data visualization library, with some advantages over `matplotlib` in terms of interactive display. This include rotate-able visualization, and zoom features that will help seeing more detailed velocity structure. However, running `plotly` will require large memory that could affect the efficiency of project execution, depending on users' PC.

## Instruction
This section contains guideline for functions that were created for this project. There are total 14 functions, in which all of them can be categorized according to roles as listed below:

### Documentation
**project_documentation()** return brief summary of project activities

### Data Importing
**import_file()** handle file importing through iteration and assemble multiple raw files into a single dataset with defined array shape. Each file represent single location defined by latitude and longitude, but all file has the same depth interval. This function require list of filenames as an input, and return the expected basin dataset in the form of two-dimensional numpy array

### List Making
**parameter_list()** make lists of unique values in latitude, longitude, and depth. This function require numpy array that has been created from **import_file()**, and return a tuple of unique values

### DataFrame Building
- **plotly_friendly_dataframe()** construct basin dataset in Pandas DataFrame with manipulation of data shape to follows grid-like shape that is permissible for `plotly` visualization. Because most basin have irregular boundaries, the geophysical data will usually follow the basin extent. This will lead to irregular data distribution that are difficult to follow the rectangular grid shape. This function will overcome this irregularity problem by adding null data in wider-defined rectangular area that bound the original basin extent. 
This function require numpy array from **import_file()** and return the Pandas DataFrame that has followed a rectangular shape
- **northeast_southwest_slice()** construct basin dataset with coordinates in northeast - southwest diagonal line only, through latitude-longitude pairing and dataframe subsetting. This function require primary dataframe from **plotly_friendly_dataframe()** and return the sliced dataframe
- **northwest_southeast_slice()** construct basin dataset with coordinates in northwest - southeast diagonal line only, through latitude-longitude pairing and dataframe subsetting. This function require primary dataframe from **plotly_friendly_dataframe()** and return the sliced dataframe
- **north_south_slice()** construct basin dataset with coordinates in north-south line only, through subsetting in a constant longitude. This function require primary dataframe from **plotly_friendly_dataframe()** and return the sliced dataframe
- **east_west_slice()** construct basin dataset with coordinates in east-west line only, through subsetting in a constant latitude. This function require primary dataframe from **plotly_friendly_dataframe()** and return the sliced dataframe

### Data Visualization
- **basin_scatterplot()** visualize dataframe from **plotly_friendly_dataframe()** using `matplotlib`. This function require primary dataframe from **plotly_friendly_dataframe()** and return the 3D `matplotlib` scatterplot
- **slice_scatterplot()** visualize sliced dataframe  using `matplotlib`. This function require primary dataframe from **northeast_southwest_slice()**, **northwest_southeast_slice()**, **north_south_slice()**, **east_west_slice()**, and return the 3D `matplotlib` scatterplot
- **northeast_southwest_contourplot()** and **northwest_southeast_contourplot()** visualize sliced dataframe in diagonal directions using triangulated contour fill from `matplotlib`. These functions require sliced dataframe of respective orientations and return two `matplotlib` contour map, each map is basically the same but with different x axis (one using longitude and one using latitude)
- **latitudinal_longitudinal_contourplot()** visualize sliced dataframe in horizontal or vertical directions using triangulated contour fill from `matplotlib`. This function requires sliced dataframe from **north_south_slice()** with a latitude value from **parameter_list()** or **east_west_slice()** with a longitude value from **parameter_list()**, and return a contour map

### Constant Velocity Map Making
- **isovelocity()** generate numpy array that contains depth of certain velocity. Given that velocity are measure parameter in which is extremely difficult to obtain regular interval values, certain velocity map can be generated through depth interpolation in each locations. This function requires list of file directories and desired velocity value as the input, and return the numpy array consists of latitude, longitude, and depth.

## Testing

### Documentation
**test_project_documentation()** assert whether the documentation type is string or not

### Data Importing
**test_import_file()** assert if the type of dataset output is numpy array with four number of columns, following three-dimensional coordinate (latitude, longitude, depth) and velocity as targeted subsurface properties

### List Making
**test_parameter_list()** assert if the type of output is tuple that contains three lists, each list contain unique values of latitude, longitude, and depth

### DataFrame Building
- **test_plotly_friendly_dataframe()** assert whether the dataset output is in Pandas DataFrame or not, as well as checking that the number of columns is supposedly four
- **test_northeast_southwest_slice()** assert whether the dataset output is in Pandas DataFrame or not, the number of columns is supposedly four, and check that the depth extent of this sliced dataframe is same with the depth extent of primary dataframe
- **test_northwest_southeast_slice()** assert whether the dataset output is in Pandas DataFrame or not, the number of columns is supposedly four, and check that the depth extent of this sliced dataframe is same with the depth extent of primary dataframe
- **test_north_south_slice()** assert whether the dataset output is in Pandas DataFrame or not, the number of columns is supposedly four, the depth extent of this sliced dataframe is same with the depth extent of primary dataframe, and the longitude value on the dataframe is the same for all rows
- **test_east_west_slice()** assert whether the dataset output is in Pandas DataFrame or not, the number of columns is supposedly four, the depth extent of this sliced dataframe is same with the depth extent of primary dataframe, and the latitude value on the dataframe is the same for all rows

### Data Visualization
- **test_basin_scatterplot()** assert if the function can return the visualization image
- **test_slice_scatterplot()** assert if the function can return the visualization image
- **test_northeast_southwest_contourplot()** and **test_northwest_southeast_contourplot()** assert if the function can return the visualization image
- **test_latitudinal_longitudinal_contourplot()** assert if the function can return the visualization image

### Constant Velocity Map Making
- **test_isovelocity()** assert if the type of dataset ouput is numpy array and consists of three columns

## Limitations/Future Improvement
- The aforementioned functions were made to follow the measurement grid in Jakarta Basin. While the measurement follows the irregular basin extent of Jakarta, the measurement follow regular grid of latitude and longitude, resulting in lesser unique values in latitude and longitude lists. However, there might be irregular measurement point intervals in a region due to geographical, political, or administrative constraint. The irregular measurement plot could be more difficult for these functions to be applied. This irregularity problems can be overcome through the grid interpolation
- There are many more visualization package with more options and features such as PyVista. However, packages that have more elaborate features usually require more computing power and time. This will affect the running efficiency of a program. More efficient project execution can be performed by closing background apps in a PC or using more high-specification devices.
- diagonal have no defined coordinate parameter because this basin data follow latitude-longitude format. Diagonal line have varied lat-long value in each point, hence the visualization of the same line was performed twice to give more clarity in terms of latitude and longitude.
