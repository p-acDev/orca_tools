import OrcFxAPI
import pandas as pd
import sys
import pickle

def extract_line_elevation(model):

    lines = [obj for obj in model.objects if type(obj) == OrcFxAPI.OrcaFlexLineObject]
    data = {}
    for line in lines:
        data[line.name] = {'curv': line.RangeGraph('Z', OrcFxAPI.Period(OrcFxAPI.pnStaticState)).X,
                           'X': line.RangeGraph('X', OrcFxAPI.Period(OrcFxAPI.pnStaticState)).Mean,
                           'Y': line.RangeGraph('Y', OrcFxAPI.Period(OrcFxAPI.pnStaticState)).Mean,
                           'Z': line.RangeGraph('Z', OrcFxAPI.Period(OrcFxAPI.pnStaticState)).Mean}
                           
    
    return data


if __name__ == "__main__":

    model = OrcFxAPI.Model(sys.argv[1])
    data = extract_line_elevation(model)
    with open(f'{sys.argv[1][:-4].pkl', 'wb') as f:
        pickle.dump(data)
