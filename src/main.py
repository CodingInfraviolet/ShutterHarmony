import cv2
import rawpy
import os
import glob
import numpy as np
import scipy.spatial
from collections import namedtuple

Image = namedtuple('Image', 'icon features filename')

def insensitive_glob(pattern):
    def either(c):
        return '[%s%s]' % (c.lower(), c.upper()) if c.isalpha() else c
    return glob.glob(''.join(map(either, pattern)))

def extract_features(image, vector_size=32):
    try:
        # Using KAZE, cause SIFT, ORB and other was moved to additional module
        # which is adding addtional pain during install
        alg = cv2.KAZE_create()
        # Dinding image keypoints
        kps = alg.detect(image)
        # Getting first 32 of them. 
        # Number of keypoints is varies depend on image size and color pallet
        # Sorting them based on keypoint response value(bigger is better)
        kps = sorted(kps, key=lambda x: -x.response)[:vector_size]
        # computing descriptors vector
        kps, dsc = alg.compute(image, kps)
        # Flatten all of them in one big vector - our feature vector
        dsc = dsc.flatten()
        # Making descriptor of same size
        # Descriptor vector size is 64
        needed_size = (vector_size * 64)
        if dsc.size < needed_size:
            # if we have less the 32 descriptors then just adding zeros at the
            # end of our feature vector
            dsc = np.concatenate([dsc, np.zeros(needed_size - dsc.size)])
    except cv2.error as e:
        print('Error: ', e)
        return None

    return dsc

def sort_by_distance(point, other_points, distance_function):
  return sorted(other_points, key=lambda p: distance_function(point, p))

class AugmentedPoint:
  def __init__(self, point, cluster):
    self.point = point
    self.cluster = cluster

def cluster_images_with_dbscan(points, distance_function, e):
  # See https://towardsdatascience.com/the-5-clustering-algorithms-data-scientists-need-to-know-a36d136ef68#4591
  
  if len(points) == 0:
    return []

  next_cluster_number = 0

  augmented_points = [AugmentedPoint(point=point, cluster=-1) for point in points]

  unvisited = augmented_points[:]

  # While there are still points to consider
  while len(unvisited) > 0:
    # Try to find the first unvisited point a home
    augmented_point = unvisited[0]

    # Sort all other points by distance, excluding current point
    closest_points = sort_by_distance(augmented_point, augmented_points, lambda a, b: distance_function(a.point, b.point))[1:]

    # Drop all points too far away to join
    viable_points = list(filter(lambda another_point: distance_function(augmented_point.point, another_point.point) < e, closest_points))

    if len(viable_points) == 0:
      # Can't join another cluster. Add into its own cluster.
      augmented_point.cluster = next_cluster_number
      next_cluster_number = next_cluster_number + 1
    else:
      # Found a new home!
      point_to_join = viable_points[0]

      if point_to_join.cluster == -1:
        # If the closest point does not have a home, form a new cluster with it
        augmented_point.cluster = next_cluster_number
        point_to_join.cluster = next_cluster_number
        next_cluster_number = next_cluster_number + 1
      else:
        # If the point is part of a cluster, join that cluster
        augmented_point.cluster = point_to_join.cluster

    # We have merged, mark this point as done
    unvisited = unvisited[1:]

  # All points have now been visited and joined together. Group by cluster id and return.
  clusters = [[] for _ in range(next_cluster_number)]
  for augmented_point in augmented_points:
    clusters[augmented_point.cluster].append(augmented_point.point)
  
  return clusters


if __name__=="__main__":
  image_directory = 'test/resources'
  os.chdir(image_directory)

  image_filenames = insensitive_glob("*.arw")

  print("Loading images")
  images = []

  for image_filename in image_filenames:
    raw_image = rawpy.imread(image_filename)
    rgb_image = raw_image.postprocess()

    medium_image = cv2.resize(rgb_image, (1024, 1024))
    features = extract_features(medium_image)

    icon = cv2.resize(rgb_image, (100, 100))
    
    image = Image(icon, features, image_filename)

    print(image_filename)
    print(features)
    print("-"*80)

    images.append(image)

print("Clustering images")

clusters = cluster_images_with_dbscan(images, lambda a, b: scipy.spatial.distance.cosine(a.features, b.features), 0.3)

i = 1
for cluster in clusters:
  print("Cluster %s: " % i)
  for item in cluster:
    print("  - %s" % item.filename)
  i = i + 1

# path = 'test/resources/0A.ARW'
# with rawpy.imread(path) as raw:
#     rgb = raw.postprocess()
#     cv2.imshow("Camera Organiser", rgb)

#     cv2.waitKey(0)