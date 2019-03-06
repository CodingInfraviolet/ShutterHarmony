"""
Usage:
main.py <directory>
"""

import numpy as np
import time
import os
import os.path as path
import image_loading
import group_sorting
from docopt import docopt

def image_distance_mse_sum_norm(a, b):
        return np.sum((a.icon / np.sum(a.icon) - b.icon / np.sum(b.icon))**2)

def group_images(images):
  images = sorted(images, key=lambda x: x.creation_time)

  difference_threshold = 0.00002
  difference_function = image_distance_mse_sum_norm

  differences = np.array([])
  for i in range(len(images) - 1):
      differences = np.append(differences, (difference_function(images[i], images[i + 1])))

  breaking_points = np.append([0], differences > difference_threshold)
  groups = np.cumsum(breaking_points)
  grouped_images = [[] for _ in range((groups[-1] + 1))]
  for i, group in enumerate(groups):
      grouped_images[group] = list(grouped_images[group]) + [images[i]]
  return grouped_images

def print_groups(groups):
    i = 1
    for group in groups:
      print("Group %s: " % i)
      for item in group:
        print("  - %s" % item.filepath)
      i = i + 1


if __name__=="__main__":
  arguments = docopt(__doc__)

  print("Loading images")
  
  loader = image_loading.ImageLoader()
  loader.load_images(image_loading.list_images(arguments["<directory>"]))

  groups = group_sorting.sort_groups_by_sharpness(group_images(loader.images))

  target_folder = path.join(arguments["<directory>"], "grouped")

  if not os.path.isdir(target_folder):
    print("mkdir -p {0}".format(target_folder))

  for iGroup, group in enumerate(groups):
      print("mkdir {0}".format(path.join(target_folder, str(iGroup))))
      for iImage, image in enumerate(group):
          print("cp {0} {1}".format(image.filepath, path.join(path.join(target_folder, str(iGroup)), str(iImage) + ".ARW")))