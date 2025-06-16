import pandas as pd
import geopandas as gpd
import numpy as np
from geopandas.tools import sjoin
import warnings
import sys, array

sys.path.append("path/to/pstqgis_3.3.1_2024-11-01/pst/pstalgo/python")

import pstalgo
from pstalgo import Radii, DistanceType


###Script Configuration###

props = {
    'network': '', # path/to/shapefile.shp
    'crs': 3006,
    'radius_type':'walking', #can be either straight, walking, steps, angular or axmeter
    'radius_threshold': 1000, #must match the units of the chosen radius type
    'angle_threshold':0,
    'angle_precision':1,
    'norm_normalization':True, 
    'norm_hillier':True,
    'norm_syntax':True,
    'weigh_by_length': True,
    'output_N':True,
    'output_TD':True,
    'output_MD':True,
    'output_file': "AI.shp" #choose output filename
    }


###Function Definition###

def perform_angular_integration(props):

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
    total_counts   =  array.array('I', [0]) * line_count
    total_depths   =  array.array('f', [0]) * line_count

    if weigh_by_length:
        
        total_weights = array.array('f', [0]) * line_count
        total_depth_weights = array.array('f', [0]) * line_count

        pstalgo.AngularIntegration(
                graph_handle = graph,
                radius = radius,
                weigh_by_length = True,
                angle_threshold = props['angle_threshold'],
                angle_precision = props['angle_precision'],
                out_node_counts = total_counts,
                out_total_depths = total_depths,
                out_total_weights = total_weights,
                out_total_depth_weights = total_depth_weights)

        if props['norm_normalization']:
            scores_norm = array.array('f', [0]) * line_count
            pstalgo.AngularIntegrationNormalizeLengthWeight(total_weights, total_depth_weights, line_count, scores_norm)
            roads[f'AI_norm']=pd.Series(scores_norm)
        if props['norm_syntax']:
            scores_syntax = array.array('f', [0]) * line_count
            pstalgo.AngularIntegrationSyntaxNormalizeLengthWeight(total_weights, total_depth_weights, line_count, scores_syntax)
            roads[f'AInrm_sntx']=pd.Series(scores_syntax)
        if props['norm_hillier']:
            norm_hillier = array.array('f', [0]) * line_count
            pstalgo.AngularIntegrationHillierNormalizeLengthWeight(total_weights, total_depth_weights, line_count, norm_hillier)
            roads[f'AInorm_hil']=pd.Series(norm_hillier)
	    
        if props['output_N']:
            roads[f'AI_N']=pd.Series(total_counts)
        if props['output_TD']:
            roads[f'AI_TD']=pd.Series(total_depths)
        if props['output_MD']:
            mean_depth_weights=MeanDepthGen(total_depths,total_counts)
            roads[f'AI_MD']=pd.Series(mean_depth_weights)


    else:
        pstalgo.AngularIntegration(
				graph_handle = graph,
				radius = radius,
				weigh_by_length = False,
				angle_threshold = props['angle_threshold'],
				angle_precision = props['angle_precision'],
				out_node_counts = total_counts,
				out_total_depths = total_depths,
				out_total_weights = None,
				out_total_depth_weights = None)

        if props['norm_normalization']:
            scores_norm = array.array('f', [0]) * line_count
            pstalgo.AngularIntegrationNormalize(total_counts, total_depths, line_count, scores_norm)
            roads[f'AI_norm']=pd.Series(scores_norm)
        if props['norm_syntax']:
            scores_syntax = array.array('f', [0]) * line_count
            pstalgo.AngularIntegrationSyntaxNormalize(total_counts, total_depths, line_count, scores_syntax)
            roads[f'AInrm_sntx']=pd.Series(scores_syntax)
        if props['norm_hillier']:
            norm_hillier = array.array('f', [0]) * line_count
            pstalgo.AngularIntegrationHillierNormalize(total_counts, total_depths, line_count, norm_hillier)
            roads[f'AInorm_hil']=pd.Series(norm_hillier)

        if props['output_N']:
            roads[f'AI_N']=pd.Series(total_counts)
        if props['output_TD']:
            roads[f'AI_TD']=pd.Series(total_depths)
        if props['output_MD']:
            mean_depth_weights=MeanDepthGen(total_depths,total_counts)
            roads[f'AI_MD']=pd.Series(mean_depth_weights)

    return roads.to_file("AI.shp")
    

def MeanDepthGen(TD_vector, N_vector):
	for i in range(len(TD_vector)):
		N = N_vector[i]-1  # IMPORTANT: -1 here since origin line is included in the count
		yield TD_vector[i]/N if N > 0 else 0.0
    


###Script Execution###


perform_angular_integration(props=props)






