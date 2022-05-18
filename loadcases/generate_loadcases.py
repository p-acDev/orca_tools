import pandas as pd
import OrcFxAPI
import sys

def extract_model(file_path):

    model = OrcFxAPI.Model(file_path)

    return model

def extract_global_load(input_file_name, array_name):

    df = pd.read_excel(input_file_name, sheet_name=array_name)

    return df

def set_island_load(model, array_name, X, Y):

    # initialize the list in orcaflex global load to recieve the data
    model[array_name].GlobalAppliedForceX = [0]
    model[array_name].GlobalAppliedForceY = [0]


    model[array_name].GlobalAppliedForceX[0] = X
    model[array_name].GlobalAppliedForceY[0] = Y

    return model

def get_islands(model):

    islands = [obj for obj in model.objects if type(obj) == OrcFxAPI.OrcaFlex6DBuoyObject]

    return islands, model

if __name__ == "__main__":

    static_model_path_name = sys.argv[1]
    input_file = sys.argv[2]
    model = extract_model(static_model_path_name)

    islands, model = get_islands(model)

    for island in islands:
        print(island.name)
        df_load = extract_global_load(input_file, island.name)
        for i in range(len(df_load['direction'])):
            print(df_load["direction"].iloc[i])
            direction = df_load["direction"].iloc[i]
            X = df_load["X"].iloc[i]
            Y = df_load["Y"].iloc[i]
            model = set_island_load(model, island.name,  X, Y)
            model_name = static_model_path_name.replace('initialposition', f"{direction}deg")
            model.SaveData(model_name)
    
    