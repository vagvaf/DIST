import pandas as pd
import geopandas as gpd
import numpy as np
import warnings
import sys, array

sys.path.append("path/to/pstqgis_3.3.1_2024-11-01/pst/pstalgo/python")

import pstalgo
from pstalgo import Radii, DistanceType

props = {
    'network': '', # path/to/shapefile.shp
    'crs': 3006,
    'radius_type':'walking',
    'radius_threshold': 2000,
    'norms_none':True,
    'norm_normalization':True,
    'norm_standard':True,
    'norm_syntax':True,
    'weigh_by_length': True,
    'output_file': "AB.shp" #choose output filename
    }

def perform_angular_betwenness(road_network, props):

    road_network = props['network']
    crs = props['crs']
    radius_type =  props['radius_type']
    radius_threshold = props['radius_threshold']
    weigh_by_length = props['weigh_by_length']


    radius_args = {radius_type:radius_threshold}
    radius = Radii(**radius_args)

    roads = gpd.read_file(road_network)
    roads = roads.to_crs(crs)


    road_coords = roads.get_coordinates()
    line_coords = []
    for index, row in road_coords.iterrows():
        line_coords.append(row['x'])
        line_coords.append(row['y'])

    line_coords = array.array('d', line_coords)
    line_count = int(len(line_coords) / 4)


    
    graph = pstalgo.CreateSegmentGraph(line_coords, None, None)

    # Allocate output arrays
    scores         =  array.array('f', [0]) * line_count
    scores_norm    =  array.array('f', [0]) * line_count if props['norm_normalization'] else None
    scores_std     =  array.array('f', [0]) * line_count if props['norm_standard'] else None
    scores_syntax  =  array.array('f', [0]) * line_count if props['norm_syntax'] else None
    total_counts   =  array.array('I', [0]) * line_count
    total_depths   =  array.array('f', [0]) * line_count
    total_depth_weights =  array.array('f', [0]) * line_count if props['weigh_by_length'] else None


    pstalgo.FastSegmentBetweenness(
				graph_handle = graph,
				distance_type = pstalgo.DistanceType.ANGULAR,
				weigh_by_length = weigh_by_length,
				radius = radius,
				out_betweenness = scores,
				out_node_count = total_counts,
				out_total_depth = total_depths)

    mean_depth_weights=MeanDepthGen(total_depths,total_counts)

    roads[f'AB1']=pd.Series(scores).astype(int)


    # Normalization
    if scores_norm:
        pstalgo.AngularChoiceNormalize(scores, total_counts, len(scores), scores_norm)
        roads[f'AB_norm']=pd.Series(scores_norm)
        
    # Standard normalization
    if scores_std:
        pstalgo.StandardNormalize(scores, len(scores), scores_std)
        roads[f'ABnorm_std']=pd.Series(scores_std)
	
    # Syntax normalization
    if scores_syntax:
        pstalgo.AngularChoiceSyntaxNormalize(scores, total_depth_weights, len(scores), scores_syntax)
        roads[f'ABnrm_sntx']=pd.Series(scores_syntax)

    roads[f'AB_N']=pd.Series(total_counts)
    roads[f'AB_TD']=pd.Series(total_depths)
    roads[f'AB_MD']=pd.Series(mean_depth_weights)

    


    return roads.to_file(props['output_file'])

def MeanDepthGen(TD_vector, N_vector):
	for i in range(len(TD_vector)):
		N = N_vector[i]-1  # IMPORTANT: -1 here since origin line is included in the count
		yield TD_vector[i]/N if N > 0 else 0.0
    


###################SCRIPT EXECUTION####################################


perform_angular_betwenness(props=props)






