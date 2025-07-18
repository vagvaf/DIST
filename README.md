# Automating Place Syntac Tool processes with Python

## Introduction

The aim of this repository is to provide a scripting interface to Place Syntax Tool (PST) library and its plugin for QGIS. For more info for PST visit: https://smog.chalmers.se/projects/pst-plugin-for-qgis/

Note that the user has to enter a valid path to a pst library (see inside the code for how to do that).

## Angular Betweeness

The Angular Betweeness script allows performing angular betweeness analyses. The user can use all the options that are available for the PST qgis plugin. For more information see section 6.5 and 6.4 in the PST documentation: https://www.researchgate.net/publication/385514803_PST_Documentation_v331_241101

Below there is an explanation for each option.

```
props = {
    'network': '', --- The path to the shapefile of the (segmented) network
    'crs': 3006, --- The EPSG code for the refetence system
    'radius_type':'walking', -- can be either straight, walking, steps, angular or axmeter
    'radius_threshold': 2000, --- must match the units of the chosen radius type
    'norms_none':True, --- No normalization. Can be True/False.
    'norm_normalization':True, --- Normalization (Turner 2007). Can be True/False. 
    'norm_standard':True, --- Standard normalization (0-1). Can be True/False.
    'norm_syntax':True, --- Syntax normalization (NACH). Can be True/False.
    'weigh_by_length': True, --- The analysis also offers an option for weighing by length. Can be True/False
    'output_file': "AB.shp" --- location and name of the output file.
    }
```

## Angular Integration

The Angular Integration script allows performing angular integration analyses. The user can use all the options that are available for the PST qgis plugin. For more information see section 6.3 in the PST documentation: https://www.researchgate.net/publication/385514803_PST_Documentation_v331_241101

Below there is an explanation for each option.

```
props = {
    'network': '', --- The path to the shapefile of the (segmented) network
    'crs': 3006, --- The EPSG code for the refetence system
    'radius_type':'walking', -- can be either straight, walking, steps, angular or axmeter
    'radius_threshold': 1000, --- must match the units of the chosen radius type
    'angle_threshold':0, --- All angles lower than this threshold value will be truncated to zero.
    'angle_precision':1, --- When calculating the angular deviation between two pairs of segments the angle is rounded to the closes multiple of specified angle precision
    'norm_normalization':True, --- Normalization (Turner 2007). Can be True/False. 
    'norm_hillier':True, --- Normalization (Hillier). Can be True/False. 
    'norm_syntax':True, --- Syntax normalization (NAIN. Can be True/False.
    'weigh_by_length': True, --- The analysis also offers an option for weighing by length. Can be True/False
    'output_N':True, , Provide Node count (N) output. Can be True/False.
    'output_TD':True, --- Provide Total depth (TD) output. Can be True/False.
    'output_MD':True, -- Provide Mean depth (MD) output. Can be True/False.
    'output_file': "AI.shp" --- location and name of the output file.
    }
```
