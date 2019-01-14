"""
Contains all common imports for data processing and analysis

Created on 2019-01-02-13-42
Author: Stephan Rasp, raspstephan@gmail.com
"""

import pandas as pd
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
import matplotlib.patches as patches
from PIL import Image
import seaborn as sns
import itertools
import pdb

subj_id2name = {60811:'BCO_DJF_Aqua',60812:'BCO_DJF_Terra',60813: 'BCO_MAM_Aqua',
                60814: 'BCO_MAM_Terra',60815:'R2_DJF_Aqua',60816:'R2_DJF_Terra',
                60817:'R3_DJF_Aqua', 60818:'R3_DJF_Terra',60819:'R3_SON_Aqua',
                60835: 'R3_SON_Terra'}