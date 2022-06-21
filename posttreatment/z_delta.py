import OrcFxAPI
import pickle
import numpy as np
import tqdm
import pandas as pd
from collections import OrderedDict
from itertools import product
import sys
from extract_line_elevation import extract_line_elevation

def nodes_distances(data, line1_name, line2_name):

 
    distances = OrderedDict()
    
     # find the min distance between lines
    for i in range(len(data[line1_name]['curv'])):
        # we want to exclude minimal distance xy when we are at shared anchoring. That's why we start at 1
        distances_ij = np.zeros((len(data[line2_name]['curv'])))
        for j in range(len(data[line2_name]['curv'])):
            d = ((data[line1_name]['X'][i] - data[line2_name]['X'][j])**2 + (data[line1_name]['Y'][i] - data[line2_name]['Y'][j])**2 )**0.5
            distances_ij[j] = d
        distances[f'{line1_name}_node_{i}'] = distances_ij

    df_node_distance = pd.DataFrame(distances)
    df_node_distance.index = [f'{line2_name}_node_{j}' for j in range(len(data[line2_name]['curv']))]
    
    return df_node_distance

def get_location_min_xy(data, line1_name, line2_name):

    df_node_distance = nodes_distances(data, line1_name, line2_name)
    location = df_node_distance[df_node_distance == df_node_distance.min().min()].dropna(how='all').dropna(axis=1)
    
    return location

def potential_crossing(data, line_name_check, side_name):
    '''Find the min clearance for a single line Vs all lines from a side'''
    
    clearance = OrderedDict()
    
    # line names of line we want to check the clash with line_name
    crossing_line_names = [line_name for line_name in data.keys() if side_name in line_name]
    for clashing_line in crossing_line_names:
        location = get_location_min_xy(data, line_name_check, clashing_line)
        if location.values[0][0] < 1:
            clearance[clashing_line] = {'xy_distance': location.values[0][0],
                                        'line_name_check_node': location.columns[0].split('_')[-1],
                                        'crossing_line_check_node': location.index[0].split('_')[-1]
                                        }

    df = pd.DataFrame(clearance)
    
    return df.T

def build_clashing_matrices(data, side1, side2):

    clashing_data = OrderedDict()
    
    for line_name_check in tqdm.tqdm([line_name for line_name in data.keys() if side1 in line_name]):
        
        clearance = potential_crossing(data, line_name_check, side2)
        if not clearance.empty:
            # add the Z in clearance df
            clearance['z_line_check'] = clearance['line_name_check_node'].apply(lambda elem:data[line_name_check]['Z'][int(elem)])
            crossing_line_names = clearance.index
            z_crossing_line = [data[crossing_line]['Z'][int(clearance['crossing_line_check_node'].loc[crossing_line])] for crossing_line in clearance.index]
            clearance['z_crossing_line'] = z_crossing_line
            clearance['delta_z'] = clearance['z_line_check'] - clearance['z_crossing_line']
            clashing_data[line_name_check] = clearance
        
    return clashing_data
    

def build_z_delta(data, side1, side2, output_name=''):

    print(f'{side1} Vs {side2}')
    
    try:
        clashing_data = build_clashing_matrices(data, side1, side2)
    except KeyError:
        clashing_data = None
        

    if clashing_data:    

        dfs = []

        for line_name_check in clashing_data.keys():
            dfs.append(clashing_data[line_name_check]['delta_z'])
        

        df = pd.concat(dfs, axis=1)
        df.columns = clashing_data.keys()

        # export the results
        # export clashing data
        with pd.ExcelWriter(f'{output_name}_{side1}_Vs_{side2}_clashing_report.xlsx') as excel_writer:
            for line_name_check in clashing_data.keys(): 
                df_clashing = clashing_data[line_name_check]
                df_clashing.to_excel(excel_writer, sheet_name = line_name_check)

        # export the delta_z matrix
        df.to_excel(f'{output_name}_{side1}_Vs_{side2}_delta_z.xlsx')
    
        return clashing_data, df

    else:

        with open(f'{output_name}_{side1}_Vs_{side2}_NO_CROSSING', 'wb') as f:
            pass
        print('NO CLASHING')
        return {}, pd.DataFrame()



if __name__ == "__main__":

    data = extract_line_elevation(OrcFxAPI.Model(sys.argv[1]))
        

    sides1 = ['FRONT', 'BACK']
    sides2 = ['LEFT', 'RIGHT']
    for side1, side2 in product(sides1, sides2):
        clashing_data, df = build_z_delta(data, side1, side2, sys.argv[1][:-4])



