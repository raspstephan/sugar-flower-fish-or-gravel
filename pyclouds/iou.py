"""
Functions to comute the multi-label, multi-class Intersect over Union score.

Created on 2019-01-02-14-05
Author: Stephan Rasp, raspstephan@gmail.com
"""
from .imports import *
from .helpers import *
from numba import jit


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
            u = compute_area_sum_from_annos(np.array(ac1 + ac2).astype(np.int32), img_size)
        else:
            #i, u = iou_one_class(ac1, ac2)
            # Also need to convert to integers
            i, u = iou_one_class_from_annos(
                np.array(ac1).astype(np.int32), np.array(ac2).astype(np.int32), img_size)
        i_tot += i; u_tot += u
    return i_tot / u_tot


def iou_one_class_from_annos(annos1, annos2, img_size, return_iou=False):
    """
    Returns the IoU from lists of [x, y, w, h] annotations.
    Image size must be given because arrays are created internally.
    If return_iou is True, the actual IoU score is computed,
    otherwise i, u will be returned.
    """
    arr1 = fill_array_with_boxes(annos1, img_size)
    arr2 = fill_array_with_boxes(annos2, img_size)
    i = intersect_from_arrs(arr1, arr2)
    u = union_from_arrs(arr1, arr2)
    if return_iou:
        return i/u
    else:
        return i, u


def fill_array_with_boxes(annos, img_size):
    """
    Creates an array where all areas of the array that are in one of the boxes are True,
    otherwise False
    """
    arr = np.zeros(img_size, dtype=bool)
    for a in annos:
        arr[a[0]:a[0]+a[2], a[1]:a[1]+a[3]] = True
    return arr


def intersect_from_arrs(arr1, arr2):
    """Applies bitwise_and followed by a sum. Note that the sum operation is expensive."""
    return np.sum(np.bitwise_and(arr1, arr2))


def union_from_arrs(arr1, arr2):
    """Applies bitwise_or followed by a sum. Note that the sum operation is expensive."""
    return np.sum(np.bitwise_or(arr1, arr2))


def compute_area_sum_from_annos(annos, img_size):
    """Compute the area from annotations"""
    return np.sum(fill_array_with_boxes(annos, img_size))






