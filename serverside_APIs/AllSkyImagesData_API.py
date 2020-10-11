# import matplotlib
# matplotlib.use('ps')
#
# from matplotlib import pyplot as plt
import numpy as np
import io, cv2, pickle, uuid, threading, os, sys
# import pandas as pd
from libs import *
from .batches_generator import batches_generator
# from queue import Queue


a = np.random.randn()



class GeneratedExample:
    def __init__(self, img_full_fname, img_cached_fname):
        self.cached_file_name = img_cached_fname
        self.img_full_name = img_full_fname
        self.img_basename = os.path.basename(img_full_fname)



class AllSkyImagesDataAPI(object):
    def __init__(self, src_data_path = './src_data/', shuffle = True):
        self.abs_src_data_path = os.path.join(os.getcwd(), src_data_path)
        self.shuffle = shuffle

        self.fnames = ServiceDefs.find_files(self.abs_src_data_path, "*.jpg")
        self.basenames2filenames = dict([(os.path.basename(fname), fname) for fname in self.fnames])
        self.indices = np.arange(0, len(self.fnames), 1)
        basenames_indices = [(os.path.basename(fname), idx) for idx,fname in zip(self.indices, self.fnames)]
        self.basenames2indices = dict(basenames_indices)
        self.indices2basenames = dict([(t[1], t[0]) for t in basenames_indices])
        if shuffle:
            self.shuffle_files()

        self.indices_batch_generator = batches_generator(self.indices, batch_size=1, loop=False)

        self.currentImageBinary = None

        self.generated_examples_history = []


    def shuffle_files(self):
        self.indices = np.random.permutation(self.indices)

    def reset_files_generator(self, reshuffle = False):
        if reshuffle:
            self.shuffle_files()
        self.indices_batch_generator = batches_generator(self.indices, batch_size=1, loop=False)

    def read_next_image(self, tmp_image_fname):
        img_fname_idx = next(self.indices_batch_generator)[0]
        img_fname = self.fnames[img_fname_idx]
        img_basename = os.path.basename(img_fname)

        image = cv2.imread(img_fname)

        #
        # probably, some preprocessing here
        #

        self.currentImageBinary = image

        cv2.imwrite(tmp_image_fname, self.currentImageBinary)
        example = GeneratedExample(img_fname, tmp_image_fname)
        self.generated_examples_history.append(example)
        return example

    def read_sprcific_image(self, img_basename, tmp_image_fname):
        img_fname_idx = self.basenames2indices[img_basename]
        img_fname = self.fnames[img_fname_idx]
        assert os.path.basename(img_fname) == img_basename
        # img_basename = os.path.basename(img_fname)

        image = cv2.imread(img_fname)

        #
        # probably, some preprocessing here
        #

        self.currentImageBinary = image

        cv2.imwrite(tmp_image_fname, self.currentImageBinary)
        example = GeneratedExample(img_fname, tmp_image_fname)
        self.generated_examples_history.append(example)
        return example