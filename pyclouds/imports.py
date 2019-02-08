"""
Contains all common imports for data processing and analysis

Created on 2019-01-02-13-42
Author: Stephan Rasp, raspstephan@gmail.com
"""

import pandas as pd
import xarray as xr
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from collections import defaultdict, OrderedDict
import matplotlib.patches as patches
from PIL import Image
import seaborn as sns
from itertools import combinations
import pdb
from tqdm import tqdm_notebook as tqdm
import warnings
warnings.filterwarnings("ignore")

subj_id2name = {60811:'Region1_DJF_Aqua',60812:'Region1_DJF_Terra',60813: 'Region1_MAM_Aqua',
                60814: 'Region1_MAM_Terra',60815:'Region2_DJF_Aqua',60816:'Region2_DJF_Terra',
                60817:'Region3_DJF_Aqua', 60818:'Region3_DJF_Terra',60819:'Region3_SON_Aqua',
                60835: 'Region3_SON_Terra'}

classes = ['Sugar', 'Flower', 'Fish', 'Gravel']

l2c = {'Sugar': [241, 244, 66], 'Flower': [244, 65, 65], 'Fish': [65, 241, 244], 'Gravel': [73, 244, 65]}

