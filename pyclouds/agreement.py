"""
Agreement functions. simple agreement plus IoU

Created on 2019-01-02-14-05
Author: Stephan Rasp, raspstephan@gmail.com
"""
from .imports import *
from .helpers import *
classes = ['Sugar', 'Flower', 'Fish', 'Gravel']

import multiprocessing as mp






def get_agreement_over_subjects(subjects, annos_df, thresh=0.15, tq=None, user=None):
    agree = defaultdict(int)
    tot = defaultdict(int)
    for s in tqdm(subjects, disable=tq):
        if user is None:
            agree, tot = simple_agreement_by_class_with_overlap(s, annos_df, agree, tot, thresh)
        else:
            agree, tot = simple_agreement_by_class_and_user_with_overlap(s, annos_df, user, agree, tot, thresh)
    return agree, tot


def get_agreement_over_subjects_mp(subjects, annos_df, thresh=0.15, procs=1, user=None):
    subjects = list(subjects)
    n_sub = len(subjects)
    pool = mp.Pool(procs)
    out = [
        pool.apply_async(
            get_agreement_over_subjects,
            args=(subjects[int(i*(1/procs)*n_sub):int((i+1)*(1/procs)*n_sub)],
                  annos_df, thresh, True, user))
        for i in range(procs)
    ]
    results = [p.get() for p in out]
    agree = defaultdict(int)
    tot = defaultdict(int)
    for c in classes:
        agree[c] += sum([r[0][c] for r in results])
        tot[c] += sum([r[1][c] for r in results])
    pool.close()
    return agree, tot


def simple_agreement(subj_id, annos_df):
    """
    This simple score checks how many times two users saw the same class in an image.
    Returns the number of agreements between all combinations of two users for one subj_id
    and the total number of possible agreements.
    """
    ans = annos_df[annos_df.subject_ids == subj_id]
    users = ans.user_name.unique()

    agree = 0
    tot = 0
    for u1, u2 in combinations(users, 2):
        #         print(u1, u2)
        a1 = ans[ans.user_name == u1].dropna(subset=['tool_label'])
        a2 = ans[ans.user_name == u2].dropna(subset=['tool_label'])
        # How many classes in agreement
        agree_tmp = len(set(a1.tool_label) & set(a2.tool_label))
        agree += agree_tmp * 2
        # How many classes in total
        tot += len(set(list(a1.tool_label) + list(a2.tool_label))) + agree_tmp

    #         print(agree_tmp * 2)
    #         print(len(set(list(a1.tool_label) + list(a2.tool_label))) + agree_tmp)

    return agree, tot


def simple_agreement_by_class(subj_id, annos_df, agree=None, tot=None):
    """
    Essentially the same as the simply agreement score but stratified by class.
    """
    ans = annos_df[annos_df.subject_ids == subj_id]
    users = ans.user_name.unique()

    if agree is None: agree = defaultdict(int)
    if tot is None: tot = defaultdict(int)
    for u1, u2 in combinations(users, 2):
        for c in classes:
            a1 = ans[(ans.user_name == u1) & (ans.tool_label == c)]
            a2 = ans[(ans.user_name == u2) & (ans.tool_label == c)]
            # Option 1: both zero --> skip
            if (len(a1) == 0) & (len(a2) == 0):
                pass
            # Option 2: Both people have this class:
            elif (len(a1) > 0) and (len(a2) > 0):
                tot[c] += 2
                agree[c] += 2
            # Option 3: Only one user has this class
            else:
                tot[c] += 1

    return agree, tot


def simple_agreement_by_class_with_overlap(subj_id, annos_df, agree=None, tot=None, thresh=0.1,
                                           img_size=(2100, 1400)):
    """
    Essentially the same as the simple agreement score by class, but conditional on an IoU overlap
    of at least thresh.
    """
    ans = annos_df[annos_df.subject_ids == subj_id]
    users = ans.user_name.unique()

    if agree is None: agree = defaultdict(int)
    if tot is None: tot = defaultdict(int)
    for u1, u2 in combinations(users, 2):
        for c in classes:
            a1 = ans[(ans.user_name == u1) & (ans.tool_label == c)]
            a2 = ans[(ans.user_name == u2) & (ans.tool_label == c)]
            # Option 1: both zero --> skip
            if (len(a1) == 0) & (len(a2) == 0):
                pass
            # Option 2: Both people have this class:
            elif (len(a1) > 0) and (len(a2) > 0):
                # Now check if overlap > threshold
                annos1 = [[int(r[c]) for c in ['x', 'y', 'width', 'height']] for i, r in
                          a1.iterrows()]
                annos2 = [[int(r[c]) for c in ['x', 'y', 'width', 'height']] for i, r in
                          a2.iterrows()]
                iou = iou_one_class_from_annos(annos1, annos2, img_size, True)
                if iou > thresh:
                    tot[c] += 2
                    agree[c] += 2
                else:
                    tot[c] += 2
            # Option 3: Only one user has this class
            else:
                tot[c] += 1

    return agree, tot


def simple_agreement_by_class_and_user_with_overlap(subj_id, annos_df, user, agree=None, tot=None,
                                                    thresh=0.1, img_size=(2100, 1400)):
    ans = annos_df[annos_df.subject_ids == subj_id]
    users = ans.user_name.unique()

    if agree is None: agree = defaultdict(int)
    if tot is None: tot = defaultdict(int)

    other_users = [u for u in users if u != user]

    if (user not in users) or (len(other_users) == 0):
        return agree, tot

    u1 = user
    for u2 in other_users:
        for c in classes:
            a1 = ans[(ans.user_name == u1) & (ans.tool_label == c)]
            a2 = ans[(ans.user_name == u2) & (ans.tool_label == c)]
            # Option 1: both zero --> skip
            if (len(a1) == 0) & (len(a2) == 0):
                pass
            # Option 2: Both people have this class:
            elif (len(a1) > 0) and (len(a2) > 0):
                # Now check if overlap > threshold
                annos1 = [[int(r[c]) for c in ['x', 'y', 'width', 'height']] for i, r in
                          a1.iterrows()]
                annos2 = [[int(r[c]) for c in ['x', 'y', 'width', 'height']] for i, r in
                          a2.iterrows()]
                iou = iou_one_class_from_annos(annos1, annos2, img_size, True)

                if iou > thresh:
                    tot[c] += 1
                    agree[c] += 1
                else:
                    tot[c] += 2
            # Option 3: Only user1 has this class
            elif len(a1) > 0:
                tot[c] += 1

    return agree, tot


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
    del arr1, arr2
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
        a =[np.int(ai) for ai in a]
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






