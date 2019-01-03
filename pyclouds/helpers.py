"""
Helper functions to handle data, etc.

Created on 2019-01-02-13-05
Author: Stephan Rasp, raspstephan@gmail.com
"""
from .imports import *


def wh2xy(x, y, w, h):
    """Converts [x, y, w, h] to [x1, y1, x2, y2], i.e. bottom left and top right coords."""
    return x, y, x+w, y+h


def annos_from_df(clas_df, img_size):
    """Dictionary for every subject containing all annotations (also empty ones!)"""
    annos = defaultdict(list)
    for i, r in clas_df.iterrows():
        if len(r['annotations']['value']) > 0 :
            for a in r['annotations']['value']:
                x = np.max([0., a['x']]); y = np.max([0., a['y']])
                w = np.min([img_size[0] - a['x'], a['width']])
                h = np.min([img_size[1] - a['y'], a['height']])
                annos[r['subject_ids']].append([
                    r['user_name'],
                    [x, y, w, h],
                    a['tool_label']
                ])
        else:   # No annotation
            annos[r['subject_ids']].append([
                r['user_name'],
                [None, None, None, None],
                None
            ])
    return annos


def plot_with_annos(subject_id, annos, users=None):
    fig, ax = plt.subplots(figsize=(15, 10))
    img = Image.open(subj2fn[subject_id])
    ax.imshow(img)
    nones = []
    for a in annos[s]:
        if a[2] is not None:
            if users is not None and a[0] in users:
                coords = a[1]
                rect = patches.Rectangle((coords[0],coords[1]), coords[2], coords[3], facecolor='none', edgecolor='r')
                ax.add_patch(rect)
                ax.text(coords[0],coords[1], a[2] + ' - ' + a[0], color='red', fontsize=15, va='top')
        else:
            nones.append(a[0])
    if len(nones) > 0:
        ax.text(0, -50, 'None: ' + str(nones), color='red', fontsize=15, va='top')