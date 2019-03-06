
import os
import cv2
import rawpy
import time
import multiprocessing
import glob
import platform
import os.path as path
import numpy as np
from threading import Thread

def insensitive_glob(pattern):
    def either(c):
        return '[%s%s]' % (c.lower(), c.upper()) if c.isalpha() else c
    return glob.glob(''.join(map(either, pattern)))

def creation_time(path_to_file):
    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            return stat.st_mtime

def list_images(directory):
  return insensitive_glob(path.join(directory, "*.arw"))

def sharpness(image):
    fourier_transform = np.abs(np.fft.fftshift(np.fft.fft2(image)))
    maximum_value = np.max(fourier_transform)
    e = maximum_value / 1000
    high_pixels = np.sum(fourier_transform > e)
    total_pixels = fourier_transform.shape[0] * fourier_transform.shape[1]
    return high_pixels / (fourier_transform.shape[0] * fourier_transform.shape[1])

def crop_image(image):
    if image.shape[0] < image.shape[1]:
      crop_start = int((image.shape[1] - image.shape[0]) / 2)
      cropped_image = image[:, crop_start:crop_start + image.shape[0]]
    else:
      crop_start = int((image.shape[0] - image.shape[1]) / 2)
      cropped_image = image[crop_start:crop_start + image.shape[0],:]
    return cropped_image

class Image:
  def __init__(self, ready, filepath, icon, creation_time, sharpness):
    self.ready = ready
    self.filepath = filepath
    self.icon = icon
    self.creation_time = creation_time
    self.sharpness = sharpness

class ValueAtom:
  def __init__(self, value):
    self.value = value
  
  def set(self, value):
    self.value = value

  def get(self):
    return self.value

def load_image(lazy_image):
  raw_image = rawpy.imread(lazy_image.filepath)
  rgb_image = raw_image.postprocess(use_camera_wb=True, output_bps=8)
  cropped_image = crop_image(rgb_image)

  lazy_image.icon          = cv2.resize(rgb_image, (100, 100))
  lazy_image.creation_time = creation_time(lazy_image.filepath)
  lazy_image.sharpness     = sharpness(cropped_image)
  lazy_image.ready         = True
  print("Loaded {0}".format(lazy_image.filepath))

class ImageLoader:
  def __init__(self):
    self.images = None
    self.progress_atom = ValueAtom(0.0)
    # self.cpu_pool = multiprocessing.Pool(multiprocessing.cpu_count() * 2)
    self.cpu_pool = multiprocessing.Pool(2)

  def load_images(self, image_list):
    self.images = [Image(ready=False, filepath=filepath, icon=None, creation_time=None, sharpness=None) for filepath in image_list]
    for image in self.images:
      load_image(image)
