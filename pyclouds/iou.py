"""
Functions to comute the multi-label, multi-class Intersect over Union score.

Created on 2019-01-02-14-05
Author: Stephan Rasp, raspstephan@gmail.com
"""
from .imports import *


def get_comp_data(subject_id, user1, user2, annos):
    subj_annos = annos[subject_id]
    users = list(set([a[0] for a in subj_annos]))
    if user1 in users and user2 in users:
        annos1 = [a[1:] for a in subj_annos if a[0] == user1]
        annos2 = [a[1:] for a in subj_annos if a[0] == user2]
        if annos1[0][1] is None and annos2[0][1] is None:
            iou = 1.
        elif annos1[0][1] is None:
            iou = 0.
        elif annos2[0][1] is None:
            iou = 0.
        else:
            iou = iou_multi_class(annos1, annos2)
        return iou
    else:
        return None


def iou_multi_class(annos1, annos2, classes, img_size):
    """For two users"""
    i_tot = 0; u_tot = 0
    for c in classes:
        ac1 = [a[0] for a in annos1 if a[1] == c]
        ac2 = [a[0] for a in annos2 if a[1] == c]
        if len(ac1) == 0 and len(ac2) == 0:   # None of the users has this class
            i = 0; u = 0
        elif len(ac1) == 0 or len(ac2) == 0:
            i = 0
            u = compute_area_sum(ac1 + ac2)
        else:
            #i, u = iou_one_class(ac1, ac2)
            # Also need to convert to integers
            i, u = iou_one_class_from_annos(
                np.array(ac1).astype(np.int32), np.array(ac2).astype(np.int32), img_size)
        i_tot += i; u_tot += u
    return i_tot / u_tot


def iou_one_class(annos1, annos2):
    """annos1 and annos2 are lists with the coordinates of each annotation"""
    # All permutations
    i = 0
    for a1 in annos1:
        for a2 in annos2:
            i += compute_intersect(a1, a2)
    # Need to compute the overlap between the boxes of 1 and 2
    i1 = 0
    i2 = 0
    for b1, b2 in itertools.combinations(annos1, 2):
        i1 += compute_intersect(b1, b2)
    for b1, b2 in itertools.combinations(annos2, 2):
        i2 += compute_intersect(b1, b2)
    u = compute_area_sum(annos1 + annos2) - i  # - i1 -i2

    iou = i / u  # (i - i1 - i2) / u
    return i, u


def compute_area_sum(annos):
    areas = [a[2] * a[3] for a in annos]
    return np.sum(areas)


def compute_intersect(a1, a2):
    """
    https://www.pyimagesearch.com/2016/11/07/intersection-over-union-iou-for-object-detection/
    Computes the intersect between two boxes.
    """
    x1a, y1a, x2a, y2a = wh2xy(*a1)
    x1b, y1b, x2b, y2b = wh2xy(*a2)
    xA = max(x1a, x1b)
    yA = max(y1a, y1b)
    xB = min(x2a, x2b)
    yB = min(y2a, y2b)
    i = max(0, xB - xA) * max(0, yB - yA) # max(0, xB - xA + 1) * max(0, yB - yA + 1)
    return i


def wh2xy(x, y, w, h):
    return x, y, x+w, y+h


### NEW FUNCTIONS, NEEDS CLEANUP!

def fill_array_with_boxes(annos, img_size):
    """
    Creates an array where all areas of the array that are in one of the boxes are True, otherwise False
    """
    arr = np.zeros(img_size, dtype=bool)
    for a in annos:
        arr[a[0]:a[0]+a[2], a[1]:a[1]+a[3]] = True
    return arr

def intersect_from_arrs(arr1, arr2):
    return np.sum(np.bitwise_and(arr1, arr2))
def union_from_arrs(arr1, arr2):
    return np.sum(np.bitwise_or(arr1, arr2))
def iou_one_class_from_arrs(arr1, arr2):
    return intersect_from_arrs(arr1, arr2) / union_from_arrs(arr1, arr2)
def iou_one_class_from_annos(annos1, annos2, img_size):
    i = intersect_from_arrs(
        fill_array_with_boxes(annos1, img_size), fill_array_with_boxes(annos2, img_size))
    u = union_from_arrs(
        fill_array_with_boxes(annos1, img_size), fill_array_with_boxes(annos2, img_size))
    return i, u
    #return iou_one_class_from_arrs(
    #    fill_array_with_boxes(annos1, img_size), fill_array_with_boxes(annos2, img_size))

