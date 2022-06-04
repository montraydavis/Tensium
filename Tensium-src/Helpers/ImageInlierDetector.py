import numpy as np
from PIL import Image, ImageOps
from scipy.spatial import cKDTree
from skimage.feature import plot_matches
from skimage.measure import ransac
from skimage.transform import AffineTransform

import tensorflow as tf

import tensorflow_hub as hub


class ImageInlierDetector():
    delf = hub.load('https://tfhub.dev/google/delf/1').signatures['default']

    def get_image_inliers(self, image1: Image, image2: Image):
        try:
            image1 = ImageOps.fit(image1.convert(
                'RGB'), (500, 500), Image.ANTIALIAS)
            image2 = ImageOps.fit(image2.convert(
                'RGB'), (500, 500), Image.ANTIALIAS)

            result1 = self.run_delf(image1)
            result2 = self.run_delf(image2)
        except:
            return 0

        return self.match_images(result1, result2)

    def match_images(self, result1, result2):
        distance_threshold = 0.8

        # Read features.
        num_features_1 = result1['locations'].shape[0]
        print("Loaded image 1's %d features" % num_features_1)

        num_features_2 = result2['locations'].shape[0]
        print("Loaded image 2's %d features" % num_features_2)

        # Find nearest-neighbor matches using a KD tree.
        d1_tree = cKDTree(result1['descriptors'])
        _, indices = d1_tree.query(
            result2['descriptors'],
            distance_upper_bound=distance_threshold)

        # Select feature locations for putative matches.
        locations_2_to_use = np.array([
            result2['locations'][i, ]
            for i in range(num_features_2)
            if indices[i] != num_features_1
        ])
        locations_1_to_use = np.array([
            result1['locations'][indices[i], ]
            for i in range(num_features_2)
            if indices[i] != num_features_1
        ])

        # Perform geometric verification using RANSAC.
        try:
            _, inliers = ransac(
                (locations_1_to_use, locations_2_to_use),
                AffineTransform,
                min_samples=3,
                residual_threshold=20,
                max_trials=1000)

            return sum(inliers)
        except:
            return 0

    def run_delf(self, image):
        np_image = np.array(image)
        float_image = tf.image.convert_image_dtype(np_image, tf.float32)

        return self.delf(
            image=float_image,
            score_threshold=tf.constant(100.0),
            image_scales=tf.constant(
                [0.25, 0.3536, 0.5, 0.7071, 1.0, 1.4142, 2.0]),
            max_feature_num=tf.constant(1000))

    pass
