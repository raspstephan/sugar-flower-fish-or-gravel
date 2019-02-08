"""
Plotting helpers

Created on 2019-01-31-15-17
Author: Stephan Rasp, raspstephan@gmail.com
"""

from .imports import *

l2c = {'Sugar': [241, 244, 66], 'Flower': [244, 65, 65], 'Fish': [65, 241, 244],
           'Gravel': [73, 244, 65]}

def plot_img_with_annos(subj_id, img_path, subj_df, annos_df=None, user=None, cols=1,
                        figsize=(18, 15), ax_obj=None):

    if type(subj_id) not in [list, np.ndarray]: subj_id = [subj_id]
    nfigs = len(subj_id)
    rows = np.ceil(nfigs / cols).astype(int)
    if ax_obj is None:
        fig, axs = plt.subplots(rows, cols, figsize=figsize)
    else: axs = ax_obj

    for s, ax in zip(subj_id, axs.flat if (nfigs > 1)  else [axs]):
        fn = str(img_path + subj_df[subj_df.subject_id == s].iloc[0]['fn'])
        img = Image.open(fn)
        ax.imshow(img)
        ax.set_xticks([]);
        ax.set_yticks([])
        if annos_df is not None:
            ans = annos_df[annos_df.subject_ids == s]
            if user is not None: ans = ans[ans.user_name == user]
            nones = []
            for i, a in ans.iterrows():
                if np.isfinite(a['x']):
                    rect = patches.Rectangle((a['x'], a['y']), a['width'], a['height'],
                                             facecolor='none',
                                             edgecolor=np.array(l2c[a['tool_label']]) / 255, lw=2)
                    ax.add_patch(rect)
                    ax.text(a['x'], a['y'], a['tool_label'] + ' - ' + a['user_name'],
                            color=(0, 1, 0), fontsize=15, va='top')
                else:
                    nones.append(a['user_name'])
            if len(nones) > 0:
                ax.text(0, -50, 'None: ' + str(nones), color='red', fontsize=15, va='top')
    if ax is None: plt.tight_layout()
