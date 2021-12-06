# from __future__ import print_function
import os
import os.path
import numpy as np
from plyfile import PlyData
import argparse

import matplotlib.pyplot as plt

from augmentation.pointwolf import PointWOLF

def gen_modelnet_id(root):
    classes = []
    with open(os.path.join(root, 'train.txt'), 'r') as f:
        for line in f:
            classes.append(line.strip().split('/')[0])
    classes = np.unique(classes)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../misc/modelnet_id.txt'), 'w') as f:
        for i in range(len(classes)):
            f.write('{}\t{}\n'.format(classes[i], i))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', type=str, default="ModelNet40")


    args = parser.parse_args()

    fns = []

    with open(os.path.join(args.data_path, '{}.txt'.format("trainval")), 'r') as f:
        for line in f:
            fns.append(line.strip())

    cat = {}
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), './misc/modelnet_id.txt'), 'r') as f:
        for line in f:
            ls = line.strip().split()
            cat[ls[0]] = int(ls[1])

    print(cat)
    classes = list(cat.keys())

    class_counts = {key: [] for key, _ in cat.items()}

    for fn in fns:
        cls_str = fn.split('/')[0]
        cls = cat[cls_str]
        with open(os.path.join(args.data_path, fn), 'rb') as f:
            plydata = PlyData.read(f)
        pts = np.vstack([plydata['vertex']['x'], plydata['vertex']['y'], plydata['vertex']['z']]).T

        class_counts[cls_str].append(len(pts))


    max_points = {key: max(values) for key, values in cat.items()}
    number_of_examples = {key: len(values) for key, values in cat.items()}

    import pdb
    pdb.set_trace()
