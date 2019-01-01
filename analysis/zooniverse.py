def JSONParser(data):
    """call json.loads"""
    import json
    return json.loads(data)


def load_classifications(filename, json_columns=None):
    """
    Load classifications into pandas dataframe.
    Some columns of the csv are embedded json and need special parsing.
    """
    import pandas as pd
    json_columns = json_columns or ['metadata', 'annotations', 'subject_data']
    converters = {i: JSONParser for i in json_columns}

    return pd.read_csv(filename, converters=converters)

def unpack(series):
    """
    Return the first value in a series.
    All annotations values are lists because of a few multiple tasks.
    The second multiple task always has the value of 'None of the above'
    (For this dataset!)
    """
    return [a[0] for a in series]


def parse_classifications(filename,**kwarg):
    """
    Load classifications and datamunge annotations column.
    """
    data = load_classifications(filename,**kwarg)

    # Only need the first item in the annotations list of json objects
    data['annotations'] = unpack(data['annotations'])
    return data

def extract_labels(annotations):
    annos = []
    for a in annotations:
        for box in a['value']:
            annos.append([box['x'], box['y'], box['width'],
                          box['height'], box['tool_label']
            ])
    return annos

def most_common_boxes(boxes, visualize=False, return_all_pattern=False):
    """
    Combine most common boxes of one image
    into one grid
    """
    import numpy as np
    pattern_dic = {'Sugar': 1, 'Flower': 2, 'Fish': 3, 'Gravel': 4}
    
    grid = np.zeros((2100,1400,5),dtype="int")
    for b,box in enumerate(boxes):
        # Get coordinates of single label
        coords = np.round(box[0:4],0).astype(int)
        x0 = coords[0]
        y0 = coords[1]
        # restrict x1,y1 to domain size
        x1 = min(x0 + coords[2],2100)
        y1 = min(y0 + coords[3],1400)
        pattern = pattern_dic[box[4]]
        # Add box to specific layer of grid
        grid[x0:x1,y0:y1,pattern] += 1
    if visualize: visualize_grid(grid)
    common_box = np.argmax(grid,axis=2)
    if visualize: visualize_common_box(common_box)
    if return_all_pattern: return grid
    else: return common_box