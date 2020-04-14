"""
Plotting helpers

Created on 2019-01-31-15-17
Author: Stephan Rasp, raspstephan@gmail.com
"""

from .imports import *
import matplotlib.patheffects as PathEffects

lss = {
    'User 1': '-',
    'User 2': ':',
    'User 3': '--',
    'User 4': '-.',
}

def plot_img_with_annos(subj_id, img_path, annos_df, user=None, cols=1,
                        figsize=(18, 15), ax_obj=None, show_boxes=True, show_labels=True,
                        show_names=True, l2c=l2c, user_ls=False):

    if type(subj_id) not in [list, np.ndarray]: subj_id = [subj_id]
    nfigs = len(subj_id)
    rows = np.ceil(nfigs / cols).astype(int)
    if ax_obj is None:
        fig, axs = plt.subplots(rows, cols, figsize=figsize)
    else: axs = ax_obj

    for s, ax in zip(subj_id, axs.flat if (nfigs > 1)  else [axs]):
        fn = str(img_path + annos_df[annos_df.subject_ids == s].iloc[0]['fn'])
        img = Image.open(fn)
        ax.imshow(img)
        ax.set_xticks([])
        ax.set_yticks([])
        if show_boxes:
            ans = annos_df[annos_df.subject_ids == s]
            if user is not None: ans = ans[ans.user_name.apply(lambda x: user in x)]
            nones = []
            for i, a in ans.iterrows():
                if np.isfinite(a['x']):
                    rect = patches.Rectangle((a['x'], a['y']), a['width'], a['height'],
                                             facecolor='none',
                                             edgecolor=l2c[a['tool_label']], lw=3,
                                             zorder=0.1,
                                             ls=lss[a['user_name']] if user_ls else '-')
                    ax.add_patch(rect)
                    if show_labels:
                        s = a['tool_label']
                        if show_names: s += ' - ' + a['user_name']
                        txt = ax.text(a['x'], a['y'], s, color='white', fontsize=15, va='top', zorder=0.2)
                        txt.set_path_effects([PathEffects.withStroke(linewidth=5, foreground='k')])
                else:
                    nones.append(a['user_name'])

            t  = f'Total: {len(ans.user_name.unique())} {"user" if len(ans.user_name.unique()) == 1 else "users"}'
            if len(nones) > 0:
                s = ', '.join(nones) if show_names and show_labels else f"{str(len(nones))}{' user' if len(nones) else ' users'}"
                t += '; No label: ' + s
            if len(nones) > 0 or user_ls:
                txt = ax.text(10, 10, t, color='w', fontsize=15, va='top')
                txt.set_path_effects([PathEffects.withStroke(linewidth=5, foreground='k')])

    if ax_obj is None: plt.tight_layout()
