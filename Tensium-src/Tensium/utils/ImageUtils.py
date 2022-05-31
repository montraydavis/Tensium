import base64
import io

from PIL import Image


def compare_image(self, image1, image2) -> bool:
    if image1 is not None:
        prev_image_match = True
        for prev_image in range(0, len(image2)):
            if image2[prev_image] != image1[prev_image]:
                prev_image_match = False
                break

        if prev_image_match == False:
            return False

    return True
