import OrcFxAPI
import pandas as pd
import numpy as np
import os
import re
import sys

def extract_lines(model):

    lines = [obj for obj in model.objects if type(obj) == OrcFxAPI.OrcaFlexLineObject]
    
    return lines

def extract_island(model):

    island = [obj for obj in model.objects if ((type(obj) == OrcFxAPI.OrcaFlex6DBuoyObject) and ("ARRAY") in obj.name)][0]

    return island

def format_line_result(model, line):

    res = {}
    res["Azimuth (End A)"] = line.TimeHistory("Azimuth", OrcFxAPI.Period(OrcFxAPI.pnStaticState), OrcFxAPI.oeEndA)[0]
    res["Declination (End A)"] = line.TimeHistory("Declination", OrcFxAPI.Period(OrcFxAPI.pnStaticState), OrcFxAPI.oeEndA)[0]
    res["Effective Tension (End A)"] = line.TimeHistory("Effective Tension", OrcFxAPI.Period(OrcFxAPI.pnStaticState), OrcFxAPI.oeEndA)[0]
    res["Azimuth (End B)"] = line.TimeHistory("Azimuth", OrcFxAPI.Period(OrcFxAPI.pnStaticState), OrcFxAPI.oeEndB)[0]
    res["Declination (End B)"] = line.TimeHistory("Declination", OrcFxAPI.Period(OrcFxAPI.pnStaticState), OrcFxAPI.oeEndB)[0]
    res["Effective Tension (End B)"] = line.TimeHistory("Effective Tension", OrcFxAPI.Period(OrcFxAPI.pnStaticState), OrcFxAPI.oeEndB)[0]

    return pd.DataFrame(res, index=[line.name])

def format_island_result(island, model_name):

    res = {}
    # axis for post treat is iverted with regard to Orcaflex
    res['X'] = island.TimeHistory("Y", OrcFxAPI.Period(OrcFxAPI.pnStaticState))[0]
    res['Y'] = island.TimeHistory("X", OrcFxAPI.Period(OrcFxAPI.pnStaticState))[0]
    res['Rot'] = island.TimeHistory("Rotation 3", OrcFxAPI.Period(OrcFxAPI.pnStaticState))[0]

    df = pd.DataFrame(res, index=[1]).T
    df.columns = [model_name.split("_")[-1].split(".")[0].replace('deg', '°')]

    return df

def get_model_direction(all_files, water_level):
    
    reg = rf'{water_level}_[0-9]+deg'

    directions = re.findall(reg, all_files)
    
    return {elem: int(elem.split("_")[1].split('deg')[0]) for elem in directions}

def get_filename_ordered(directions, folder, water_level):

    df = pd.DataFrame(directions, index=[1]).T.sort_values(by=1)

    filenames = [[elem for elem in os.listdir(folder) if (f'{water_level}_initialposition' in elem)][0]]

    for elem in df.index:
        for filename in os.listdir(folder):
            if elem in filename:
                filenames.append(filename)

    return df, filenames

def create_output_lines(folder, water_level):
    dfs_lines = []
    dfs_islands = []

    all_files_string = " ".join([elem for elem in os.listdir(folder) if elem.endswith('.sim')])

    # get the water level files in order
    directions = get_model_direction(all_files_string, water_level)
    direction_ordered, filenames = get_filename_ordered(directions, folder, water_level)

    for filename in filenames:
        print(filename)
        model = OrcFxAPI.Model(os.path.join(folder, filename))
        
        lines = extract_lines(model)
        island = extract_island(model)

        df_output_island = format_island_result(island, filename)
        df_output_lines = pd.concat([format_line_result(model, line) for line in lines])
        
        dfs_lines.append(df_output_lines)
        dfs_islands.append(df_output_island)

    df_results_lines = pd.concat(dfs_lines, axis=1)
    df_results_lines.columns = pd.MultiIndex.from_product([[elem.split("_")[-1].split(".")[0].replace("deg", "°") for elem in filenames], df_output_lines.columns], names=['model', 'var'])

    return df_results_lines, dfs_islands, model


if __name__ == "__main__":
    
    folder = sys.argv[1]
    output_file_path_name = sys.argv[2]
    water_levels = sys.argv[3:]

    with pd.ExcelWriter(output_file_path_name, engine='openpyxl') as excel_writer:
        for water_level in water_levels:
            print(water_level)
            df_results_lines, dfs_islands, model = create_output_lines(folder, water_level)
            df_results_lines.to_excel(excel_writer, startcol=1,  sheet_name=water_level, startrow=8)
            # remove the blank lines pandas adds when it writes multi index in excel
            excel_writer.sheets[water_level].delete_rows(11)
            for i, df_island in enumerate(dfs_islands):
                if df_island.columns[0] == 'initialposition':
                    df_island.to_excel(excel_writer, startcol=1, startrow=4, sheet_name=water_level)
                else:
                    df_island.to_excel(excel_writer, index=False, sheet_name=water_level, startrow=4, startcol=8 + (i-1)*6)
