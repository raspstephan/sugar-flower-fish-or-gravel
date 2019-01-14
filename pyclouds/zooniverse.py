from .imports import *

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


def split_classification_df(df_or_fn, workflow_name=None, workflow_version=None, date_range=None,
                            drop_nli=False, subj_df_or_fn=None):
    """
    Input: either raw classification dataframe that comes out of parse_classifications()
    or string of classification csv file.
    Takes as input the raw classification dataframe that comes out of parse_classifications().
    Adds a datetime column. If not None, returns only rows with workflow_name, workflow_version.
    Optionally, returns only labels in a certain date range. Dates must be in string format 'yyyy-mm-dd'.
    Optionally, drops all labels of users that were not-logged-in (nli).
    """
    if type(df_or_fn) is str:
        df = parse_classifications(
            df_or_fn, json_columns=['metadata', 'annotations', 'subject_data'])
    elif type(df_or_fn) is pd.DataFrame:
        df = df_or_fn.copy()
    else:
        raise TypeError('First argument must be csv string or DataFrame.')

    # Load subject file
    if subj_df_or_fn is not None:
        if type(subj_df_or_fn) is str:
            s_df = load_classifications(subj_df_or_fn)
        elif type(subj_df_or_fn) is pd.DataFrame:
            s_df = subj_df_or_fn.copy()
        else:
            raise TypeError('subj_df_or_str argument must be csv string or DataFrame.')
        add_subject_set_id_to_clas_df(df, s_df)

    df['datetime'] = pd.to_datetime(df['created_at'])
    if workflow_name is not None:
        df = df[df.workflow_name == workflow_name]
    if workflow_version is not None:
        df = df[df.workflow_version == workflow_version]
    if date_range is not None:
        df = df[(df.datetime.dt.date > np.datetime64(date_range[0])) &
                (df.datetime.dt.date < np.datetime64(date_range[1]))]
    if drop_nli:
        df = df[df.user_name.apply(lambda u: 'not-logged-in' not in u)]
    return df


def convert_clas_to_annos_df(clas_df):
    """
    Converts a classification pd.DataFrame parsed from the raw Zooniverse file to a pd.DataFrame
    that has one row per bounding box.
    Additionally, extracts coordinate and metadata information
    """
    # We need to figure out first how many items we have in order to allocate the new DataFrame
    count = 0
    for i, row in clas_df.iterrows():
        for anno in row.annotations['value']:
            count += 1
    # Allocate new dataframe
    annos_df = pd.DataFrame(
        columns=list(clas_df.columns) + ['x', 'y', 'width', 'height', 'tool_label', 'started_at', 'finished_at'],
        index=np.arange(count)
    )
    # go through each annotation
    j = 0
    for i, row in clas_df.iterrows():
        for anno in row.annotations['value']:
            for c in clas_df.columns:
                annos_df.iloc[j][c] = row[c]
            for coord in ['x', 'y', 'width', 'height', 'tool_label']:
                annos_df.iloc[j][coord] = anno[coord]
            for meta in ['started_at', 'finished_at']:
                annos_df.iloc[j][meta] = row.metadata[meta]
            j += 1
    # Convert start and finish times to datetime
    for meta in ['started_at', 'finished_at']:
        annos_df[meta] = pd.to_datetime(annos_df[meta])
    return annos_df


def add_subject_set_id_to_clas_df(clas_df, subj_df):
    s = subj_df.set_index('subject_id')
    s = s[s.subject_set_id.apply(lambda s: s in subj_id2name.keys())]
    clas_df['subject_set_id'] = clas_df.subject_ids.apply(
        lambda i: s.loc[i].subject_set_id if i in list(s.index) else np.nan)
    clas_df.dropna(subset=['subject_set_id'], inplace=True)
    clas_df['subject_set'] = clas_df.subject_set_id.apply(lambda s: subj_id2name[s])
    return clas_df



