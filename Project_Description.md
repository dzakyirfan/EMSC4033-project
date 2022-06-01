# EMSC4033 project plan template

## Project title
Velocity Structure of Jakarta Basin

## Executive summary

Dataset Preparation and 3D visualizations of shear-wave velocity (Vs) model from Jakarta Basin. Velocity properties of a basin are influenced by depth, geometries, and lithology of the basin. This makes the shear-waves velocities of a basin can be highly heterogeneous. The visualizations help analysing shear-wave velocity of a basin to reveal the properties pattern and distribution easier. After the 3D model was created, we can extract 2D cross-sections in multiple orientation for more apparent image of subsurface shear velocity. Furthermore, depth of constant velocity can be extracted and mapped as a proxy of basin depth or certain geological parameters. 

## Goals

- Create a function to import hundreds of raw txt file into a single, structured numpy array that is ready for data analysis
- Create a function to prepare a visualization-friendly dataset
- Create functions that enable cross-section of 3D shear-velocity model in multiple orientations: north-south, east-west, and diagonal
- Create a function to build constant-velocity depth dataset

## Background and Innovation  

A sedimentary basin consists of different geological characteristics from rocks around the basin. The difference leads to the contrasting properties and may have an implication in natural hazards, where sedimentary basin could amplify and extend the propagating seismic waves. What makes it more challenging is that there are variation of properties inside the basin. This 8033 project is the precursor of my research project, to visualize the shear-wave velocity properties of a basin in which the different values have different response toward the propagating earthquake. This project can be done using Python, specifically with pacakges such as Numpy, Pandas, Matplotlib, and Plotly. While Numpy and Matplotlib are relatively basic module for number analysis, storing, and visualizations, those modules can be utilized and crafted to subset dataset in a desired line out of 3D volume. On the other hand, Plotly offer delicate visualization with more features than Matplotlib.

## Resources & Timeline

I could be able to start this project thanks to:
- The shear-wave velocity data from Rexha Verdhona Ry as part of his research project that I will continue later on
- The suggestion and approval of Phil Cummins as my research supervisor

To build this project, I will do the following steps:
  - I will be using os, glob, and Numpy to build a function for exporting and arranging hundreds of raw data into one structured Numpy array that is ready for visualization
  - I will use the scatterplot feature of Matplotlib to build a data visualization function of subsurface velocity with respect to the coordinates and depth.
  - I will also use Plotly to visualize interactive basin model
  - The 3D model that I have visualized is then used for making the 2D cross-sections using Matplotlib. I will make functions to create dataset in desired cross-sectional area from north-south, east-west, and diagonal line by indexing, subsetting, and/or filtering Pandas DataFrame
  - The dataset of sliced lines can be an input for 2D visualization using Matplotlib triagulation contour, using matplotlib.axes.tricontourf()
  - The imported files can be further interpolated to obtain constant-velocity depth data in a built function

## Testing, validation, documentation
- Testing for data import will be created to assert the correct type of input and number of data columns in terms of parameters
- Testing for visualization to assert that the visualization function can be run
- Testing for cross-section or data slice to assert the correct data type and DataFrame structure

**Note:** You need to think about how you will know your code is correct and achieves the goals that are set out above (specific tests that can be implemented automatically using, for example, the `assert` statement in python.)  It can be really helpful if those tests are also part of the documentation so that when you tell people how to do something with the code, the example you give is specifically targetted by some test code.

_Provide some specific tests with values that you can imagine `assert`ing_
