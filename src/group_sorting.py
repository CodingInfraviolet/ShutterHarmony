import numpy as np

def image_sharpness(image_mat):
    """
    This function was derived from the paper "Image Sharpness Measure for Blurred Images in Frequency Domain"
    by Kanjar De and V. Masilamani.
    See https://ac.els-cdn.com/S1877705813016007/1-s2.0-S1877705813016007-main.pdf?_tid=f95122a8-c9be-45ec-90a7-e15fb5ecaed3&acdnat=1551129901_433e1bc6f9e722f8250c67330dc43d4a
    """

    fourier_transform = np.abs(np.fft.fftshift(np.fft.fft2(image_mat)))
    maximum_value = np.max(fourier_transform)
    e = maximum_value / 1000
    th = np.sum(fourier_transform > e)
    total_pixels = fourier_transform.shape[0] * fourier_transform.shape[1]
    
    return th / (fourier_transform.shape[0] * fourier_transform.shape[1])

def sort_groups_by_sharpness(groups):
  return list(map(lambda group: list(reversed(sorted(group, key=lambda image: image.sharpness))), groups))