#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
=========================================================
Vector Quantization Example
=========================================================

Face, a 1024 x 768 size image of a raccoon face,
is used here to illustrate how `k`-means is
used for vector quantization.

"""
print(__doc__)


# Code source: Gaël Varoquaux
# Modified for documentation by Jaques Grobler
# License: BSD 3 clause

import os
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt

from sklearn import cluster
from mk_tk_slice_viewer import viewer3d

fname = 'ciexxx_graxxxx_SE00008_i_cut.nii'
fdir  = '/home/marek/Dropbox/To_synchro/work/all_data'
#fdir  = 'F:\marek\Dropbox\To_synchro\work\\all_data'
fpath = os.path.join(fdir, fname)

face0 = nib.load(fpath).get_data()
face = face0[180:280,180:310,:]

n_clusters = 4
np.random.seed(0)

X = face.reshape((-1, 1))  # We need an (n_sample, n_feature) array
k_means = cluster.KMeans(n_clusters=n_clusters, n_init=4)
k_means.fit(X)
values = k_means.cluster_centers_.squeeze()
labels = k_means.labels_

# create an array from labels and values
face_compressed = np.choose(labels, values)
face_compressed.shape = face.shape

vmin = face.min()
vmax = face.max()

if 0:
    # original face
    plt.figure(1, figsize=(3, 2.2))
    plt.imshow(face, cmap=plt.cm.gray, vmin=vmin, vmax=vmax)

    # compressed face
    plt.figure(2, figsize=(3, 2.2))
    plt.imshow(face_compressed, cmap=plt.cm.gray, vmin=vmin, vmax=vmax)

    # equal bins face
    regular_values = np.linspace(0, vmax, n_clusters + 1)
    regular_labels = np.searchsorted(regular_values, face) - 1
    regular_values = .5 * (regular_values[1:] + regular_values[:-1])  # mean
    regular_face = np.choose(regular_labels.ravel(), regular_values, mode="clip")
    regular_face.shape = face.shape
    plt.figure(3, figsize=(3, 2.2))
    plt.imshow(regular_face, cmap=plt.cm.gray, vmin=vmin, vmax=vmax)

    # histogram
    plt.figure(4, figsize=(3, 2.2))
    plt.clf()
    plt.axes([.01, .01, .98, .98])
    plt.hist(X, bins=256, color='.5', edgecolor='.5')
    plt.yticks(())
    plt.xticks(regular_values)
    values = np.sort(values)
    for center_1, center_2 in zip(values[:-1], values[1:]):
        plt.axvline(.5 * (center_1 + center_2), color='b')

    for center_1, center_2 in zip(regular_values[:-1], regular_values[1:]):
        plt.axvline(.5 * (center_1 + center_2), color='r', linestyle='--')

    plt.show()

viewer3d(face_compressed)