def convert_pixelCoords2latlonCoords(coords,regions):
    """
    Converts label coordinates which are originally given
    in units of pixels into geographical coordinates.
    
    Parameters
    -----
    coords : sequence of tuples [(lon0,lat0,lon1,lat1),(...),...]
        List of tuples of length 4 consisting the corner
        coordinates of a label (NOT x,y,w,h)
    regions : sequence of integers
        List of length `coords` to identify the region and its
        base coordinates
    
    Returns
    -------
    coords_latlon : array
        Input coordinates as geographical coordinates in degree N
        and degree E
    
    Example
    -------
    >>> convert_pixelCoords2latlonCoords([(20,200,400,100)],[1])
    array([[-60.79990472],
           [ 12.00142959],
           [-56.99809433],
           [ 11.0007148 ]])
    >>> convert_pixelCoords2latlonCoords([(20,200,100,400)],[1])
    array([[-60.79990472],
           [ 12.00142959],
           [-59.99952358],
           [ 14.00285919]])
    """
    import numpy as np
    region_coords = {0: [(-61,10),(-40,24)], 1:[(-61,10),(-40,24)],
                     2:[(159,8),(180,22)],3:[(-135,-15),(-114,-1)],
                     4:[(-135,-15),(-114,-1)]
                    }
    coords_latlon = np.empty((4,len(coords)))
    
    for c,(coord,region) in enumerate(zip(coords,regions)):
        region_coord_latlon = region_coords[region]
        lons=np.linspace(region_coord_latlon[0][0],region_coord_latlon[1][0],2100)#[::-1]
        lats=np.linspace(region_coord_latlon[0][1],region_coord_latlon[1][1],1400)
        
        coords_latlon[:,c] = [lons[coord[0]],lats[coord[1]],lons[coord[2]],lats[coord[3]]]
    return coords_latlon


def convert_latlonCoord2pixelCoord(coords_geo,regions):
    """
    Converts geographical coordinates of a label to coordinates
    given as pixels from the lower left border of an image.
    
    Parameters
    -----
    coords_geo : sequence of tuples [(lon0,lat0),(...),...]
        List of tuples of length 2 consisting of a
        coordinate given in degree N and degree E.
        The `coords` need to be within the region, otherwise
        an error is raised
    regions : sequence of integers
        List of length `coords` to identify the region and its
        base coordinates
    
    Returns
    -------
    coords_pixel : array
        Input coordinates as pixel coordinates relative to
        the lower left corner of the image
    
    Raises
    ------
    AssertionError in case coords_geo is outside of region.
    
    Example
    -------
    >>> convert_latlonCoord2pixelCoord([(-59.4287,13.16272)],[0])
    array([[157],
           [316]])
    """
    import numpy as np
    region_coords = {0: [(-61,10),(-40,24)], 1:[(-61,10),(-40,24)],
                     2:[(159,8),(180,22)],3:[(-135,-15),(-114,-1)],
                     4:[(-135,-15),(-114,-1)]
                    }
    coords_pixel = np.empty((2,len(coords_geo)),dtype='int')
    
    for c,(coord,region) in enumerate(zip(coords_geo,regions)):
        region_coord_latlon = region_coords[region]
        lons=np.linspace(region_coord_latlon[0][0],region_coord_latlon[1][0],2100)#[::-1]
        lats=np.linspace(region_coord_latlon[0][1],region_coord_latlon[1][1],1400)
        
        # Check if coords are realy within region
        diff_coords_lon = np.abs(lons-coord[0])
        diff_coords_lat = np.abs(lats-coord[1])
        assert(min(diff_coords_lon) < 1),'longitude coordinate outside region'
        assert(min(diff_coords_lat) < 1),'latitude coordinate outside region'
        
        coords_pixel[:,c] = [np.argmin(diff_coords_lon),np.argmin(diff_coords_lat)]
    return coords_pixel
