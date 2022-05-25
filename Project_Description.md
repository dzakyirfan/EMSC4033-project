# EMSC4033 project plan template

## Project title
Velocity structure of Jakarta Basin

## Executive summary

Visualizations of the three-dimensional model of shear-wave velocity (Vs) in a Jakarta Basin. Velocity properties of a basin are influenced by depth, geometries, and lithology of the basin. This makes the shear-waves velocities of a basin can be highly heterogeneous. The visualizations help the analysis of basin shear-wave velocity, make it easier to reveal the pattern and changes. After the 3D model was created, we can extract 2D cross-sections out of it for more apparent image of velocity distribution in a requested orientation. 

## Goals

- Make a function to import hundreds of raw txt file into a single, structured numpy array that is ready for data analysis
- Visualize 3D model of shear-wave velocities of a sedimentary basin
- Create the function that enable the multi-orientation cross-section of 3D shear-velocity model

## Background and Innovation  

A sedimentary basin consists of different geological characteristics from rocks around the basin. The difference leads to the contrasting properties and may have an implication in natural hazards, where sedimentary basin could amplify and extend the propagating seismic waves. What makes it more challenging is that there are variation of properties inside the basin. This 8033 project is the precursor of my research project, to visualize the shear-wave velocity properties of a basin in which the different values have different response toward the passing earthquake. This project can be done using Python, specifically with pacakges such as Numpy, Matplotlib, Plotly, and PyVista. While Numpy and Matplotlib are rather basic packages for data arranging and visualizations, PyVista is able to create 2D line and contour surfaces that will be useful for this project.

## Resources & Timeline

I could be able to start this project thanks to:
- The shear-wave velocity data from Rexha Verdhona Ry as part of his research project that I will continue later on
- The suggestion and approval of Phil Cummins as my research supervisor

To build this project, I will do the following steps:
  - I will be using os, glob, and Numpy to build a function for exporting and arranging 442 raw data into one structured Numpy array that is ready for visualization
  - I will use the scatter plot feature of Matplotlib to visualize the velocity distribution with respect to the coordinates and depth.
  - I will also use a feature from Plotly and PyVista to visualize the 3D model and compare it with the Matplotlib
  - The 3D model that I have visualized is then used for making the 2D cross-sections using the PyVista. I will make the vertical cross-sections from north-south, east-west, and diagonal sections

## Testing, validation, documentation

**Note:** You need to think about how you will know your code is correct and achieves the goals that are set out above (specific tests that can be implemented automatically using, for example, the `assert` statement in python.)  It can be really helpful if those tests are also part of the documentation so that when you tell people how to do something with the code, the example you give is specifically targetted by some test code.

_Provide some specific tests with values that you can imagine `assert`ing_
